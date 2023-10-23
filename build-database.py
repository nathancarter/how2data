
import solutions
import topics
import tasks
import software
import log
import os
import pandas as pd
import numpy as np
import progress

filename = 'how-to-data-archive.h5'

log.heading( 'Preparation' )

tasks_df = tasks.all()
log.info( 'Loaded tasks table' )
topics_df = topics.all()
log.info( 'Loaded topics table' )
solutions_df = solutions.all()
log.info( 'Loaded solutions table' )
software_df = software.all()
log.info( 'Loaded software table' )

if os.path.exists( filename ):
    log.file_delete( filename )
    os.remove( filename )

log.heading( 'Extending tables' )

# Note: no extensions needed to software table

tasks_df['url'] = ''
tasks_df['description'] = ''
tasks_df['generated'] = ''
pbar = progress.ProgressBar( 'Tasks table' )
pbar.set_step( 0, len( tasks_df ) )
for index, row in tasks_df.iterrows():
    task = tasks.Task( row )
    row['url'] = task.url
    row['description'] = task.description()
    row['generated'] = task.generated_markdown()
    pbar.step()
pbar.end()
log.info( 'Extended tasks table' )

topics_df['url'] = ''
topics_df['tasks'] = np.nan
topics_df['generated'] = ''
topics_df['pdf urls'] = np.nan
pbar = progress.ProgressBar( 'Topics table' )
pbar.set_step( 0, len( topics_df ) )
for index, row in topics_df.iterrows():
    topic = topics.Topic( row )
    row['url'] = topic.url
    row['tasks'] = topic.tasks()['task name'].tolist()
    row['generated'] = topic.generated_markdown()
    row['pdf urls'] = [ topics.Topic.pdf_url( file ) for file in topic.existing_pdf_files() ]
    pbar.step()
pbar.end()
log.info( 'Extended topics table' )

solutions_df['url'] = ''
solutions_df['inner content'] = ''
solutions_df['generated'] = ''
solutions_df['generated interior only'] = ''
pbar = progress.ProgressBar( 'Solutions table' )
pbar.set_step( 0, len( solutions_df ) )
for index, row in solutions_df.iterrows():
    solution = solutions.Solution( row )
    row['url'] = solution.url
    row['inner content'] = solution.inner_content
    row['generated'] = solution.generated_markdown()
    row['generated interior only'] = solution.generated_body()
    pbar.step()
pbar.end()
solutions_df = solutions_df.astype( str ) # prevent warnings when saving to HDF; whole table is strings anyway
log.info( 'Extended solutions table' )

log.heading( 'Writing final results' )

with pd.HDFStore( filename ) as db:
    db['software'] = software_df
    log.info( 'Stored software table' )
    db['tasks'] = tasks_df
    log.info( 'Stored tasks table' )
    db['topics'] = topics_df
    log.info( 'Stored topics table' )
    db['solutions'] = solutions_df
    log.info( 'Stored solutions table' )

with pd.HDFStore( filename ) as db:
    log.built(
        'HDF5 database file',
        filename,
        keys=db.keys(),
        size=f'{os.path.getsize( filename )/1024/1024:0.2f}MB'
    )
