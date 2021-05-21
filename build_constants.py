
import os

# What extensions count as documents vs. images?
doc_extensions = [ '.md', '.markdown' ]
img_extensions = [ '.jpg', '.jpeg', '.png', '.gif' ]

# Important folders
main_folder = os.path.dirname( os.path.realpath( __file__ ) )
jekyll_input_folder = os.path.join( main_folder, 'jekyll-input' )
static_folder = os.path.join( main_folder, 'database', 'static' )
tasks_folder = os.path.join( main_folder, 'database', 'tasks' )
task_imgs_folder = os.path.join( jekyll_input_folder, 'assets', 'task-images' )
solutions_folder = os.path.join( main_folder, 'database', 'solutions' )
solution_imgs_folder = os.path.join( jekyll_input_folder, 'assets', 'solution-images' )

# Which Jupyter kernels are supported for which languages
kernel_for_software = {
    'Python' : 'python3',
    'Julia' : 'julia-1.6',
    'R' : 'ir'
}
