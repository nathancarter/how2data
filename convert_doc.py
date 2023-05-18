
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
from utils import *
import files

###
###  ENSURE WE GOT A VALID INPUT FILE AND CAN READ IT
###

if len( sys.argv ) != 2:
    print( 'Usage: python convert_doc.py my-input-file.md' )
    sys.exit( 1 )
input_file = sys.argv[1]
if not os.path.isfile( input_file ):
    print( 'No such file:', input_file )
    sys.exit( 1 )
valid_types = [ '.md', '.markdown', '.ipynb', '.Rmd' ]
if files.extension( input_file ) not in valid_types:
    print( 'Invalid file type:', files.extension( input_file ) )
    print( '  Expected one of:', ', '.join( valid_types ) )
    sys.exit( 1 )
print( 'Processing this input file:', input_file )
output_folder = files.without_extension( input_file )
if os.path.exists( output_folder ):
    print( 'This file/folder exists already:', output_folder )
    print( 'We cannot use it as the output folder.  Delete it first?' )
    sys.exit( 1 )

###
###  CONVERT NON-MARKDOWN FORMATS TO LINES OF MARKDOWN
###

markdown = read_doc_to_markdown( input_file )
lines = markdown.split( '\n' )
print( 'Successfully read input file in markdown form.' )

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
        print( '\tStored task named:', task_name )
        task_text = None
        return
    if solution_name is not None and solution_text is not None:
        solutions.append( {
            'task name' : task_name,
            'solution name' : solution_name,
            'solution text' : solution_text
        } )
        print( '\tStored solution named:', solution_name )
        solution_name = None
        solution_text = None
        return
    print( 'Error saving this stuff:' )
    print( '\tTask name:', task_name )
    print( '\tTask text:', task_text )
    print( '\tSolution name:', solution_name )
    print( '\tSolution text:', solution_text )
    sys.exit( 1 )
for index, line in enumerate( lines ):
    if line.startswith( '# How to ' ):
        add_solution()
        task_name = line[2:]
        task_text = ''
        print( f'\tLine {index+1} is a task heading: {task_name}' )
    elif line.startswith( '## ' ):
        add_solution()
        solution_name = line[3:]
        solution_text = ''
        print( f'\tLine {index+1} is a solution heading: {solution_name}' )
    elif solution_text != None:
        solution_text += line + '\n'
    elif task_text != None:
        task_text += line + '\n'
    elif line.strip() == '':
        continue
    else:
        print( f'Unexpected content in line {index+1}:\n{line}' )
        print( 'Content should only be inside tasks or solutions.' )
        sys.exit( 1 )
add_solution()

###
###  WRITE OUTPUT FILES
###

files.ensure_folder_exists( output_folder )
def make_file ( name, text ):
    files.write_text_file( name, text )
    print( 'Created file:', name )
for solution in solutions:
    task_folder = os.path.join( output_folder, solution['task name'] )
    if 'task text' in solution:
        files.ensure_folder_exists( task_folder )
        make_file( os.path.join( task_folder, 'description.md' ),
            solution['task text'] )
    else:
        output_file = os.path.join( task_folder, solution['solution name']+'.md' )
        make_file( output_file, solution['solution text'] )
print( 'Done.' )
