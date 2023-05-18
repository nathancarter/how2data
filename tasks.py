
import how_to_data
import config
import pandas as pd
import files
import markdown
import os

df = None

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
