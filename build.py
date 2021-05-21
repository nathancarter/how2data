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

# Delete files generated in last build
section_heading( 'Deleting old files from Jekyll input folder' )
to_delete = ' '.join( [
    os.path.join( solution_imgs_folder, f'*{ext}' ) for ext in img_extensions
] )
print( f'Running: rm {to_delete}' )
os.system( f'rm {to_delete}' )

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
    elif file.endswith( '-template.md' ):
        pass # we will process these later
    else:
        copy_static_file( file )
for ( task, software, filename ) in solution_imgs:
    copy_solution_image_file( task, software, filename )
for ( filename ) in task_image_files:
    copy_solution_image_file( filename )

# Generate files from database
section_heading( 'Generating files from database content' )
# Note: solution building must go first so task pages can read the generated results
for task, subfolders in solution_docs.items():
    for software, solutions in subfolders.items():
        for solution in solutions:
            build_solution_page( task, software, solution )
# Now task pages get built second, so they can read the generated solution pages
for task_filename in task_files:
    task_name = os.path.splitext( task_filename )[0]
    build_task_page( task_name )
delete_ungenerated_markdown()

# Run Jekyll on newly copied files
section_heading( 'Running Jekyll build process' )
code = os.system( 'bundle exec jekyll build' )
if code != 0:
    sys.exit( code )

# State completion
section_heading( 'Build completed successfully.' )
