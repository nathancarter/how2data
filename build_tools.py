
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
from datetime import datetime

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
# Make a separate copy that unites all solution columns
permalink_for_sw = dict( zip( software_df['name'], software_df['permalink'] ) )
tasks_table_with_links = tasks_table.copy()
tasks_table_with_links['Solutions'] = ''
for index, row in tasks_table_with_links.iterrows():
    to_join = [ ]
    for col in tasks_table.columns:
        if col.startswith( 'Solutions in' ) and row[col] != '':
            to_join.append( f'In {col[13:]}: {row[col]}' )
    row['Solutions'] = '<br>'.join( to_join )
tasks_table_with_links = tasks_table_with_links[['Task','Solutions']]

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

# The contributors list
contributors_list = [ ]
for entry in solutions_df['author']:
    if type(entry) == str:  # maybe it's a single-author solution
        contributors_list.append( entry )
    else:
        try:  # maybe it's a multi-author solution, so add each one
            for author in entry:
                contributors_list.append( author )
        except TypeError:  # probably author was NaN, so do nothing
            pass
contributors_list = pd.Series( contributors_list ).value_counts()
contributors_list_markdown = pd.DataFrame( {
    'Author' : contributors_list.index,
    'Solutions contributed' : contributors_list
} ).to_markdown( index=False )

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
        f'--set-kernel {kernel} --output="{ipynb_out}" "{tmp_md_doc}"',
        f'rm "{tmp_md_doc}"' )
    # convert that to markdown again
    jupyter_config_file = os.path.join( main_folder,
        f'jupyter_nbconvert_config_{software}.py' )
    command_to_run = 'jupyter nbconvert --to=markdown --execute ' + \
        f"--JupyterApp.config_file='{jupyter_config_file}' " + \
        f'--output="{tmp_md_doc}" "{ipynb_out}"'
    ensure_shell_command_succeeds( command_to_run, f'rm "{ipynb_out}"' )
    # read it back into a string
    result = read_text_file( tmp_md_doc )
    ensure_shell_command_succeeds( f'rm "{tmp_md_doc}"' )
    # workaround for buggy way that SVGs get embedded in markdown:
    result = result \
        .replace( '![svg](data:image/svg;base64,<?xml version="1.0" encoding="utf-8"?>', '' ) \
        .replace( ' /></svg>\n)', ' /></svg>\n' )
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
    longer_first = tasks_df.sort_values( 'task name', ascending=False )
    for index, task_row in longer_first.iterrows():
        markdown = re.sub( '(?<!\\[)(' + re.escape( task_row['task name'] ) + ')',
            lambda x: f'[{x.group(0)}](../{task_row["permalink"]})',
            markdown, flags=re.IGNORECASE )
    return markdown

###
###  TOOLS THAT BUILD PAGES IN THE SITE
###

# Main function to build a solution page.  1st parameter is any row from solutions_df.
def build_solution_page ( solution_row, force_rerun_solution=False,
                          in_folder=None, out_folder=jekyll_input_folder,
                          task_row=None ):
    out_filename = solution_row['permalink'] + '.md'
    if in_folder is None:
        in_folder = os.path.join( tasks_folder, solution_row['task name'] )
    input_file = os.path.join( in_folder, solution_row['solution filename'] )
    output_file = os.path.join( out_folder, out_filename )
    task_file = get_unique_markdown_doc( os.path.join(
        in_folder, 'description' ) )
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
    if task_row is None:
        task_row = tasks_df[tasks_df['task name'] == solution_row['task name']].iloc[0]
    contributors = solution_row["author"]
    if type( contributors ) == str:
        contributors = f'Contributed by {contributors}'
    else:
        try:
            contributors = 'Contributed by:\n\n' + \
                '\n'.join( [ f' * {author}' for author in contributors ] )
        except TypeError:
            contributors = ''
    write_markdown( output_file, fill_template( 'solution',
        TITLE = solution_row['solution title'],
        PERMALINK = solution_row['permalink'],
        TASK_PAGE_LINK = f'[See all solutions.](../{task_row["permalink"]})',
        DESCRIPTION =
            adjust_image_filenames( adjust_image_for_task( solution_row['task name'] ),
                make_all_task_names_links( task_row['content'] ) ),
        MARKDOWN_CONTENT = wrap_in_html_comments( run_markdown(
            content, in_folder, solution_row['software'] ) ),
        CONTRIBUTORS = contributors
    ) )
    print( f'Built solution for: {solution_row["task name"]}' )
    print( f'          Software: {solution_row["software"]}' )
    print( f'     Solution name: {solution_row["solution name"]}' )
    print()
    mark_as_regenerated( out_filename )
    return output_file

# How to fetch a generated solution's body from within the generated markdown
def get_generated_solution_body ( solution_row, folder=jekyll_input_folder ):
    title = solution_row['solution title']
    generated_file = blogify( title ) + '.md'
    all_content = read_text_file( os.path.join( folder, generated_file ) )
    return unwrap_from_html_comments( all_content )

# How to build a task page; pass any row from tasks_df.
# IMPORTANT NOTE:  This assumes that you've already processed all the solutions files
# using the build_solution_page() function on any files that need their solutions
# rebuilt/updated.  See that function defined above.
def build_task_page ( row, out_folder=jekyll_input_folder, solution_rows=None ):
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( out_folder, out_filename )
    all_solutions = ''
    software_for_this_task = solution_rows if solution_rows is not None else \
        solutions_df[solutions_df['task name'] == row['task name']]
    for index, solution_row in software_for_this_task.iterrows():
        solution_name = without_extension( solution_row['solution name'] )
        solution_name = solution_name[0].upper() + solution_name[1:]
        all_solutions += fill_template( 'solution-in-software',
            NAME = solution_name,
            SOFTWARE = solution_row['software'],
            PERMALINK = solution_row['permalink'],
            BODY = unescape_for_jekyll( get_generated_solution_body(
                solution_row, out_folder ) )
        )
    if all_solutions == '':
        all_solutions = '## Solutions\n\nNo solutions exist yet in the database for this task.'
    opportunities = list( software_df['name'][
        ~software_df['name'].isin(software_for_this_task['software'])] )
    if len( opportunities ) > 0:
        opportunities = "\n".join( [ f" * {software}" for software in opportunities ] )
        opportunities = fill_template( 'opportunities',
            OPPORTUNITIES_LIST = opportunities )
    else:
        opportunities = ''
    related_topics = topics_df[topics_df['content'].str.contains( row['task name'], regex=False )]
    if len( related_topics ) > 0:
        related_topics = '\n'.join( list( ' * ' + related_topics['markdown link'] ) )
    else:
        related_topics = '*None*'
    write_markdown( output_file, fill_template( 'task',
        TITLE = row['task name'],
        PERMALINK = row['permalink'],
        DESCRIPTION =
            adjust_image_filenames( adjust_image_for_task( row['task name'] ),
                make_all_task_names_links( row['content'] ) ),
        SOLUTIONS = all_solutions,
        TOPICS = related_topics,
        OPPORTUNITIES = opportunities
    ) )
    mark_as_regenerated( out_filename )
    return output_file

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
    write_markdown( output_file, fill_template( 'software',
        TITLE = row['title'],
        SOFTWARE_NAME = row['name'],
        PERMALINK = row['permalink'],
        SOFTWARE_ICON = row['large icon markdown'],
        NUMBER_OF_SOLUTIONS = str( row['num solutions'] ),
        SOFTWARE_TASK_TABLE = table1,
        OPPORTUNITIES = table2
    ) )
    mark_as_regenerated( out_filename )

# Generate a page for a given topic, from a row in the topics_df DataFrame.
def build_topic_page ( row ):
    pdf_downloads = ''
    for sindex, srow in software_df.iterrows():
        possible_packages = solutions_df[solutions_df['software'] == srow['name']]
        possible_packages = possible_packages['solution name'].unique().tolist()
        for package in possible_packages:
            pdf_filename = build_topic_pdf( row, srow['name'], package )
            if pdf_filename is not None:
                pdf_filename = '../assets/downloads/' + pdf_filename
                if package == 'solution':
                    pdf_downloads += \
                        f' * [Solutions in pure {srow["name"]} (download PDF)]({pdf_filename})\n'
                else:
                    pdf_downloads += \
                        f' * [Solutions in {srow["name"]} {package} (download PDF)]({pdf_filename})\n'
    if pdf_downloads == '':
        pdf_downloads = 'No PDF downloads available for this topic yet.'
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( jekyll_input_folder, out_filename )
    write_markdown( output_file, fill_template( 'topic',
        TITLE = row['topic name'],
        PERMALINK = row['permalink'],
        CONTENT = make_all_task_names_links( row['content'] ),
        CONTRIBUTORS =
            f'Contributed by {row["author"]}' if row["author"] != np.nan else '',
        DOWNLOADS = pdf_downloads
    ) )
    mark_as_regenerated( out_filename )

# Convert all HTML-style tables/etc. within markdown text to LaTeX instead
def html_sections_to_latex ( markdown, folder=main_folder ):
    # are there any sectionsn to process?  if not, just return the input
    section = re.search( '\n<div(?:.|\n)*?<\\/div.*\n', markdown )
    if section is None:
        return markdown
    # there is a section to process; use pandoc on a temporary HTML file
    tmp_html_file = os.path.join( folder, 'tmp.html' )
    tmp_tex_file = os.path.join( folder, 'tmp.tex' )
    write_text_file( tmp_html_file, section.group(0) )
    ensure_shell_command_succeeds(
        f'pandoc --from=html --to=latex --output="{tmp_tex_file}" "{tmp_html_file}"',
        f'rm "{tmp_html_file}"' )
    section_as_tex = read_text_file( tmp_tex_file )
    ensure_shell_command_succeeds( f'rm "{tmp_tex_file}"' )
    # replace the section with its TeX-ified version
    markdown = markdown[:section.start()] + section_as_tex + markdown[section.end():]
    # recur on the new markdown, with one less section to process
    return html_sections_to_latex( markdown )

# Generate a PDF for a given topic, using a given software package.
def build_topic_pdf ( topic_row, software_name, solution_name='solution', min_proportion=0.5 ):
    site_url = 'https://how-to-data.org/'
    # make first page with TOC that links to all later pages
    description_and_toc = make_all_task_names_links( topic_row['content'] )
    tasks = tasks_df[tasks_df.permalink.apply(
        lambda link: link in description_and_toc )].copy()
    tasks['where appears'] = tasks.permalink.apply(
        lambda link: description_and_toc.index( link ) )
    tasks = tasks.sort_values( by='where appears' )
    # if none of those tasks were edited more recently than the last PDF we generated, stop
    if solution_name == 'solution':
        pair_of_names = f'pure {software_name}'
    else:
        pair_of_names = f'{software_name} {solution_name}'
    title = f'{topic_row["topic name"]} in {pair_of_names}'
    outfile = os.path.join( jekyll_input_folder, 'assets', 'downloads', title + '.pdf' )
    must_build = False
    if os.path.exists( outfile ):
        pdf_modified = os.path.getmtime( outfile )
        for index, task_row in tasks.iterrows():
            task_modified = os.path.getmtime(
                os.path.join( main_folder, task_row['task filename'] ) )
            if task_modified > pdf_modified:
                must_build = True
        if not must_build:
            print( f'PDF already up-to-date for: {title}' )
            return title + '.pdf'
    else:
        must_build = True
    # create the structure of the Markdown input to pandoc
    markdown = fill_template( 'topic-pdf',
        TITLE = title,
        SITE_URL = site_url,
        DATE = datetime.now().strftime("%d %B %Y"),
        DESCRIPTION = description_and_toc
    )
    # check to see if we have enough solutions to proceed, to save time
    num_solutions = 0
    solutions_in_sw = solutions_df[(solutions_df['software'] == software_name) \
                                 & (solutions_df['solution name'] == solution_name)]
    for index, task_row in tasks.iterrows():
        if sum( solutions_in_sw['task name'] == task_row['task name'] ) > 0:
            num_solutions += 1
    proportion = num_solutions / len( tasks )
    if proportion < min_proportion:
        print( f'    Not generating PDF for: {title}   (only {proportion*100:0.1f}% solved)' )
        return None
    # now add all tasks, one at a time
    for index, task_row in tasks.iterrows():
        task_solutions = solutions_in_sw[solutions_in_sw['task name'] == task_row['task name']]
        if len( task_solutions ) > 0:
            solution = html_sections_to_latex(
                unescape_for_jekyll(
                    get_generated_solution_body(
                        task_solutions.iloc[0,:] ) ) )
        else:
            solution = 'How to Data does not yet contain a solution for this task in ' \
                     + pair_of_names + '.'
        markdown += fill_template( 'topic-pdf-solution',
            TASK = task_row['task name'],
            DESCRIPTION = make_all_task_names_links( task_row['content'] ),
            SOFTWARE = pair_of_names,
            SOLUTION = solution
        )
    # fix all hyperlinks to be either within-the-PDF links or marked as external
    def process_one_link ( match ):
        text = match.group( 1 )
        href = match.group( 2 )
        if href[:3] == '../':
            if href[3:] in tasks.permalink.to_list():
                href = f'#{href[3:]}'
            else:
                href = f'{site_url}{href[3:]}'
                text = f'{text} (on website)'
        elif href[0] == '.':
            print( '\tWarning: Bad external URL:', f'[{text}]({href})' )
        return f'[{text}]({href})'
    markdown = re.sub( '(?<!\\!)\\[([^]]*)\\]\\(([^)]*)\\)', process_one_link, markdown,
        flags=re.IGNORECASE )
    # write all that markdown to a file, run pandoc on it to create a PDF, then delete the .md
    print( f'        Generating PDF for: {title}' )
    tmp_md_doc = os.path.join( topics_folder, 'pandoc-temp-file.md' )
    write_markdown( tmp_md_doc, markdown, add_escapes=False )
    command_to_run = 'pandoc --from=markdown --to=pdf --pdf-engine=xelatex' \
                + ' -V geometry:margin=1in -V urlcolor:NavyBlue --standalone' \
                + f' --include-in-header="{os.path.join(main_folder,"pandoc-latex-header.tex")}"' \
                + f' --lua-filter="{os.path.join(main_folder,"pandoc-pdf-tweaks.lua")}"' \
                + f' --output="{outfile}" "{tmp_md_doc}"'
    ensure_shell_command_succeeds( command_to_run, f'rm "{tmp_md_doc}"' )
    return title + '.pdf'
