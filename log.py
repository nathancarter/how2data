
import sys

enabled = True
def enable ():
    global enabled
    enabled = True
def disable ():
    global enabled
    enabled = False

# Function for printing section headings in the console output
def heading ( title ):
    if not enabled:
        return
    print()
    print()
    print( title )
    print( '-' * len( title ) )

# Pad text on the left to right-justify it
def right_justify ( text, width ):
    width = max( width, 25 )
    return ( ' ' * ( width - len( text ) ) ) + text

# Print a table of key-value pairs in helpful output format
def out ( **kwargs ):
    if not enabled:
        return
    width = max( len( key ) for key in kwargs )
    for key, value in kwargs.items():
        print( right_justify( key, width ) + ': ' + str( value ) )
    print()

# Print a table of error info and quit the build process
def error ( message, **kwargs ):
    out( { **{ 'Build error' : message }, **kwargs } )
    sys.exit( 1 )

# Print a table of warning info but do not quit the build process
def warning ( message, **kwargs ):
    out( **{ **{ 'Build warning' : message }, **kwargs } )

# Print a table of any kind of info
def info ( message, **kwargs ):
    out( **{ **{ 'Build info' : message }, **kwargs } )

# Print info about copying a file
def file_copy ( source, dest, **kwargs ):
    out( **{ **{ 'Copied: Source' : source, 'Dest' : dest }, **kwargs } )

# Print info about deleting a file
def file_delete ( filename, **kwargs ):
    out( **{ **{ 'Running rm on' : filename }, **kwargs } )

# Print info about a missing file that will cause us to rebuild it
def file_missing ( source, **kwargs ):
    out( **{ f"Must rebuild because DNE": source, **kwargs } )

# Print info about building a file from sources
def built ( desc, target, *sources, **kwargs ):
    out( **{
        f"Built {desc}": target,
        **{ f"Newer than source {i+1}": sources[i] for i in range(len(sources)) },
        **kwargs
    } )
    print()

# Print info about not building a file when that's not needed
def not_built ( target, *sources, **kwargs ):
    out( **{
        "Not rebuilding target": target,
        **{ f"Newer than source {i+1}": sources[i] for i in range(len(sources)) },
        **kwargs
    } )
