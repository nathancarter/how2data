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
#  slow.  In particular, Jekyll's rebuilding of the site feed can take over
#  30 seconds on some hardware.
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
#  and pushing.  There is a script to automate this process, finish_preview.sh,
#  in this same folder.
#
#  Thus you run many times this preview script, which is fast, but you run
#  only once the full site rebuilding script, which is slow.
#
##############

import os, sys, glob
from build_tools import *
import http.server
import socketserver
import functools
import files
import markdown
import yaml
import log
import shell

# Ensure preview folders exist
log.heading( 'Ensuring preview folders exist' )
preview_folder = os.path.join(
    os.path.dirname( os.path.realpath( __file__ ) ), 'preview' )
files.ensure_folder_exists( preview_folder )
generated_folder = os.path.join( preview_folder, 'generated' )
files.ensure_folder_exists( generated_folder )

# Delete all content from generated files folder
log.heading( 'Deleting old files from output folder' )
to_delete = os.path.join( generated_folder, '*' )
log.file_delete( to_delete )
shell.run_and_continue( f'rm {to_delete}' )

# Generate a task DataFrame from just the one task in the preview folder
log.heading( 'Gathering task description data' )
task_desc_file = markdown.get_unique_doc(
    os.path.join( preview_folder, 'description' ) )
tasks_df = pd.DataFrame( {
    'task name' : [ 'Preview' ],
    'task filename' : [ config.relativize_path( task_desc_file ) ],
    'content' : [ markdown.read_doc( task_desc_file ) ],
    'permalink' : [ config.blogify( 'Preview' ) ]
} )
tasks_df['markdown link'] = tasks_df['task name'].apply(
    lambda name: f'[{name}](../{config.blogify(name)})' )
# print( tasks_df )
log.info( f"Read file: {task_desc_file}" )

# Generate a solutions DataFrame from just the solutions in the preview folder
log.heading( 'Gathering solutions data' )
json = [ ]
for solution_file in files.docs_inside( preview_folder ):
    if files.without_extension( solution_file ) == 'description':
        continue
    bits = files.without_extension( solution_file ).split( ', ' )
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
        'solution path' : config.relativize_path( input_file ),
        'solution title' : f'Preview (in {files.without_extension( solution_file )})'
    }
    markdown_content = markdown.read_doc( input_file )
    metadata, content = yaml.split_string( markdown_content )
    next['content'] = content + files.modification_text( input_file )
    for key, value in metadata.items():
        next[key] = value
    next['raw content'] = markdown_content
    next['permalink'] = config.blogify( next['solution title'] )
    json.append( next )
solutions_df = pd.DataFrame( json )
# Add links to solution pages to each solution row
def link_to_solution ( solution_row ):
    return f'[{solution_row["solution name"]}](../{config.blogify(solution_row["solution title"])})'
solutions_df['markdown link'] = solutions_df.apply( link_to_solution, axis=1 )
# print( solutions_df )
log.info( 'Read solutions', **{
    f"Solution {i+1}" : solutions_df['solution filename'].iloc[i]
    for i in range(len(solutions_df))
} )

# Load custom styles and scripts for previews
preamble = files.read_text_file( './jekyll-input/_includes/head_custom.html' ) + '''
    <meta charset="utf-8" />
    <style>
        div.sourceCode {
            background-color: #eeeeee;
            border: 1px solid #aaaaaa;
        }
    </style>
'''

# Build solutions and task
log.heading( 'Compiling solutions' )
for index, row in solutions_df.iterrows():
    solution = solutions.Solution( row )
    solution.build_file( preview_folder, generated_folder, tasks.Task( tasks_df.iloc[0] ) )
    generated_html = generated_md[:-3] + '.html'
    shell.run_or_halt(
        f'pandoc --to=html --mathjax --output="{generated_html}" "{generated_md}"' )
    files.prepend_text_to_file( generated_html, preamble )
    # print( f'Converted to {generated_html}\n' )
    log.built( f"HTML for {row['solution name']}", generated_html, generated_md )
log.heading( 'Compiling task page' )
for index, row in tasks_df.iterrows():
    generated_md = tasks.Task( row ).build_file( generated_folder, solutions_df )
    generated_html = generated_md[:-3] + '.html'
    shell.run_or_halt(
        f'pandoc --to=html --mathjax --output="{generated_html}" "{generated_md}"' )
    files.prepend_text_to_file( generated_html, preamble )
    # print( f'Converted to {generated_html}\n' )
    log.built( f"HTML for {row['task name']}", generated_html, generated_md )

# Show it to the user via a simple HTTP server
log.heading( 'Preview generated successfully' )
port = 8000
handler = functools.partial( http.server.SimpleHTTPRequestHandler,
                             directory=generated_folder )
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer( ( '', port ), handler ) as httpd:
    log.info( 'View preview here', **{
        "Folder" : generated_folder,
        "Task Description" : f"http://localhost:{port}/preview.html"
        **{
            f"Solution {i+1}" : f"http://localhost:{port}/{row['permalink']}.html"
            for i, row in solutions_df.iterrows()
        }
    } )
    httpd.serve_forever()
