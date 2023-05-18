
# This Python script is not part of the How to Data build process.
# It is a separate script useful for the following particular purpose.
# If you've written a single document that contains many task-solution pairs,
# this script will break it into all the individual files to include in the
# database/ folder.
# 
# It supports:
#  * Markdown input (.md/.markdown)
#  * Jupyter notebook input (.ipynb)
#  * RMarkdown input (.Rmd)
# 
# It follows these conventions:
#  * Every top-level heading (#) should begin with "How to" and will be treated
#    as the name of a task whose description follows the heading.
#  * Every level-two heading (##) will be treated as the name of a solution,
#    and should follow the existing conventions for the site, such as
#    "R, using ggplot2" or "Python" or "Python, using NumPy."
#  * Text and code following a level-two heading will be treated as the content
#    of the solution, until a new heading comes along.
#
# Example document with those conventions:
# (start)---------------------------------
#
# # How to add two numbers
#
# Assume we have two numbers stored in variables a and b.  How do we sum them?
#
# ## Python
#
# We use the highly complex `+` operator.  Note the subtlety:
#
# ```python
# a + b
# ```
#
# ## R
#
# Don't be fooled; the solution in R is not at all like the solution in Python.
#
# ```R
# a + b
# ```
#
# (end)-----------------------------------
#
# Usage:
# python convert_doc.py my-input-file.md (or any other supported format)
# Creates a folder my-input-file/ containing all the task subfolders described
# in my-input-file.md.  These can be proofread and then moved to the
# database/tasks/ folder once they look good.

import sys
import os
import files
import markdown

###
###  ENSURE WE GOT A VALID INPUT FILE AND CAN READ IT
###

if len( sys.argv ) != 2:
    log.out( Usage='python convert_doc.py my-input-file.md' )
    sys.exit( 1 )
input_file = sys.argv[1]
if not os.path.isfile( input_file ):
    log.error( 'No such file', Filename=input_file )
valid_types = [ '.md', '.markdown', '.ipynb', '.Rmd' ]
if files.extension( input_file ) not in valid_types:
    log.error( 'Invalid file type:',
               Extension=files.extension( input_file ),
               Expected=', '.join( valid_types ) )
log.info( 'Processing input file' + input_file )
output_folder = files.without_extension( input_file )
if os.path.exists( output_folder ):
    log.error( 'Output folder already exists.  Delete it first?',
               Folder=output_folder )

###
###  CONVERT NON-MARKDOWN FORMATS TO LINES OF MARKDOWN
###

markdown_content = markdown.read_doc( input_file )
lines = markdown_content.split( '\n' )
log.info( 'Successfully read input file in markdown form.' )

###
###  PROCESS EACH LINE IN FILE
###

solutions = [ ]
task_name = None
task_text = None
solution_name = None
solution_text = None
def add_solution ():
    global task_name, task_text, solution_name, solution_text
    if task_name is None:
        return
    if task_text is not None:
        solutions.append( {
            'task name' : task_name,
            'task text' : task_text
        } )
        log.info( 'Stored task named:', task_name )
        task_text = None
        return
    if solution_name is not None and solution_text is not None:
        solutions.append( {
            'task name' : task_name,
            'solution name' : solution_name,
            'solution text' : solution_text
        } )
        log.info( 'Stored solution named:', solution_name )
        solution_name = None
        solution_text = None
        return
    log.error( 'Could not save the following data', **{
        "Task name" : task_name,
        "Task text" : task_text,
        "Solution name" : solution_name,
        "Solution text" : solution_text
    } )
for index, line in enumerate( lines ):
    if line.startswith( '# How to ' ):
        add_solution()
        task_name = line[2:]
        task_text = ''
        log.info( f'Line {index+1} is a task heading: {task_name}' )
    elif line.startswith( '## ' ):
        add_solution()
        solution_name = line[3:]
        solution_text = ''
        log.info( f'Line {index+1} is a solution heading: {solution_name}' )
    elif solution_text != None:
        solution_text += line + '\n'
    elif task_text != None:
        task_text += line + '\n'
    elif line.strip() == '':
        continue
    else:
        log.error( f'Unexpected content in line {index+1}:\n{line}',
                   Details='Content should be inside only tasks or solutions.' )
add_solution()

###
###  WRITE OUTPUT FILES
###

files.ensure_folder_exists( output_folder )
def make_file ( name, text ):
    files.write_text_file( name, text )
    log.built( name )
for solution in solutions:
    task_folder = os.path.join( output_folder, solution['task name'] )
    if 'task text' in solution:
        files.ensure_folder_exists( task_folder )
        make_file( os.path.join( task_folder, 'description.md' ),
            solution['task text'] )
    else:
        output_file = os.path.join( task_folder, solution['solution name']+'.md' )
        make_file( output_file, solution['solution text'] )
log.info( 'Done.' )
