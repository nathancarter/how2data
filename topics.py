
import config
import pandas as pd
import numpy as np
import files
import os
import markdown
import yaml
import log
import software
import solutions
import tasks
import static_files
from datetime import datetime
import re
import shell

df = None

# Load from disk a table of all the topics in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        json = [ ]
        for topic_file in files.just_docs( os.listdir( config.topics_folder ) ):
            if topic_file == 'README.md':
                continue
            full_filename = os.path.join( config.topics_folder, topic_file )
            markdown_content = markdown.read_doc( full_filename )
            metadata, content = yaml.split_string( markdown_content )
            content += files.modification_text( full_filename )
            next = {
                'topic name' : files.without_extension( topic_file ),
                'topic filename' : config.relativize_path( full_filename ),
                'permalink' : config.blogify( files.without_extension( topic_file ) ),
                'content' : content,
                'raw content' : markdown_content
            }
            for key, value in metadata.items():
                next[key] = value
            json.append( next )
        df = pd.DataFrame( json )
        # Add links to topic pages
        df['markdown link'] = df['topic name'].apply(
            lambda name: f'[{name}](../{config.blogify(name)})' )
    return df

# Clear cache so we're forced to re-examine what's on disk.
# Useful if you just added a topic.
def clear_cache ():
    global df
    df = None

def _pair_to_title ( package, libraries='solution' ):
    if libraries == 'solution':
        return f'pure {package}'
    else:
        return f'{package} {libraries}'

# Objects of the following class represent an individual row in the topics df.
class Topic:

    # The row may be an integer index, a topic name, or a row from the df.
    # Consider each option below.
    def __init__ ( self, row ):
        if isinstance( row, pd.Series ):
            self.index = row.name
        elif isinstance( row, str ):
            self.index = dict( zip( all()['topic name'], all().index ) )[row]
        elif isinstance( row, int ):
            self.index = row
        else:
            raise TypeError( f"Topics cannot be constructed from a {type(row)}" )
        self._row = all().iloc[self.index,:]
        self._tasks = None

    # Getters for all columns in the tasks df
    @property
    def topic_name ( self ):
        return self._row['topic name']
    @property
    def topic_filename ( self ):
        return self._row['topic filename']
    @property
    def permalink ( self ):
        return self._row['permalink']
    @property
    def content ( self ):
        return self._row['content']
    @property
    def raw_content ( self ):
        return self._row['raw content']
    @property
    def author ( self ):
        return self._row['author']
    @property
    def markdown_link ( self ):
        return self._row['markdown link']

    # And a getter for the whole row
    @property
    def row ( self ):
        return self._row
    # And for its online link in the live website
    @property
    def url ( self ):
        return config.site_link( self.permalink )
    
    # Same as self.content, but with all task names converted to Markdown links
    def content_with_links ( self ):
        return tasks.make_links( self.content )

    # List of all Tasks that appear in this topic, in the order that they appear
    # This may be slow, so the result is cached.
    def tasks ( self ):
        if self._tasks is None:
            content = self.content_with_links()
            is_relevant = lambda link: link in content
            my_position = lambda link: content.index( link )
            result = tasks.all()[tasks.all().permalink.apply( is_relevant )].copy()
            result['where appears'] = result.permalink.apply( my_position )
            self._tasks = result.sort_values( by='where appears' )
        return self._tasks
    
    # Get a copy of the tasks() table, with an extra boolean column at the end, called "included".
    # Values in that column are true iff the corresponding row has a solution in the given software and libraries.
    # TO BE CLEAR: This function returns THE SAME number of rows as tasks(), but just marks them as included or
    # not.  This gives you the opportunity to filter or loop over the collection with greater flexibility.
    def tasks_for ( self, software, libraries='software' ):
        relevant = solutions.all_for( software, libraries )
        result = self.tasks().copy()
        result['included'] = result['task name'].isin( relevant['task name'] )
        return result

    # Title of a PDF for this topic, given the software and libraries the PDF will focus on.
    # This doubles as the filename for the PDF as well.
    def pdf_title ( self, package, libraries='solution' ):
        return f'{self.topic_name} in {_pair_to_title(package,libraries)}'

    # Full path to the output PDF for this topic, given the software and libraries the PDF will focus on
    # The final parameter can be used to specify a different "main folder" than the default from config.
    def pdf_outfile ( self, package, libraries='solution', folder=config.jekyll_input_folder ):
        return os.path.join( folder, 'assets', 'downloads',
            self.pdf_title(package,libraries) + '.pdf' )

    # Whether we must rebuild the PDF for this topic-software-library triple,
    # based on the timestamps of all relevant files on disk.
    # The final parameter can be used to specify a different "main folder" than the default from config.
    def must_build_pdf ( self, package, libraries='solution', folder=config.main_folder ):
        outfile = self.pdf_outfile( package, libraries )
        if not os.path.exists( outfile ):
            log.info( f'Rebuilding because DNE {outfile}' )
            return True
        pdf_last_modified = os.path.getmtime( outfile )
        for index, row in self.tasks().iterrows():
            task_last_modified = os.path.getmtime( os.path.join( folder, tasks.Task( row ).task_filename ) )
            if task_last_modified > pdf_last_modified:
                log.info( f'Rebuilding because newer {tasks.Task( row ).task_filename}' )
                return True
        return False

    # The TOC and description for a PDF built from this topic, in the given software and libraries,
    # as a Markdown string
    def pdf_header ( self, package, libraries='solution' ):
        return static_files.fill_template( 'topic-pdf',
            TITLE = self.pdf_title( package, libraries ),
            SITE_URL = config.site_url,
            DATE = datetime.now().strftime("%d %B %Y"),
            DESCRIPTION = self.content_with_links() )
    
    # The portion of the PDF body that goes with the given task.
    def pdf_one_solution ( self, task, package, libraries='solution', temp_folder=config.topics_folder ):
        relevant = solutions.all_for( package, libraries )
        for_this_portion = relevant[relevant['task name'] == task.task_name]
        if len( for_this_portion ) > 0:
            solution_text = markdown.html_sections_to_latex( markdown.unescape_for_jekyll(
                solutions.Solution( for_this_portion.iloc[0,:] ).generated_body() ),
                temp_folder )
        else:
            solution_text = 'How to Data does not yet contain a solution for this task in ' \
                          + self.pdf_title( package, libraries ) + '.'
        return static_files.fill_template( 'topic-pdf-solution',
            TASK = task.task_name,
            DESCRIPTION = self.content_with_links(),
            SOFTWARE = self.pdf_title( package, libraries ),
            SOLUTION = solution_text )

    # All the markdown content for generating the PDF for this task in the given software and libraries
    def build_pdf_text ( self, package, libraries='solution', temp_folder=config.topics_folder ):
        result = self.pdf_header( package, libraries )
        df = self.tasks()
        for index, task_row in df.iterrows():
            task = tasks.Task( task_row )
            result += self.pdf_one_solution( task, package, libraries, temp_folder )
        # fix all hyperlinks to be either within-the-PDF links or marked as external
        def process_one_link ( match ):
            text = match.group( 1 )
            href = match.group( 2 )
            if href[:3] == '../':
                if href[3:] in df.permalink.to_list():
                    href = f'#{href[3:]}'
                else:
                    href = f'{config.site_link(href[3:])}'
                    text = f'{text} (on website)'
            elif href[0] == '.':
                log.warning( 'Bad external URL:', f'[{text}]({href})' )
            return f'[{text}]({href})'
        return re.sub( '(?<!\\!)\\[([^]]*)\\]\\(([^)]*)\\)', process_one_link,
            result, flags=re.IGNORECASE )

    # Build the markdown content this topic needs for the PDF for the given software and libraries,
    # save that markdown to a temp file, and compile it into a PDF.  Then delete the temp file.
    # The parameters are passed directly to build_text().
    def build_pdf_file (
        self, package, libraries='solution',
        temp_folder=config.topics_folder, out_folder=config.jekyll_input_folder,
        main_folder=config.main_folder
    ):
        outfile = self.pdf_outfile( package, libraries, out_folder )
        tmp_md_doc = os.path.join( temp_folder, 'pandoc-temp-file.md' )
        markdown.write( tmp_md_doc,
            self.build_pdf_text( package, libraries, temp_folder ), add_escapes=False )
        command_to_run = 'pandoc --from=markdown --to=pdf --pdf-engine=xelatex' \
                    + ' -V geometry:margin=1in -V urlcolor:NavyBlue --standalone' \
                    + f' --include-in-header="{os.path.join(main_folder,"pandoc-latex-header.tex")}"' \
                    + f' --lua-filter="{os.path.join(main_folder,"pandoc-pdf-tweaks.lua")}"' \
                    + f' --output="{outfile}" "{tmp_md_doc}"'
        shell.run_or_halt( command_to_run, f'rm "{tmp_md_doc}"' )
        log.built( "PDF", outfile )
        return self.pdf_title( package, libraries ) + '.pdf'

    # Build all PDFs that make sense for this topic and return the list of their filenames.
    # This function need not be called by clients; it is called as part of the build_file() routine.
    def build_all_pdf_files (
        self, min_proportion=0.5, temp_folder=config.topics_folder, out_folder=config.jekyll_input_folder,
        main_folder=config.main_folder
    ):
        result = [ ]
        for package, libraries in software.names_with_libraries():
            tasks = self.tasks_for( package, libraries )
            proportion = sum( tasks['included'] ) / len( tasks )
            if proportion > min_proportion:
                title = self.pdf_title( package, libraries )
                result.append( title )
                if self.must_build_pdf( package, libraries ):
                    self.build_pdf_file( package, libraries, temp_folder, out_folder, main_folder )
                else:
                    log.not_built( title, Reason="Already up to date" )
            else:
                log.not_built( self.pdf_outfile( package, libraries, out_folder ),
                    Reason="Not enough solutions available",
                    Percentage=f"{proportion*100:0.1f}%" )
        return result

    # Must this topic be rebuilt?  Right now, we always rebuild these because it's easy.
    # The second parameter would be passed directly to output_file() if we later upgraded
    # this function to do any file-based comparisons.
    def must_build ( self, folder=None ):
        return True
    
    # Build the markdown content this topic generates but just return it as a string.
    # This necessitates first building any PDFs that will be linked to from this markdown,
    # and including links to them herein.
    def build_text ( self ):
        pdf_files = self.build_all_pdf_files()
        pdf_downloads = ''
        if len( pdf_files ) > 0:
            for pdf_title in pdf_files:
                link_text = pdf_title.replace( self.topic_name, 'Solutions' ) + ' (download PDF)'
                pdf_filename = '../assets/downloads/' + pdf_title + '.pdf'
                pdf_downloads += f' * [{link_text}]({pdf_filename})\n'
        else:
            pdf_downloads = 'No PDF downloads available for this topic yet.'
        return static_files.fill_template( 'topic',
            TITLE = self.topic_name,
            PERMALINK = self.permalink,
            CONTENT = self.content_with_links(),
            CONTRIBUTORS = f'Contributed by {self.author}' if self.author != np.nan else '',
            DOWNLOADS = pdf_downloads )

    # What Markdown file does this topic generate?  The result is an absolute path.
    # By default, the result will be in the jekyll input folder defined in config.py.
    # But you can choose a different output folder with the second argument.
    def output_file ( self, folder=None ):
        if folder is None:
            folder = config.jekyll_input_folder
        return os.path.join( folder, self.permalink + '.md' )

    # Build the markdown content this topic generates and save it to disk.
    # This necessitates first building any PDFs that will be linked to from this markdown,
    # and including links to them herein.
    def build_file ( self, folder=None ):
        markdown_content = self.build_text()
        output_file = self.output_file( folder )
        markdown.write( output_file, markdown_content )
        files.mark_as_regenerated( self.permalink + '.md' )
        return output_file

    # Run build_file() if needed.
    # Otherwise, log that it wasn't needed, but mark the file as up-to-date.
    def build ( self, folder=None, force=False ):
        if force or self.must_build( folder ):
            self.build_file( folder )
        else:
            log.not_built( self.output_file( folder ), self.topic_name )
            files.mark_as_regenerated( self.permalink + '.md' )

    # Read from disk the most recent generated markdown content for this topic.
    # Parameter customizes what folder is passed to output_file().
    def generated_markdown ( self, folder=None ):
        return files.read_text_file( self.output_file( folder ) )
