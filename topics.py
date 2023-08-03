
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
import itertools

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
    # Only one solution per task will be marked as included for any given task and software pair,
    # the last one whose required libraries are a subset of the ones specified in the final parameter.
    def tasks_for ( self, software, libraries='software' ):
        result = self.tasks().copy()
        result['included'] = [
            tasks.Task( row ).first_solution_using( software, libraries ) is not None
            for _, row in result.iterrows()
        ]
        return result

    # Title of a PDF for this topic, given the software the PDF will focus on.
    # This doubles as the filename for the PDF as well.
    def pdf_title ( self, package ):
        return f'{self.topic_name} in {package}'

    # Full path to the output PDF for this topic, given the software the PDF will focus on
    # The final parameter can be used to specify a different "main folder" than the default from config.
    def pdf_outfile ( self, package, folder=config.jekyll_input_folder ):
        return os.path.join( folder, 'assets', 'downloads',
            self.pdf_title( package ) + '.pdf' )

    # Whether we must rebuild the PDF for this topic-software-library triple,
    # based on the timestamps of all relevant files on disk.
    # The final parameter can be used to specify a different "main folder" than the default from config.
    def must_build_pdf ( self, package, libraries='solution', folder=config.main_folder ):
        outfile = self.pdf_outfile( package )
        if not os.path.exists( outfile ):
            log.info( f'Rebuilding because DNE {outfile}' )
            return True
        pdf_last_modified = os.path.getmtime( outfile )
        solutions_involved = [
            tasks.Task( row ).first_solution_using( package, libraries )
            for _, row in self.tasks().iterrows()
        ]
        solutions_involved = [ sol for sol in solutions_involved if sol is not None ]
        for solution in solutions_involved:
            task = solution.task()
            task_last_modified = os.path.getmtime( task.task_filename )
            if task_last_modified > pdf_last_modified:
                log.info( f'Rebuilding because newer {task.task_filename}' )
                return True
            sol_last_modified = os.path.getmtime( solution.output_file() )
            if sol_last_modified > pdf_last_modified:
                log.info( f'Rebuilding because newer {solution.output_file()}' )
                return True
        return False

    # The TOC and description for a PDF built from this topic, in the given software and libraries,
    # as a Markdown string
    def pdf_header ( self, package ):
        return static_files.fill_template( 'topic-pdf',
            TITLE = self.pdf_title( package ),
            SITE_URL = config.site_url,
            DATE = datetime.now().strftime("%d %B %Y"),
            DESCRIPTION = self.content_with_links() )
    
    # The portion of the PDF body that goes with the given task.
    def pdf_one_solution ( self, task, package, libraries='solution', temp_folder=config.topics_folder ):
        solution = task.first_solution_using( package, libraries )
        if solution is not None:
            solution_text = markdown.html_sections_to_latex( markdown.unescape_for_jekyll(
                solution.generated_body() ), temp_folder )
            solution_name = _pair_to_title( solution.software, solution.solution_name )
        else:
            solution_text = f'How to Data does not yet contain a solution for this task in {package}.'
            solution_name = package
        return static_files.fill_template( 'topic-pdf-solution',
            TASK = task.task_name,
            DESCRIPTION = tasks.make_links( task.content ),
            SOFTWARE = solution_name,
            SOLUTION = solution_text )

    # All the markdown content for generating the PDF for this task in the given software and libraries
    def build_pdf_text ( self, package, libraries='solution', temp_folder=config.topics_folder ):
        result = self.pdf_header( package )
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
        outfile = self.pdf_outfile( package, out_folder )
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
        return self.pdf_title( package ) + '.pdf'

    # Build all PDFs that make sense for this topic and return the list of their filenames.
    # This function need not be called by clients; it is called as part of the build_file() routine.
    # Note that this will create one PDF per software package, and it will choose a set of libraries
    # for that software package that (1) maximizes the number of tasks from this topic that will
    # be solved and within that (2) minimizes the number of libraries included.
    def build_all_pdf_files (
        self, min_proportion=0.5, temp_folder=config.topics_folder, out_folder=config.jekyll_input_folder,
        main_folder=config.main_folder
    ):
        result = [ ]
        # loop through all software packages
        for sw_name in software.all()['name']:
            sw = software.Software( sw_name )
            best_lib_set = None
            best_num_sols = 0
            max_num_sols = 0
            # consider every possible subset of the libraries for it in our database
            # counting from the smallest sets upwards in size
            libraries = sw.all_libraries()
            for size in range(len(libraries)+1):
                for lib_subset in itertools.combinations( libraries, size ):
                    # record which of them has the best coverage (most # solutions it can handle)
                    # and because we are counting upwards in size, we will retain the smallest
                    # subset (or one tied for smallest) that achieves that maximum
                    tasks_for_subset = self.tasks_for( sw_name, software.libs_set_to_str( lib_subset ) )
                    max_num_sols = len( tasks_for_subset )
                    num_sols = sum( tasks_for_subset['included'] )
                    if num_sols > best_num_sols:
                        best_num_sols = num_sols
                        best_lib_set = lib_subset
            # if the coverage of the best one we found is not sufficient, stop here
            proportion = best_num_sols / max_num_sols
            if proportion < min_proportion:
                log.not_built( self.pdf_outfile( sw_name, out_folder ),
                    Reason="Not enough solutions available",
                    Percentage=f"{proportion*100:0.1f}%" )
                continue
            # it is sufficient, so we can build a PDF for this software package (and this topic).
            # but should we?  depends on file timestamps, so we check that now.
            libraries = software.libs_set_to_str( best_lib_set )
            if not self.must_build_pdf( sw_name, libraries ):
                log.not_built( self.pdf_outfile( sw_name, out_folder ),
                    Reason="Already up to date" )
                continue
            # okay we can actually build this PDF!  Do so...
            self.build_pdf_file( sw_name, libraries, temp_folder, out_folder, main_folder )
            result.append( self.pdf_title( sw_name ) )
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
