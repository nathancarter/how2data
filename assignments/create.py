#!/opt/conda/bin/python

# For information on how this script works, see the README.md file in the
# /assignments folder in this repository.

#####
#
#  Import main tools from the repo
#
#####

import sys, os
script_folder = os.path.dirname( os.path.realpath( __file__ ) )
parent_folder = os.path.dirname( script_folder )
sys.path.append( parent_folder )
from build_tools import *
from collections import OrderedDict
import json
import files

#####
#
#  Data and functions used by the main code further below
#
#####

def print_usage_info ():
    print( f'''{sys.argv[0]} usage:

create.py software
    summarize the software supported and the default file format for each
create.py formats
    list all supported file formats, including ones that may not be the
    default file format for any given piece of software
create.py list
    summarize the opportunities for creating assignments
create.py list verbose
    same as previous, plus also include the name of every relevant task
create.py list <X> <Y>
    list of tasks that could be converted from software X to software Y
create.py convert <X> <Y> [format] [text]
    convert tasks in software X to assignments in software Y, stored in files
    in the given format.  If the format is not provided, the default format
    for software Y is used instead.  If the final argument is provided, then
    only tasks whose names contain that text are converted.
''' )

# Compute binary information of which tasks have solutions in which software
binary_info = solutions_df()[['task name','software']].copy().drop_duplicates()
binary_info['marker'] = 1
binary_info = binary_info.pivot(
    index=['task name'], columns='software', values='marker' )
binary_info = binary_info.fillna( 0 )
for sw in software_df().name:
    binary_info[sw] = binary_info[sw].astype( bool )

# Declarations of file formats supported, plus defaults
supported_formats = {
    "Rmd" : "RMarkdown",
    "ipynb" : "Jupyter notebooks",
    "docx" : "Microsoft Word documents"
}
default_formats = {
    "R" : "Rmd",
    "Python" : "ipynb",
    "Excel" : "docx"
}
software_using_code = [ 'R', 'Python' ] # not Excel

# List every possible ordered pair of distinct software packages
def software_pairs ():
    return [
        (a,b) for a in software_df().name for b in software_df().name if a != b
    ]

# Compute the list of task names that need to be (or could be) converted from
# one given piece of software to another given piece of software
def tasks_to_convert ( have, need ):
    select_rows = binary_info[have] & ~binary_info[need]
    return list( binary_info[select_rows].index )

# Get the sections (contents of level-2 headings) from a markdown string,
# returning the result as a heading-to-content mapping, in dictionary form.
def sections ( markdown ):
    result = OrderedDict()
    section = None
    content = ''
    for line in markdown.split( '\n' ):
        if line[:3] == '## ':
            if section is not None:
                result[section] = content
            section = line[3:]
            content = ''
        elif section is not None:
            content += line + '\n'
    return result

# Link to a page in the site online
def online_link ( page_name ):
    return f'https://how-to-data.org/{page_name}/'

# Extract from a solution section the link to view that solution alone
def extract_view_link ( section_content ):
    link_lines = [
        line for line in section_content.split( '\n' )
        if '[View this solution alone.](' in line
    ]
    if len( link_lines ) != 1:
        raise Error( f'Expected 1 view link, found {len(link_lines)}.' )
    return online_link( link_lines[0][31:-1] )

# Extract from a solution section just its inner content, dropping the view
# link from the top and the timestamp and contact-us link from the bottom
def extract_inner_content ( section_content ):
    view_link_start = section_content.index( '[View this solution alone.](' )
    view_link_end = section_content.index( ')', view_link_start )
    timestamp_start = section_content.index( 'Content last modified on ' )
    return section_content[view_link_end+1:timestamp_start]

# Alter each code block using the given callback
def alter_code_blocks ( markdown, callback ):
    result = ''
    block_content = None
    for line in markdown.split( '\n' ):
        if block_content is None: # outside a block
            if line.startswith( '```' ): # new block starts here!
                block_content = line + '\n'
            else:
                result += line + '\n'
        else: # inside a block
            block_content += line + '\n'
            if line.startswith( '```' ): # old block ends here
                result += callback( block_content )
                block_content = None
    if block_content is not None:
        raise Error( 'Ended markdown inside a code block' )
    return result
# Callback for changing from one software to another
def change_software ( from_sw, to_sw ):
    if to_sw in software_using_code:
        line1 = f'### You should replace it with {to_sw} code instead.'
        line2 = f'### After changing the code above, be sure you get the same'
        line3 = '### Then delete these comments surrounding your code.\n' + \
                f'### And delete the old {from_sw} output (below) as well.'
    else:
        line1 = f'### You should replace this whole block with instructions\n' + \
                f'### on how to accomplish the same goal using {to_sw} instead.'
        line2 = f'### After replacing this code, be sure your method gets the same'
        line3 = '### When you\'re done, this code and its output should be gone.'
    def result ( block_markdown ):
        lines = block_markdown.split( '\n' )
        return '\n'.join( [
            f'```{to_sw}',
            f'### The {from_sw} code below has been commented out.',
            line1,
            f'###',
            '',
            *[ f'# {line}' for line in lines[1:-2] ],
            '',
            '###',
            line2,
            f'### results that the original {from_sw} code gave, shown below.',
            line3,
            '```'
        ] ) + '\n'
    return result

# Convert markdown to Jupyter notebook format
def quote_each_line ( text, indent=0 ):
    return ',\n'.join( [
        ( ' ' * indent ) + json.dumps( line+'\n' )
        for line in text.split( '\n' )
    ] )
def md_to_md_cell ( markdown ):
    return f'''  {{
   "source": [
{quote_each_line( markdown )}
   ],
   "cell_type": "markdown",
   "metadata": {{}}
  }}'''
def code_to_code_cell ( code ):
    return f'''  {{
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {{}},
   "outputs": [],
   "source": [
{quote_each_line( code )}
   ]
  }}'''
def notebook_with_cells ( cells ):
    tmp_file = os.path.join( script_folder, 'tmp' )
    files.write_text_file( tmp_file+'.md', 'Dummy text' )
    ensure_shell_command_succeeds(
        f'pandoc "{tmp_file}.md" --output="{tmp_file}.ipynb"',
        f'rm "{tmp_file}.md"' )
    template = json.loads( files.read_text_file( tmp_file+'.ipynb' ) )
    ensure_shell_command_succeeds( f'rm "{tmp_file}.ipynb"' )
    flag = "REPLACE_THIS_WITH_ACTUAL_CELLS"
    template["cells"] = [ flag ]
    return json.dumps( template ).replace( '"'+flag+'"', ',\n'.join( cells ) )
def md_to_ipynb ( markdown ):
    cells = [ ]
    md = ''
    code = None
    for line in markdown.split( '\n' ):
        if code is None: # outside a block
            if line.startswith( '```' ): # new block starts here!
                cells.append( md_to_md_cell( md ) )
                md = None
                code = ''
            else: # extend existing markdown section
                md += line + '\n'
                if line.startswith( '-----' ): # start a new cell
                    cells.append( md_to_md_cell( md ) )
                    md = ''
        else: # inside a block
            if line.startswith( '```' ): # old block ends here
                cells.append( code_to_code_cell( code ) )
                md = ''
                code = None
            else: # extend existing code section
                code += line + '\n'
    if code is not None:
        raise Error( 'Ended markdown inside a code block' )
    else:
        cells.append( md_to_md_cell( md ) )
    return notebook_with_cells( cells )

# Export some markdown text in a chosen file format, using a temp file and
# pandoc as needed
def finalize_export ( filename, markdown, format ):
    out_folder = os.path.dirname( filename )
    print( f'Ensuring folder exists:', out_folder )
    files.ensure_folder_exists( out_folder )
    if format in ['md','markdown','Markdown']:
        print( f'Exporting {filename}.md...' )
        files.write_text_file( filename+'.md', markdown )
    elif format in ['ipynb']:
        print( f'Exporting {filename}.ipynb...' )
        files.write_text_file( filename+'.ipynb', md_to_ipynb( markdown ) )
    elif format in ['doc','docx']:
        print( f'Exporting {filename}.md...' )
        files.write_text_file( filename+'.md', markdown )
        print( f'Converting to {format}...' )
        ensure_shell_command_succeeds(
            f'pandoc "{filename}.md" --output="{filename}.{format}"',
            f'rm "{filename}.md"' )
    elif format in ['Rmd','RMarkdown','Rmarkdown']:
        print( f'Exporting {filename}.md...' )
        files.write_text_file( filename+'.md',
            markdown.replace( '\n```R', '\n```{r}' ) )
        print( f'Converting to {format}...' )
        ensure_shell_command_succeeds(
            f'mv "{filename}.md" "{filename}.Rmd"' )
    else:
        raise Error( f'FORMAT {format} NOT YET IMPLEMENTED!' )
    print( 'Done.' )

# Convert the given task from software 1 to software 2, storing the result in
# a file in the given format, stored in this folder (with this script).
def convert ( task_name, from_sw, to_sw, format ):
    # Get markdown content of software in which the task is already solved
    content = files.read_text_file(
        os.path.join( jekyll_input_folder, blogify( task_name )+'.md' ) )
    sections_dict = sections( content )
    # For each solution in the "from" software, create a file in the "to"
    # software that contains the old solution, plus instructions on how to
    # update it into the new software.
    relevant_sections = [ s for s in sections_dict
                          if s.endswith( f'in {from_sw}' ) ]
    for rel_sec in relevant_sections:
        out_file = os.path.join( script_folder, task_name, rel_sec )
        out_content = f'''
# Assignment: {task_name} in {to_sw}

**This file should help you write a solution to the task "{task_name}" using
{to_sw}.**

## Getting started

 1. Read the full description of the "{task_name}" task.  You can find it
    [on this page]({online_link(blogify(task_name))})
    of the How to Data website.
 2. Read the solution below, which was written using {from_sw}.  You can see
    that same solution displayed more nicely on the same page from the site,
    or you can view it in isolation
    [on this page]({extract_view_link(sections_dict[rel_sec])}).
'''
        if from_sw in software_using_code and to_sw in software_using_code:
            out_content += f'''

## Doing the work

 * Your job is to replace the old code in {from_sw} with new code in {to_sw}.
   This may also require altering some of the text outside the code blocks.
'''[1:]
        elif from_sw in software_using_code:
            out_content += f'''
 * Your job is to replace the code blocks with written instructions, because
   {from_sw} uses code but {to_sw} does not.  This probably requires altering
   some of the text that currently sits outside the code blocks.
'''[1:]
        elif to_sw in software_using_code:
            out_content += f'''
 * Your job is to replace the instructions in {from_sw} with code blocks in
   {to_sw}, and some explanations about what the code is doing.
'''[1:]
        else:
            out_content += f'''
 * Your job is to replace the instructions that were written for {from_sw}
   with instructions for {to_sw}.
'''[1:]
        out_content += f'''
 * *Try to change as little as possible,* so that the two solutions are
   as similar as they can reasonably be.  This lets readers of the website
   more easily compare the two side-by-side.
 * Use the same example problems whenever possible, and ensure that you get
   the same result in {to_sw} as the original solution shows for {from_sw}.

## When you're ready to submit your work

 1. Delete these instructions, that is, everything up to the horizontal line
    you see below.'''
        if format == 'ipynb':
            out_content += \
                '    That should mean deleting just the first notebook cell.'
        out_content += f'''\n
 2. Save your file with a new name (no longer about {from_sw}, but mentioning
    {to_sw} and optionally any additional packages).
 3. Then the file is ready to submit!  Email it to the site maintainer.

-------------------

{alter_code_blocks(extract_inner_content(sections_dict[rel_sec]),change_software(from_sw,to_sw))}
'''[1:]
        finalize_export( out_file, out_content, format )

#####
#
#  Code supporting the actual commands the user might issue
#
#####

# create.py software - list software supported and default file formats
if sys.argv[1:] == ['software']:
    print( 'Software # Solutions Default format' )
    print( '-------- ----------- --------------' )
    for software in software_df().name:
        num_sols = sum( binary_info[software] )
        format = default_formats[software] \
            if software in default_formats else None
        print( f'{software:8} {num_sols:11} {format:14}' )
    sys.exit()

# create.py formats - list supported file formats
if sys.argv[1:] == ['formats']:
    for key in supported_formats:
        print( f'{key} ({supported_formats[key]})' )
    sys.exit()

# create.py list - summarize opportunities for creating assignments
if sys.argv[1:] == ['list']:
    for (have,need) in software_pairs():
        num_tasks = len( tasks_to_convert( have, need ) )
        if num_tasks > 0:
            print( f'{have:7} -> {need:7}:{num_tasks:3}' )
    sys.exit()

# create.py list verbose - detailed list of opportunities for creating asgts
if sys.argv[1:] == ['list','verbose']:
    for (have,need) in software_pairs():
        task_names = tasks_to_convert( have, need )
        if len( task_names ) > 0:
            print( f'{have:7} -> {need:7}:{len( task_names ):3}' )
            for task_name in task_names:
                print( task_name )
    sys.exit()

# create.py list <X> <Y> - detailed list like previous but just for X -> Y
if len( sys.argv ) == 4 and sys.argv[1] == 'list':
    (have,need) = sys.argv[2:]
    if (have,need) not in software_pairs():
        print( 'Not a valid pair of software packages:', (have,need) )
        sys.exit( 1 )
    for task_name in tasks_to_convert( have, need ):
        print( task_name )
    sys.exit()

# create.py convert <X> <Y> [format] [text] - convert solution(s)
if 4 <= len( sys.argv ) <= 6 and sys.argv[1] == 'convert':
    (have,need) = sys.argv[2:4]
    if (have,need) not in software_pairs():
        print( 'Not a valid pair of software packages:', (have,need) )
        sys.exit( 1 )
    if len( sys.argv ) > 4:
        format = sys.argv[4]
    elif need in default_formats:
        format = default_formats[need]
    else:
        print( 'No default format for this software:', need )
        sys.exit( 1 )
    if format not in supported_formats:
        print( 'Unsupported format:', format )
        sys.exit( 1 )
    search = sys.argv[5] if len( sys.argv ) == 6 else ''
    task_names = [
        task_name for task_name in tasks_to_convert( have, need )
        if search in task_name
    ]
    for task_name in task_names:
        convert( task_name, have, need, format )
    sys.exit()

print_usage_info()
