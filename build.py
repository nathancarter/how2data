#!/opt/conda/bin/python

#######################
#
#  This is the main build script for this repository.
#  Any other Python files in this folder are imported by this one.
#  To understand the build process, read the comments on each section below.
#
#######################

import os, sys, glob
from build_tools import *

# Command line parameters
# -f/--force = rerun all solution code even if modification dates don't require it
rerun_solutions = '-f' in sys.argv or '--force' in sys.argv

# Delete files generated in last build
section_heading( 'Deleting old files from Jekyll input folder' )
to_delete = ' '.join( [
    os.path.join( jekyll_imgs_folder, f'*{ext}' ) for ext in img_extensions
] )
print( f'Running: rm {to_delete}' )
run_shell_command_ignoring_errors( f'rm {to_delete}' )

# Copy files to Jekyll input folder
section_heading( 'Copying files to Jekyll input folder' )
replacements = {
    'SET_OF_SOFTWARE_PACKAGES': software_table.to_markdown( index=False ),
    'SET_OF_TASKS' : tasks_table_with_links.to_markdown( index=False ),
    'LIST_OF_TOPICS' : '\n'.join( [
        f' * {link}' for link in topics_df['markdown link'] ] ),
    'OVERALL_STATS' : stats_table.to_markdown( index=False ),
    'CONTRIBUTORS_LIST' : contributors_list_markdown
}
for filename in files_df[files_df['type'] == 'static page']['filename']:
    copy_static_file( filename, replacements )
for index, row in files_df[files_df['type'] == 'task image'].iterrows():
    copy_task_image_file( row['full path'], row['filename'] )

# Generate files from database
section_heading( 'Generating files from database content' )
# Note: solution building must go first so task pages can read the generated results
for index, row in solutions_df.iterrows():
    build_solution_page( row, rerun_solutions )
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

# Zip up examples to reference from the Contributing page
section_heading( 'Zipping examples for contributors' )
infiles = glob.iglob( 'examples/*', recursive=True )
outfile = 'jekyll-input/assets/downloads/examples-for-contributing-to-how-to-data.zip'
if any( ( must_rebuild_file( infile, outfile ) for infile in infiles ) ):
    howto = 'examples/How to use this folder'
    ensure_shell_command_succeeds( f'pandoc --to=docx --output="{howto}.docx" "{howto}.md"' )
    ensure_folder_exists(
        os.path.join( jekyll_input_folder, 'assets', 'downloads' ) )
    ensure_shell_command_succeeds( f'cd examples && zip -orv9 "../{outfile}" *' )
else:
    print( 'No changes to source; no action needed.' )

# Run Jekyll on newly copied files
section_heading( 'Running Jekyll build process' )
ensure_shell_command_succeeds( 'bundle exec jekyll build --incremental --profile' )

# State completion
section_heading( 'Build completed successfully.' )
