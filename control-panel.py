
##
##  This script has many imports because it interfaces with all of this project's modules
##

import streamlit as st
import pandas as pd
import numpy as np
import requests
import how_to_data
import software
import solutions
import topics
import tasks
import config
import files
import yaml
import markdown
import os
import re


##
##  Define a few constants, simple relationships not stored elsewhere
##  (Consider later moving these to the config module?)
##

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


##
##  Define many small utility functions used in the main code, further below.
##  Each such function is documented individually in this section.
##

# Display a dataframe to streamlit.
# The number of rows is printed first, so users know to scroll if it is large.
# Optionally a list of column names to omit can be provided, and they will be
# left out of the display, and a message printed that the reason is because they
# had large text content that doesn't belong in a table.
def show_df ( df, cols_to_omit=None ):
    if cols_to_omit is not None:
        df = df.drop( cols_to_omit, axis=1 )
    st.write( f'Showing {len(df)} rows:' )
    st.dataframe( df )
    if cols_to_omit is not None:
        col_name_list = ", ".join( [ f'"{col}"' for col in cols_to_omit ] )
        st.write( f'''
            The following column(s) were omitted from this table,
            because each entry would be a large quantity of text,
            which cannot be browsed inside a table cell: {col_name_list}
        ''' )

# Compute and return a dataframe of summary statistics for the whole website.
# Show a Streamlit spinner while the computation occurs.
def get_site_stats ():
    with st.spinner( 'Loading site statistics...' ):
        df = how_to_data.stats()
        df['Content'] = df['Content'].str.split( ']', expand=True ).iloc[:,0].str[1:]
        return df

# Compute and return a dataframe of supported file formats.
# Show a Streamlit spinner while the computation occurs.
def get_file_formats ():
    df = pd.DataFrame( { 'Extension' : supported_formats.keys() } )
    df['Format name'] = df['Extension'].map( supported_formats )
    return df

# Compute and return a dataframe of all solutions in the database on disk.
# Show a Streamlit spinner while the computation occurs.
def get_solutions ():
    with st.spinner( 'Loading all solutions...' ):
        return solutions.all()

# Compute and return a list of software-library combinations used anywhere in the
# site, together with the number of solutions in each such combination.
# Show a Streamlit spinner while the computation occurs.
def get_libraries ():
    df = get_solutions()
    libraries = df['solution filename'].str.split( '.', expand=True ).iloc[:,0]
    libraries = libraries.apply( lambda name: \
        name if ',' in name else f'Pure {name} (no extra libraries)' )
    libraries = libraries.value_counts()
    return pd.DataFrame( {
        'Software package and libraries' : libraries.index,
        'Number of solutions' : libraries.values
    } ).sort_values( by='Software package and libraries' ).reset_index( drop=True )

# Compute and return a dataframe of all software packages supported by the site.
# Show a Streamlit spinner while the computation occurs.
def get_software ():
    with st.spinner( 'Loading software package list...' ):
        return software.all()

# Compute and return a dataframe of all topics stored in the database.
# Show a Streamlit spinner while the computation occurs.
def get_topics ():
    with st.spinner( 'Loading all topics...' ):
        return topics.all()

# Compute and return a dataframe of all tasks in the database.
# Show a Streamlit spinner while the computation occurs.
def get_tasks ():
    with st.spinner( 'Loading all tasks...' ):
        return tasks.all()

# Compute and return a dataframe of all authors mentioned for any solution in the
# database, and the number of solutions credited to each author.
# Show a Streamlit spinner while the computation occurs.
def get_author_stats ():
    authors = [ ]
    for author in get_solutions()['author']:
        if type( author ) == str or author is np.nan:
            authors.append( author )
        else:
            authors += author
    authors = pd.Series( authors ).value_counts()
    df = pd.DataFrame( {
        'Author name and email' : authors.index,
        'Solutions contributed' : authors.values
    } )
    df['Author name and email'][df['Author name and email'].isna()] = 'Uncredited'
    return df.sort_values( by='Author name and email' ).reset_index( drop=True )

# Compute and return a dataframe of all tasks in the database, together with the list
# of topics that each task is mentioned in, if any.  The table is sorted in decreasing
# order of the number of topics the task appears in, so that tasks that are not
# associated with a topic will appear on the bottom and can be detected that way.
# Show a Streamlit spinner while the computation occurs.
def get_task_topic_relationships ():
    df = pd.DataFrame( { 'Task name' : get_tasks()['task name'] } )
    top_df = get_topics()
    df['Topic names'] = df['Task name'].apply( lambda name: \
        list( top_df[top_df['content'].str.contains( name, regex=False )]['topic name'] ) )
    df['Number of topics that include the task'] = df['Topic names'].apply( len )
    df = df[['Task name','Number of topics that include the task','Topic names']]
    return df.sort_values( by='Number of topics that include the task', ascending=False )

# Compute and return a dataframe of all tasks and the software packages in which they
# have solutions, plus the list of software packages in which they do not have solutions,
# so that a developer can see what opportunities there are to convert existing solutions
# into new languages or packages, to increase the coverage of the database.
# Show a Streamlit spinner while the computation occurs.
def get_task_software_table ():
    software_names = get_software().name
    matrix = get_solutions()[['task name','software']].copy().drop_duplicates()
    with st.spinner( 'Computing task-software table...' ):
        matrix['marker'] = 1
        matrix = matrix.pivot( index=['task name'], columns='software', values='marker' )
        matrix = matrix.fillna( 0 )
        for sw in software_names:
            matrix[sw] = matrix[sw].astype( bool )
        froms = [ ]
        tos = [ ]
        tasks = [ ]
        for have_sol_in in software_names:
            for need_sol_in in software_names:
                if have_sol_in != need_sol_in:
                    selection = matrix[have_sol_in] & ~matrix[need_sol_in]
                    for task_name in matrix[selection].index:
                        froms.append( have_sol_in )
                        tos.append( need_sol_in )
                        tasks.append( task_name )
        return pd.DataFrame( {
            'Task name' : tasks,
            'Could convert existing solution from' : froms,
            'To a new solution in' : tos
        } )

# Create on disk a new task with the given name and fill its folder with a placeholder
# description file.  Throw an error if the task name is invalid (must start with "How to ")
# or if the folder already exists.  Otherwise, clear the tasks cache so that the next
# time anyone computes the list of tasks, it will be reloaded from disk and this newest
# task detected.
def create_task ( new_task_name ):
    new_folder = os.path.join( config.tasks_folder, new_task_name )
    desc_file = os.path.join( new_folder, 'description.md' )
    if new_task_name[:7] != 'How to ':
        raise ValueError( 'Task names must begin with "How to ".' )
    elif os.path.isdir( new_folder ):
        raise ValueError( 'A task with that name already exists.' )
    else:
        os.mkdir( new_folder )
        files.write_text_file( desc_file,
            'Replace this text with a description of the task.' )
        tasks.clear_cache()

# Utility function for making a two-column output table in a streamlit page.
def show_row ( label ):
    col1, col2 = st.columns( [ 1, 4 ] )
    col1.write( label )
    return col2
    # Example usage: show_row( 'Name:' ).write( 'Jim!' )

# Use streamlit to print to the page a given solution (for a given task).
# The parameter must be a Solution instance (as defined in solutions.py).
# It will be shown in an expandable section of the page, with a warning at the top
# indicating that it won't be formatted exactly like it would on the website.
def show_solution_preview ( solution ):
    file = solution.output_file()
    if not os.path.isfile( file ):
        show_row( 'Preview' ).warning( '''
            This solution is new and has not yet been compiled,
            therefore no preview is available.

            Visit the "Build the site" tab at the top of this control panel
            and run Step 1, then return here to see a preview of this solution.
        ''' )
        return
    show_row( f'Generated markdown' ) \
        .write( f'`{config.relativize_path(solution.output_file())}`' )
    with show_row( 'Preview' ):
        with st.expander( 'Click to expand/collapse' ):
            if requests.get( solution.url ).status_code == 404:
                st.warning( f'''
                    The preview below is not formatted exactly like the online version
                    will be; some links may be broken.  Later if you publish this
                    solution, it will be visible at `{solution.url}`.
                ''' )
            else:
                st.warning( f'''
                    The preview below is not formatted exactly like the online version;
                    some links may be broken.
                    [The published version is here.]({solution.url})
                ''' )
            if solution.must_build():
                st.error( '''
                    **The preview below is out of date.**

                    The source file has been edited, but the page has not yet been
                    rebuilt from that source file.

                    To solve this, visit the "Build the site" tab of this control panel app,
                    and run Step 1.  Then return here to see an updated preview.
                ''' )
            header, content = yaml.split_file( file )
            split_header = '\n## Solution'
            split_point = content.index( split_header )
            content = content[split_point + len(split_header) + 1:]
            content = re.sub( '\n#', '\n##', content )
            st.markdown( content, unsafe_allow_html=True )

# Use streamlit to print to the page all solutions for a given task.
# This function just calls show_solution_preview() in a loop for all solutions of the task.
def show_solution_previews ( task ):
    with st.spinner( 'Loading task solutions...' ):
        sols = task.solutions()
    if len( sols ) == 0:
        show_row( '' ).write( '(no solutions yet for this task)' )
    else:
        for index, solution in enumerate( sols ):
            st.divider()
            show_row( f'### Solution {index+1}' ) \
                .write( f'### In {solution.solution_filename.split( "." )[0]}' )
            show_row( f'Source file' ) \
                .write( f'`{solution.solution_path}` (To edit this solution, edit this file.)' )
            show_solution_preview( solution )

# First, add streamlit header to show what task we're about to display.
# Second, show some filename info and the task's description, which is edtiable.
# Third, show all solutions, using the show_solution_previews() function.
def show_task_preview ( task ):
    show_row( '### Task name' ).write( f'### {task.task_name}' )
    show_row( 'Folder' ).write( f'`{config.relativize_path(task.folder)}`' )
    show_row( 'Description' ).info( task.description() )
    show_row( 'Description source file' ).write(
        f'`{task.task_filename}` (To edit the description, edit this file.)' )
    show_solution_previews( task )

# Try to create a new solution for the given task, with the given filename,
# and based on an existing solution with the given filename (or None to start from scratch).
# Throw an error if any part of the process fails (e.g., file already exists).
def create_solution ( task, filename, based_on=None ):
    file_to_create = os.path.join( task.folder, filename )
    software, file_type = filename.split( '.' )
    if based_on is not None:
        based_on = solutions.Solution( f'{task.task_name} (in {based_on})' )
        return based_on.make_assignment( software, file_type )
    else:
        abs_filename = os.path.join( task.folder, software )
        content = f'''
# Fill this file with a solution to the task {task.task_name} in {software}

(Replace these instructions with your new solution to the task.)

## What should your solution contain?

Solve the problem in the task description as briefly and clearly as possible.
(If the task description has already been published to the site, you can find it
[at this URL]({task.url}).)

If there are already other solutions for the task "{task.task_name},"
try to imitate their structure and content as much as possible, so that this solution
is as similar as it can reasonably be to the others.  This lets readers of the website
more easily compare solutions side-by-side.  Use the same example problems whenever
possible, and ensure that you get the same results as in the other solutions.

If there aren't any, you should create a simple example problem, perhaps by typing
in a small dataset (e.g., 10 numbers) or by loading a free sample dataset
(as documented [here](https://how-to-data.org/how-to-quickly-load-some-sample-data/)).

## What style should you use?

 * Imitate the style of other solutions on the website.
 * Keep your solution as short as possible.
 * Provide code that is easy to copy and re-use.
 * Explain all code as briefly and clearly as possible.

## What can you assume the reader knows?

The reader will already have read the task description and you can assume that they
understood it.  Assume they understand the theory related to the task and your solution,
and all you have to provide is the relevant code or software instructions, and how to
interpret any output the software gives.

## When you're done

You have two choices; pick one:

 * Email this solution file to the site maintainer.
 * Commit this file to git and then create a pull request on GitHub.
        '''
        markdown.export( content, abs_filename, file_type )
    solutions.clear_cache()


##
##  Configure streamlit, print main header, and create 3-tab app layout
##

st.set_page_config(
    page_title='How-to-Data Developer Control Panel',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

'# How-to-Data Developer Control Panel'

report_tab, content_tab, build_tab = st.tabs( [
    'Browse reports',
    'View/edit tasks and solutions',
    'Build the site'
] )


##
##  Create report tab
##  (This just shows a drop-down list of reports, and choosing any one displays it.)
##

with report_tab:
    col1, col2 = st.columns( [ 1, 3 ] )
    selection = col1.selectbox(
        label='Choose a report to view:',
        options=[
            'Supported software packages',
            'Supported file formats',
            'Packages and libraries used',
            'Topics',
            'Tasks',
            'Solutions',
            'Author stats',
            'Opportunities to add content',
            'Site summary statistics',
            'Task-topic relationships'
        ]
    )
    with col2:
        match selection:
            case 'Site summary statistics':
                show_df( get_site_stats() )
            case 'Supported file formats':
                show_df( get_file_formats() )
            case 'Supported software packages':
                show_df( get_software() )
            case 'Packages and libraries used':
                show_df( get_libraries() )
            case 'Topics':
                show_df( get_topics(), [ 'content', 'raw content' ] )
            case 'Tasks':
                show_df( get_tasks(), [ 'content' ] )
            case 'Solutions':
                show_df( get_solutions(), [ 'content', 'raw content' ] )
            case 'Author stats':
                show_df( get_author_stats() )
            case 'Task-topic relationships':
                df = get_task_topic_relationships()
                show_df( df )
                num_orphans = ( df['Number of topics that include the task'] == 0 ).sum()
                st.write( f'Number of tasks not associated with any topic: {num_orphans}' )
            case 'Opportunities to add content':
                df = get_task_software_table()
                col1, col2 = st.columns( 2 )
                from_filter = col1.selectbox(
                    label='Show only existing solutions in this software:',
                    options=[ 'all', *df['Could convert existing solution from'].unique() ] )
                to_filter = col2.selectbox(
                    label='Show only solutions needed in this software:',
                    options=[ 'all', *df['To a new solution in'].unique() ] )
                if from_filter != 'all':
                    df = df[df['Could convert existing solution from'].isin( [ from_filter ] )]
                if to_filter != 'all':
                    df = df[df['To a new solution in'].isin( [ to_filter ] )]
                show_df( df )
    st.divider()
    col1, col2 = st.columns( [ 1, 3 ] )
    col1.write( '''
        Content not up-to-date?
    ''' )
    if col2.button( 'Reload database', key='reload1' ):
        how_to_data.clear_caches()
        st.experimental_rerun()


##
##  Create content tab
##  On the left, the user can choose any existing task from a drop-down menu.
##  On the right, the user can enter a name and press enter to create a new task.
##  In either case, the selected/created task is shown below, using the
##  show_task_preview() function defined in the utilities section, above.
##  Then controls are shown at the bottom for adding new solutions.
##

with content_tab:
    col1, col2 = st.columns( 2 )
    def handle_new_task_creation ():
        new_task_name = st.session_state.new_task_name
        try:
            create_task( new_task_name )
            col2.success( f'New task folder created: {new_task_name}' )
            st.session_state.select_task = new_task_name
        except ValueError as e:
            col2.error( str( e ) )
    col2.text_input( 'Or add a new task to the database:',
        placeholder='How to dance well (click to edit)',
        key='new_task_name', on_change=handle_new_task_creation )
    with col1:
        df = get_tasks()
    un_chosen_text = '(click to choose one)'
    current_task = col1.selectbox(
        label='Choose an existing task to view:',
        options=[ un_chosen_text, *df['task name'] ],
        key='select_task' )
    st.divider()
    if current_task == un_chosen_text:
        st.write( '(Task information will be shown here after you select a task above.)')
    else:
        task = tasks.Task( current_task )
        show_task_preview( task )
        st.divider()
        with show_row( '### To add a solution' ):
            software_name = st.selectbox(
                'In which software will your solution be implemented?',
                software.all()['name'].sort_values() )
            libraries = st.text_input(
                'Does it use any extra libraries (e.g., "ggplot" or "NumPy and Matplotlib")?',
                placeholder='(optional)' )
            file_types = [
                f'{format} (.{extension})'.replace( 's (.', ' (.' )
                for extension, format in supported_formats.items()
            ]
            file_types.sort()
            file_type = st.selectbox( 'What type of file will your solution be stored in?', file_types )
            prefix = 'Yes, start with a copy of the existing solution in '
            solution_names = [
                prefix + solution.solution_filename.split( "." )[0]
                for solution in task.solutions()
            ]
            solution_names.insert( 0, 'No, start from an empty document' )
            existing = st.selectbox(
                'Do you want any initial content in that file to help you get started writing?',
                solution_names )
            if st.button( 'Create new solution' ):
                try:
                    filename = software_name
                    if libraries != '':
                        filename += ', using ' + libraries
                    filename += file_type.split( '(' )[1][:-1]
                    if existing == solution_names[0]:
                        existing = None
                    else:
                        existing = existing[len(prefix):]
                    new_file = create_solution( task, filename, existing )
                    solutions.clear_cache()
                    st.experimental_rerun()
                except NotImplementedError as e:
                    st.error( str( e ) )
        st.divider()
        with show_row( 'Content not up-to-date?' ):
            if st.button( 'Reload database', key='reload2' ):
                how_to_data.clear_caches()
                st.experimental_rerun()

##
##  Create build tab
##  This tab describes the two steps of the build process and how and when to use each.
##  It provides buttons for running each of the two steps of the build process.
##

with build_tab:
    col1, col2 = st.columns( 2 )
    col1.write( '## Step 1. Re-run database' )
    col1.markdown( '''
        The database of tasks and solutions is stored in the `database`
        folder of the repository.  This command finds any portion of that
        database that has changed since it was last run, executes its code,
        and stores the output in the `jekyll-input` folder.
    ''' )
    col1.info( '''
        **You want to run this task if you made changes to a task description
        or a solution source file.**
    ''' )
    col1.warning( '''
        After you run it, you should return to the "View/edit tasks and solutions" tab
        to verify that your changes look the way you expect.  **You may repeat Step 1
        as many times as needed to get your work looking correct before you proceed
        to Step 2.**
    ''' )
    if col1.button( '🏃‍♂️ Run solution code' ):
        pbar = col1.progress( 0, 'Running solution code...' )
        warning = col1.warning( '''
            This will take a very long time the first time you run it.

            Subsequent runs should be much faster.

            This page will be automatically reloaded when the process is complete.
        ''' )
        def update_progress_bar ( proportion, elapsed, remaining, elapsed_str, remaining_str ):
            pbar.progress( proportion,
                f'Running solution code... {proportion*100:0.1f}% ' \
              + f'{elapsed_str} elapsed / ~{remaining_str} left' )
        how_to_data.database_to_jekyll( False, True, update_progress_bar )
        st.experimental_rerun() # ensure refresh of view/edit tab contents
    col2.write( '## Step 2. Build website' )
    col2.markdown( '''
        Jekyll is a tool for converting Markdown documents into a website.
        Step 1 of the build process turns all our tasks, solutions, and other
        site content into markdown files in the `jekyll-input` folder
        of the repository.  This step uses Jekyll to make them into a website.
    ''' )
    col2.info( '''
        **You want to run this task if you ran step 1 and now want to prepare the
        website to publish on GitHub.**
    ''' )
    col2.warning( '''
        Before running this step, **you should first check the "View/edit tasks
        and solutions" tab to proofread any recent changes** you made, so that you
        don't publish to GitHub any errors you could have caught by checking.
    ''' )
    if col2.button( '🔨 Build website' ):
        with col2:
            with st.spinner( 'Building website using Jekyll (~1 minute)' ):
                how_to_data.jekyll_to_site()
        col2.success( 'Website has been rebuilt.' )
