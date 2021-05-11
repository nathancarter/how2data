#!/opt/conda/bin/python

import os, sys
from build_tools import *

section_heading( 'Database build process' )
for file in static_pages:
    if file == 'software.md':
        copy_static_file( file, {
            'SET_OF_SOFTWARE_PACKAGES': software_table
        } )
    else:
        copy_static_file( file )

section_heading( 'Jekyll build process' )
sys.exit( os.system( 'bundle exec jekyll build' ) )
