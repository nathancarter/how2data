
#######################
#
#  Simple, low-level utilities to make writing code elsewhere easier.
#  E.g., reading/writing text, reading/writing YAML, filtering folders by file
#  extension, etc.
#  None of these is specific to this project; they just make for cleaner code elsewhere.
#
#######################

import os
import re
import sys
import files
import log

# How to blogify a title into a filename (with lower case and hyphens).
def blogify ( title ):
    return re.sub( '^-+|-+$', '', re.sub( '[^a-z0-9]+', '-', title.lower() ) )

# Must we rebuild an output file?  This function says yes if the output file
# does not exist, or is older than the input file that would be used to build it.
def must_rebuild_file ( input, output ):
    if not os.path.exists( output ):
        log.file_missing( output )
        return True
    input_modified = os.path.getmtime( input )
    output_modified = os.path.getmtime( output )
    return input_modified > output_modified

# Run a shell command and stop the whole app if it gives an error.
# However, if the cleanup command is given, run that one even if you abort.
def ensure_shell_command_succeeds ( command, cleanup = None ):
    code = os.system( command )
    errors = { }
    if code != 0:
        errors = {
            'Received error code' : code,
            'From shell command' : command
        }
    cleanup_code = 0
    if cleanup != None:
        cleanup_code = os.system( cleanup )
        if cleanup_code != 0:
            errors.update( {
                'Cleanup received error code' : cleanup_code,
                'From cleanup command' : cleanup_code,
                'After shell command' : command
            } )
    if code != 0 or cleanup_code != 0:
        log.error( 'Build process exiting with error code 1.', **errors )

# Run a shell command and don't care whether it gives an error.
def run_shell_command_ignoring_errors ( command ):
    code = os.system( command )
    if code != 0:
        log.warning( 'Suppressing shell error', **{
            'Received error code' : code,
            'From shell command' : command
        } )
