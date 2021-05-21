#!/opt/conda/bin/python

import os, sys
from build_tools import *

section_heading( 'Database build process' )
for task, subfolders in solution_docs.items():
    if not is_a_task( task ):
        print( 'Build error: Solution folder not named after any existing task' )
        print( '     Folder:', os.path.join( solutions_folder, task ) )
        sys.exit( 1 )
    for software, solutions in subfolders.items():
        if not is_a_software_package( software ):
            print( 'Build error: Software folder not named after any existing package' )
            print( '     Folder:', os.path.join( solutions_folder, task, software ) )
            print( '   Packages:', ', '.join( software_names ) )
            sys.exit( 1 )
for file in static_pages:
    if file == 'software.md':
        copy_static_file( file, {
            'SET_OF_SOFTWARE_PACKAGES': software_table
        } )
    elif file == 'tasks.md':
        copy_static_file( file, {
            'SET_OF_TASKS' : tasks_table
        } )
    else:
        copy_static_file( file )

section_heading( 'Jekyll build process' )
sys.exit( os.system( 'bundle exec jekyll build' ) )
