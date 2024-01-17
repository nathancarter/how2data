
import numpy as np
import pandas as pd
import subprocess
import os

archive = '../how-to-data-archive.h5'
solutions = './ai-generated-solutions.csv'
wrapper_start = '<!-- beginning of wrapper -->'
wrapper_end = '<!-- ending of wrapper -->'
suffix = 'Content last modified on '
tempfolder = 'originals'
subfolder = 'pdfs'
perm_file = 'key.csv'

human_df = pd.read_hdf( archive, 'solutions' )
ai_df = pd.read_csv( solutions )

to_remove = [
    '(See [how to quickly load some sample data](../how-to-quickly-load-some-sample-data).)'
]

pre_replacements = {
    'α' : ' $\\alpha$ ',
    'β' : ' $\\beta$ ',
    'x̄' : ' $\\bar{x}$ ',
    'σ' : ' $\\sigma$ ',
    'σ' : ' $\\sigma$ ',
    '√' : ' $\\sqrt{}$ ',
    'χ' : ' $\\chi$ ',
    '≈' : ' $\\approx$ ',
    'λ' : ' $\\lambda$ ',
    'μ' : ' $\\mu$ ',
    '≠' : ' $\\neq$ ',
    '≤' : ' $\\leq$ ',
    'Σ' : ' $\\Sigma$ ',
    'π' : ' $\\pi$ ',
    '₀' : '0',
    '₁' : '1',
    'θ' : ' $\\theta$ ',
    '⋮' : ' $\\vdots$ ',
    '\\[' : '$$',
    '\\]' : '$$'
}
post_replacements = {
    '─' : '-',
    '∞' : 'infinity',
    '∪' : 'union',
    '⋮' : '$\\vdots$'
}

def fix_md ( markdown ):
    lines = markdown.split( '\n' )
    for i in range( len( lines ) ):
        lines[i] = lines[i].replace( '\\( ', '$' )
        lines[i] = lines[i].replace( ' \\)', '$' )
        lines[i] = lines[i].replace( '\\(', '$' )
        lines[i] = lines[i].replace( '\\)', '$' )
        if i > 0:
            if lines[i][:2] == '- ' and lines[i-1][:2] != '- ' and lines[i-1] != '':
                lines[i-1] += '\n'
            if lines[i][:2] == '* ' and lines[i-1][:2] != '* ' and lines[i-1] != '':
                lines[i-1] += '\n'
    return '\n'.join( lines )

if not os.path.exists( tempfolder ):
    os.mkdir( tempfolder )
if not os.path.exists( subfolder ):
    os.mkdir( subfolder )

def get_human_solution ( index ):
    row = human_df.iloc[index,:]
    permalink = row['permalink']
    with open( f'../jekyll-input/{permalink}.md', 'r' ) as file:
        markdown = file.read()
    start_index = markdown.find( wrapper_start )
    end_index = markdown.find( wrapper_end )
    markdown = markdown[start_index+len(wrapper_start):end_index]
    suffix_index = markdown.find( suffix )
    markdown = markdown[:suffix_index]
    for item in to_remove:
        markdown = markdown.replace( item, '' )
    result = subprocess.run(
        [ 'pandoc', '--from', 'markdown', '--to', 'latex' ],
        input=markdown.encode( 'utf-8' ), capture_output=True
    ).stdout.decode( 'utf-8' )
    for key, value in post_replacements.items():
        result = result.replace( key, value )
    return result

def get_ai_solution ( row_index, col_index ):
    markdown = ai_df.iloc[row_index,col_index]
    for key, value in pre_replacements.items():
        markdown = markdown.replace( key, value )
    markdown = fix_md( markdown )
    with open( './tmp.md', 'w' ) as file:
        file.write( markdown )
    result = subprocess.run(
        [ 'jupytext', 'tmp.md', '--to', 'markdown', '--execute', '--output', '-' ],
        capture_output=True
    )
    if result.returncode == 0:
        result = result.stdout.decode( 'utf-8' )
    else:
        result = markdown
    subprocess.run( [ 'rm', 'tmp.md' ] )
    result = subprocess.run(
        [ 'pandoc', '--from', 'markdown', '--to', 'latex' ],
        input=result.encode( 'utf-8' ), capture_output=True
    ).stdout.decode( 'utf-8' )
    for key, value in post_replacements.items():
        result = result.replace( key, value )
    return result

def row_to_latex ( row_index ):
    row = ai_df.iloc[row_index,:]
    with open( 'preamble.tex', 'r' ) as file:
        preamble = file.read()
    latex = f'''
{preamble}
\\begin{{document}}
\\section*{{Question {row_index+1}}}
\\subsection*{{Short version}}
{row['short prompt']}
\\subsection*{{Long version}}
{row['long prompt']}
    '''
    answers = [ get_human_solution( row_index ) ]
    print( f'\tRan human code for row {row_index+1}' )
    for col_index in range( 2, len( row ) ):
        answers.append( get_ai_solution( row_index, col_index ) )
        print( f'\tRan AI code for row {row_index+1} col {col_index}' )
    perm = np.random.permutation( len( answers ) )
    for i in range( len( answers ) ):
        latex += f'''
\\newpage
\\section*{{Answer {i+1}}}
{answers[perm[i]]}
        '''
    latex += '\n\\end{document}'
    return latex, perm

def texfile ( index ):
    return os.path.join( tempfolder, f'question-{index+1}.tex' )

def latex_to_file ( latex, index ):
    with open( texfile( index ), 'w' ) as file:
        file.write( latex )

if not os.path.isfile( perm_file ):
    perm_df = pd.DataFrame( { 'question' : range( 1, len( ai_df ) + 1 ) } )
    for index in range( 1, len( ai_df.columns ) ):
        perm_df[f'answer {index}'] = pd.NA
    perm_df.to_csv( 'key.csv', index=False )
else:
    perm_df = pd.read_csv( perm_file )
names = [ 'human written', *ai_df.columns[2:] ]
for index, row in ai_df.iterrows():
    if not any( row.isna() ) and os.path.isfile( texfile( index ) ):
        # print( f'Skipping row {index+1} out of {len( ai_df )}...' )
        continue
    print( f'Starting on row {index+1} out of {len( ai_df )}...' )
    latex, perm = row_to_latex( index )
    latex_to_file( latex, index )
    for i in range( len( perm ) ):
        perm_df.iloc[index,i+1] = names[perm[i]]
    perm_df.to_csv( perm_file, index=False )
