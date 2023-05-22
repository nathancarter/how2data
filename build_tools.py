
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
                    solutions.Solution( task_solutions.iloc[0,:] ).generated_body() ),
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
