
import subprocess
import log

# Run a shell command and stop the whole app if it gives an error.
# However, if the cleanup command is given, run that one even if you abort.
def run_or_halt ( command, cleanup=None, show_output=False ):
    result = subprocess.run( command, shell=True, capture_output=not show_output )
    code = result.returncode
    errors = { }
    if code != 0:
        errors = {
            'Received error code' : code,
            'From shell command' : command,
            'With error message' : result.stderr.decode( 'UTF-8' )
        }
    cleanup_code = 0
    if cleanup != None:
        result = subprocess.run( cleanup, shell=True, capture_output=True )
        cleanup_code = result.returncode
        if cleanup_code != 0:
            errors.update( {
                'Cleanup received error code' : cleanup_code,
                'From cleanup command' : cleanup_code,
                'After shell command' : command,
                'With error message' : result.stderr.decode( 'UTF-8' )
            } )
    if code != 0 or cleanup_code != 0:
        log.error( 'Build process exiting with error code 1.', **errors )

# Run a shell command and don't care whether it gives an error.
def run_and_continue ( command, show_output=False ):
    result = subprocess.run( command, shell=True, capture_output=not show_output )
    if result.returncode != 0:
        log.warning( 'Suppressing shell error', **{
            'Received error code' : result.returncode,
            'From shell command' : command,
            'With error message' : result.stderr.decode( 'UTF-8' )
        } )
