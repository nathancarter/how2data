
import how_to_data
import config
import solutions
import pandas as pd
import numpy as np
import yaml
import tasks
import static_files
import os
import markdown
import files

df = None
pretty_df = None

# Function-building function used in all(), below
def software_package_icon ( height, is_link ):
    def result ( package_row ):
        name = package_row['name']
        icon = package_row['icon']
        icon_markdown = f'![{name} icon]({icon}){{: style="height: {height}px;" }}'
        return icon_markdown if not is_link \
            else f'[{icon_markdown}](../{package_row["permalink"]})'
    return result

# Function used in all(), below.
def software_package_website ( package_row ):
    url = package_row['website']
    return f'[{url}]({url})'

# Load from disk a table of all the software packages in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        df = pd.DataFrame( yaml.read_header( config.database_config_file )['software'] )
        df['title'] = df['name'].apply( lambda name: f'Software package: {name}' )
        df['permalink'] = df['title'].apply( config.blogify )
        # Add markdown code for each package's icon
        df['icon markdown'] = \
            df.apply( software_package_icon( 50, True ), axis=1 )
        df['large icon markdown'] = \
            df.apply( software_package_icon( 150, False ), axis=1 )
        df['name as link'] = df.apply( ( lambda row:
            f'[{row["name"]}](../{row["permalink"]})' ), axis=1 )
        # Add markdown code for each package's website
        df['website markdown'] = df.apply( software_package_website, axis=1 )
        # Add count of number of solutions in database for each piece of software
        df['num solutions'] = df['name'].apply( lambda name: \
            sum( solutions.all()['software'] == name ) )
        check_consistency_with_solutions()
    return df

# Verify that the solutions and software packages dataframes we've loaded are consistent.
# If they are not, abort the build here with an error message.
# Or if either one is not yet loaded, do nothing.
def check_consistency_with_solutions ():
    if df is not None and solutions.df is not None:
        for index, task_row in solutions.all().iterrows():
            if task_row['software'] not in list( df['name'] ):
                log.error( 'Software folder not named after any existing package',
                        Folder=os.path.join( config.tasks_folder,
                            task_row['task name'], task_row['software'] ),
                        Packages=', '.join( list( df['name'] ) ) )

# Prettify a portion of the full df for use on the software packages page
def table ():
    global pretty_df
    if pretty_df is None:
        pretty_df = all()[['name as link', 'icon markdown', 'num solutions', 'website markdown']]
        pretty_df.columns = [ 'Software Package', 'Icon', 'Number of solutions', 'Website' ]
    return pretty_df

# We often care not just about the list of software packages (Python, R, Excel, etc.),
# but also about the libraries used within them (e.g., "Python, using sklearn and matplotlib").
# The following function fetches the list of all package-library pairs from the Solutions
# database.  If the library is given as merely "solution" then it means no special libraries.
# If it is given as anything else, it will begin with the phrase "using " and then be followed
# by the libraries used.
def names_with_libraries ():
    df = solutions.all()[['software','solution name']].drop_duplicates()
    return list( zip( df['software'], df['solution name'] ) )

# Objects of the following class represent an individual row in the software packages df.
class Software:

    # The row may be an integer index, a software package name, or a row from the df.
    # Consider each option below.
    def __init__ ( self, row ):
        if isinstance( row, pd.Series ):
            self.index = row.name
        elif isinstance( row, str ):
            self.index = dict( zip( all()['name'], all().index ) )[row]
        elif isinstance( row, int ):
            self.index = row
        else:
            raise TypeError( f"Software cannot be constructed from a {type(row)}" )
        self._row = all().iloc[self.index,:]

    # Getters for all columns in the software df
    @property
    def name ( self ):
        return self._row['name']
    @property
    def icon ( self ):
        return self._row['icon']
    @property
    def website ( self ):
        return self._row['website']
    @property
    def title ( self ):
        return self._row['title']
    @property
    def permalink ( self ):
        return self._row['permalink']
    @property
    def icon_markdown ( self ):
        return self._row['icon markdown']
    @property
    def large_icon_markdown ( self ):
        return self._row['large icon markdown']
    @property
    def name_as_link ( self ):
        return self._row['name as link']
    @property
    def website_markdown ( self ):
        return self._row['website markdown']
    @property
    def num_solutions ( self ):
        return self._row['num solutions']

    # And a getter for the whole row
    @property
    def row ( self ):
        return self._row
    
    # Utility function for use in a table of solutions for this software,
    # in the column for "other solutions."  This will either produce the text "None"
    # if there are none, or it will produce text of the form "3 (view)" if there are
    # 3 solutions, for example, where the word "view" is a link to all of them.
    def link_to_other_solutions ( self, task ):
        sol_is_for_task = solutions.all()['task name'] == task.task_name
        sol_uses_this_sw = solutions.all()['software'] == self.name
        num_not_in_this_sw = sum(sol_is_for_task) - \
            sum(sol_is_for_task & sol_uses_this_sw)
        if num_not_in_this_sw > 0:
            return f'{num_not_in_this_sw} ([view](../{task.permalink}))'
        else:
            return 'None'

    # Create a tasks table that will be filtered to produce either a solutions table or
    # an opportunities table, in the functions below.
    # This function is for internal use only, by those two functions.
    # This function also returns a filter for the tasks table that is true iff
    # the task has a solution in this software package.
    def _tasks_table_with_filter ( self ):
        table = tasks.table()[['Task',f'Solutions in {self.name}']].copy()
        table['Solutions in other software packages'] = \
            tasks.all().apply( lambda x: self.link_to_other_solutions( tasks.Task( x ) ), axis=1 )
        has_solution_using_self = table.iloc[:,1].isin([''])
        return table, has_solution_using_self

    # Return a DataFrame of all the solutions that exist in this piece of software,
    # with links to how many solutions exist in other software, built by the function above.
    def solutions ( self ):
        result, filter = self._tasks_table_with_filter()
        result = result[~filter]
        if len( result ) > 0:
            result = result.to_markdown( index=False )
        else:
            result = f'*No tasks have solutions in {row["name"]} yet.*  ' + \
                'Consider [submitting one!](../contributing)'
        return result

    # Return a DataFrame of all the solutions that exist to create solutions in this piece of software,
    # with links to how many solutions exist in other software, built by the function above.
    def opportunities ( self ):
        result, filter = self._tasks_table_with_filter()
        result = result[filter]
        result[f'Solutions in {self.name}'] = \
            f'none yet<br/>(Want to [submit one](../contributing)?)'
        if len( result ) > 0:
            result = result.to_markdown( index=False )
        else:
            result = f'*None---all tasks have solutions in {self.name}!*'
        return result

    # What file does this software generate?  The result is an absolute path.
    # By default, the result will be in the jekyll input folder defined in config.py.
    # But you can choose a different output folder with the second argument.
    def output_file ( self, folder=None ):
        if folder is None:
            folder = config.jekyll_input_folder
        return os.path.join( folder, self.permalink + '.md' )

    # Must this software be rebuilt?  Right now, we always rebuild these because it's easy.
    # The second parameter would be passed directly to output_file() if we later upgraded
    # this function to do any file-based comparisons.
    def must_build ( self, folder=None ):
        return True
    
    # Build the markdown content this software generates but just return it as a string.
    def build_text ( self ):
        return static_files.fill_template( 'software',
            TITLE = self.title,
            SOFTWARE_NAME = self.name,
            PERMALINK = self.permalink,
            SOFTWARE_ICON = self.large_icon_markdown,
            NUMBER_OF_SOLUTIONS = str( self.num_solutions ),
            SOFTWARE_TASK_TABLE = self.solutions(),
            OPPORTUNITIES = self.opportunities()
        )

    # Build the markdown content this software generates and save it to disk.
    # The parameter is used to compute the appropriate output file.
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
            log.not_built( self.output_file( folder ), self.name )
            files.mark_as_regenerated( self.permalink + '.md' )

    # Read from disk the most recent generated markdown content for this software.
    # Parameter customizes what folder is passed to output_file().
    def generated_markdown ( self, folder=None ):
        return files.read_text_file( self.output_file( folder ) )
