
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
###  READ STATIC PAGES, TEMPLATES, AND OTHER MISC. FILES FROM DISK
###

ensure_folder_exists( os.path.join( tasks_folder, 'images' ) )
json = [ ]
for filename in just_docs( os.listdir( static_folder ) ):
    metadata, content = file_split_yaml_header( os.path.join( static_folder, filename ) )
    json.append( {
        'type' : 'template' if filename.endswith( '-template.md' ) else 'static page',
        'filename' : filename,
        'full path' : path_in_project( os.path.join( static_folder, filename ) ),
        'metadata' : metadata,
        'content' : content,
        'raw content' : read_text_file( os.path.join( static_folder, filename ) )
    } )
json += [
    {
        'type' : 'task image',
        'filename' : task_image,
        'full path' : path_in_project( os.path.join( tasks_folder, task_image ) ),
        'metadata' : np.nan,
        'content' : np.nan,
        'raw content' : np.nan
    } \
    for static_page in just_imgs( os.listdir( os.path.join( tasks_folder, 'images' ) ) )
]
files_df = pd.DataFrame( json )

###
###  READ TASK LIST FROM DISK
###

tasks_df = pd.DataFrame( [
    {
        'task name' : without_extension( task_file ),
        'task filename' : path_in_project( os.path.join( tasks_folder, task_file ) ),
        'content' : read_text_file( os.path.join( tasks_folder, task_file ) ),
        'permalink' : blogify( without_extension( task_file ) )
    } \
    for task_file in just_docs( os.listdir( tasks_folder ) ) \
    if task_file != 'README.md'
] )
# Add links to task pages
tasks_df['markdown link'] = tasks_df['task name'].apply(
    lambda name: f'[{name}](../{blogify(name)})' )

###
###  READ SOLUTIONS FROM DISK
###

json = [ ]
for task_name in subfolders( solutions_folder ):
    for software_name in subfolders( os.path.join( solutions_folder, task_name ) ):
        for solution_file in docs_inside( os.path.join(
                solutions_folder, task_name, software_name ) ):
            input_file = os.path.join(
                solutions_folder, task_name, software_name, solution_file )
            next = {
                'task name' : task_name,
                'software' : software_name,
                'solution name' : without_extension( solution_file ),
                'solution filename' : solution_file,
                'solution path' : path_in_project( input_file ),
                'solution title' :
                    f'{task_name} ({without_extension( solution_file )}, in {software_name})'
            }
            metadata, content = file_split_yaml_header( input_file )
            next['content'] = content
            for key, value in metadata.items():
                next[key] = value
            next['raw content'] = read_text_file( input_file )
            next['permalink'] = blogify( next['solution title'] )
            json.append( next )
solutions_df = pd.DataFrame( json )
# Add links to solution pages to each solution row
def link_to_solution ( solution_row ):
    return f'[{solution_row["solution name"]}](../{blogify(solution_row["solution title"])})'
solutions_df['markdown link'] = solutions_df.apply( link_to_solution, axis=1 )

###
###  READ SOLUTION IMAGES FROM DISK
###

solution_images_df = pd.DataFrame( [
    {
        'task name' : task_name,
        'software' : software_name,
        'solution name' : without_extension( solution_file ),
        'image filename' : image_file,
        'image path' : path_in_project( os.path.join(
            solutions_folder, task_name, software_name, image_file ) )
    } \
    for task_name in subfolders( solutions_folder ) \
    for software_name in subfolders( os.path.join( solutions_folder, task_name ) ) \
    for image_file in imgs_inside( os.path.join( solutions_folder, task_name, software_name ) )
] )

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
###  CHECK CONSISTENCY AMONG solutions_df, tasks_df, and software_df
###

for index, task_row in solutions_df.iterrows():
    if task_row['task name'] not in list( tasks_df['task name'] ):
        print( 'Build error: Solution folder not named after any existing task' )
        print( '     Folder:', os.path.join( solutions_folder, task_row['task name'] ) )
        print( '   Basename:', task_row['task name'] )
        print( '    Options:', ', '.join( tasks_df['task name'] ) )
        sys.exit( 1 )
    if task_row['software'] not in list( software_df['name'] ):
        print( 'Build error: Software folder not named after any existing package' )
        print( '     Folder:', os.path.join(
            solutions_folder, task_row['task name'], task_row['software'] ) )
        print( '   Packages:', ', '.join( list( software_df['name'] ) ) )
        sys.exit( 1 )
