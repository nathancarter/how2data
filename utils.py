
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

# Get all contents of a text file
def read_text_file ( file ):
    with open( file, 'r' ) as f:
        return f.read()

# Reverse of the previous
def write_text_file ( file, text ):
    with open( file, 'w' ) as f:
        f.write( text )

# Ensure that a folder exists, creating it if needed
def ensure_folder_exists ( path ):
    if not os.path.isdir( path ):
        os.mkdir( path )

# Get all YAML from a YAML file into a Python dict
def read_yaml_from_file ( file ):
    return YAML().load( read_text_file( file ) )

# Open a text file and split out the YAML header,
# returning the YAML dictionary and the remaining text content
# as a pair
def file_split_yaml_header ( filename ):
    with open( filename, 'r' ) as f:
        lines = f.readlines()
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

# Tools to easily filter for certain types of content within a folder
doc_extensions = [ '.md', '.markdown' ]
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
    return [ x for x in os.listdir( folder ) if is_doc( x ) ]
def imgs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_img( x ) ]

# Function for printing section headings in the console output
def section_heading ( title ):
    print()
    print()
    print( title )
    print( '-' * len( title ) )

# How to blogify a title into a filename (with lower case and hyphens).
def blogify ( title ):
    return re.sub( '^-+|-+$', '', re.sub( '[^a-z0-9]+', '-', title.lower() ) )

# Get pieces of a filename/path
def file_extension ( filename ):
    return os.path.splitext( filename )[1]
def without_extension ( filename ):
    return os.path.splitext( filename )[0]

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
