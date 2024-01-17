
import os
import pandas as pd
import subprocess
import glob

infolder = 'texs'
outfolder = 'pdfs'
solutions = './ai-generated-solutions.csv'

def get_infile ( index ):
    return os.path.join( infolder, f'question-{index+1}.tex' )

def get_outfile ( index ):
    return os.path.join( outfolder, f'question-{index+1}.pdf' )

def attempt ( *args ):
    print( 'Running:', args )
    result = subprocess.run( args, capture_output=True )
    if result.returncode != 0:
        print( result.stdout.decode( 'utf-8' ) )
        print( result.stderr.decode( 'utf-8' ) )
        raise Exception( f'Halted in: {args}' )

num_solutions = len( pd.read_csv( solutions ) )
for index in range( num_solutions ):
    target = get_outfile( index )
    source = get_infile( index )
    if os.path.isfile( target ) and os.path.getmtime( target ) > os.path.getmtime( source ):
        continue
    if not os.path.isfile( source ):
        raise Exception( f'Missing input file for question {index+1}' )
    attempt( 'pdflatex', '-halt-on-error', source )
    pdffile = os.path.basename( source[:-4] + '.pdf' )
    attempt( 'mv', pdffile, target )
    attempt( 'rm', *glob.glob( '*.aux' ), *glob.glob( '*.log' ) )
    print( f'Compiled {source} --> {target} successfully' )
