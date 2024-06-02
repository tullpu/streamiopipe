from streamiopipe import *
import sys
import io

@stringiopipe
def definitions(outstream,instream):
    for line in instream:
        if line.strip().startswith('def'):
            outstream.write(f"{line.strip().split('(')[0][4:]}\n")

with StreamIOPipe() as sp:
    sp.run(definitions)
