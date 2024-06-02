import io 
import sys

def byteiopipe(func):
    def wrapper(instream,**kwargs):
        outstream = io.BytesIO()
        func(outstream,instream,**kwargs)
        outstream.seek(0)
        return outstream
    return wrapper

def stringiopipe(func):
    def wrapper(instream,**kwargs):
        outstream = io.StringIO()
        func(outstream,instream,**kwargs)
        outstream.seek(0)
        return outstream
    return wrapper

class StreamIOPipe(object):
    def __init__(self,filein=None,fileout=None,text=True):
        self.fileout = fileout
        self.text = text 
        self.data = self.from_stream(filein)

        if text:
            self.r = 'rt'
            self.w = 'wt'
        else:
            self.r = 'rb'
            self.w = 'wb'

    def from_stream(self,filename=None):
        if filename:
            with open(filename,self.r) as fp:
                if self.text:
                    return io.StringIO(fp.read())
                else:
                    return io.BytesIO(fp.read())
        else:
            if self.text:
                return io.StringIO(sys.stdin.read())
            else:
                return io.BytesIO(sys.stdin.buffer.read())

    def to_stream(self,streamin,filename=None):
        if filename:
            with open(filename,self.w) as fp:
                fp.write(streamin.getvalue())
        else:
            if self.text:
                sys.stdout.buffer.write(streamin.getvalue().encode('utf-8'))
            else:
                sys.stdout.buffer.write(streamin.getvalue())

    
    def __enter__(self):
        return self

    def run(self,func,**kwargs):
        self.data = func(self.data,**kwargs);

    def iterate(self,funcs):
        for p in funcs:
            (cmd,args) = (*p,{})
            self.run(cmd,**args)

    def __exit__(self, exc_type, exc_val, traceback):
        self.to_stream(self.data,self.fileout)

