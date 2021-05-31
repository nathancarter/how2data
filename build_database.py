
#######################
#
#  This module reads all the contents of the database folder in this repo,
#  and provides convenient functions for querying that information.
#  It is used by build_tools.py.
#
#######################

from build_constants import *
from utils import *
import pandas as pd
import numpy as np
import sys

###
###  ENSURE KEY FOLDERS EXIST
###

ensure_folder_exists( os.path.join( topics_folder, 'images' ) )
ensure_folder_exists( jekyll_imgs_folder )

###
###  READ STATIC PAGES, TEMPLATES, AND OTHER MISC. FILES FROM DISK
###

json = [
    {
        'type' : 'topic image',
        'filename' : topic_image,
        'full path' : path_in_project( os.path.join( topics_folder, topic_image ) ),
        'metadata' : np.nan,
        'content' : np.nan,
        'raw content' : np.nan
    } \
    for topic_image in just_imgs( os.listdir( os.path.join( topics_folder, 'images' ) ) )
] + [
    {
        'type' : 'task image',
        'filename' : task_image,
        'full path' : path_in_project( os.path.join( task_folder, task_image ) ),
        'metadata' : np.nan,
        'content' : np.nan,
        'raw content' : np.nan
    } \
    for task_folder in subfolders( tasks_folder ) \
    for task_image in just_imgs( task_folder )
]
for filename in just_docs( os.listdir( static_folder ) ):
    full_filename = os.path.join( static_folder, filename )
    metadata, content = file_split_yaml_header( full_filename )
    json.append( {
        'type' : 'template' if filename.endswith( '-template.md' ) else 'static page',
        'filename' : filename,
        'full path' : path_in_project( full_filename ),
        'metadata' : metadata,
        'content' : content,
        'raw content' : read_text_file( full_filename )
    } )
files_df = pd.DataFrame( json )

###
###  READ TASK LIST FROM DISK
###

rows = [ ]
for task_folder in subfolders( tasks_folder ):
    task_desc_file = get_unique_markdown_doc(
        os.path.join( tasks_folder, task_folder, 'description' ) )
    rows.append( {
        'task name' : task_folder,
        'task filename' : path_in_project( task_desc_file ),
        'content' : read_doc_to_markdown( task_desc_file ),
        'permalink' : blogify( task_folder )
    } )
tasks_df = pd.DataFrame( rows )
# Add links to task pages
tasks_df['markdown link'] = tasks_df['task name'].apply(
    lambda name: f'[{name}](../{blogify(name)})' )

###
###  READ TOPIC LIST FROM DISK
###

json = [ ]
for topic_file in just_docs( os.listdir( topics_folder ) ):
    if topic_file == 'README.md':
        continue
    full_filename = os.path.join( topics_folder, topic_file )
    markdown = read_doc_to_markdown( full_filename )
    metadata, content = string_split_yaml_header( markdown )
    content += modification_text( full_filename )
    next = {
        'topic name' : without_extension( topic_file ),
        'topic filename' : path_in_project( full_filename ),
        'permalink' : blogify( without_extension( topic_file ) ),
        'content' : content,
        'raw content' : markdown
    }
    for key, value in metadata.items():
        next[key] = value
    json.append( next )
topics_df = pd.DataFrame( json )
# Add links to topic pages
topics_df['markdown link'] = topics_df['topic name'].apply(
    lambda name: f'[{name}](../{blogify(name)})' )

###
###  READ SOLUTIONS FROM DISK
###

json = [ ]
for task_name in subfolders( tasks_folder ):
    for solution_file in docs_inside( os.path.join( tasks_folder, task_name ) ):
        if without_extension( solution_file ) == 'description':
            continue
        bits = without_extension( solution_file ).split( ', ' )
        software_name = bits[0]
        if len( bits ) == 1:
            solution_name = 'solution'
        else:
            solution_name = ', '.join( bits[1:] )
        input_file = os.path.join( tasks_folder, task_name, solution_file )
        next = {
            'task name' : task_name,
            'software' : software_name,
            'solution name' : solution_name,
            'solution filename' : solution_file,
            'solution path' : path_in_project( input_file ),
            'solution title' :
                f'{task_name} (in {without_extension( solution_file )})'
        }
        markdown = read_doc_to_markdown( input_file )
        metadata, content = string_split_yaml_header( markdown )
        next['content'] = content + modification_text( input_file )
        for key, value in metadata.items():
            next[key] = value
        next['raw content'] = markdown
        next['permalink'] = blogify( next['solution title'] )
        json.append( next )
solutions_df = pd.DataFrame( json )
# Add links to solution pages to each solution row
def link_to_solution ( solution_row ):
    return f'[{solution_row["solution name"]}](../{blogify(solution_row["solution title"])})'
solutions_df['markdown link'] = solutions_df.apply( link_to_solution, axis=1 )

###
###  READ SOFTWARE PACKAGE LIST FROM CONFIG FILE
###

software_df = pd.DataFrame( read_yaml_from_file( database_config_file )['software'] )
software_df['title'] = software_df['name'].apply( lambda name: f'Software package: {name}' )
software_df['permalink'] = software_df['title'].apply( blogify )
# Add markdown code for each package's icon
def software_package_icon ( height, is_link ):
    def result ( package_row ):
        name = package_row['name']
        icon = package_row['icon']
        icon_markdown = f'![{name} icon]({icon}){{: style="height: {height}px;" }}'
        return icon_markdown if not is_link \
            else f'[{icon_markdown}](../{package_row["permalink"]})'
    return result
software_df['icon markdown'] = \
    software_df.apply( software_package_icon( 50, True ), axis=1 )
software_df['large icon markdown'] = \
    software_df.apply( software_package_icon( 150, False ), axis=1 )
software_df['name as link'] = software_df.apply( ( lambda row:
    f'[{row["name"]}](../{row["permalink"]})' ), axis=1 )
# Add markdown code for each package's website
def software_package_website ( package_row ):
    url = package_row['website']
    return f'[{url}]({url})'
software_df['website markdown'] = software_df.apply( software_package_website, axis=1 )
# Add count of number of solutions in database for each piece of software
software_df['num solutions'] = software_df['name'].apply( lambda name: \
    sum( solutions_df['software'] == name ) )

###
###  CHECK CONSISTENCY AMONG solutions_df AND software_df
###

for index, task_row in solutions_df.iterrows():
    if task_row['software'] not in list( software_df['name'] ):
        print( 'Build error: Software folder not named after any existing package' )
        print( '     Folder:', os.path.join(
            tasks_folder, task_row['task name'], task_row['software'] ) )
        print( '   Packages:', ', '.join( list( software_df['name'] ) ) )
        sys.exit( 1 )
