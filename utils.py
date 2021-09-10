
#######################
#
#  Simple, low-level utilities to make writing code elsewhere easier.
#  E.g., reading/writing text, reading/writing YAML, filtering folders by file
#  extension, etc.
#  None of these is specific to this project; they just make for cleaner code elsewhere.
#
#######################

from ruamel.yaml import YAML
import os
import re
import time
import sys
import json

# Get pieces of a filename/path
def file_extension ( filename ):
    return os.path.splitext( filename )[1]
def without_extension ( filename ):
    return os.path.splitext( filename )[0]

# Get all contents of a text file
def read_text_file ( file ):
    with open( file, 'r' ) as f:
        return f.read()

# Reverse of the previous
def write_text_file ( file, text ):
    with open( file, 'w' ) as f:
        f.write( text )
# When writing Markdown, be aware that Jekyll messes with \{ and \},
# which screws up our math, so fix them.
def write_markdown ( file, markdown ):
    write_text_file( file, markdown.replace( '\\{', '\\\\{' )
                                   .replace( '\\}', '\\\\}' ) )

# Ensure that a folder exists, creating it if needed
def ensure_folder_exists ( path ):
    if not os.path.isdir( path ):
        os.mkdir( path )

# Get all YAML from a YAML file into a Python dict
def read_yaml_from_file ( file ):
    return YAML().load( read_text_file( file ) )

# Split out the YAML header and content of a markdown document given as
# a text string, returning the YAML dictionary and the remaining text
# content as a pair.
def string_split_yaml_header ( text ):
    lines = [ line+'\n' for line in text.split( '\n' ) ]
    # if yaml header exists, find its end and return it and the content
    if lines[0] == '---\n':
        lines = lines[1:]
        yaml_end = lines.index( '---\n' )
        return (
            YAML().load( ''.join( lines[:yaml_end] ) ),
            ''.join( lines[yaml_end+1:] )
        )
    # otherwise return an empty yaml header and just the content
    return {}, ''.join( lines )
# Open a text file and run the above function on it
def file_split_yaml_header ( filename ):
    with open( filename, 'r' ) as f:
        return string_split_yaml_header( f.read() )

# Tools to easily filter for certain types of content within a folder
doc_extensions = [ '.md', '.markdown', '.Rmd', '.ipynb', '.doc', '.docx' ]
img_extensions = [ '.jpg', '.jpeg', '.png', '.gif' ]
def has_any_extension ( filename, extensions ):
    return any( ( filename.endswith( ext ) for ext in extensions ) )
def is_doc ( filename ):
    return has_any_extension( filename, doc_extensions )
def is_img ( filename ):
    return has_any_extension( filename, img_extensions )
def just_docs ( filenames ):
    return [ x for x in filenames if is_doc( x ) ]
def just_imgs ( filenames ):
    return [ x for x in filenames if is_img( x ) ]
def subfolders ( folder ):
    return [ x for x in os.listdir( folder ) \
             if os.path.isdir( os.path.join( folder, x ) ) ]
def docs_inside ( folder ):
    result = [ x for x in os.listdir( folder ) if is_doc( x ) ]
    filenames = list( map( without_extension, result ) )
    if len( set( filenames ) ) < len( filenames ):
        print( 'Documents with same name and different extensions!' )
        print( 'In this folder:', folder )
        sys.exit( 1 )
    return result
def imgs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_img( x ) ]

# Crucial function:  This finds the unique file with the given filename and
# path, but with any extension from doc_extensions, and reads it in,
# converting to markdown if necessary.  If there is no such file, or are
# multiple such files, it quits with an error.
def get_unique_markdown_doc ( path_and_base_filename ):
    which_exist = [ extension for extension in doc_extensions \
        if os.path.exists( path_and_base_filename + extension ) and \
        os.path.isfile( path_and_base_filename + extension ) ]
    if len( which_exist ) == 0:
        print( 'No document file found with this base:', path_and_base_filename )
        print( '          and any of these extensions:', ' '.join( doc_extensions ) )
        sys.exit( 1 )
    if len( which_exist ) > 1:
        print( 'Multiple documents found with this base:', path_and_base_filename )
        for extension in doc_extensions:
            print( '                                  Found:',
                path_and_base_filename + extension )
        sys.exit( 1 )
    return path_and_base_filename + which_exist[0]
# Function that converts an .ipynb file into markdown text.
# If that .ipynb file has markdown links to images stored as cell attachments,
# they are converted into data URIs.
def ipynb_to_markdown ( filename ):
    with open( filename, 'r' ) as f:
        cells = json.load( f )['cells']
    attached_src_attr = \
        re.compile( 'src="attachment:([^"]*)"|src=\'attachment:([^\']*)\'' )
    result = ''
    for cell in cells:
        if cell['cell_type'] == 'markdown':
            new_chunk = '\n' + ''.join( cell['source'] ) + '\n'
            match = attached_src_attr.search( new_chunk )
            while match:
                before = new_chunk[:match.start()]
                after = new_chunk[match.end():]
                src = match.group( 1 ) if match.group( 1 ) else match.group( 2 )
                attachment = cell['attachments'][src]
                mime_type = list( attachment.keys() )[0]
                base_64_data = attachment[mime_type]
                new_attr = f'src="data:{mime_type};base64, {base_64_data}"'
                new_chunk = before + new_attr + after
                match = attached_src_attr.search( new_chunk )
            result += new_chunk
        elif cell['cell_type'] == 'code':
            result += '\n```python\n' + ''.join( cell['source'] ) + '\n```\n'
        else:
            print( 'Unknown cell type:', cell['cell_type'] )
            print( '     In this file:', filename )
            sys.exit( 1 )
    while result[0] == '\n':
        result = result[1:]
    return result
# To pair with get_unique_markdown_doc:  Read any document whose extension is in
# doc_extensions into markdown text.  It can support markdown (no conversion
# needed) or RMarkdown (tiny conversion needed) or Jupyter notebooks (more
# conversion needed).
def read_doc_to_markdown ( filename ):
    extension = file_extension( filename )
    if extension in [ '.md', '.markdown' ]:
        return read_text_file( filename )
    if extension in [ '.Rmd' ]:
        return read_text_file( filename ).replace( '```{r}', '```R' )
    if extension in [ '.ipynb' ]:
        return ipynb_to_markdown( filename )
    if extension in [ '.doc', '.docx' ]:
        tmp_file = os.path.join( *os.path.split( filename )[:-1], 'temp.ipynb' )
        ensure_shell_command_succeeds( f'pandoc -o "{tmp_file}" "{filename}"' )
        result = ipynb_to_markdown( tmp_file )
        ensure_shell_command_succeeds( f'rm "{tmp_file}"' )
        return result
    print( 'Unknown document type:', extension )
    print( '        For this file:', filename )
    sys.exit( 1 )

# Function for printing section headings in the console output
def section_heading ( title ):
    print()
    print()
    print( title )
    print( '-' * len( title ) )

# How to blogify a title into a filename (with lower case and hyphens).
def blogify ( title ):
    return re.sub( '^-+|-+$', '', re.sub( '[^a-z0-9]+', '-', title.lower() ) )

# Must we rebuild an output file?  This function says yes if the output file
# does not exist, or is older than the input file that would be used to build it.
def must_rebuild_file ( input, output ):
    if not os.path.exists( output ):
        print( f'Must rebuild because DNE: {output}' )
        return True
    input_modified = os.path.getmtime( input )
    output_modified = os.path.getmtime( output )
    return input_modified > output_modified

# How to place some special content in an HTML or markdown file and
# indicate that it's special by wrapping it in comment flags, so that you
# can extract it again later.  This assumes only one such special block per file.
start_comment = '<!-- beginning of wrapper -->'
end_comment   = '<!-- ending of wrapper -->'
def wrap_in_html_comments ( text ):
    return f'{start_comment}\n\n{text}\n\n{end_comment}\n'
def unwrap_from_html_comments ( text ):
    begin = text.index( start_comment )
    end = text.index( end_comment )
    return text[begin+len(start_comment):end]

# Create a brief sentence that describes the last modification time of a file
def modification_text ( filename ):
    mod_time = time.gmtime( os.path.getmtime( filename ) )
    return time.strftime(
        '\n\nContent last modified on %d %B %Y.', mod_time )

# Run a shell command and stop the whole app if it gives an error.
# However, if the cleanup command is given, run that one even if you abort.
def ensure_shell_command_succeeds ( command, cleanup = None ):
    code = os.system( command )
    if code != 0:
        print( f'Above errors yielded error code {code}.' )
    cleanup_code = 0
    if cleanup != None:
        cleanup_code = os.system( cleanup )
        if cleanup_code != 0:
            print( f'When attempting to clean up, got error code {cleanup_code}!' )
    if code != 0 or cleanup_code != 0:
        print( f'How2Data build exiting with error code 1.' )
        sys.exit( 1 )
# Run a shell command and don't care whether it gives an error.
def run_shell_command_ignoring_errors ( command ):
    code = os.system( command )
    if code != 0:
        print( f'Above errors yielded error code {code}.' )
        print( f'How2Data build ignoring them and continuing anyway...' )
