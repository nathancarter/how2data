
import os
import time

# Get pieces of a filename/path
def extension ( filename ):
    return os.path.splitext( filename )[1]
def without_extension ( filename ):
    return os.path.splitext( filename )[0]

# Get all contents of a text file
def read_text_file ( file ):
    with open( file, 'r' ) as f:
        return f.read()

# Reverse of the previous
def write_text_file ( file, text ):
    with open( file, 'w' ) as f:
        f.write( text )

# Prepend text to a file
def prepend_text_to_file ( file, preamble ):
    write_text_file( file, preamble + read_text_file( file ) )

# Ensure that a folder exists, creating it if needed
def ensure_folder_exists ( path ):
    if not os.path.isdir( path ):
        os.mkdir( path )

# Tools to easily filter for certain types of content within a folder
doc_extensions = [ '.md', '.markdown', '.Rmd', '.ipynb', '.doc', '.docx' ]
img_extensions = [ '.jpg', '.jpeg', '.png', '.gif' ]
def has_any_extension ( filename, extensions ):
    return any( ( filename.endswith( ext ) for ext in extensions ) )
def is_doc ( filename ):
    return has_any_extension( filename, doc_extensions )
def is_img ( filename ):
    return has_any_extension( filename, img_extensions )
def just_docs ( filenames ):
    return [ x for x in filenames if is_doc( x ) ]
def just_imgs ( filenames ):
    return [ x for x in filenames if is_img( x ) ]
def subfolders ( folder ):
    return [ x for x in os.listdir( folder ) \
             if os.path.isdir( os.path.join( folder, x ) ) ]
def docs_inside ( folder ):
    result = [ x for x in os.listdir( folder ) if is_doc( x ) ]
    filenames = list( map( without_extension, result ) )
    if len( set( filenames ) ) < len( filenames ):
        print( 'Documents with same name and different extensions!' )
        print( 'In this folder:', folder )
        sys.exit( 1 )
    return result
def imgs_inside ( folder ):
    return [ x for x in os.listdir( folder ) if is_img( x ) ]

# Create a brief sentence that describes the last modification time of a file
def modification_text ( filename ):
    mod_time = time.gmtime( os.path.getmtime( filename ) )
    return time.strftime(
        '\n\nContent last modified on %d %B %Y.', mod_time )
