
#######################
#
#  High-level build tools factored out of build.py to keep that file cleaner.
#  Declarations of constants specific to this project are in build_constants.py. 
#
#######################

import config
import how_to_data
import os
import pandas as pd
import numpy as np
import re
import shutil
import sys
from datetime import datetime
import files
import markdown
import log
import tasks
import topics
import solutions
import software
import static_files
import shell

###
###  TOOLS THAT BUILD PAGES IN THE SITE
###

# Used in the build_solution_page function below
github_url = 'https://github.com/nathancarter/how2data'
new_github_issue_url = f'{github_url}/issues/new/choose'
def edit_on_github_url ( filename ):
    return f'{github_url}/tree/main/{config.relativize_path( filename )}'

# Main function to build a solution page.  1st parameter is any row from solutions.all().
def build_solution_page ( solution_row, force_rerun_solution=False,
                          in_folder=None, out_folder=config.jekyll_input_folder,
                          task_row=None, config_folder=None ):
    out_filename = solution_row['permalink'] + '.md'
    if in_folder is None:
        in_folder = os.path.join( config.tasks_folder, solution_row['task name'] )
    input_file = os.path.join( in_folder, solution_row['solution filename'] )
    output_file = os.path.join( out_folder, out_filename )
    task_file = markdown.get_unique_doc( os.path.join(
        in_folder, 'description' ) )
    if not force_rerun_solution \
    and not files.must_rebuild( input_file, output_file ) \
    and not files.must_rebuild( task_file, output_file ):
        log.not_built( output_file, input_file, task_file )
        files.mark_as_regenerated( out_filename )
        return
    content = markdown.adjust_image_filenames(
        tasks.image_link_adjuster( solution_row['task name'] ),
        tasks.make_links( solution_row['content'] ) )
    content += f'\n\nSee a problem?  [Tell us]({new_github_issue_url}) or ' + \
        f'[edit the source]({edit_on_github_url(input_file)}).'
    if task_row is None:
        task_row = tasks.all()[tasks.all()['task name'] == solution_row['task name']].iloc[0]
    contributors = solution_row["author"]
    if type( contributors ) == str:
        contributors = f'Contributed by {contributors}'
    else:
        try:
            contributors = 'Contributed by:\n\n' + \
                '\n'.join( [ f' * {author}' for author in contributors ] )
        except TypeError:
            contributors = ''
    markdown.write( output_file, static_files.fill_template( 'solution',
        TITLE = solution_row['solution title'],
        PERMALINK = solution_row['permalink'],
        TASK_PAGE_LINK = f'[See all solutions.](../{task_row["permalink"]})',
        DESCRIPTION =
            markdown.adjust_image_filenames(
                tasks.image_link_adjuster( solution_row['task name'] ),
                tasks.make_links( task_row['content'] ) ),
        MARKDOWN_CONTENT = markdown.wrap_in_html_comments( markdown.run(
            content, in_folder, solution_row['software'] ) ),
        CONTRIBUTORS = contributors
    ) )
    log.built( 'solution for', solution_row["task name"],
               Software=solution_row["software"],
               Solution=solution_row["solution name"] )
    files.mark_as_regenerated( out_filename )
    return output_file

# How to fetch a generated solution's body from within the generated markdown
def get_generated_solution_body ( solution_row, folder=config.jekyll_input_folder ):
    title = solution_row['solution title']
    generated_file = config.blogify( title ) + '.md'
    all_content = files.read_text_file( os.path.join( folder, generated_file ) )
    return markdown.unwrap_from_html_comments( all_content )

# How to build a task page; pass any row from tasks.all().
# IMPORTANT NOTE:  This assumes that you've already processed all the solutions files
# using the build_solution_page() function on any files that need their solutions
# rebuilt/updated.  See that function defined above.
def build_task_page ( row, out_folder=config.jekyll_input_folder, solution_rows=None ):
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( out_folder, out_filename )
    all_solutions = ''
    software_for_this_task = solution_rows if solution_rows is not None else \
        solutions.all()[solutions.all()['task name'] == row['task name']]
    for index, solution_row in software_for_this_task.iterrows():
        solution_name = files.without_extension( solution_row['solution name'] )
        solution_name = solution_name[0].upper() + solution_name[1:]
        all_solutions += static_files.fill_template( 'solution-in-software',
            NAME = solution_name,
            SOFTWARE = solution_row['software'],
            PERMALINK = solution_row['permalink'],
            BODY = markdown.unescape_for_jekyll( get_generated_solution_body(
                solution_row, out_folder ) )
        )
    if all_solutions == '':
        all_solutions = '## Solutions\n\nNo solutions exist yet in the database for this task.'
    opportunities = list( software.all()['name'][
        ~software.all()['name'].isin(software_for_this_task['software'])] )
    if len( opportunities ) > 0:
        opportunities = "\n".join( [ f" * {software}" for software in opportunities ] )
        opportunities = static_files.fill_template( 'opportunities',
            OPPORTUNITIES_LIST = opportunities )
    else:
        opportunities = ''
    related_topics = topics.all()[topics.all()['content'].str.contains( row['task name'], regex=False )]
    if len( related_topics ) > 0:
        related_topics = '\n'.join( list( ' * ' + related_topics['markdown link'] ) )
    else:
        related_topics = '*None*'
    markdown.write( output_file, static_files.fill_template( 'task',
        TITLE = row['task name'],
        PERMALINK = row['permalink'],
        DESCRIPTION =
            markdown.adjust_image_filenames(
                tasks.image_link_adjuster( row['task name'] ),
                tasks.make_links( row['content'] ) ),
        SOLUTIONS = all_solutions,
        TOPICS = related_topics,
        OPPORTUNITIES = opportunities
    ) )
    files.mark_as_regenerated( out_filename )
    return output_file

# Generate a page for a given software package,
# from a row in the software.all() DataFrame.
def build_software_page ( row ):
    out_filename = row['permalink'] + '.md'
    output_file = os.path.join( config.jekyll_input_folder, out_filename )
    sol_uses_this_sw = solutions.all()['software'] == row['name']
    def link_to_other_solutions ( task_row ):
        sol_is_for_task = solutions.all()['task name'] == task_row['task name']
        num_not_in_this_sw = sum(sol_is_for_task) - \
            sum(sol_is_for_task & sol_uses_this_sw)
        if num_not_in_this_sw > 0:
            return f'{num_not_in_this_sw} ([view](../{task_row["permalink"]}))'
        else:
            return 'None'
    my_tasks_table = tasks.table()[['Task',f'Solutions in {row["name"]}']].copy()
    my_tasks_table['Solutions in other software packages'] = \
        tasks.all().apply( link_to_other_solutions, axis=1 )
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
    markdown.write( output_file, static_files.fill_template( 'software',
        TITLE = row['title'],
        SOFTWARE_NAME = row['name'],
        PERMALINK = row['permalink'],
        SOFTWARE_ICON = row['large icon markdown'],
        NUMBER_OF_SOLUTIONS = str( row['num solutions'] ),
        SOFTWARE_TASK_TABLE = table1,
        OPPORTUNITIES = table2
    ) )
    files.mark_as_regenerated( out_filename )

# Generate a page for a given topic, from a row in the topics.all() DataFrame.
# The second argument is a folder in which to store temp files during the process.
def build_topic_page ( row, temp_folder ):
    pdf_downloads = ''
    for sindex, srow in software.all().iterrows():
        possible_packages = solutions.all()[solutions.all()['software'] == srow['name']]
        possible_packages = possible_packages['solution name'].unique().tolist()
        for package in possible_packages:
            pdf_filename = build_topic_pdf( row, srow['name'], package, temp_folder )
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
    output_file = os.path.join( config.jekyll_input_folder, out_filename )
    markdown.write( output_file, static_files.fill_template( 'topic',
        TITLE = row['topic name'],
        PERMALINK = row['permalink'],
        CONTENT = tasks.make_links( row['content'] ),
        CONTRIBUTORS =
            f'Contributed by {row["author"]}' if row["author"] != np.nan else '',
        DOWNLOADS = pdf_downloads
    ) )
    files.mark_as_regenerated( out_filename )

# Generate a PDF for a given topic, using a given software package.
# The third argument is the main repo folder, which will get cleaned up later.
def build_topic_pdf (
    topic_row, software_name, main_folder,
    solution_name='solution', min_proportion=0.5
):
    site_url = 'https://how-to-data.org/'
    # make first page with TOC that links to all later pages
    description_and_toc = tasks.make_links( topic_row['content'] )
    tasks_copy = tasks.all()[tasks.all().permalink.apply(
        lambda link: link in description_and_toc )].copy()
    tasks_copy['where appears'] = tasks_copy.permalink.apply(
        lambda link: description_and_toc.index( link ) )
    tasks_copy = tasks_copy.sort_values( by='where appears' )
    # if none of those tasks were edited more recently than the last PDF we generated, stop
    if solution_name == 'solution':
        pair_of_names = f'pure {software_name}'
    else:
        pair_of_names = f'{software_name} {solution_name}'
    title = f'{topic_row["topic name"]} in {pair_of_names}'
    outfile = os.path.join( config.jekyll_input_folder, 'assets', 'downloads', title + '.pdf' )
    must_build = False
    if os.path.exists( outfile ):
        pdf_modified = os.path.getmtime( outfile )
        for index, task_row in tasks_copy.iterrows():
            task_modified = os.path.getmtime(
                os.path.join( main_folder, task_row['task filename'] ) )
            if task_modified > pdf_modified:
                must_build = True
        if not must_build:
            log.not_built( f"PDF for {title}", Reason="Already up to date" )
            return title + '.pdf'
    else:
        must_build = True
    # create the structure of the Markdown input to pandoc
    markdown = static_files.fill_template( 'topic-pdf',
        TITLE = title,
        SITE_URL = site_url,
        DATE = datetime.now().strftime("%d %B %Y"),
        DESCRIPTION = description_and_toc
    )
    # check to see if we have enough solutions to proceed, to save time
    num_solutions = 0
    solutions_in_sw = solutions.all()[(solutions.all()['software'] == software_name) \
                                 & (solutions.all()['solution name'] == solution_name)]
    for index, task_row in tasks_copy.iterrows():
        if sum( solutions_in_sw['task name'] == task_row['task name'] ) > 0:
            num_solutions += 1
    proportion = num_solutions / len( tasks_copy )
    if proportion < min_proportion:
        log.not_built( f"PDF for {title}",
                       Reason=f"only {proportion*100:0.1f}% solved" )
        return None
    # now add all tasks, one at a time
    for index, task_row in tasks_copy.iterrows():
        task_solutions = solutions_in_sw[solutions_in_sw['task name'] == task_row['task name']]
        if len( task_solutions ) > 0:
            solution = markdown.html_sections_to_latex(
                markdown.unescape_for_jekyll(
                    get_generated_solution_body(
                        task_solutions.iloc[0,:] ) ),
                main_folder )
        else:
            solution = 'How to Data does not yet contain a solution for this task in ' \
                     + pair_of_names + '.'
        markdown += static_files.fill_template( 'topic-pdf-solution',
            TASK = task_row['task name'],
            DESCRIPTION = tasks.make_links( task_row['content'] ),
            SOFTWARE = pair_of_names,
            SOLUTION = solution
        )
    # fix all hyperlinks to be either within-the-PDF links or marked as external
    def process_one_link ( match ):
        text = match.group( 1 )
        href = match.group( 2 )
        if href[:3] == '../':
            if href[3:] in tasks_copy.permalink.to_list():
                href = f'#{href[3:]}'
            else:
                href = f'{site_url}{href[3:]}'
                text = f'{text} (on website)'
        elif href[0] == '.':
            log.warning( 'Bad external URL:', f'[{text}]({href})' )
        return f'[{text}]({href})'
    markdown = re.sub( '(?<!\\!)\\[([^]]*)\\]\\(([^)]*)\\)', process_one_link, markdown,
        flags=re.IGNORECASE )
    # write all that markdown to a file, run pandoc on it to create a PDF, then delete the .md
    log.built( f"PDF for {title}" )
    tmp_md_doc = os.path.join( topics_folder, 'pandoc-temp-file.md' )
    markdown.write( tmp_md_doc, markdown, add_escapes=False )
    command_to_run = 'pandoc --from=markdown --to=pdf --pdf-engine=xelatex' \
                + ' -V geometry:margin=1in -V urlcolor:NavyBlue --standalone' \
                + f' --include-in-header="{os.path.join(main_folder,"pandoc-latex-header.tex")}"' \
                + f' --lua-filter="{os.path.join(main_folder,"pandoc-pdf-tweaks.lua")}"' \
                + f' --output="{outfile}" "{tmp_md_doc}"'
    shell.run_or_halt( command_to_run, f'rm "{tmp_md_doc}"' )
    return title + '.pdf'
