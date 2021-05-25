
#######################
#
#  High-level build tools factored out of build.py to keep that file cleaner.
#  Lower-level tools appear in utils.py; most are independent of this project,
#  such as shortcuts for reading/writing text files.
#  Declarations of constants specific to this project are in build_constants.py. 
#
#######################

from build_constants import *
from build_database import *
from utils import *
import os
import pandas as pd
import numpy as np
import re
import shutil
import sys

###
###  FILES, FOLDERS, AND CONFIGURATION
###

# Ensure certain key folders exist
ensure_folder_exists( task_imgs_folder )
ensure_folder_exists( solution_imgs_folder )

# The software table to be inserted on the software packages page
software_table = software_df[['name', 'icon markdown', 'num solutions', 'website markdown']]
software_table.columns = ['Software Package', 'Icon', 'Number of solutions', 'Website']
software_table = software_table.to_markdown( index=False )

# Generate the tasks table for the tasks page and render as markdown
tasks_table = pd.DataFrame( { 'Task' : tasks_df['markdown link'] } )
def links_for_task_solutions_in_software ( task_name, software_name ):
    return ', '.join( list( solutions_df[ \
        (solutions_df['task name'] == task_name) & \
        (solutions_df['software'] == software_name)]['markdown link'] ) )
for index, software_row in software_df.iterrows():
    tasks_table[f'Solutions in {software_row["name"]}'] = \
        tasks_df['task name'].apply( lambda task_name:
            links_for_task_solutions_in_software( task_name, software_row['name'] ) )
tasks_table = tasks_table.to_markdown( index=False )

###
###  MOVING/TRACKING FILES
###

# We will generate a lot of markdown files in the Jekyll input folder.
# But we don't want any old/stale files to stay there across builds, such as if we
# were to rename a source file, thus generating a file of a different name, and
# orphaning the original.
# But if we just wipe the dest folder every time, we lose a big opportunity for
# efficiency by not re-generating expensive files that aren't stale.
# So we create the following functions to mark what's been regenerated and what
# hasn't, and let us delete any no-longer-needed stuff.
files_generated = [ ]
def mark_as_regenerated ( file ):
    files_generated.append( file )
def delete_ungenerated_markdown ():
    for file in os.listdir( jekyll_input_folder ):
        if is_doc( file ) and file not in files_generated:
            os.system( f'rm {os.path.join( jekyll_input_folder, file )}' )

# Function for copying a static file from the database folder to the
# Jekyll input folder, optionally doing some text replacements en route
def copy_static_file ( filename, replacements = dict() ):
    source = os.path.join( static_folder, filename )
    dest = os.path.join( jekyll_input_folder, filename )
    content = read_text_file( source )
    for original, replacement in replacements.items():
        content = content.replace( original, replacement )
    write_text_file( dest, content )
    print( 'Copied: Source:      ', source )
    print( '        Dest:        ', dest )
    print( '        Replacements:', len(replacements) )
    mark_as_regenerated( filename )

# Function for copying an image file from a solutions subfolder to the Jekyll
# input folder.
def copy_solution_image_file ( task, software, image ):
    source = os.path.join( solutions_folder, task, software, image )
    dest = os.path.join( solution_imgs_folder, f'{task}-{software}-{image}' )
    shutil.copy2( source, dest )
    print( 'Copied: Source:', source )
    print( '        Dest:  ', dest )
# Function for copying a task file from a solutions subfolder to the Jekyll
# input folder.
def copy_task_image_file ( filename ):
    source = os.path.join( tasks_folder, filename )
    dest = os.path.join( task_imgs_folder, filename )
    shutil.copy2( source, dest )
    print( 'Copied: Source:', source )
    print( '        Dest:  ', dest )

###
###  PROCESSING MARKDOWN AND RUNNING CODE THEREIN
###

# When processing a markdown file, we may want to manipulate its image
# links.  The following function maps any given function over the set
# of image links in a string containing markdown, producing a new string.
# The function passed as input should take as input three parameters:
# img_code = the full image code, such as "![alt-text here](filename.png)"
# alt_text = just the alt text, what's in between the brackets above
# filename = just the filename, what's in between parentheses above
# It should return either a new image tag as a string OR an alt-text/filename
# pair as a tuple, which will be formed into an image tag.
def map_over_images ( func, markdown ):
    result = ''
    while True:
        match = re.search( '!\\[([^]]*)\\]\\(([^)]*)\\)', markdown )
        if match is None:
            break
        start, end = match.span()
        changed = func( match.group( 0 ), match.group( 1 ), match.group( 2 ) )
        if type( changed ) == tuple:
            changed = f'![{changed[0]}]({changed[1]})'
        result += markdown[:start] + changed
        markdown = markdown[end:]
    return result + markdown

# Function to run a given markdown document as if it were a Jupyter notebook.
# You specify the markdown content as a string, the folder in which to run it
# (using a temp file that will be deleted aftewards), and the name of the
# software package.  If that software package has a kernel, according to the
# kernel_for_software dictionary defined above, we will run it using that
# kernel; otherwise this function will function as the identity function.
# It returns another string of markdown content, this time with execution
# outputs included (iff there is a relevant kernel).
def run_markdown ( markdown, folder, software ):
    if software in kernel_for_software:
        kernel = kernel_for_software[software]
    else:
        return markdown
    tmp_md_doc = os.path.join( folder, 'jupyter-temp-file.md' )
    ipynb_out = tmp_md_doc[:-3] + '.ipynb'
    # write markdown to temp file
    write_text_file( tmp_md_doc, markdown )
    # run it, creating a notebook containing the outputs
    code = os.system( 'jupytext --to ipynb --execute ' + \
        f'--set-kernel {kernel} --output="{ipynb_out}" "{tmp_md_doc}"' )
    os.system( f'rm "{tmp_md_doc}"' )
    if code != 0:
        sys.exit( code )
    # convert that to markdown again
    code = os.system( 'jupyter nbconvert --to=markdown ' + \
        f'--output="{tmp_md_doc}" "{ipynb_out}"' )
    os.system( f'rm "{ipynb_out}"' )
    if code != 0:
        sys.exit( code )
    # read it back into a string
    result = read_text_file( tmp_md_doc )
    os.system( f'rm "{tmp_md_doc}"' )
    return result

# Main function to build a solution page.  Parameter is any row from solutions_df.
def build_solution_page ( solution_row ):
    out_filename = blogify( solution_row['solution title'] ) + '.md'
    input_file = os.path.join( solutions_folder, solution_row['task name'],
        solution_row['software'], solution_row['solution filename'] )
    output_file = os.path.join( jekyll_input_folder, out_filename )
    if not must_rebuild_file( input_file, output_file ):
        print( f'Not rebuilding this: {output_file}' )
        print( f'   It is newer than: {input_file}' )
        mark_as_regenerated( out_filename )
        return
    metadata = solution_row['metadata']
    def adjust_img_path ( code, alt_text, filename ):
        new_filename = f'{task}-{software}-{filename}'
        return (
            alt_text,
            os.path.join( '..', 'assets', 'solution-images', new_filename )
        )
    content = map_over_images( adjust_img_path, solution_row['content'] )
    write_text_file( output_file,
        solution_template
        .replace( 'TITLE', title )
        .replace( 'PERMALINK', blogify( title ) )
        .replace( 'TASK_PAGE_LINK',
            '(Later we will put here a link to the task page; not yet implemented.)' )
        .replace( 'MARKDOWN_CONTENT', wrap_in_html_comments( run_markdown(
            content,
            os.path.join( solutions_folder, task, software ),
            software ) ) )
        .replace( 'CONTRIBUTORS',
            f'Contributed by {metadata["author"]}' if "author" in metadata else '' )
    )
    print( f'Built solution for: {solution_row["task name"]}' )
    print( f'          Software: {solution_row["software"]}' )
    print( f'     Solution name: {solution_row["solution name"]}' )
    print()
    mark_as_regenerated( out_filename )

# How to fetch a generated solution's body from within the generated markdown
def get_generated_solution_body ( solution_row ):
    title = solution_row['solution title']
    generated_file = blogify( title ) + '.md'
    all_content = read_text_file( os.path.join( jekyll_input_folder, generated_file ) )
    return unwrap_from_html_comments( all_content )

# How to build a task page; pass any row from tasks_df.
# IMPORTANT NOTE:  This assumes that you've already processed all the solutions files
# using the build_solution_page() function on any files that need their solutions
# rebuilt/updated.  See that function defined above.
def build_task_page ( row ):
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( jekyll_input_folder, out_filename )
    def adjust_img_path ( code, alt_text, filename ):
        return (
            alt_text,
            os.path.join( '..', 'assets', 'task-images', filename )
        )
    content = map_over_images( adjust_img_path, row['content'] )
    all_solutions = ''
    software_for_this_task = \
        solutions_df[solutions_df['task name'] == row['task name']]
    for index, solution_row in software_for_this_task.iterrows():
        solution_name = without_extension( solution_row['solution name'] )
        solution_name = solution_name[0].upper() + solution_name[1:]
        all_solutions += f'''

## {solution_name}, in {solution_row["software"]}

{get_generated_solution_body( solution_row )}

'''
    if all_solutions == '':
        all_solutions = '## Solutions\n\nNo solutions exist yet in the database for this task.'
    opportunities = list( software_df['name'][
        ~software_df['name'].isin(software_for_this_task['software'])] )
    if len( opportunities ) > 0:
        opportunities = '\n'.join(
            [ f' * {software}' for software in opportunities ] )
    else:
        opportunities = '*None* --- this task has solutions for each ' + \
            'software package in this website\'s database.'
    write_text_file( output_file,
        files_df[files_df['filename'] == 'task-template.md']['raw content'].iloc[0]
        .replace( 'TITLE', row['task name'] )
        .replace( 'PERMALINK', row['permalink'] )
        .replace( 'DESCRIPTION', 'Description of the task will go here.' )
        .replace( 'SOLUTIONS', all_solutions )
        .replace( 'TOPICS', 'Topics are not yet implemented.' )
        .replace( 'OPPORTUNITIES', opportunities )
    )
    mark_as_regenerated( out_filename )
