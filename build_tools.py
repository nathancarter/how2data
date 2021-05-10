
import os

def section_heading ( title ):
    print( '-' * len( title ) )
    print( title )
    print( '-' * len( title ) )

def markdown_files ( filenames ):
    return [
        x for x in filenames if x[-3:] == '.md' or x[-9:] == '.markdown'
    ]

main_folder = os.path.dirname( os.path.realpath( __file__ ) )
static_folder = os.path.join( main_folder, 'database', 'static' )
static_pages = markdown_files( os.listdir( static_folder ) )
jekyll_input_folder = os.path.join( main_folder, 'jekyll-input' )
