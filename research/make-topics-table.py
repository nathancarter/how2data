
import pandas as pd
import os
import subprocess

infile = '../how-to-data-archive.h5'
outfile = './task-topic-relationships.csv'
infolder = 'pdfs'
outfolder = 'pdfs-by-course'

# software_df = pd.read_hdf( infile, 'software' )
topics_df = pd.read_hdf( infile, 'topics' )
tasks_df = pd.read_hdf( infile, 'tasks' )
solutions_df = pd.read_hdf( infile, 'solutions' )

df = solutions_df[['task name','software']].copy()
df['question #'] = list( range( 1, len( df ) + 1 ) )
df = df[['question #','task name','software']]

for index, row in topics_df.iterrows():
    print( f'Computing column {row["topic name"]}...' )
    course_code = row['topic name'].split()[-1]
    df[course_code] = df['task name'].apply(
        lambda task_name : task_name in row['raw content']
    ).replace( { True : 'X', False : '' } )

print( f'Saving file {outfile}...' )
df.to_csv( outfile )

print( 'Done.' )

if not os.path.exists( outfolder ):
    os.mkdir( outfolder )

notes = ''
def tee ( text ):
    global notes
    print( text )
    notes += text + '\n'
for software in [ 'Python', 'R' ]:
    tee( '-'*len(software) )
    tee( software )
    tee( '-'*len(software) )
    for topic in topics_df['topic name']:
        course_code = topic.split()[-1]
        if course_code == 'GR526':
            continue
        questions = df[(df['software'] == software) & (df[course_code] == 'X')]
        question_nums = [ str(num) for num in questions['question #'] ]
        tee( f'{course_code}: {", ".join( question_nums )}' )
        if not os.path.exists( os.path.join( outfolder, course_code ) ):
            os.mkdir( os.path.join( outfolder, course_code ) )
        for num in questions['question #']:
            subprocess.run( [
                'cp',
                os.path.join( infolder, f'question-{num}.pdf' ),
                os.path.join( outfolder, course_code, f'question-{num}.pdf' )
            ] )
with open( os.path.join( outfolder, 'notes.txt' ), 'w' ) as f:
    f.write( notes )
