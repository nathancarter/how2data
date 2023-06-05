
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
import os
import pandas as pd
import progress

# Ensure relevant folders exist
files.ensure_folder_exists( os.path.join( config.topics_folder, 'images' ) )
files.ensure_folder_exists( config.jekyll_imgs_folder )

# Clear all caches
def clear_caches ():
    topics.clear_cache()
    solutions.clear_cache()
    tasks.clear_cache()

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
def database_to_jekyll ( force_rerun=False, quiet=False, callback=None ):
    # Respect quiet flag--use progress bar instead
    if quiet:
        log.disable()
        pbar = progress.ProgressBar( 'How to Data build process:' )
        if callback is not None:
            pbar.callback = callback
        pbar.start()

    # Delete files generated in last build
    if quiet:
        pbar.set_phase( 0, 7 )
        pbar.set_step( 0, 1 )
    log.heading( 'Deleting old files from Jekyll input folder' )
    to_delete = ' '.join( [
        os.path.join( config.jekyll_imgs_folder, f'*{ext}' )
        for ext in files.img_extensions
    ] )
    log.file_delete( to_delete )
    shell.run_and_continue( f'rm {to_delete}' )

    # Copy files to Jekyll input folder
    if quiet:
        pbar.set_phase( 1, 7 )
        pbar.set_step( 0, 2 )
    log.heading( 'Copying files to Jekyll input folder' )
    replacements = {
        'SET_OF_SOFTWARE_PACKAGES': software.table().to_markdown( index=False ),
        'SET_OF_TASKS' : tasks.table_with_links().to_markdown( index=False ),
        'LIST_OF_TOPICS' : '\n'.join( [
            f' * {link}' for link in topics.all()['markdown link'] ] ),
        'OVERALL_STATS' : stats().to_markdown( index=False ),
        'CONTRIBUTORS_LIST' : contributors().to_markdown( index=False )
    }
    for filename in static_files.all()[static_files.all()['type'] == 'static page']['filename']:
        static_files.copy( filename, replacements )
    if quiet:
        pbar.set_step( 1, 2 )
    for index, row in static_files.all()[static_files.all()['type'] == 'task image'].iterrows():
        tasks.copy_image( row['full path'], row['filename'] )

    # Generate files from database
    log.heading( 'Generating files from database content' )
    # Note: solution building must go first so task pages can read the generated results
    if quiet:
        pbar.set_phase( 2, 7 )
        pbar.set_step( 0, len( solutions.all() ) )
    for index, row in solutions.all().iterrows():
        solutions.Solution( row ).build( force=force_rerun )
        if quiet:
            pbar.step()
    # Now task pages get built second, so they can read the generated solution pages
    if quiet:
        pbar.set_phase( 3, 7 )
        pbar.set_step( 0, len( tasks.all() ) )
    for index, row in tasks.all().iterrows():
        tasks.Task( row ).build()
        if quiet:
            pbar.step()
    # Create a page for each software package; the sequencing of this step is not important.
    if quiet:
        pbar.set_phase( 4, 7 )
        pbar.set_step( 0, len( software.all() ) )
    for index, row in software.all().iterrows():
        software.Software( row ).build()
        if quiet:
            pbar.step()
    # Create a page for each topic; the sequencing of this step is not important.
    if quiet:
        pbar.set_phase( 5, 7 )
        pbar.set_step( 0, len( topics.all() ) )
    for index, row in topics.all().iterrows():
        topics.Topic( row ).build()
        if quiet:
            pbar.step()
    files.delete_ungenerated_markdown()

    # Zip up examples to reference from the Contributing page
    if quiet:
        pbar.set_phase( 6, 7 )
        pbar.set_step( 0, 1 )
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

    if quiet:
        pbar.end()
        print( 'Jekyll build process:' )

# Run a build from the Jekyll input folder to the site, using Jekyll
def jekyll_to_site ():
    shell.run_or_halt( 'bundle exec jekyll build --incremental', show_output=True )
