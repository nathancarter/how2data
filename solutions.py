
import config
import software
import pandas as pd
import files
import os
import markdown
import yaml
import tasks
import static_files
import log

df = None

# Load from disk a table of all the solutions in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        json = [ ]
        for task_name in files.subfolders( config.tasks_folder ):
            for solution_file in files.docs_inside( os.path.join( config.tasks_folder, task_name ) ):
                if files.without_extension( solution_file ) == 'description':
                    continue
                bits = files.without_extension( solution_file ).split( ', ' )
                software_name = bits[0]
                if len( bits ) == 1:
                    solution_name = 'solution'
                else:
                    solution_name = ', '.join( bits[1:] )
                input_file = os.path.join( config.tasks_folder, task_name, solution_file )
                next = {
                    'task name' : task_name,
                    'software' : software_name,
                    'solution name' : solution_name,
                    'solution filename' : solution_file,
                    'solution path' : config.relativize_path( input_file ),
                    'solution title' :
                        f'{task_name} (in {files.without_extension( solution_file )})'
                }
                markdown_content = markdown.read_doc( input_file )
                metadata, content = yaml.split_string( markdown_content )
                next['content'] = content + files.modification_text( input_file )
                for key, value in metadata.items():
                    next[key] = value
                next['raw content'] = markdown_content
                next['permalink'] = config.blogify( next['solution title'] )
                json.append( next )
        df = pd.DataFrame( json )
        # Add links to solution pages to each solution row
        def link_to_solution ( solution_row ):
            return f'[{solution_row["solution name"]}](../{config.blogify(solution_row["solution title"])})'
        df['markdown link'] = df.apply( link_to_solution, axis=1 )
        software.check_consistency_with_solutions()
    return df

# Clear cache so we're forced to re-examine what's on disk.
# Useful if you just added a solution.
def clear_cache ():
    global df
    df = None

# Get just those solutions for a specific software package and libraries
# (of for any subset of the given set of libraries, if the second param is True)
def all_for ( software_name, libraries='solution', allow_subsets=False ):
    selection = [ ]
    for index, row in all().iterrows():
        if row['software'] != software_name:
            selection.append( False )
        elif row['solution name'] == libraries:
            selection.append( True )
        elif allow_subsets and software.library_subset( row['solution name'], libraries ):
            selection.append( True )
        else:
            selection.append( False )
    return all()[selection]

# Private data and function used in class defined below
github_url = 'https://github.com/nathancarter/how2data'
new_github_issue_url = f'{github_url}/issues/new/choose'
def edit_on_github_url ( filename ):
    return f'{github_url}/tree/main/{config.relativize_path( filename )}'

# Function for internal use only, by a method of the Solution class.
# Creates transforms to pass to markdown.transform_code().
def _transform_software ( from_sw, to_sw ):
    if to_sw in software.using_code:
        line1 = f'### You should replace it with {to_sw} code instead.'
        line2 = f'### After changing the code above, be sure you get the same'
        line3 = f'### Then delete these comments surrounding your code.\n' + \
                f'### And delete the old {from_sw} output (below) as well.'
    else:
        line1 = f'### You should replace this whole block with instructions\n' + \
                f'### on how to accomplish the same goal using {to_sw} instead.'
        line2 = f'### After replacing this code, be sure your method gets the same'
        line3 = f'### When you\'re done, this code and its output should be gone.'
    def result ( block_markdown ):
        lines = block_markdown.split( '\n' )
        return '\n'.join( [
            f'```{to_sw}',
            f'### The {from_sw} code below has been commented out.',
            line1,
            f'###',
            '',
            *[ f'# {line}' for line in lines[1:-2] ],
            '',
            '###',
            line2,
            f'### results that the original {from_sw} code gave, which you can',
            f'### see on the web at the link given at the top of this file.',
            line3,
            '```'
        ] ) + '\n'
    return result

# Objects of the following class represent an individual row in the solutions df.
class Solution:

    # The row may be an integer index, a solution title, or a row from the df.
    # Consider each option below.
    def __init__ ( self, row ):
        if isinstance( row, pd.Series ):
            self.index = row.name
        elif isinstance( row, str ):
            self.index = dict( zip( all()['solution title'], all().index ) )[row]
        elif isinstance( row, int ):
            self.index = row
        else:
            raise TypeError( f"Solutions cannot be constructed from a {type(row)}" )
        self._row = all().iloc[self.index,:]

    # Getters for all columns in the solutions df
    @property
    def task_name ( self ):
        return self._row['task name']
    @property
    def software ( self ):
        return self._row['software']
    @property
    def solution_name ( self ):
        return self._row['solution name']
    @property
    def solution_filename ( self ):
        return self._row['solution filename']
    @property
    def solution_path ( self ):
        return self._row['solution path']
    @property
    def solution_title ( self ):
        return self._row['solution title']
    @property
    def content ( self ):
        return self._row['content']
    @property
    def author ( self ):
        return self._row['author']
    @property
    def raw_content ( self ):
        return self._row['raw content']
    @property
    def permalink ( self ):
        return self._row['permalink']
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
    # And for its content, but without the last modified date
    @property
    def inner_content ( self ):
        result = self.content.split( '\n' )
        if result[-1].startswith( 'Content last modified' ):
            result = result[:-1]
        return '\n'.join( result )

    # What file in the database defines this solution?  The result is an absolute path.
    # We assume we're working in the subfolder of the database folder defined in config.py,
    # the specific subfolder containing the task for this solution.
    # But you can choose a different containing folder for the solution file with the second argument.
    def input_file ( self, folder=None ):
        if folder is None:
            folder = os.path.join( config.tasks_folder, self.task_name )
        return os.path.join( folder, self.solution_filename )
    
    # What file does this solution generate?  The result is an absolute path.
    # By default, the result will be in the jekyll input folder defined in config.py.
    # But you can choose a different output folder with the second argument.
    def output_file ( self, folder=None ):
        if folder is None:
            folder = config.jekyll_input_folder
        return os.path.join( folder, self.permalink + '.md' )

    # What file in the database describes this solution's task?  The result is an absolute path.
    # We assume we're working in the subfolder of the database folder defined in config.py,
    # the specific subfolder containing the task for this solution.
    # But you can choose a different containing folder for the solution file with the second argument.
    def task_file ( self, folder=None ):
        if folder is None:
            folder = os.path.join( config.tasks_folder, self.task_name )
        return markdown.get_unique_doc( os.path.join( folder, 'description' ) )
    
    # Get the Task instance associated with this Solution.
    def task ( self ):
        return tasks.Task( tasks.all()[tasks.all()['task name'] == self.task_name].iloc[0] )

    # Must this solution be rebuilt?  Timestamps of relevant files are checked.
    # Parameters customize what folders are passed to input_file(), output_file(), and task_file().
    def must_build ( self, in_folder=None, out_folder=None ):
        return files.must_rebuild( self.input_file( in_folder ), self.output_file( out_folder ) ) \
            or files.must_rebuild( self.task_file( in_folder ), self.output_file( out_folder ) )
    
    # Build the markdown content this solution generates but just return it as a string.
    # Parameter 2 customizes what folder is passed to input_file().
    # Parameter 3 can be used to provide a Task, so we don't have to look one up.
    def build_text ( self, folder=None, task=None ):
        if folder is None:
            folder = os.path.join( config.tasks_folder, self.task_name )
        input_file = self.input_file( folder )
        content = markdown.adjust_image_filenames(
            tasks.image_link_adjuster( self.task_name ),
            tasks.make_links( self.content ) )
        content += f'\n\nSee a problem?  [Tell us]({new_github_issue_url}) or ' + \
            f'[edit the source]({edit_on_github_url(input_file)}).'
        if task is None:
            task = self.task()
        if type( self.author ) == str:
            contributors = f'Contributed by {self.author}'
        else:
            try:
                contributors = 'Contributed by:\n\n' + \
                    '\n'.join( [ f' * {author}' for author in self.author ] )
            except TypeError:
                contributors = ''
        return static_files.fill_template( 'solution',
            TITLE = self.solution_title,
            PERMALINK = self.permalink,
            TASK_PAGE_LINK = f'[See all solutions.](../{task.permalink})',
            DESCRIPTION =
                markdown.adjust_image_filenames(
                    tasks.image_link_adjuster( self.task_name ),
                    tasks.make_links( task.content ) ),
            MARKDOWN_CONTENT = markdown.wrap_in_html_comments( markdown.run(
                content, folder, self.software ) ),
            CONTRIBUTORS = contributors
        )

    # Build the markdown content this solution generates and save it to disk.
    # Parameters customize what folders are passed to input_file(), output_file(), and build_text().
    def build_file ( self, in_folder=None, out_folder=None, task=None ):
        markdown_content = self.build_text( in_folder, task )
        output_file = self.output_file( out_folder )
        markdown.write( output_file, markdown_content )
        log.built( 'solution for', self.task_name,
                   Software=self.software,
                   Solution=self.solution_name )
        files.mark_as_regenerated( self.permalink + '.md' )
        return output_file
    
    # Run build_file() if needed.
    # Otherwise, log that it wasn't needed, but mark the file as up-to-date.
    def build ( self, in_folder=None, out_folder=None, task=None, force=False ):
        if force or self.must_build( in_folder, out_folder ):
            self.build_file( in_folder, out_folder, task )
        else:
            log.not_built( self.output_file( out_folder ),
                           self.input_file( in_folder ),
                           self.task_file( in_folder ) )
            files.mark_as_regenerated( self.permalink + '.md' )
    
    # Read from disk the most recent generated markdown content for this solution.
    # This is the entire file, not just the "body"; see the next function for getting the body only.
    # Parameter customizes what folder is passed to output_file().
    def generated_markdown ( self, folder=None ):
        return files.read_text_file( self.output_file( folder ) )

    # Same as previous function, but the solution body only (no description, footer, etc.).
    def generated_body ( self, folder=None ):
        return markdown.unwrap_from_html_comments( self.generated_markdown( folder ) )

    # Save a copy of this Solution, but rewritten as an assignment for an expert user
    # to do by rewriting this solution in the given piece of software.  That is, we add
    # an instructions header that explains how to rewrite the solution into the new
    # software, and we store the solution with that new header in a file in the same
    # folder as this sotluion, but in the given format.  All code blocks in this
    # solution are also edited so that they explain to the user how to rewrite them.
    # The software parameter is a string, such as "Python, using sklearn" or "Julia".
    # The format parameter is a string, as markdown.export() expects, such as
    # "Rmd" or "ipynb" or "docx".
    def make_assignment ( self, new_software, format ):
        # Get markdown content of this solution
        content = self.inner_content
        if format not in config.extension_for_type:
            log.error( 'Conversion not supported for this format',
                       Format=format )
        format = config.extension_for_type[format]
        abs_filename = os.path.join( self.task().folder, new_software )
        content_to_edit = markdown.transform_code( content,
            _transform_software( self.software, new_software ) )
        instructions = f'''
# This file should help you write a solution to the task {self.task_name} in {new_software}

## Before you begin

 1. Read the full description of the "{self.task_name}" task.  You can find it
    [on this page]({self.task().url}) of the How to Data website.
 2. Read the solution below, which was written using {self.software}.  You can see
    that same solution displayed more nicely on the same page from the site,
    or you can view it in isolation [on this page]({self.url}).

## Doing the work

'''[1:]
        if self.software in software.using_code and new_software in software.using_code:
            instructions += f'''
 1. Your job is to replace the old code in {self.software} with new code in {new_software}.
    This may also require altering some of the that sits outside code blocks.
'''[1:]
        elif self.software in software.using_code:
            instructions += f'''
 1. Your job is to replace the code blocks with written instructions, because
    {self.software} is a programming language but {new_software} does not use code.
    This requires not only removing all code blocks, but also extending the text that
    currently sits outside the code blocks to include new, step-by-step instructions
    of what to click or type in {new_software}.
'''[1:]
        elif new_software in software.using_code:
            instructions += f'''
 1. Your job is to replace the instructions about {self.software} with code blocks in
    {new_software}, plus some explanations about what the code you add is doing.
'''[1:]
        else:
            instructions += f'''
 1. Your job is to replace the instructions that were written for {self.software}
    with instructions for {new_software}.
'''[1:]
        instructions += f'''
 2. *Try to change as little as possible,* so that the two solutions are
    as similar as they can reasonably be.  This lets readers of the website
    more easily compare the two side-by-side.  Obviously, you'll have to remove any
    reference to {self.software}, but make your result as parallel to the original
    as you can.
 3. Use the same example problems whenever possible, and ensure that you get
    the same result in {new_software} as the original solution shows for {self.software}.

## How to submit your finished solution

 1. Delete these instructions, that is, everything up to the horizontal line
    you see below.'''
        if format == 'ipynb':
            instructions += \
                '    That should mean deleting just this one, big markdown cell.'
        instructions += f'''\n
 2. Email this file to the site maintainer, or if you are familiar with git and
    GitHub, you can commit this file and then create a pull request.

-------------------

'''
        return markdown.export( instructions + content_to_edit, abs_filename, format )
