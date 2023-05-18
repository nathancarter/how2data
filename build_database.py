
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
import files

###
###  ENSURE KEY FOLDERS EXIST
###

files.ensure_folder_exists( os.path.join( topics_folder, 'images' ) )
files.ensure_folder_exists( jekyll_imgs_folder )

###
###  READ STATIC PAGES, TEMPLATES, AND OTHER MISC. FILES FROM DISK
###

_files_df = None
def files_df ():
    global _files_df
    if _files_df is None:
        json = [
            {
                'type' : 'topic image',
                'filename' : topic_image,
                'full path' : path_in_project( os.path.join( topics_folder, topic_image ) ),
                'metadata' : np.nan,
                'content' : np.nan,
                'raw content' : np.nan
            } \
            for topic_image in files.just_imgs( os.listdir( os.path.join( topics_folder, 'images' ) ) )
        ] + [
            {
                'type' : 'task image',
                'filename' : task_image,
                'full path' : path_in_project( os.path.join( task_folder, task_image ) ),
                'metadata' : np.nan,
                'content' : np.nan,
                'raw content' : np.nan
            } \
            for task_folder in files.subfolders( tasks_folder ) \
            for task_image in files.just_imgs( task_folder )
        ]
        for filename in files.just_docs( os.listdir( static_folder ) ):
            full_filename = os.path.join( static_folder, filename )
            metadata, content = file_split_yaml_header( full_filename )
            json.append( {
                'type' : 'template' if filename.endswith( '-template.md' ) else 'static page',
                'filename' : filename,
                'full path' : path_in_project( full_filename ),
                'metadata' : metadata,
                'content' : content,
                'raw content' : files.read_text_file( full_filename )
            } )
        _files_df = pd.DataFrame( json )
    return _files_df
def fill_template ( name, **kwargs ):
    text = files_df()[files_df()['filename'] == name+'-template.md']['raw content'].iloc[0]
    for key, value in kwargs.items():
        text = text.replace( key, value )
    return text

###
###  READ TASK LIST FROM DISK
###

_tasks_df = None
def tasks_df ():
    global _tasks_df
    if _tasks_df is None:
        rows = [ ]
        for task_folder in files.subfolders( tasks_folder ):
            task_desc_file = get_unique_markdown_doc(
                os.path.join( tasks_folder, task_folder, 'description' ) )
            rows.append( {
                'task name' : task_folder,
                'task filename' : path_in_project( task_desc_file ),
                'content' : read_doc_to_markdown( task_desc_file ),
                'permalink' : blogify( task_folder )
            } )
        _tasks_df = pd.DataFrame( rows )
        # Add links to task pages
        _tasks_df['markdown link'] = _tasks_df['task name'].apply(
            lambda name: f'[{name}](../{blogify(name)})' )
    return _tasks_df

###
###  READ TOPIC LIST FROM DISK
###

_topics_df = None
def topics_df ():
    global _topics_df
    if _topics_df is None:
        json = [ ]
        for topic_file in files.just_docs( os.listdir( topics_folder ) ):
            if topic_file == 'README.md':
                continue
            full_filename = os.path.join( topics_folder, topic_file )
            markdown = read_doc_to_markdown( full_filename )
            metadata, content = string_split_yaml_header( markdown )
            content += files.modification_text( full_filename )
            next = {
                'topic name' : files.without_extension( topic_file ),
                'topic filename' : path_in_project( full_filename ),
                'permalink' : blogify( files.without_extension( topic_file ) ),
                'content' : content,
                'raw content' : markdown
            }
            for key, value in metadata.items():
                next[key] = value
            json.append( next )
        _topics_df = pd.DataFrame( json )
        # Add links to topic pages
        _topics_df['markdown link'] = _topics_df['topic name'].apply(
            lambda name: f'[{name}](../{blogify(name)})' )
    return _topics_df

###
###  READ SOLUTIONS FROM DISK
###

_solutions_df = None
def solutions_df ():
    global _solutions_df
    if _solutions_df is None:
        json = [ ]
        for task_name in files.subfolders( tasks_folder ):
            for solution_file in files.docs_inside( os.path.join( tasks_folder, task_name ) ):
                if files.without_extension( solution_file ) == 'description':
                    continue
                bits = files.without_extension( solution_file ).split( ', ' )
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
                        f'{task_name} (in {files.without_extension( solution_file )})'
                }
                markdown = read_doc_to_markdown( input_file )
                metadata, content = string_split_yaml_header( markdown )
                next['content'] = content + files.modification_text( input_file )
                for key, value in metadata.items():
                    next[key] = value
                next['raw content'] = markdown
                next['permalink'] = blogify( next['solution title'] )
                json.append( next )
        _solutions_df = pd.DataFrame( json )
        # Add links to solution pages to each solution row
        def link_to_solution ( solution_row ):
            return f'[{solution_row["solution name"]}](../{blogify(solution_row["solution title"])})'
        _solutions_df['markdown link'] = _solutions_df.apply( link_to_solution, axis=1 )
        check_consistency()
    return _solutions_df

###
###  READ SOFTWARE PACKAGE LIST FROM CONFIG FILE
###

_software_df = None
def software_df ():
    global _software_df
    if _software_df is None:
        _software_df = pd.DataFrame( read_yaml_from_file( database_config_file )['software'] )
        _software_df['title'] = _software_df['name'].apply( lambda name: f'Software package: {name}' )
        _software_df['permalink'] = _software_df['title'].apply( blogify )
        # Add markdown code for each package's icon
        def software_package_icon ( height, is_link ):
            def result ( package_row ):
                name = package_row['name']
                icon = package_row['icon']
                icon_markdown = f'![{name} icon]({icon}){{: style="height: {height}px;" }}'
                return icon_markdown if not is_link \
                    else f'[{icon_markdown}](../{package_row["permalink"]})'
            return result
        _software_df['icon markdown'] = \
            _software_df.apply( software_package_icon( 50, True ), axis=1 )
        _software_df['large icon markdown'] = \
            _software_df.apply( software_package_icon( 150, False ), axis=1 )
        _software_df['name as link'] = _software_df.apply( ( lambda row:
            f'[{row["name"]}](../{row["permalink"]})' ), axis=1 )
        # Add markdown code for each package's website
        def software_package_website ( package_row ):
            url = package_row['website']
            return f'[{url}]({url})'
        _software_df['website markdown'] = _software_df.apply( software_package_website, axis=1 )
        # Add count of number of solutions in database for each piece of software
        _software_df['num solutions'] = _software_df['name'].apply( lambda name: \
            sum( solutions_df()['software'] == name ) )
        check_consistency()
    return _software_df

###
###  HOW TO CHECK CONSISTENCY AMONG solutions_df() AND software_df()
###

def check_consistency ():
    global _solutions_df, _software_df
    if _solutions_df is not None and _software_df is not None:
        for index, task_row in solutions_df().iterrows():
            if task_row['software'] not in list( software_df()['name'] ):
                print( 'Build error: Software folder not named after any existing package' )
                print( '     Folder:', os.path.join(
                    tasks_folder, task_row['task name'], task_row['software'] ) )
                print( '   Packages:', ', '.join( list( software_df()['name'] ) ) )
                sys.exit( 1 )
