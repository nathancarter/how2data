
import os
from ruamel.yaml import YAML
import pandas as pd
import numpy as np

# Function for printing section headings in the console output
def section_heading ( title ):
    print( '-' * len( title ) )
    print( title )
    print( '-' * len( title ) )

# Function for filtering a list of filenames for just Markdown files
def markdown_files ( filenames ):
    return [
        x for x in filenames if x[-3:] == '.md' or x[-9:] == '.markdown'
    ]

# Global variables for important folders in this repo and their contents
main_folder = os.path.dirname( os.path.realpath( __file__ ) )
static_folder = os.path.join( main_folder, 'database', 'static' )
static_pages = markdown_files( os.listdir( static_folder ) )
tasks_folder = os.path.join( main_folder, 'database', 'tasks' )
task_files = [
    file for file in markdown_files( os.listdir( tasks_folder ) ) \
    if file != 'README.md'
]
task_image_files = os.listdir( os.path.join( tasks_folder, 'images' ) )
jekyll_input_folder = os.path.join( main_folder, 'jekyll-input' )

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

# Function for converting a software package into the Markdown code for its icon
def software_package_name ( package ):
    return package['name']

# Function for converting a software package into the Markdown code for its name
def software_package_icon ( package ):
    name = package['name']
    icon = package['icon']
    return f'![{name} icon]({icon}){{: style="height: 50px;" }}'

# Function for converting a software package into the Markdown code for its
# icon and name together
def software_package_website ( package ):
    url = package['website']
    return f'[{url}]({url})'

# The software table to be inserted on the software packages page
software_table = configuration['software']
software_table = pd.DataFrame( {
    "Software Package" : map( software_package_name, software_table ),
    "Icon" : map( software_package_icon, software_table ),
    "Number of solutions" : np.nan,
    "Website" : map( software_package_website, software_table )
} )
software_table = software_table.to_markdown( index=False )

# THe tasks table to be insert on the tasks page
tasks_table = pd.DataFrame( {
    "Task" : [ os.path.splitext( filename )[0] for filename in task_files ]
} )
for package in configuration['software']:
    tasks_table[f'Solutions in {package["name"]}'] = np.nan
tasks_table = tasks_table.to_markdown( index=False )
