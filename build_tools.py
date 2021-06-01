
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
###  GENERATING TABLES
###

# The software table to be inserted on the software packages page
software_table = software_df[[
    'name as link', 'icon markdown', 'num solutions', 'website markdown']]
software_table.columns = [
    'Software Package', 'Icon', 'Number of solutions', 'Website']

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
# Make a separate copy in which the column headers are markdown links
tasks_table_with_links = tasks_table.copy()
new_column_names = list( tasks_table_with_links.columns )
permalink_for_sw = dict( zip( software_df['name'], software_df['permalink'] ) )
for index, col in enumerate( new_column_names ):
    if col.startswith( 'Solutions in ' ):
        software_name = col[13:]
        new_column_names[index] = \
            f'[Solutions in {col[13:]}](../{permalink_for_sw[col[13:]]})'
tasks_table_with_links.columns = new_column_names

# The summary stats table to be inserted on the main page
stats_table = pd.DataFrame( {
    'Content' : [
        '[Topics](topics)',
        '[Tasks](tasks)',
        '[Solutions](tasks)',
        '[Software packages](software)'
    ],
    'Quantity' : [
        len( topics_df ),
        len( tasks_df ),
        len( solutions_df ),
        len( software_df )
    ]
} )

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
            ensure_shell_command_succeeds(
                f'rm {os.path.join( jekyll_input_folder, file )}' )

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

# Function for copying a task file from a task folder to the Jekyll
# input folder.
def copy_task_image_file ( full_path, filename ):
    source = full_path
    dest = os.path.join( jekyll_imgs_folder, filename )
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
# More useful special case of previous function
def adjust_image_filenames ( func, markdown ):
    return map_over_images(
        lambda code, alt_text, filename: ( alt_text, func( filename ) ),
        markdown
    )

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
    ensure_shell_command_succeeds( 'jupytext --to ipynb ' + \
        f'--set-kernel {kernel} --output="{ipynb_out}" "{tmp_md_doc}"' )
    ensure_shell_command_succeeds( f'rm "{tmp_md_doc}"' )
    # convert that to markdown again
    jupyter_config_file = os.path.join( main_folder, 'jupyter_nbconvert_config.py' )
    command_to_run = 'jupyter nbconvert --to=markdown --execute ' + \
        f"--JupyterApp.config_file='{jupyter_config_file}' " + \
        f'--output="{tmp_md_doc}" "{ipynb_out}"'
    ensure_shell_command_succeeds( command_to_run )
    ensure_shell_command_succeeds( f'rm "{ipynb_out}"' )
    # read it back into a string
    result = read_text_file( tmp_md_doc )
    ensure_shell_command_succeeds( f'rm "{tmp_md_doc}"' )
    return result

###
###  BUILD TOOLS USED BELOW
###

def adjust_image_for_task ( task ):
    def result ( filename ):
        return os.path.join( '..', 'assets', 'dynamic-images', f'{task}-{filename}' )
github_url = 'https://github.com/nathancarter/how2data'
new_github_issue_url = f'{github_url}/issues/new/choose'
def edit_on_github_url ( filename ):
    return f'{github_url}/tree/main/{path_in_project( filename )}'
def make_all_task_names_links ( markdown ):
    for index, task_row in tasks_df.iterrows():
        markdown = markdown.replace( task_row['task name'],
            f'[{task_row["task name"]}](../{task_row["permalink"]})' )
    return markdown

###
###  TOOLS THAT BUILD PAGES IN THE SITE
###

# Main function to build a solution page.  1st parameter is any row from solutions_df.
def build_solution_page ( solution_row, force_rerun_solution=False ):
    out_filename = solution_row['permalink'] + '.md'
    input_file = os.path.join( tasks_folder, solution_row['task name'],
        solution_row['solution filename'] )
    output_file = os.path.join( jekyll_input_folder, out_filename )
    task_file = get_unique_markdown_doc( os.path.join(
        tasks_folder, solution_row['task name'], 'description' ) )
    if not force_rerun_solution \
    and not must_rebuild_file( input_file, output_file ) \
    and not must_rebuild_file( task_file, output_file ):
        print( f'Not rebuilding this: {output_file}' )
        print( f'   It is newer than: {input_file}' )
        print( f'     and newer than: {task_file}' )
        mark_as_regenerated( out_filename )
        return
    content = adjust_image_filenames(
        adjust_image_for_task( solution_row['task name'] ),
        make_all_task_names_links( solution_row['content'] ) )
    content += f'\n\nSee a problem?  [Tell us]({new_github_issue_url}) or ' + \
        f'[edit the source]({edit_on_github_url(input_file)}).'
    task_row = tasks_df[tasks_df['task name'] == solution_row['task name']].iloc[0]
    write_text_file( output_file,
        files_df[files_df['filename'] == 'solution-template.md']['raw content'].iloc[0]
        .replace( 'TITLE', solution_row['solution title'] )
        .replace( 'PERMALINK', solution_row['permalink'] )
        .replace( 'TASK_PAGE_LINK', f'[See all solutions.](../{task_row["permalink"]})' )
        .replace( 'DESCRIPTION',
            adjust_image_filenames( adjust_image_for_task( solution_row['task name'] ),
                make_all_task_names_links( task_row['content'] ) ) )
        .replace( 'MARKDOWN_CONTENT', wrap_in_html_comments( run_markdown(
            content,
            os.path.join( tasks_folder, solution_row['task name'] ),
            solution_row['software'] ) ) )
        .replace( 'CONTRIBUTORS',
            f'Contributed by {solution_row["author"]}' if solution_row["author"] != np.nan else '' )
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
    all_solutions = ''
    software_for_this_task = \
        solutions_df[solutions_df['task name'] == row['task name']]
    for index, solution_row in software_for_this_task.iterrows():
        solution_name = without_extension( solution_row['solution name'] )
        solution_name = solution_name[0].upper() + solution_name[1:]
        all_solutions += f'''

## {solution_name}, in {solution_row["software"]}

[View this solution alone.](../{solution_row["permalink"]})

{get_generated_solution_body( solution_row )}

'''
    if all_solutions == '':
        all_solutions = '## Solutions\n\nNo solutions exist yet in the database for this task.'
    opportunities = list( software_df['name'][
        ~software_df['name'].isin(software_for_this_task['software'])] )
    if len( opportunities ) > 0:
        opportunities = "\n".join( [ f" * {software}" for software in opportunities ] )
        opportunities = f'''
## Opportunities

This website does not yet contain a solution for this task in any of the following
software packages.

{opportunities}

If you can contribute a solution using any of these pieces of software,
see [our Contributing page](contributing) for how to help extend this website.
'''
    else:
        opportunities = ''
    related_topics = topics_df[topics_df['content'].str.contains( row['task name'] )]
    if len( related_topics ) > 0:
        related_topics = '\n'.join( list( ' * ' + related_topics['markdown link'] ) )
    else:
        related_topics = '*None*'
    write_text_file( output_file,
        files_df[files_df['filename'] == 'task-template.md']['raw content'].iloc[0]
        .replace( 'TITLE', row['task name'] )
        .replace( 'PERMALINK', row['permalink'] )
        .replace( 'DESCRIPTION',
            adjust_image_filenames( adjust_image_for_task( row['task name'] ),
                make_all_task_names_links( row['content'] ) ) )
        .replace( 'SOLUTIONS', all_solutions )
        .replace( 'TOPICS', related_topics )
        .replace( 'OPPORTUNITIES', opportunities )
    )
    mark_as_regenerated( out_filename )

# Generate a page for a given software package,
# from a row in the software_df DataFrame.
def build_software_page ( row ):
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( jekyll_input_folder, out_filename )
    sol_uses_this_sw = solutions_df['software'] == row['name']
    def link_to_other_solutions ( task_row ):
        sol_is_for_task = solutions_df['task name'] == task_row['task name']
        num_not_in_this_sw = sum(sol_is_for_task) - \
            sum(sol_is_for_task & sol_uses_this_sw)
        if num_not_in_this_sw > 0:
            return f'{num_not_in_this_sw} ([view](../{task_row["permalink"]}))'
        else:
            return 'None'
    my_tasks_table = tasks_table[['Task',f'Solutions in {row["name"]}']].copy()
    my_tasks_table['Solutions in other software packages'] = \
        tasks_df.apply( link_to_other_solutions, axis=1 )
    solution_needed = my_tasks_table.iloc[:,1].isin([''])
    table1 = my_tasks_table[~solution_needed]
    if len( table1 ) > 0:
        table1 = table1.to_markdown( index=False )
    else:
        table1 = f'*No tasks have solutions in {row["name"]} yet.*  ' + \
            'Consider [submitting one!](../contributing)'
    table2 = my_tasks_table[solution_needed].copy()
    table2[f'Solutions in {row["name"]}'] = \
        f'none yet<br/>(Want to [submit one](../contributing)?)'
    if len( table2 ) > 0:
        table2 = table2.to_markdown( index=False )
    else:
        table2 = f'*None---all tasks have solutions in {row["name"]}!*'
    write_text_file( output_file,
        files_df[files_df['filename'] == 'software-template.md']['raw content'].iloc[0]
        .replace( 'TITLE', row['title'] )
        .replace( 'SOFTWARE_NAME', row['name'] )
        .replace( 'PERMALINK', row['permalink'] )
        .replace( 'SOFTWARE_ICON', row['large icon markdown'] )
        .replace( 'NUMBER_OF_SOLUTIONS', str( row['num solutions'] ) )
        .replace( 'SOFTWARE_TASK_TABLE', table1 )
        .replace( 'OPPORTUNITIES', table2 )
    )
    mark_as_regenerated( out_filename )

# Generate a page for a given topic, from a row in the topics_df DataFrame.
def build_topic_page ( row ):
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( jekyll_input_folder, out_filename )
    write_text_file( output_file,
        files_df[files_df['filename'] == 'topic-template.md']['raw content'].iloc[0]
        .replace( 'TITLE', row['topic name'] )
        .replace( 'PERMALINK', row['permalink'] )
        .replace( 'CONTENT', make_all_task_names_links( row['content'] ) )
        .replace( 'CONTRIBUTORS',
            f'Contributed by {row["author"]}' if row["author"] != np.nan else '' )
    )
    mark_as_regenerated( out_filename )
