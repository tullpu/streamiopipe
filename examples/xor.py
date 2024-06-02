from streamiopipe import *
import sys
import io
import struct

@byteiopipe
def xor(outstream,instream):
    for block in iter(lambda: instream.read(1), b''):
        byte = block[0]
        out = byte ^ 0xFA
        outstream.write(struct.pack("=B",out))

with StreamIOPipe(text=False) as sp:
    sp.run(xor)

