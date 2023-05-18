
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
import sys
import files

# Get all YAML from a YAML file into a Python dict
def read_yaml_from_file ( file ):
    return YAML().load( files.read_text_file( file ) )

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

# Run a shell command and stop the whole app if it gives an error.
# However, if the cleanup command is given, run that one even if you abort.
def ensure_shell_command_succeeds ( command, cleanup = None ):
    code = os.system( command )
    if code != 0:
        print( f'How2Data build process received this error code: {code}' )
        print( f'From running this shell command: {command}' )
    cleanup_code = 0
    if cleanup != None:
        cleanup_code = os.system( cleanup )
        if cleanup_code != 0:
            print( f'How2Data build process received this error code: {cleanup_code}' )
            print( f'From runnin this cleanup command: {cleanup_code}' )
            print( f'Right after this shell code: {command}' )
    if code != 0 or cleanup_code != 0:
        print( f'How2Data build exiting with error code 1.' )
        sys.exit( 1 )
# Run a shell command and don't care whether it gives an error.
def run_shell_command_ignoring_errors ( command ):
    code = os.system( command )
    if code != 0:
        print( f'How2Data build process received this error code: {code}' )
        print( f'From running this shell command: {command}' )
        print( f'How2Data build ignoring them and continuing anyway...' )
