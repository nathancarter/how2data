
import config
import os
import re
import json
import files
import log
import shell

# Jekyll messes with single-dollar-sign LaTeX expressions,
# unescaping every backslash within them (by one level),
# but it leaves double-dollar-sign ones alone.
# So we do the following, to escape every backslash
# EXCEPT those that are inside double-dollar-sign LaTeX expressions:
def has_double_dollar_section ( text ):
    return re.match( '\\s*\\$\\$.*\\$\\$\\s*', text )
def has_single_dollar_section ( text ):
    return re.match( '\\s*\\$.*\\$\\s*', text )
def escape_for_jekyll ( markdown ):
    def fix_line ( line ):
        if has_single_dollar_section( line ) and not has_double_dollar_section( line ):
            return line.replace( '\\', '\\\\' )
        else:
            return line
    return '\n'.join( fix_line( line ) for line in markdown.split( '\n' ) )

# Inverse of previous function
def unescape_for_jekyll ( markdown ):
    def fix_line ( line ):
        if has_single_dollar_section( line ) and not has_double_dollar_section( line ):
            return line.replace( '\\\\', '\\' )
        else:
            return line
    return '\n'.join( fix_line( line ) for line in markdown.split( '\n' ) )

# When writing Markdown, be aware that Jekyll messes with LaTex; see below.
def write ( file, markdown, add_escapes=True ):
    if add_escapes:
        markdown = escape_for_jekyll( markdown )
    files.write_text_file( file, markdown )

# Crucial function:  This finds the unique file with the given filename and
# path, but with any extension from files.doc_extensions, and reads it in,
# converting to markdown if necessary.  If there is no such file, or are
# multiple such files, it quits with an error.
def get_unique_doc ( path_and_base_filename ):
    which_exist = [ extension for extension in files.doc_extensions \
        if os.path.exists( path_and_base_filename + extension ) and \
        os.path.isfile( path_and_base_filename + extension ) ]
    if len( which_exist ) == 0:
        log.error( "No document file found", **{
            "Base of filename" : path_and_base_filename,
            "Possible extensions" : ' '.join( files.doc_extensions )
        } )
    if len( which_exist ) > 1:
        log.error( "Multiple documents found (must be unique)", **{
            "Base of filename" : path_and_base_filename,
            **{ f"Result {i+1}": which_exist[i] for i in range(len(which_exist)) }
        } )
    return path_and_base_filename + which_exist[0]

# Function that converts an .ipynb file into markdown text.
# If that .ipynb file has markdown links to images stored as cell attachments,
# they are converted into data URIs.
def ipynb_to_markdown ( filename ):
    with open( filename, 'r' ) as f:
        cells = json.load( f )['cells']
    attached_src_attr = \
        re.compile( 'src="attachment:([^"]*)"|src=\'attachment:([^\']*)\'' )
    result = ''
    for cell in cells:
        if cell['cell_type'] == 'markdown':
            new_chunk = '\n' + ''.join( cell['source'] ) + '\n'
            match = attached_src_attr.search( new_chunk )
            while match:
                before = new_chunk[:match.start()]
                after = new_chunk[match.end():]
                src = match.group( 1 ) if match.group( 1 ) else match.group( 2 )
                attachment = cell['attachments'][src]
                mime_type = list( attachment.keys() )[0]
                base_64_data = attachment[mime_type]
                new_attr = f'src="data:{mime_type};base64, {base_64_data}"'
                new_chunk = before + new_attr + after
                match = attached_src_attr.search( new_chunk )
            result += new_chunk
        elif cell['cell_type'] == 'code':
            result += '\n```python\n' + ''.join( cell['source'] ) + '\n```\n'
        else:
            log.error( 'Unknown cell type', Type=cell['cell_type'], Filename=filenme )
    while result[0] == '\n':
        result = result[1:]
    return result

# To pair with get_unique_doc:  Read any document whose extension is in
# files.doc_extensions into markdown text.  It can support markdown (no conversion
# needed) or RMarkdown (tiny conversion needed) or Jupyter notebooks (more
# conversion needed).
def read_doc ( filename ):
    extension = files.extension( filename )
    if extension in [ '.md', '.markdown' ]:
        return files.read_text_file( filename )
    if extension in [ '.Rmd' ]:
        return files.read_text_file( filename ).replace( '```{r}', '```R' )
    if extension in [ '.ipynb' ]:
        return ipynb_to_markdown( filename )
    if extension in [ '.doc', '.docx' ]:
        tmp_file = os.path.join( *os.path.split( filename )[:-1], 'temp.ipynb' )
        shell.run_or_halt( f'pandoc -o "{tmp_file}" "{filename}"' )
        result = ipynb_to_markdown( tmp_file )
        shell.run_or_halt( f'rm "{tmp_file}"' )
        return result
    log.error( 'Unknown document type', Type=extension, File=filename )

# How to place some special content in an HTML or markdown file and
# indicate that it's special by wrapping it in comment flags, so that you
# can extract it again later.  This assumes only one such special block per file.
start_comment = '<!-- beginning of wrapper -->'
end_comment   = '<!-- ending of wrapper -->'
def wrap_in_html_comments ( text ):
    return f'{start_comment}\n\n{text}\n\n{end_comment}\n'
def unwrap_from_html_comments ( text ):
    begin = text.index( start_comment )
    end = text.index( end_comment )
    return text[begin+len(start_comment):end]

# Convert all HTML-style tables/etc. within markdown text to LaTeX instead
# Parameter 1 is a string containing markdown.
# Parameter 2 is the name of a folder in which to store temp files during the work.
def html_sections_to_latex ( markdown, folder ):
    # are there any sections to process?  if not, just return the input
    section = re.search( '\n<div(?:.|\n)*?<\\/div.*\n', markdown )
    if section is None:
        return markdown
    # there is a section to process; use pandoc on a temporary HTML file
    tmp_html_file = os.path.join( folder, 'tmp.html' )
    tmp_tex_file = os.path.join( folder, 'tmp.tex' )
    files.write_text_file( tmp_html_file, section.group(0) )
    shell.run_or_halt(
        f'pandoc --from=html --to=latex --output="{tmp_tex_file}" "{tmp_html_file}"',
        f'rm "{tmp_html_file}"' )
    section_as_tex = files.read_text_file( tmp_tex_file )
    shell.run_or_halt( f'rm "{tmp_tex_file}"' )
    # replace the section with its TeX-ified version
    markdown = markdown[:section.start()] + section_as_tex + markdown[section.end():]
    # recur on the new markdown, with one less section to process
    return html_sections_to_latex( markdown, folder )

# Function to run a given markdown document as if it were a Jupyter notebook.
# You specify the markdown content as a string, the folder in which to run it
# (using a temp file that will be deleted aftewards), and the name of the
# software package.  If that software package has a kernel, according to the
# kernel_for_software dictionary defined below, we will run it using that
# kernel; otherwise this function will behave as the identity function.
# It returns another string of markdown content, this time with execution
# outputs included (iff there is a relevant kernel).
kernel_for_software = {
    'Python' : 'python3',
    'Julia'  : 'julia-1.8',
    'R'      : 'ir'
}
def run ( markdown, folder, software ):
    if software in kernel_for_software:
        kernel = kernel_for_software[software]
    else:
        return markdown
    tmp_md_doc = os.path.join( folder, 'jupyter-temp-file.md' )
    ipynb_out = tmp_md_doc[:-3] + '.ipynb'
    # write markdown to temp file
    files.write_text_file( tmp_md_doc, markdown )
    # run it, creating a notebook containing the outputs
    shell.run_or_halt( 'jupytext --to ipynb ' + \
        f'--set-kernel {kernel} --output="{ipynb_out}" "{tmp_md_doc}"',
        f'rm "{tmp_md_doc}"' )
    # convert that to markdown again
    config_param = ''
    jupyter_config_file = os.path.join( config.main_folder,
        f'jupyter_nbconvert_config_{software}.py' )
    command_to_run = 'jupyter nbconvert --to=markdown --execute ' + \
        f"--JupyterApp.config_file='{jupyter_config_file}' " + \
        f'--output="{tmp_md_doc}" "{ipynb_out}"'
    shell.run_or_halt( command_to_run, f'rm "{ipynb_out}"' )
    # read it back into a string
    result = files.read_text_file( tmp_md_doc )
    shell.run_or_halt( f'rm "{tmp_md_doc}"' )
    # workaround for buggy way that SVGs get embedded in markdown:
    result = result \
        .replace( '![svg](data:image/svg;base64,<?xml version="1.0" encoding="utf-8"?>', '' ) \
        .replace( '![svg](data:image/svg;base64,<?xml version="1.0" encoding="UTF-8"?>', '' ) \
        .replace( '</svg>\n)', '</svg>\n' )
    return result

# When processing a markdown file, we may want to manipulate its image
# links.  The following function maps any given function over the set
# of image links in a string containing markdown, producing a new string.
# The function passed as input should take as input three parameters:
# img_code = the full image code, such as "![alt-text here](filename.png)"
# alt_text = just the alt text, what's in between the brackets above
# filename = just the filename, what's in between parentheses above
# It should return either a new image tag as a string OR an alt-text/filename
# pair as a tuple, which will be formed into an image tag.
def map_over_images ( func, markdown ):
    result = ''
    while True:
        match = re.search( '!\\[([^]]*)\\]\\(([^)]*)\\)', markdown )
        if match is None:
            break
        start, end = match.span()
        changed = func( match.group( 0 ), match.group( 1 ), match.group( 2 ) )
        if type( changed ) == tuple:
            changed = f'![{changed[0]}]({changed[1]})'
        result += markdown[:start] + changed
        markdown = markdown[end:]
    return result + markdown

# More useful special case of previous function
def adjust_image_filenames ( func, markdown ):
    return map_over_images(
        lambda code, alt_text, filename: ( alt_text, func( filename ) ),
        markdown
    )

# Replace each code block in a given markdown string
# with that code block's image under a given transformation function.
def transform_code ( markdown, transform ):
    result = ''
    block_content = None
    for line in markdown.split( '\n' ):
        if block_content is None: # outside a block
            if line.startswith( '```' ): # new block starts here!
                block_content = line + '\n'
            else:
                result += line + '\n'
        else: # inside a block
            block_content += line + '\n'
            if line.startswith( '```' ): # old block ends here
                result += transform( block_content )
                block_content = None
    if block_content is not None:
        raise Error( 'Ended markdown inside a code block' )
    return result

# Several private methods used only in the to_ipynb() function, below.
#
# Convert a markdown string into a JSON fragment for use in an ipynb file.
def _quote_each_line ( text, indent=0 ):
    return ',\n'.join( [
        ( ' ' * indent ) + json.dumps( line+'\n' )
        for line in text.split( '\n' )
    ] )
# Convert a markdown string into the JSON for a full Jupyter notebook
# markdown cell.
def _md_cell ( markdown ):
    return f'''  {{
   "source": [
{_quote_each_line( markdown )}
   ],
   "cell_type": "markdown",
   "metadata": {{}}
  }}'''
# Convert a string containing code (in any language) into a Jupyter notebook
# code cell.
def _code_cell ( code ):
    return f'''  {{
   "cell_type": "code",
   "execution_count": 0,
   "metadata": {{}},
   "outputs": [],
   "source": [
{_quote_each_line( code )}
   ]
  }}'''
# Convert an array of cells (each of which is already in JSON format)
# into the JSON content representing an entire Jupyter notebook, as a string.
# This requires creating some temp files, so that pandoc can create a tiny
# Jupyter notebook for us, into which we can substitute our list of cells.
def _cells_to_nb ( cells, tmp_folder=config.main_folder ):
    tmp_file = os.path.join( tmp_folder, '_temp_file' )
    files.write_text_file( tmp_file+'.md', 'Dummy text' )
    shell.run_or_halt(
        f'pandoc "{tmp_file}.md" --output="{tmp_file}.ipynb"',
        f'rm "{tmp_file}.md"' )
    template = json.loads( files.read_text_file( tmp_file+'.ipynb' ) )
    shell.run_or_halt( f'rm "{tmp_file}.ipynb"' )
    flag = "REPLACE_THIS_WITH_ACTUAL_CELLS"
    template["cells"] = [ flag ]
    return json.dumps( template ).replace( '"'+flag+'"', ',\n'.join( cells ) )

# Convert the given markdown content, in string form, into a Jupyter notebook,
# where code blocks become code cells and all other content becomes markdown
# cells.
def to_ipynb ( markdown ):
    cells = [ ]
    md = ''
    code = None
    for line in markdown.split( '\n' ):
        if code is None: # outside a block
            if line.startswith( '```' ): # new block starts here!
                cells.append( _md_cell( md ) )
                md = None
                code = ''
            else: # extend existing markdown section
                md += line + '\n'
                if line.startswith( '-----' ): # start a new cell
                    cells.append( _md_cell( md ) )
                    md = ''
        else: # inside a block
            if line.startswith( '```' ): # old block ends here
                cells.append( _code_cell( code ) )
                md = ''
                code = None
            else: # extend existing code section
                code += line + '\n'
    if code is not None:
        raise Error( 'Ended markdown inside a code block' )
    else:
        cells.append( _md_cell( md ) )
    return _cells_to_nb( cells )

# Export some markdown text in a chosen file format, using a temp file and
# pandoc as needed.  The filename should omit the extension, which will be
# decided based on the format.  For example, you could call:
# export('...','/path/to/my_file','Rmd') or
# export('...','/path/to/my_file','RMarkdown')
# and get the same result in either case, normalized to an .Rmd file.
# The filename, however, should be absolute, just without an extension.
def export ( markdown, filename, format ):
    out_folder = os.path.dirname( filename )
    log.info( 'Ensuring folder exists', Folder=out_folder )
    files.ensure_folder_exists( out_folder )
    if format not in config.extension_for_type:
        log.error( 'Markdown export not supported for this format',
                   Format=format )
    format = config.extension_for_type[format]
    out_file = filename + '.' + format
    match format:
        case 'md':
            log.info( 'Exporting file', Filename=out_file )
            files.write_text_file( out_file, markdown )
        case 'ipynb':
            log.info( 'Exporting file', Filename=f"{filename}.ipynb" )
            files.write_text_file( out_file, to_ipynb( markdown ) )
        case 'doc' | 'docx':
            log.info( 'Exporting file', Filename=out_file )
            files.write_text_file( f'{filename}.md', markdown )
            log.info( 'Converting file', **{ "New format" : f'{filename}.md' } )
            shell.run_or_halt(
                f'pandoc "{filename}.md" --output="{out_file}"',
                f'rm "{filename}.md"' )
        case 'Rmd':
            log.info( 'Exporting file', Filename=f"{out_file}" )
            files.write_text_file( out_file,
                markdown.replace( '\n```R', '\n```{r}' ) )
    log.info( 'Done.' )
    return filename + '.' + format
