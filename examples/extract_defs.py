from streamiopipe import *
import sys
import io

@stringiopipe
def definitions(outstream,instream):
    """ extract and print all the function names
    """
    for line in instream:
        if line.strip().startswith('def'):
            outstream.write(f"{line.strip().split('(')[0][4:]}\n")

# read from stdin and write to stdout
with StreamIOPipe() as sp:
    sp.run(definitions)
