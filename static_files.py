
import config
import log
import pandas as pd
import files
import os
import yaml
import build_tools

df = None

# Load from disk a table of all the static pages, templates, and other misc. files.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        json = [
            {
                'type' : 'topic image',
                'filename' : topic_image,
                'full path' : config.relativize_path( os.path.join( config.topics_folder, topic_image ) ),
                'metadata' : np.nan,
                'content' : np.nan,
                'raw content' : np.nan
            } \
            for topic_image in files.just_imgs( os.listdir( os.path.join( config.topics_folder, 'images' ) ) )
        ] + [
            {
                'type' : 'task image',
                'filename' : task_image,
                'full path' : config.relativize_path( os.path.join( config.task_folder, task_image ) ),
                'metadata' : np.nan,
                'content' : np.nan,
                'raw content' : np.nan
            } \
            for task_folder in files.subfolders( config.tasks_folder ) \
            for task_image in files.just_imgs( task_folder )
        ]
        for filename in files.just_docs( os.listdir( config.static_folder ) ):
            full_filename = os.path.join( config.static_folder, filename )
            metadata, content = yaml.split_file( full_filename )
            json.append( {
                'type' : 'template' if filename.endswith( '-template.md' ) else 'static page',
                'filename' : filename,
                'full path' : config.relativize_path( full_filename ),
                'metadata' : metadata,
                'content' : content,
                'raw content' : files.read_text_file( full_filename )
            } )
        df = pd.DataFrame( json )
    return df

# Use one of the templates in the files() list, applying the given dictionary to fill it out.
def fill_template ( name, **kwargs ):
    if df is None:
        log.error( 'Cannot fill template before loading static files table' )
    text = df[df['filename'] == name+'-template.md']['raw content'].iloc[0]
    for key, value in kwargs.items():
        text = text.replace( key, value )
    return text

# Function for copying a static file from the database folder to the
# Jekyll input folder, optionally doing some text replacements en route
def copy ( filename, replacements = dict() ):
    source = os.path.join( config.static_folder, filename )
    dest = os.path.join( config.jekyll_input_folder, filename )
    content = files.read_text_file( source )
    for original, replacement in replacements.items():
        content = content.replace( original, replacement )
    files.write_text_file( dest, content )
    log.file_copy( source, dest, Replacements=len(replacements) )
    build_tools.mark_as_regenerated( filename )
