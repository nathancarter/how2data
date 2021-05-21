
from ruamel.yaml import YAML

# Get all contents of a text file
def read_text_file ( file ):
    with open( file, 'r' ) as f:
        return f.read()

# Reverse of the previous
def write_text_file ( file, text ):
    with open( file, 'w' ) as f:
        f.write( text )

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
