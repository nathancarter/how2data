
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from time import time

infile = '../how-to-data-archive.h5'
outfile = './ai-generated-solutions.csv'
models = [ 'gpt-3.5-turbo', 'gpt-4-1106-preview' ]

# software_df = pd.read_hdf( infile, 'software' )
# topics_df = pd.read_hdf( infile, 'topics' )
tasks_df = pd.read_hdf( infile, 'tasks' )
solutions_df = pd.read_hdf( infile, 'solutions' )

load_dotenv()

client = OpenAI( api_key=os.getenv( 'OPENAI_API_KEY' ) )

def get_completion ( prompt, model ):
    messages = [ { 'role': 'user', 'content': prompt } ]
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0 )
    return response.choices[0].message.content

def short_solution_prompt ( solution_row ):
    title = solution_row['solution title']
    title = title[0].lower() + title[1:]
    return f'I need to know {title}.'

def long_solution_prompt ( solution_row ):
    start = short_solution_prompt( solution_row )
    tool = start[start.rfind( ' (' )+2:-2]
    start = start[:start.rfind( ' (' )]
    task_row = tasks_df[tasks_df['task name'] == solution_row['task name']].iloc[0]
    description = task_row['content'].strip()
    index = description.find( 'Related tasks:' )
    if index >= 0:
        description = description[:index].strip()
    description = description.replace( '\n', ' ' )
    description = description.replace( '  ', ' ' )
    return f'I have a question about doing data science {tool}. {start}. ' \
        + f'More specifically: {description}'

all_times = [ ]
def mark_start_time ():
    return time()
def mark_elapsed_time ( start_time ):
    global all_times
    all_times.append( time() - start_time )

def report_progress ( results_df ):
    relevant_cells = results_df.iloc[:,2:]
    num_cells_to_do = relevant_cells.isna().sum().sum()
    num_cells_done = relevant_cells.notna().sum().sum()
    print( f'OVERALL: {num_cells_done} queries done, {num_cells_to_do} queries to do' )

def save_progress ( results_df ):
    results_df.to_csv( outfile, index=False )
    if len( all_times ) == 0:
        print( '\tNo queries done yet in this run.' )
        return
    relevant_cells = results_df.iloc[:,2:]
    num_cells_to_do = relevant_cells.isna().sum().sum()
    print( f'\tLast query took {all_times[-1]:0.2f}s' )
    average_query_time = sum( all_times ) / len( all_times )
    print( f'\tAverage query time: {average_query_time:0.2f}s' )
    print( f'\tExpected completion time: {average_query_time * num_cells_to_do / 60:0.2f}m' )

if not os.path.isfile( outfile ):
    results_df = pd.DataFrame( {
        'short prompt' : [ short_solution_prompt( row ) for _, row in solutions_df.iterrows() ],
        'long prompt' : [ long_solution_prompt( row ) for _, row in solutions_df.iterrows() ]
    } )
    for model in models:
        results_df[ f'result from {model} on short prompt' ] = pd.NA
        results_df[ f'result from {model} on long prompt' ] = pd.NA
    save_progress( results_df )

results_df = pd.read_csv( outfile )
report_progress( results_df )
for index, row in results_df.iterrows():
    to_do_this_row = row.isna().sum()
    print( f'LOOPING: {to_do_this_row} queries to do in row {index} of {len( results_df )}' )
    for model in models:
        start_time = mark_start_time()
        results_df.at[ index, f'result from {model} on short prompt' ] = \
            get_completion( row['short prompt'], model )
        mark_elapsed_time( start_time )
        save_progress( results_df )
        report_progress( results_df )
        start_time = mark_start_time()
        results_df.at[ index, f'result from {model} on long prompt' ] = \
            get_completion( row['long prompt'], model )
        mark_elapsed_time( start_time )
        save_progress( results_df )
        report_progress( results_df )
