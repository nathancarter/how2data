
import how_to_data
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

# Get just those solutions for a specific software package and libraries
def all_for ( software, libraries='solution' ):
    return all()[( all()['software'] == software ) & ( all()['solution name'] == libraries )]

# Private data and function used in class defined below
github_url = 'https://github.com/nathancarter/how2data'
new_github_issue_url = f'{github_url}/issues/new/choose'
def edit_on_github_url ( filename ):
    return f'{github_url}/tree/main/{config.relativize_path( filename )}'

# Objects of the following class represent an individual row in the solutions df.
class Solution:

    # The row may be an integer index, a solution filename, or a row from the df.
    # Consider each option below.
    def __init__ ( self, row ):
        if isinstance( row, pd.Series ):
            self.index = row.name
        elif isinstance( row, str ):
            self.index = dict( zip( all()['solution filename'], all().index ) )[row]
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
