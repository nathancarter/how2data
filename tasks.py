
import how_to_data
import config
import pandas as pd
import files
import markdown
import os
import re
import software
import solutions
import topics
import static_files

df = None
pretty_df = None
pretty_df_with_links = None

# Load from disk a table of all the tasks in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        rows = [ ]
        for task_folder in files.subfolders( config.tasks_folder ):
            task_desc_file = markdown.get_unique_doc(
                os.path.join( config.tasks_folder, task_folder, 'description' ) )
            rows.append( {
                'task name' : task_folder,
                'task filename' : config.relativize_path( task_desc_file ),
                'content' : markdown.read_doc( task_desc_file ),
                'permalink' : config.blogify( task_folder )
            } )
        df = pd.DataFrame( rows )
        # Add links to task pages
        df['markdown link'] = df['task name'].apply(
            lambda name: f'[{name}](../{config.blogify(name)})' )
    return df

# Function for copying a task file from a task folder to the Jekyll
# input folder.  (This is typically images, hence the function name.)
def copy_image ( full_path_to_source, filename ):
    dest = os.path.join( config.jekyll_imgs_folder, filename )
    shutil.copy2( full_path_to_source, dest )
    log.file_copy( full_path_to_source, dest )

# Function generator whose result is a function that renames image links
# to point to the appropriate subfolder of the jekyll input folder
# where images for tasks are stored.
def image_link_adjuster ( task ):
    def result ( filename ):
        return os.path.join( '..', 'assets', 'dynamic-images', f'{task}-{filename}' )

# Find all task names in the given markdown content
# and convert each to a link to the corresponding task page.
def make_links ( markdown ):
    longer_first = all().sort_values( 'task name', ascending=False )
    for index, task_row in longer_first.iterrows():
        markdown = re.sub( '(?<!\\[)(' + re.escape( task_row['task name'] ) + ')',
            lambda x: f'[{x.group(0)}](../{task_row["permalink"]})',
            markdown, flags=re.IGNORECASE )
    return markdown

# Prettify a portion of the full df for use on the tasks page
def table ():
    global pretty_df
    if pretty_df is None:
        pretty_df = pd.DataFrame( { 'Task' : all()['markdown link'] } )
        def links_for_task_solutions_in_software ( task_name, software_name ):
            return ', '.join( list( solutions.all()[ \
                (solutions.all()['task name'] == task_name) & \
                (solutions.all()['software'] == software_name)]['markdown link'] ) )
        for index, software_row in software.all().iterrows():
            pretty_df[f'Solutions in {software_row["name"]}'] = \
                all()['task name'].apply( lambda task_name:
                    links_for_task_solutions_in_software( task_name, software_row['name'] ) )
    return pretty_df

# Make a separate copy that unites all solution columns
def table_with_links ():
    global pretty_df_with_links
    if pretty_df_with_links is None:
        permalink_for_sw = dict( zip( software.all()['name'], software.all()['permalink'] ) )
        pretty_df_with_links = table().copy()
        pretty_df_with_links['Solutions'] = ''
        for index, row in pretty_df_with_links.iterrows():
            to_join = [ ]
            for col in table().columns:
                if col.startswith( 'Solutions in' ) and row[col] != '':
                    to_join.append( f'In {col[13:]}: {row[col]}' )
            row['Solutions'] = '<br>'.join( to_join )
        pretty_df_with_links = pretty_df_with_links[['Task','Solutions']]
    return pretty_df_with_links

# Objects of the following class represent an individual row in the tasks df.
class Task:

    # The row may be an integer index, a task filename, or a row from the df.
    # Consider each option below.
    def __init__ ( self, row ):
        if isinstance( row, pd.Series ):
            self.index = row.name
        elif isinstance( row, str ):
            self.index = dict( zip( all()['task filename'], all().index ) )[row]
        elif isinstance( row, int ):
            self.index = row
        else:
            raise TypeError( f"Tasks cannot be constructed from a {type(row)}" )
        self._row = all().iloc[self.index,:]

    # Getters for all columns in the tasks df
    @property
    def task_name ( self ):
        return self._row['task name']
    @property
    def task_filename ( self ):
        return self._row['task filename']
    @property
    def content ( self ):
        return self._row['content']
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
    
    # Get all solutions for this task, as Solution instances
    def solutions ( self ):
        rows = solutions.all()[solutions.all()['task name'] == self.task_name]
        return [ solutions.Solution( row ) for _, row in rows.iterrows() ]
    
    # Get the markdown content for one section of this task's page.
    # IMPORTANT!!  This assumes you've already built the relevant solution,
    # so that this function can just extract its content from disk.  (It does not build it.)
    # The solution data is looked up in the given folder,
    # which defaults to the jekyll input folder defined in config.py.
    def section ( self, solution, folder=None ):
        solution_name = files.without_extension( solution.solution_name ).title()
        return static_files.fill_template( 'solution-in-software',
            NAME = solution_name,
            SOFTWARE = solution.software,
            PERMALINK = solution.permalink,
            BODY = markdown.unescape_for_jekyll( solution.generated_body( folder ) ) )

    # Get the list of opportunities for this task.
    # That is, the list of software names for which this task doesn't yet have a solution.
    # By default, it will use the list of solutions given by this object's solutions()
    # member, but if you have a different set of Solution objects or solution_df rows,
    # you can pass that as the second argument.
    # The result is a list of strings, software package names.
    def opportunities ( self, existing_solutions=None ):
        if isinstance( existing_solutions, pd.DataFrame ):
            non_opportunities = existing_solutions['software']
        else:
            non_opportunities = [ solution.software for solution in existing_solutions ]
        return list( software.all()['name'][~software.all()['name'].isin(non_opportunities)] )

    # Get the related topics for this task, as a DataFrame.
    # That is, the list of topic names in which this task appears.
    def topics ( self ):
        return topics.all()[topics.all()['content'].str.contains( self.task_name, regex=False )]

    # What file does this task generate?  The result is an absolute path.
    # By default, the result will be in the jekyll input folder defined in config.py.
    # But you can choose a different output folder with the second argument.
    def output_file ( self, folder=None ):
        if folder is None:
            folder = config.jekyll_input_folder
        return os.path.join( folder, self.permalink + '.md' )

    # Must this task be rebuilt?  Right now, we always rebuild these because it's easy.
    def must_build ( self, folder=None, solutions=None ):
        return True
    
    # Build the markdown content this task generates but just return it as a string.
    # The second parameter customizes what folder is passed to output_file().
    # The third parameter can provide a list of existing solutions;
    # if it is not provided, we compute one using our solutions() member.
    # It can be a list of Solution instances or a DataFrame filtered from the solutions_df.
    def build_text ( self, folder=None, existing_solutions=None ):
        # Solutions on the page
        if existing_solutions is None: # provide a default
            software = self.solutions()
        elif isinstance( existing_solutions, pd.DataFrame ): # convert df to Solution list
            software = [
                existing_solutions.Solution( row )
                for _, row in existing_solutions.iterrows()
            ]
        else: # assume it is is a Solution list
            software = existing_solutions
        all_solutions = ''.join(
            self.section( solution, folder ) for solution in software )
        if all_solutions == '':
            all_solutions = '## Solutions\n\nNo solutions exist yet in the database for this task.'
        # Missing solutions we'd like to see added
        opportunities = self.opportunities( software )
        if len( opportunities ) > 0:
            opportunities = "\n".join( [ f" * {software}" for software in opportunities ] )
            opportunities = static_files.fill_template( 'opportunities',
                OPPORTUNITIES_LIST = opportunities )
        else:
            opportunities = ''
        # Topics containing this task
        related_topics = self.topics()
        if len( related_topics ) > 0:
            related_topics = '\n'.join( list( ' * ' + related_topics['markdown link'] ) )
        else:
            related_topics = '*None*'
        # Return that full page
        return static_files.fill_template( 'task',
            TITLE = self.task_name,
            PERMALINK = self.permalink,
            DESCRIPTION = markdown.adjust_image_filenames(
                image_link_adjuster( self.task_name ),
                make_links( self.content ) ),
            SOLUTIONS = all_solutions,
            TOPICS = related_topics,
            OPPORTUNITIES = opportunities )

    # Build the markdown content this task generates and save it to disk.
    # The parameters are passed directly to build_text().
    def build_file ( self, folder=None, solutions=None ):
        markdown_content = self.build_text( folder, solutions )
        output_file = self.output_file( folder )
        markdown.write( output_file, markdown_content )
        files.mark_as_regenerated( self.permalink + '.md' )
        return output_file

    # Run build_file() if needed.
    # Otherwise, log that it wasn't needed, but mark the file as up-to-date.
    def build ( self, folder=None, solutions=None, force=False ):
        if force or self.must_build( folder, solutions ):
            self.build_file( folder, solutions )
        else:
            log.not_built( self.output_file( folder ), self.task_filename )
            files.mark_as_regenerated( self.permalink + '.md' )

    # Read from disk the most recent generated markdown content for this task.
    # Parameter customizes what folder is passed to output_file().
    def generated_markdown ( self, folder=None ):
        return files.read_text_file( self.output_file( folder ) )
