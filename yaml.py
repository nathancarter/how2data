
from ruamel.yaml import YAML
import files

# Get all YAML from a YAML file into a Python dict
def read_header ( file ):
    return YAML().load( files.read_text_file( file ) )

# Split out the YAML header and content of a markdown document given as
# a text string, returning the YAML dictionary and the remaining text
# content as a pair.
def split_string ( text ):
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
def split_file ( filename ):
    with open( filename, 'r' ) as f:
        return split_string( f.read() )
