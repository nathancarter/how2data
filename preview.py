#!/opt/conda/bin/python

##############
#
#  When adding new content to this website, the naive development workflow is
#  to place the new content in the database folder, then rebuild the site and
#  view it in a browser to ensure that it looks correct before committing and
#  pushing.
# 
#  The problem with that workflow is that rebuilding such a large site,
#  despite the efficiencies provided by the tools in this repository, can be
#  slow.  In particular, Jekyll's rebuilding of the site feed can take over 1
#  minute on some hardware.
#
#  This script is meant to solve that problem.
#
#  Instead of placing the new content into the database folder, place it in
#  the preview folder instead, like this example:
#    - this_repo/preview/description.md
#    - this_repo/preview/R.Rmd
#    - this_repo/preview/Python.ipynb
#  Then run this script from the repo root.  Here's what it does:
#
#  The script builds all of the files in the preview folder into a subfolder
#  of the preview folder, preview/generated/.  They will be in HTML format
#  with almost no styling, but all code will have been run and all output will
#  be included, as well as all equations rendered.
# 
#  Furthermore, the script ends by spinning up a simple web server and
#  printing links to localhost where all the generated pages can be viewed.
#  View them and use what you see to edit the sources, re-run the script, and
#  iterate to completion.
# 
#  When you've gotten the source files into acceptable form using this method,
#  you can then create a new task folder inside the database folder and move
#  them there, then rebuild the site once as a sanity check before committing
#  and pushing.
#
#  Thus you run many times this preview script, which is fast, but you run
#  only once the full site rebuilding script, which is slow.
#
##############

import os, sys, glob
from utils import *
from build_tools import *
import http.server
import socketserver
import functools

# Ensure preview folders exist
section_heading( 'Ensuring preview folders exist' )
preview_folder = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), 'preview' )
ensure_folder_exists( preview_folder )
generated_folder = os.path.join( preview_folder, 'generated' )
ensure_folder_exists( generated_folder )

# Delete all content from generated files folder
section_heading( 'Deleting old files from output folder' )
to_delete = os.path.join( generated_folder, '*' )
print( f'Running: rm {to_delete}' )
run_shell_command_ignoring_errors( f'rm {to_delete}' )

# Generate a task DataFrame from just the one task in the preview folder
section_heading( 'Gathering task description data' )
task_desc_file = get_unique_markdown_doc(
    os.path.join( preview_folder, 'description' ) )
tasks_df = pd.DataFrame( {
    'task name' : [ 'Preview' ],
    'task filename' : [ path_in_project( task_desc_file ) ],
    'content' : [ read_doc_to_markdown( task_desc_file ) ],
    'permalink' : [ blogify( 'Preview' ) ]
} )
tasks_df['markdown link'] = tasks_df['task name'].apply(
    lambda name: f'[{name}](../{blogify(name)})' )
# print( tasks_df )
print( task_desc_file )

# Generate a solutions DataFrame from just the solutions in the preview folder
section_heading( 'Gathering solutions data' )
json = [ ]
for solution_file in docs_inside( preview_folder ):
    if without_extension( solution_file ) == 'description':
        continue
    bits = without_extension( solution_file ).split( ', ' )
    software_name = bits[0]
    if len( bits ) == 1:
        solution_name = 'solution'
    else:
        solution_name = ', '.join( bits[1:] )
    input_file = os.path.join( preview_folder, solution_file )
    next = {
        'task name' : 'Preview',
        'software' : software_name,
        'solution name' : solution_name,
        'solution filename' : solution_file,
        'solution path' : path_in_project( input_file ),
        'solution title' : f'Preview (in {without_extension( solution_file )})'
    }
    markdown = read_doc_to_markdown( input_file )
    metadata, content = string_split_yaml_header( markdown )
    next['content'] = content + modification_text( input_file )
    for key, value in metadata.items():
        next[key] = value
    next['raw content'] = markdown
    next['permalink'] = blogify( next['solution title'] )
    json.append( next )
solutions_df = pd.DataFrame( json )
# Add links to solution pages to each solution row
def link_to_solution ( solution_row ):
    return f'[{solution_row["solution name"]}](../{blogify(solution_row["solution title"])})'
solutions_df['markdown link'] = solutions_df.apply( link_to_solution, axis=1 )
# print( solutions_df )
print( '\n'.join( list( solutions_df['solution filename'] ) ) )

# Load custom styles and scripts for previews
preamble = read_text_file( './jekyll-input/_includes/head_custom.html' ) + '''
    <meta charset="utf-8" />
    <style>
        div.sourceCode {
            background-color: #eeeeee;
            border: 1px solid #aaaaaa;
        }
    </style>
'''

# Build solutions and task
section_heading( 'Compiling solutions' )
for index, row in solutions_df.iterrows():
    generated_md = build_solution_page( row, True,
        in_folder=preview_folder, out_folder=generated_folder,
        task_row=tasks_df.iloc[0] )
    generated_html = generated_md[:-3] + '.html'
    ensure_shell_command_succeeds(
        f'pandoc --to=html --mathjax --output="{generated_html}" "{generated_md}"' )
    prepend_text_to_file( generated_html, preamble )
    print( f'Converted to {generated_html}\n' )
section_heading( 'Compiling task page' )
for index, row in tasks_df.iterrows():
    generated_md = build_task_page( row, out_folder=generated_folder,
                                    solution_rows=solutions_df )
    generated_html = generated_md[:-3] + '.html'
    ensure_shell_command_succeeds(
        f'pandoc --to=html --mathjax --output="{generated_html}" "{generated_md}"' )
    prepend_text_to_file( generated_html, preamble )
    print( f'Converted to {generated_html}\n' )

# Show it to the user via a simple HTTP server
section_heading( 'Preview generated successfully -- view it here:' )
port = 8000
print( generated_folder )
Handler = functools.partial( http.server.SimpleHTTPRequestHandler,
                             directory=generated_folder )
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer( ( '', port ), Handler ) as httpd:
    print( f'Task Description: http://localhost:{port}/preview.html' )
    for index, row in solutions_df.iterrows():
        print( f'Solution:         http://localhost:{port}/{row["permalink"]}.html' )
    httpd.serve_forever()
