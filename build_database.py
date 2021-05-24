
#######################
#
#  This module reads all the contents of the database folder in this repo,
#  and provides convenient functions for querying that information.
#  It is used by build_tools.py.
#
#######################

from build_constants import *
from utils import *
import sys

# Read important content from files and directories
static_pages = just_docs( os.listdir( static_folder ) )
task_image_files = os.listdir( os.path.join( tasks_folder, 'images' ) )
solution_template = read_text_file( os.path.join( static_folder, 'solution-template.md' ) )
task_template = read_text_file( os.path.join( static_folder, 'task-template.md' ) )

###
###  SOFTWARE PACKAGES
###

# Read database/database.yml and store it in a global variable
# This contains the list of software packages.
database = read_yaml_from_file( database_config_file )

# Add some functions related to that data:
# Function for converting a software package into the Markdown code for its name
def software_package_name ( package ):
    return package['name']
# All software package names in database
def software_names ():
    return [ software_package_name( package ) for package in database['software'] ]
# How to tell if a given string is one of the official names of a software package?
def is_a_software_package ( text ):
    return text in software_names()
# Function for converting a software package into the Markdown code for its icon
def software_package_icon ( package ):
    name = package['name']
    icon = package['icon']
    return f'![{name} icon]({icon}){{: style="height: 50px;" }}'
# Function for converting a software package into the Markdown code for its website
def software_package_website ( package ):
    url = package['website']
    return f'[{url}]({url})'

###
###  SOLUTIONS
###

# Data about solutions
database['solutions'] = {
    task : {
        software : {
            'solutions' : docs_inside( os.path.join( solutions_folder, task, software ) ),
            'images' : imgs_inside( os.path.join( solutions_folder, task, software ) )
         } \
        for software in subfolders( os.path.join( solutions_folder, task ) )
    } \
    for task in subfolders( solutions_folder )
}
# What should the title be within such a solution page?  Parameters explained:
# task = exact task name, a key to the solution_docs dict.
# software = exact package name, a key to the solutions_docs[task] dict.
# solution = exact filename in the task/software/ folder, including extension.
def solution_page_title ( task, software, solution ):
    return f'{task} ({without_extension( solution )}, in {software})'

###
###  TASKS
###

# Augment the global database variable with all the tasks that are in the database folder.
database['tasks'] = {
    without_extension( task_file ) : {
        'filename' : os.path.join( tasks_folder, task_file ),
        'content' : read_text_file( os.path.join( tasks_folder, task_file ) )
    } \
    for task_file in just_docs( os.listdir( tasks_folder ) ) \
    if task_file != 'README.md'
}

# Add some functions related to that data:
# All task names in database
def task_names ():
    return sorted( database['tasks'].keys() )
# Is a given text the name of a task?
def is_a_task ( text ):
    return text in task_names()
# Get the name for a task from its filename
def task_filename ( task_name ):
    return database['tasks'][task_name]['filename']
# Function for converting a task filename into a link that can be used from the
# tasks page to that individual task
def task_page_link ( task_name ):
    return f'[{task_name}](../{blogify(task_name)})'
# How to get a task file's markdown content, which was read earlier, above.
def get_task_content ( task_name ):
    return database['tasks'][task_name]['content']
# All software packages that have a solution for a given task
def software_for_task ( task_name ):
    if task_name in database['solutions']:
        return [ name for name in software_names() \
                 if name in database['solutions'][task_name] ]
    return [ ]
# All solutions for a given task using a given software package
def solutions_for_task_in_software ( task_name, software_name ):
    if task_name not in database['solutions']:
        return [ ]
    if software_name not in database['solutions'][task_name]:
        return [ ]
    return database['solutions'][task_name][software_name]['solutions']
# All images used by solutions for a given task using a given software package
def images_for_task_in_software ( task_name, software_name ):
    if task_name not in database['solutions']:
        return [ ]
    if software_name not in database['solutions'][task_name]:
        return [ ]
    return database['solutions'][task_name][software_name]['images']
# Function for creating links to solutions for a given task and software package
def task_and_solutions_links ( task_name, software_package ):
    if task_name in database['solutions']:
        software = software_package_name( software_package )
        if software in database['solutions'][task_name]:
            return ', '.join( [
                f'[{without_extension(solution)}]' + \
                f'(../{blogify(solution_page_title(task_name,software,solution))})' \
                for solution in database['solutions'][task_name][software]['solutions']
            ] )
        else:
            return 'None'
    else:
        return 'None'

# Check consistency of database['solutions'] with database['tasks'] and database['software']
for task_name, software_data in database['solutions'].items():
    if not is_a_task( task_name ):
        print( 'Build error: Solution folder not named after any existing task' )
        print( '     Folder:', os.path.join( solutions_folder, task_name ) )
        sys.exit( 1 )
    for software_name, solutions in software_data.items():
        if not is_a_software_package( software_name ):
            print( 'Build error: Software folder not named after any existing package' )
            print( '     Folder:', os.path.join( solutions_folder, task_name, software_name ) )
            print( '   Packages:', ', '.join( software_names ) )
            sys.exit( 1 )

# import pprint
# pp = pprint.PrettyPrinter( indent=4, width=110, compact=True )
# pp.pprint( database )
# sys.exit( 0 )
