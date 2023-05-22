
import os
import re

# Global config for the whole build process
# Any of these you want to change you change before calling any build functions
main_folder = os.path.dirname( os.path.realpath( __file__ ) )
database_config_file = os.path.join( main_folder, 'database', 'database.yml' )
static_folder = os.path.join( main_folder, 'database', 'static' )
tasks_folder = os.path.join( main_folder, 'database', 'tasks' )
topics_folder = os.path.join( main_folder, 'database', 'topics' )
jekyll_input_folder = os.path.join( main_folder, 'jekyll-input' )
jekyll_imgs_folder = os.path.join( jekyll_input_folder, 'assets', 'dynamic-images' )
site_url = 'https://how-to-data.org/'

# How to make an absolute path relative to this project
# For example, if the project root is /example/path,
# then relativize_path("/example/path/foo/bar.html") == "foo/bar.html"
# and relativize_path("/not/same/path/at.all") == "/not/same/path/at.all"
def relativize_path ( input_path ):
    prefix = main_folder
    if prefix[-1] != os.path.sep:
        prefix += os.path.sep
    if input_path.startswith( prefix ):
        return input_path[len(prefix):]
    return input_path

# One site-wide global function:
# How to blogify a title of any resource into a filename (with lower case and hyphens).
def blogify ( title ):
    return re.sub( '^-+|-+$', '', re.sub( '[^a-z0-9]+', '-', title.lower() ) )
