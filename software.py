
import how_to_data
import config
import solutions
import pandas as pd
import yaml

df = None
pretty_df = None

# Function-building function used in all(), below
def software_package_icon ( height, is_link ):
    def result ( package_row ):
        name = package_row['name']
        icon = package_row['icon']
        icon_markdown = f'![{name} icon]({icon}){{: style="height: {height}px;" }}'
        return icon_markdown if not is_link \
            else f'[{icon_markdown}](../{package_row["permalink"]})'
    return result

# Function used in all(), below.
def software_package_website ( package_row ):
    url = package_row['website']
    return f'[{url}]({url})'

# Load from disk a table of all the software packages in the database.
# Cache the result so that later runs are faster.
def all ():
    global df
    if df is None:
        df = pd.DataFrame( yaml.read_header( config.database_config_file )['software'] )
        df['title'] = df['name'].apply( lambda name: f'Software package: {name}' )
        df['permalink'] = df['title'].apply( config.blogify )
        # Add markdown code for each package's icon
        df['icon markdown'] = \
            df.apply( software_package_icon( 50, True ), axis=1 )
        df['large icon markdown'] = \
            df.apply( software_package_icon( 150, False ), axis=1 )
        df['name as link'] = df.apply( ( lambda row:
            f'[{row["name"]}](../{row["permalink"]})' ), axis=1 )
        # Add markdown code for each package's website
        df['website markdown'] = df.apply( software_package_website, axis=1 )
        # Add count of number of solutions in database for each piece of software
        df['num solutions'] = df['name'].apply( lambda name: \
            sum( solutions.all()['software'] == name ) )
        check_consistency_with_solutions()
    return df

# Verify that the solutions and software packages dataframes we've loaded are consistent.
# If they are not, abort the build here with an error message.
# Or if either one is not yet loaded, do nothing.
def check_consistency_with_solutions ():
    if df is not None and solutions.df is not None:
        for index, task_row in solutions.all().iterrows():
            if task_row['software'] not in list( df['name'] ):
                log.error( 'Software folder not named after any existing package',
                        Folder=os.path.join( config.tasks_folder,
                            task_row['task name'], task_row['software'] ),
                        Packages=', '.join( list( df['name'] ) ) )

# Prettify a portion of the full df for use on the software packages page
def table ():
    global pretty_df
    if pretty_df is None:
        pretty_df = all()[['name as link', 'icon markdown', 'num solutions', 'website markdown']]
        pretty_df.columns = [ 'Software Package', 'Icon', 'Number of solutions', 'Website' ]
    return pretty_df
