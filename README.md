# StreamIOPipe

A library that allows to process streams using simple user defined functions in a sequence as if you were using pipes.


# Installation

```bash
pip install streamoipipe
```


# Examples


1. Read text from a StringIO and add line numbers

```python
from streamiopipe import *
import sys
import io

@stringiopipe
def add_lineno(outstream,instream):
    """ prepend line with an auto increment
    """
    lineno = 1

    for line in instream:
        outstream.write(f"{lineno:02d}:{line}")
        lineno+=1


text_in = io.StringIO("""January
February
March
April""")

text_out = io.StringIO()
with StreamIOPipe(filein=text_in,fileout=text_out,text=True) as sp:
    sp.run(add_lineno)

print(text_out.getvalue())
```


2. Read text from a StringIO and add line numbers and then remove them

```python
from streamiopipe import *
import sys
import io

@stringiopipe
def add_lineno(outstream,instream):
    """ prepend line with an auto increment
    """
    lineno = 1

    for line in instream:
        outstream.write(f"{lineno:02d}:{line}")
        lineno+=1

@stringiopipe
def remove_lineno(outstream,instream):
    """ prepend line with an auto increment
    """

    for line in instream:
        outstream.write(line[3:])



text_in = io.StringIO("""January
February
March
April""")

text_out = io.StringIO()
with StreamIOPipe(filein=text_in,fileout=text_out,text=True) as sp:
    sp.iterate([(add_lineno,),(remove_lineno,)])

print(text_out.getvalue())
```


3. XOR a binary file from stdin and write to stdout

```python
from streamiopipe import *
import sys
import io
import struct

@byteiopipe
def xor(outstream,instream,value=0xFA):
    """ Iterate all bytes and xor them with value
    """
    for block in iter(lambda: instream.read(1), b''):
        byte = block[0]
        out = byte ^ value
        outstream.write(struct.pack("=B",out))

# read from stdin, xor and write to stdout
with StreamIOPipe(text=False) as sp:
    sp.run(xor,value=0xBC)

```

4. XOR and Rotate Left a file from stdin and write to stdout

```python
from streamiopipe import *
import sys
import io
import struct

@byteiopipe
def xor(outstream,instream,value=0xAA):
    """ Iterate all bytes and xor them with value
    """
    for block in iter(lambda: instream.read(1), b''):
        byte = block[0]
        out = byte ^ value
        outstream.write(struct.pack("=B",out))

@byteiopipe
def rol(outstream,instream,value=1):
    """ Iterate all bytes and rotate left by value
    """
    div,mod = divmod(value,8)
    rest = 8 - mod
    for block in iter(lambda: instream.read(1), b''):
        byte = block[0]
        out = 255 & (byte << mod | byte >> rest)
        outstream.write(struct.pack("=B",out))

# read from stdin, xor and write to stdout
with StreamIOPipe(text=False) as sp:
    sp.iterate([(xor,{'value':0xD0}), (rol,{'value':4})])

```

