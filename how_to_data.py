
from build_tools import *
import files
import log
import static_files
import tasks
import topics
import solutions
import software
import config
import glob
import shell

# Build class; use instances of this to run builds
class Build:

    def __init__ ( self, **kwargs ):
        # Ensure relevant folders exist
        files.ensure_folder_exists( os.path.join( config.topics_folder, 'images' ) )
        files.ensure_folder_exists( config.jekyll_imgs_folder )
    
    # Summary stats for whole database
    def stats ():
        return pd.DataFrame( {
            'Content' : [
                '[Topics](topics)',
                '[Tasks](tasks)',
                '[Solutions](tasks)',
                '[Software packages](software)'
            ],
            'Quantity' : [
                len( topics.all() ),
                len( tasks.all() ),
                len( solutions.all() ),
                len( software.all() )
            ]
        } )

    # Contributors list for whole database
    def contributors ():
        result = [ ]
        for entry in solutions.all()['author']:
            if type(entry) == str:  # maybe it's a single-author solution
                result.append( entry )
            else:
                try:  # maybe it's a multi-author solution, so add each one
                    for author in entry:
                        result.append( author )
                except TypeError:  # probably author was NaN, so do nothing
                    pass
        result = pd.Series( result ).value_counts()
        return pd.DataFrame( {
            'Author' : result.index,
            'Solutions contributed' : result
        } )
    
    # Run a build of the database into the Jekyll input folder
    def database_to_jekyll ( self, force_rerun=False ):
        # Delete files generated in last build
        log.heading( 'Deleting old files from Jekyll input folder' )
        to_delete = ' '.join( [
            os.path.join( config.jekyll_imgs_folder, f'*{ext}' )
            for ext in files.img_extensions
        ] )
        log.file_delete( to_delete )
        shell.run_and_continue( f'rm {to_delete}' )

        # Copy files to Jekyll input folder
        log.heading( 'Copying files to Jekyll input folder' )
        replacements = {
            'SET_OF_SOFTWARE_PACKAGES': software.table().to_markdown( index=False ),
            'SET_OF_TASKS' : tasks.table_with_links().to_markdown( index=False ),
            'LIST_OF_TOPICS' : '\n'.join( [
                f' * {link}' for link in topics.all()['markdown link'] ] ),
            'OVERALL_STATS' : Build.stats().to_markdown( index=False ),
            'CONTRIBUTORS_LIST' : Build.contributors().to_markdown( index=False )
        }
        for filename in static_files.all()[static_files.all()['type'] == 'static page']['filename']:
            static_files.copy( filename, replacements )
        for index, row in static_files.all()[static_files.all()['type'] == 'task image'].iterrows():
            tasks.copy_image( row['full path'], row['filename'] )

        # Generate files from database
        log.heading( 'Generating files from database content' )
        # Note: solution building must go first so task pages can read the generated results
        for index, row in solutions.all().iterrows():
            build_solution_page( row, force_rerun, config_folder=config.main_folder )
        # Now task pages get built second, so they can read the generated solution pages
        for index, row in tasks.all().iterrows():
            build_task_page( row )
        # Create a page for each software package; the sequencing of this step is not important.
        for index, row in software.all().iterrows():
            build_software_page( row )
        # Create a page for each topic; the sequencing of this step is not important.
        for index, row in topics.all().iterrows():
            build_topic_page( row, config.main_folder )
        delete_ungenerated_markdown()

        # Zip up examples to reference from the Contributing page
        log.heading( 'Zipping examples for contributors' )
        infiles = glob.iglob( 'examples/*', recursive=True )
        outfile = 'jekyll-input/assets/downloads/examples-for-contributing-to-how-to-data.zip'
        if any( files.must_rebuild( infile, outfile ) for infile in infiles ):
            howto = 'examples/How to use this folder'
            shell.run_or_halt( f'pandoc --to=docx --output="{howto}.docx" "{howto}.md"' )
            files.ensure_folder_exists(
                os.path.join( jekyll_input_folder, 'assets', 'downloads' ) )
            shell.run_or_halt( f'cd examples && zip -orv9 "../{outfile}" *' )
        else:
            log.not_built( 'Examples for contributors', *infiles )

    # Run a build from the Jekyll input folder to the site, using Jekyll
    def jekyll_to_site ( self ):
        shell.run_or_halt( 'bundle exec jekyll build --incremental --profile' )
