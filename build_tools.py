
import os
from ruamel.yaml import YAML
import pandas as pd
import numpy as np
import re
import shutil
import sys

# What extensions count as documents vs. images?
# How can we easily filter for those extensions in a list of files?
doc_extensions = [ '.md', '.markdown' ]
img_extensions = [ '.jpg', '.jpeg', '.png', '.gif' ]
def has_any_extension ( filename, extensions ):
    return any( ( filename.endswith( ext ) for ext in extensions ) )
def is_doc ( filename ):
    return has_any_extension( filename, doc_extensions )
def is_img ( filename ):
    return has_any_extension( filename, img_extensions )
def just_docs ( filenames ):
    return [ x for x in filenames if is_doc( x ) ]
def just_imgs ( filenames ):
    return [ x for x in filenames if is_img( x ) ]
def subfolders ( folder ):
    return [ x for x in os.listdir( folder ) \
             if os.path.isdir( os.path.join( folder, x ) ) ]
def docs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_doc( x ) ]
def imgs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_img( x ) ]

# Function for printing section headings in the console output
def section_heading ( title ):
    print()
    print()
    print( title )
    print( '-' * len( title ) )

# Global variables for important folders in this repo and their contents
main_folder = os.path.dirname( os.path.realpath( __file__ ) )
static_folder = os.path.join( main_folder, 'database', 'static' )
static_pages = just_docs( os.listdir( static_folder ) )
tasks_folder = os.path.join( main_folder, 'database', 'tasks' )
task_files = [
    file for file in just_docs( os.listdir( tasks_folder ) ) \
    if file != 'README.md'
]
task_image_files = os.listdir( os.path.join( tasks_folder, 'images' ) )
jekyll_input_folder = os.path.join( main_folder, 'jekyll-input' )
solutions_folder = os.path.join( main_folder, 'database', 'solutions' )
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
solution_imgs_folder = os.path.join( jekyll_input_folder, 'assets', 'solution-images' )
if not os.path.isdir( solution_imgs_folder ):
    os.mkdir( solution_imgs_folder )
files_generated = [ ]

# Jupyter kernels for running code
kernel_for_software = {
    'Python' : 'python3',
    'Julia' : 'julia-1.6',
    'R' : 'ir'
}

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
    files_generated.append( filename )

# Function for copying an image file from a solutions subfolder to the Jekyll
# input folder.
def copy_solution_image_file ( task, software, image ):
    source = os.path.join( solutions_folder, task, software, image )
    dest = os.path.join( solution_imgs_folder, f'{task}-{software}-{image}' )
    shutil.copy2( source, dest )
    print( 'Copied: Source:', source )
    print( '        Dest:  ', dest )

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
tasks_table = pd.DataFrame( {
    "Task" : [ os.path.splitext( filename )[0] for filename in task_files ]
} )
for package in configuration['software']:
    tasks_table[f'Solutions in {package["name"]}'] = np.nan
tasks_table = tasks_table.to_markdown( index=False )

# How to tell if a given string is one of the official names of a task or a
# software package in our database?  We make some functions.
def is_a_task ( text ):
    return any( [ text + ext in task_files for ext in doc_extensions ] )
def is_a_software_package ( text ):
    return text in software_names

# How to blogify a title into a filename (with lower case and hyphens).
def blogify ( title ):
    return re.sub( '^-+|-+$', '', re.sub( '[^a-z0-9]+', '-', title.lower() ) )
def basename_and_extension ( filename ):
    bits = filename.split( '.' )
    return '.'.join( bits[:-1] ), bits[-1]

# For reading a text file and splitting it into its YAML header (if any)
# and text content:
def header_and_content ( filename ):
    with open( filename, 'r' ) as f:
        lines = f.readlines()
    # if yaml header exists, find its end and return it and the content
    if lines[0] == '---\n':
        lines = lines[1:]
        yaml_end = lines.index( '---\n' )
        return (
            YAML().load( ''.join( lines[:yaml_end] ) ),
            ''.join( lines[yaml_end+1:] )
        )
    # otherwise return an empty yaml header and just the content
    return {}, ''.join( lines )

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
    with open( tmp_md_doc, 'w' ) as f:
        f.write( markdown )
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
    with open( tmp_md_doc, 'r' ) as f:
        result = ''.join( f.readlines() )
    os.system( f'rm "{tmp_md_doc}"' )
    return result

# Must we rebuild an output file?  This function says yes if the output file
# does not exist, or is older than the input file that would be used to build it.
def must_rebuild_file ( input, output ):
    if not os.path.exists( output ):
        print( f'Must rebuild because DNE: {output}' )
        return True
    input_modified = os.path.getmtime( input )
    output_modified = os.path.getmtime( output )
    print( f'Which is older?\n{input_modified} {input}\n{output_modified} {output}' )
    return input_modified > output_modified

# For building solution pages, a few functions.  Parameters explained:
# task = exact task name, a key to the solution_docs dict.
# software = exact package name, a key to the solutions_docs[task] dict.
# solution = exact filename in the task/software/ folder, including extension.
def solution_page_destination ( task, software, solution ):
    return os.path.join( jekyll_input_folder, )
# Main function to build a solution page.  Parameters as above.
def build_solution_page ( task, software, solution ):
    basename, extension = basename_and_extension( solution )
    title = f'{task} ({basename}, in {software})'
    out_filename = blogify( title ) + '.md'
    input_file = os.path.join( solutions_folder, task, software, solution )
    output_file = os.path.join( jekyll_input_folder, out_filename )
    if not must_rebuild_file( input_file, output_file ):
        print( f'Not rebuilding this: {output_file}' )
        print( f'   It is newer than: {input_file}' )
        files_generated.append( out_filename )
        return
    header, content = header_and_content( input_file )
    def adjust_img_path ( code, alt_text, filename ):
        new_filename = f'{task}-{software}-{filename}'
        return (
            alt_text,
            os.path.join( '..', 'assets', 'solution-images', new_filename )
        )
    content = map_over_images( adjust_img_path, content )
    with open( output_file, 'w' ) as f:
        f.write( f'''---
layout: page
title: {title}
permalink: /{blogify(title)}/
nav_exclude: true
---

# {title}

(Later we will put here a link to the task page; not yet implemented.)

{run_markdown( content, os.path.join( solutions_folder, task, software ), software )}

{f'Contributed by {header["author"]}' if "author" in header else ''}
''' )
    print( f'Built solution for: {task}' )
    print( f'           Details: {basename}, in {software}' )
    print()
    files_generated.append( out_filename )

# How to clean up any markdown files we didn't just generate.
# One might think it would be easier to just blow away all markdown files before
# we generate the site, but that forces us to re-run all solution code every
# time, which is not efficient.  So we re-generate just the files we need to,
# and mark all the output files (regenerated or saved) as "generated," then
# delete every file not so marked.  Thus if any file were renamed before this
# build process, we will delete any old files generated from its old name.
def delete_ungenerated_markdown ():
    for file in os.listdir( jekyll_input_folder ):
        if is_doc( file ) and file not in files_generated:
            os.system( f'rm {os.path.join( jekyll_input_folder, file )}' )
