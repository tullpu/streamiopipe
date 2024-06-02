from streamiopipe import *
import sys
import io
import struct

@byteiopipe
def xor(outstream,instream):
    """ Iterate all bytes and xor them with 0xFA
    """
    for block in iter(lambda: instream.read(1), b''):
        byte = block[0]
        out = byte ^ 0xFA
        outstream.write(struct.pack("=B",out))

# read from stdin, xor and write to stdout
with StreamIOPipe(text=False) as sp:
    sp.run(xor)

