
import how_to_data
import config
import pandas as pd
import files
import os
import markdown
import yaml

df = None

# Load from disk a table of all the topics in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        json = [ ]
        for topic_file in files.just_docs( os.listdir( config.topics_folder ) ):
            if topic_file == 'README.md':
                continue
            full_filename = os.path.join( config.topics_folder, topic_file )
            markdown_content = markdown.read_doc( full_filename )
            metadata, content = yaml.split_string( markdown_content )
            content += files.modification_text( full_filename )
            next = {
                'topic name' : files.without_extension( topic_file ),
                'topic filename' : config.relativize_path( full_filename ),
                'permalink' : config.blogify( files.without_extension( topic_file ) ),
                'content' : content,
                'raw content' : markdown_content
            }
            for key, value in metadata.items():
                next[key] = value
            json.append( next )
        df = pd.DataFrame( json )
        # Add links to topic pages
        df['markdown link'] = df['topic name'].apply(
            lambda name: f'[{name}](../{config.blogify(name)})' )
    return df
