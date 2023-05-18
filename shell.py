
import os
import log

# Run a shell command and stop the whole app if it gives an error.
# However, if the cleanup command is given, run that one even if you abort.
def run_or_halt ( command, cleanup = None ):
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
def run_and_continue ( command ):
    code = os.system( command )
    if code != 0:
        log.warning( 'Suppressing shell error', **{
            'Received error code' : code,
            'From shell command' : command
        } )
