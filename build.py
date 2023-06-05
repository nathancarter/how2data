#!/opt/conda/bin/python

#######################
#
#  This is the main build script for this repository.
#  To understand the build process, read the comments on each section below,
#  then dive into the how_to_data module, where the major content resides.
#
#######################

import how_to_data
import sys
import log

# Command line parameters
# -f/--force = rerun all solution code even if modification dates don't require it
# -j/--no-jekyll = stop after building database into jekyll_input folder; don't run Jekyll
rerun_solutions = '-f' in sys.argv or '--force' in sys.argv
skip_jekyll = '-j' in sys.argv or '--no-jekyll' in sys.argv
quiet = '-v' not in sys.argv and '--verbose' not in sys.argv

# Build Jekyll input from database
how_to_data.database_to_jekyll( rerun_solutions, quiet )

# Run Jekyll on newly copied files
if skip_jekyll:
    log.heading( 'Skipping Jekyll build process' )
else:
    log.heading( 'Running Jekyll build process' )
    how_to_data.jekyll_to_site()

# State completion
log.heading( 'Build completed successfully.' )
