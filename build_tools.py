
#######################
#
#  High-level build tools factored out of build.py to keep that file cleaner.
#  Lower-level tools appear in utils.py; most are independent of this project,
#  such as shortcuts for reading/writing text files.
#  Declarations of constants specific to this project are in build_constants.py. 
#
#######################

from build_constants import *
from utils import *
import os
import pandas as pd
import numpy as np
import re
import shutil
import sys

# Ensure certain key folders exist
ensure_folder_exists( task_imgs_folder )
ensure_folder_exists( solution_imgs_folder )

# Read important content from files and directories
static_pages = just_docs( os.listdir( static_folder ) )
task_image_files = os.listdir( os.path.join( tasks_folder, 'images' ) )
solution_template = read_text_file( os.path.join( static_folder, 'solution-template.md' ) )
task_template = read_text_file( os.path.join( static_folder, 'task-template.md' ) )

# Read database/database.yml and store it in a global variable
configuration = read_yaml_from_file( database_config_file )

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
task_files = [
    file for file in just_docs( os.listdir( tasks_folder ) ) \
    if file != 'README.md'
]
tasks_table = pd.DataFrame( {
    "Task" : [ without_extension( filename ) for filename in task_files ]
} )
for package in configuration['software']:
    tasks_table[f'Solutions in {package["name"]}'] = np.nan
tasks_table = tasks_table.to_markdown( index=False )
# How to tell if a given string is one of the official names of a task?
def get_task_filename ( task ):
    for extension in doc_extensions:
        if task + extension in task_files:
            return os.path.join( tasks_folder, task + extension )
    return None
def is_a_task ( text ):
    return get_task_filename( text ) != None
# How to read a task file's markdown content
def get_task_content ( task ):
    filename = get_task_filename( task )
    if filename is None:
        print( 'Could not find filename for task:', task )
        sys.exit( 1 )
    return read_text_file( filename )


# Data about solutions
solution_docs = {
    task : {
        software : docs_inside( os.path.join( solutions_folder, task, software ) ) \
        for software in subfolders( os.path.join( solutions_folder, task ) )
    } \
    for task in subfolders( solutions_folder )
}
solution_imgs = [
    ( task, software, x ) \
    for task in subfolders( solutions_folder ) \
    for software in subfolders( os.path.join( solutions_folder, task ) ) \
    for x in imgs_inside( os.path.join( solutions_folder, task, software ) )
]
# How to tell if a given string is one of the official names of a software package?
def is_a_software_package ( text ):
    return text in software_names
# Functions for solution files.  Parameters explained:
# task = exact task name, a key to the solution_docs dict.
# software = exact package name, a key to the solutions_docs[task] dict.
# solution = exact filename in the task/software/ folder, including extension.
def solution_page_destination ( task, software, solution ):
    return os.path.join( jekyll_input_folder, )
# What should the title be within such a solution page?
def solution_page_title ( task, software, solution ):
    return f'{task} ({without_extension( solution )}, in {software})'


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

# Main function to build a solution page.  Parameters are the same as they
# are for solution_page_destination(), solution_page_title().
def build_solution_page ( task, software, solution ):
    title = solution_page_title( task, software, solution )
    out_filename = blogify( title ) + '.md'
    input_file = os.path.join( solutions_folder, task, software, solution )
    output_file = os.path.join( jekyll_input_folder, out_filename )
    if not must_rebuild_file( input_file, output_file ):
        print( f'Not rebuilding this: {output_file}' )
        print( f'   It is newer than: {input_file}' )
        mark_as_regenerated( out_filename )
        return
    header, content = file_split_yaml_header( input_file )
    def adjust_img_path ( code, alt_text, filename ):
        new_filename = f'{task}-{software}-{filename}'
        return (
            alt_text,
            os.path.join( '..', 'assets', 'solution-images', new_filename )
        )
    content = map_over_images( adjust_img_path, content )
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
            f'Contributed by {header["author"]}' if "author" in header else '' )
    )
    print( f'Built solution for: {task}' )
    print( f'           Details: {without_extension( solution )}, in {software}' )
    print()
    mark_as_regenerated( out_filename )

# How to fetch a generated solution's body from within the generated markdown
def get_generated_solution_body ( task, software, solution ):
    title = solution_page_title( task, software, solution )
    generated_file = blogify( title ) + '.md'
    all_content = read_text_file( os.path.join( jekyll_input_folder, generated_file ) )
    return unwrap_from_html_comments( all_content )

# How to build a task page
# IMPORTANT NOTE:  This assumes that you've already processed all the solutions files
# using the build_solution_page() function on any files that need their solutions
# rebuilt/updated.  See that function defined above.
def build_task_page ( task ):
    out_filename = blogify( task ) + '.md'
    output_file = os.path.join( jekyll_input_folder, out_filename )
    def adjust_img_path ( code, alt_text, filename ):
        return (
            alt_text,
            os.path.join( '..', 'assets', 'task-images', filename )
        )
    content = get_task_content( task )
    content = map_over_images( adjust_img_path, content )
    all_solutions = ''
    if task in solution_docs:
        for software, solutions in solution_docs[task].items():
            for solution in solutions:
                solution_name = without_extension( solution )
                solution_name = solution_name[0].upper() + solution_name[1:]
                all_solutions += f'''

## {solution_name}, {software}

{get_generated_solution_body( task, software, solution )}

'''
        opportunities = [ x for x in software_names if x not in solution_docs[task] ]
    else:
        all_solutions = 'No solutions exist yet in the database for this task.'
        opportunities = software_names
    write_text_file( output_file,
        task_template
        .replace( 'TITLE', task )
        .replace( 'PERMALINK', blogify( task ) )
        .replace( 'DESCRIPTION', 'Description of the task will go here.' )
        .replace( 'SOLUTIONS', all_solutions )
        .replace( 'TOPICS', 'Topics are not yet implemented.' )
        .replace( 'OPPORTUNITIES',
            '\n'.join( [ f' * {software}' for software in opportunities ] ) )
    )
    mark_as_regenerated( out_filename )
