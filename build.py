#!/opt/conda/bin/python

import os, sys
from build_tools import *

# Ensure things are named consistently, or throw a build error explaining the problem
section_heading( 'Checking database consistency' )
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
print( 'Check complete - no problems detected.' )

# Copy files to Jekyll input folder
section_heading( 'Copying files to Jekyll input folder' )
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

# Run Jekyll on newly copied files
section_heading( 'Running Jekyll build process' )
code = os.system( 'bundle exec jekyll build' )
if code != 0:
    sys.exit( code )

# State completion.
section_heading( 'Build completed successfully.' )
