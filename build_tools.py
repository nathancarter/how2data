
import os
from ruamel.yaml import YAML
import pandas as pd
import numpy as np

# What extensions count as documents vs. images?
# How can we easily filter for those extensions in a list of files?
doc_extensions = [ '.md', '.markdown' ]
img_extensions = [ '.jpg', '.jpeg', '.png', '.gif' ]
def has_any_extension ( filename, extensions ):
    return any( ( filename.endswith( ext ) for ext in extensions ) )
def is_doc ( filename ):
    return has_any_extension( filename, doc_extensions )
def is_img ( filename ):
    return has_any_extension( filename, img_extensions )
def just_docs ( filenames ):
    return [ x for x in filenames if is_doc( x ) ]
def just_imgs ( filenames ):
    return [ x for x in filenames if is_img( x ) ]
def subfolders ( folder ):
    return [ x for x in os.listdir( folder ) \
             if os.path.isdir( os.path.join( folder, x ) ) ]
def docs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_doc( x ) ]
def imgs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_img( x ) ]

# Function for printing section headings in the console output
def section_heading ( title ):
    print()
    print()
    print( title )
    print( '-' * len( title ) )

# Global variables for important folders in this repo and their contents
main_folder = os.path.dirname( os.path.realpath( __file__ ) )
static_folder = os.path.join( main_folder, 'database', 'static' )
static_pages = just_docs( os.listdir( static_folder ) )
tasks_folder = os.path.join( main_folder, 'database', 'tasks' )
task_files = [
    file for file in just_docs( os.listdir( tasks_folder ) ) \
    if file != 'README.md'
]
task_image_files = os.listdir( os.path.join( tasks_folder, 'images' ) )
jekyll_input_folder = os.path.join( main_folder, 'jekyll-input' )
solutions_folder = os.path.join( main_folder, 'database', 'solutions' )
solution_docs = {
    task : {
        software : docs_inside( os.path.join( solutions_folder, task, software ) ) \
        for software in subfolders( os.path.join( solutions_folder, task ) )
    } \
    for task in subfolders( solutions_folder )
}
solution_imgs = [
    os.path.join( solutions_folder, task, software, x ) \
    for task in subfolders( solutions_folder ) \
    for software in subfolders( os.path.join( solutions_folder, task ) ) \
    for x in imgs_inside( os.path.join( solutions_folder, task, software ) )
]

# Read database/database.yml and store it in a global variable
with open( os.path.join( main_folder, 'database', 'database.yml' ), 'r' ) as f:
    configuration = YAML().load( ''.join( f.readlines() ) )

# Function for copying a static file from the database folder to the
# Jekyll input folder, optionally doing some text replacements en route
def copy_static_file ( filename, replacements = dict() ):
    source = os.path.join( static_folder, filename )
    dest = os.path.join( jekyll_input_folder, filename )
    with open( source, 'r' ) as f:
        content = ''.join( f.readlines() )
    for original, replacement in replacements.items():
        content = content.replace( original, replacement )
    with open( dest, 'w' ) as f:
        f.write( content )
    print( 'Copied: Source:      ', source )
    print( '        Dest:        ', dest )
    print( '        Replacements:', len(replacements) )

# Function for converting a software package into the Markdown code for its name
def software_package_name ( package ):
    return package['name']

# Function for converting a software package into the Markdown code for its icon
def software_package_icon ( package ):
    name = package['name']
    icon = package['icon']
    return f'![{name} icon]({icon}){{: style="height: 50px;" }}'

# Function for converting a software package into the Markdown code for its website
def software_package_website ( package ):
    url = package['website']
    return f'[{url}]({url})'

# The software table to be inserted on the software packages page
software_table = configuration['software']
software_names = [ software_package_name( x ) for x in software_table ]
software_table = pd.DataFrame( {
    "Software Package" : software_names,
    "Icon" : map( software_package_icon, software_table ),
    "Number of solutions" : np.nan,
    "Website" : map( software_package_website, software_table )
} )
software_table = software_table.to_markdown( index=False )

# The tasks table to be inserted on the tasks page
tasks_table = pd.DataFrame( {
    "Task" : [ os.path.splitext( filename )[0] for filename in task_files ]
} )
for package in configuration['software']:
    tasks_table[f'Solutions in {package["name"]}'] = np.nan
tasks_table = tasks_table.to_markdown( index=False )

# How to tell if a given string is one of the official names of a task or a
# software package in our database?  We make some functions.
def is_a_task ( text ):
    return any( [ text + ext in task_files for ext in doc_extensions ] )
def is_a_software_package ( text ):
    return text in software_names
