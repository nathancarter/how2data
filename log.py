
import sys

# Function for printing section headings in the console output
def heading ( title ):
    print()
    print()
    print( title )
    print( '-' * len( title ) )

def right_justify ( text, width ):
    width = max( width, 25 )
    return ( ' ' * ( width - len( text ) ) ) + text

def out ( **kwargs ):
    width = max( len( key ) for key in kwargs )
    for key, value in kwargs.items():
        print( right_justify( key, width ) + ': ' + str( value ) )

def error ( message, **kwargs ):
    out( { **{ 'Build error' : message }, **kwargs } )
    sys.exit( 1 )

def warning ( message, **kwargs ):
    out( **{ **{ 'Build warning' : message }, **kwargs } )

def info ( message, **kwargs ):
    out( **{ **{ 'Build info' : message }, **kwargs } )

def file_copy ( source, dest, **kwargs ):
    out( **{ **{ 'Copied: Source' : source, 'Dest' : dest }, **kwargs } )

def file_delete ( filename, **kwargs ):
    out( **{ **{ 'Running rm on' : filename }, **kwargs } )

def file_missing ( source, **kwargs ):
    out( **{ f"Must rebuild because DNE": source, **kwargs } )

def built ( desc, target, *sources, **kwargs ):
    out( **{
        f"Built {desc}": target,
        **{ f"Newer than source {i+1}": sources[i] for i in range(len(sources)) },
        **kwargs
    } )
    print()

def not_built ( target, *sources, **kwargs ):
    out( **{
        "Not rebuilding target": target,
        **{ f"Newer than source {i+1}": sources[i] for i in range(len(sources)) },
        **kwargs
    } )
