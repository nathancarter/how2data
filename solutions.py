
import how_to_data
import config
import software
import pandas as pd
import files
import os
import markdown
import yaml

df = None

# Load from disk a table of all the solutions in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        json = [ ]
        for task_name in files.subfolders( config.tasks_folder ):
            for solution_file in files.docs_inside( os.path.join( config.tasks_folder, task_name ) ):
                if files.without_extension( solution_file ) == 'description':
                    continue
                bits = files.without_extension( solution_file ).split( ', ' )
                software_name = bits[0]
                if len( bits ) == 1:
                    solution_name = 'solution'
                else:
                    solution_name = ', '.join( bits[1:] )
                input_file = os.path.join( config.tasks_folder, task_name, solution_file )
                next = {
                    'task name' : task_name,
                    'software' : software_name,
                    'solution name' : solution_name,
                    'solution filename' : solution_file,
                    'solution path' : config.relativize_path( input_file ),
                    'solution title' :
                        f'{task_name} (in {files.without_extension( solution_file )})'
                }
                markdown_content = markdown.read_doc( input_file )
                metadata, content = yaml.split_string( markdown_content )
                next['content'] = content + files.modification_text( input_file )
                for key, value in metadata.items():
                    next[key] = value
                next['raw content'] = markdown_content
                next['permalink'] = config.blogify( next['solution title'] )
                json.append( next )
        df = pd.DataFrame( json )
        # Add links to solution pages to each solution row
        def link_to_solution ( solution_row ):
            return f'[{solution_row["solution name"]}](../{config.blogify(solution_row["solution title"])})'
        df['markdown link'] = df.apply( link_to_solution, axis=1 )
        software.check_consistency_with_solutions()
    return df
