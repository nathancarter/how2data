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
replacements = {
    'SET_OF_SOFTWARE_PACKAGES': software_table.to_markdown( index=False ),
    'SET_OF_TASKS' : tasks_table_with_links.to_markdown( index=False ),
    'LIST_OF_TOPICS' : '\n'.join( [
        f' * {link}' for link in topics_df['markdown link'] ] ),
    'OVERALL_STATS' : stats_table.to_markdown( index=False )
}
for filename in files_df[files_df['type'] == 'static page']['filename']:
    copy_static_file( filename, replacements )
for index, row in solution_images_df.iterrows():
    copy_solution_image_file( row['task name'], row['software'], row['image filename'] )
for filename in files_df[files_df['type'] == 'task image']['filename']:
    copy_task_image_file( filename )

# Generate files from database
section_heading( 'Generating files from database content' )
# Note: solution building must go first so task pages can read the generated results
for index, row in solutions_df.iterrows():
    build_solution_page( row )
# Now task pages get built second, so they can read the generated solution pages
for index, row in tasks_df.iterrows():
    build_task_page( row )
# Create a page for each software package; the sequencing of this step is not important.
for index, row in software_df.iterrows():
    build_software_page( row )
# Create a page for each topic; the sequencing of this step is not important.
for index, row in topics_df.iterrows():
    build_topic_page( row )
delete_ungenerated_markdown()

# Run Jekyll on newly copied files
section_heading( 'Running Jekyll build process' )
code = os.system( 'bundle exec jekyll build' )
if code != 0:
    sys.exit( code )

# State completion
section_heading( 'Build completed successfully.' )
