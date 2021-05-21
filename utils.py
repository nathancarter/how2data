
from ruamel.yaml import YAML
import os

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
