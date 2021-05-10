#!/opt/conda/bin/python

import os, sys, shutil
from build_tools import *

section_heading( 'Database build process' )
for file in static_pages:
    source = os.path.join( static_folder, file )
    dest = os.path.join( jekyll_input_folder, file )
    shutil.copyfile( source, dest )
    print( f'Copied: {source} -> {dest}' )

section_heading( 'Jekyll build process' )
sys.exit( os.system( 'jekyll build' ) )
