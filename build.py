#!/opt/conda/bin/python

#######################
#
#  This is the main build script for this repository.
#  Any other Python files in this folder are imported by this one.
#  To understand the build process, read the comments on each section below.
#
#######################

import os, sys
from build_tools import *

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
for task_name in task_names():
    for software_name in software_for_task( task_name ):
        for image in images_for_task_in_software( task_name, software_name ):
            copy_solution_image_file( task_name, software_name, filename )
for ( filename ) in task_image_files:
    copy_task_image_file( filename )

# Generate files from database
section_heading( 'Generating files from database content' )
# Note: solution building must go first so task pages can read the generated results
for task_name in task_names():
    for software_name in software_for_task( task_name ):
        for solution in solutions_for_task_in_software( task_name, software_name ):
            build_solution_page( task_name, software_name, solution )
# Now task pages get built second, so they can read the generated solution pages
for task_name in task_names():
    build_task_page( task_name )
delete_ungenerated_markdown()

# Run Jekyll on newly copied files
section_heading( 'Running Jekyll build process' )
code = os.system( 'bundle exec jekyll build' )
if code != 0:
    sys.exit( code )

# State completion
section_heading( 'Build completed successfully.' )
