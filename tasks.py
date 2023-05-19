
import how_to_data
import config
import pandas as pd
import files
import markdown
import os
import re
import software
import solutions

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
