
#######################
#
#  Declaration of constants that define the build process.
#  This includes many folder names and the set of supported Jupyter kernels.
#
#######################


import os

# Important folders
main_folder          = os.path.dirname( os.path.realpath( __file__ ) )
database_config_file = os.path.join( main_folder, 'database', 'database.yml' )
jekyll_input_folder  = os.path.join( main_folder, 'jekyll-input' )
static_folder        = os.path.join( main_folder, 'database', 'static' )
tasks_folder         = os.path.join( main_folder, 'database', 'tasks' )
task_imgs_folder     = os.path.join( jekyll_input_folder, 'assets', 'task-images' )
topics_folder        = os.path.join( main_folder, 'database', 'topics' )
topic_imgs_folder    = os.path.join( jekyll_input_folder, 'assets', 'topic-images' )
solutions_folder     = os.path.join( main_folder, 'database', 'solutions' )
solution_imgs_folder = os.path.join( jekyll_input_folder, 'assets', 'solution-images' )
# How to make an absolute path relative to this project
def path_in_project ( maybe_abs_path ):
    prefix = main_folder
    if prefix[-1] != os.path.sep:
        prefix += os.path.sep
    if maybe_abs_path.startswith( prefix ):
        return maybe_abs_path[len(prefix):]
    return maybe_abs_path

# Which Jupyter kernels are supported for which languages
kernel_for_software = {
    'Python' : 'python3',
    'Julia'  : 'julia-1.6',
    'R'      : 'ir'
}
