import io
import sys


def byteiopipe(func):
    """ decorator for procesing byte stream
    """
    
    def wrapper(instream, **kwargs):
        """ creates a stream for output calls the function and resets the stream
        
        :param instream: the input stream
        :type  instream: BytesIO
        
        :param **kwargs: optional arguments to pass extra info
        :type  **kwargs: dict

        """
        
        outstream = io.BytesIO()
        func(outstream, instream, **kwargs)
        outstream.seek(0)
        return outstream
    return wrapper


def stringiopipe(func):
    """ decorator for processing text stream
    """
    
    def wrapper(instream, **kwargs):
        """ creates a stream for output calls the function and resets the stream
        
        :param instream: the input stream
        :type  instream: StringIO
        
        :param **kwargs: optional arguments to pass extra info
        :type  **kwargs: dict

        """
        
        outstream = io.StringIO()
        func(outstream, instream, **kwargs)
        outstream.seek(0)
        return outstream
    return wrapper


class StreamIOPipe(object):
    def __init__(self, filein=None, fileout=None, text=True):
        """ [Summary]
        
        :param filein: the filname in, defaults to None/stdin
        :type  filein: StringIO/BytesIO, optional 
        
        :param fileout: the filename out, defaults to None/stdout
        :type  fileout: StringIO/BytesIO, optional 
        
        :param text: wheather it is text of binary stream, defaults to True
        :type  text: boolean, optional 
        
        """
        
        self.fileout = fileout
        self.text = text
        self.data = self.from_stream(filein)


        # set file flags for text or binary
        if text:
            self.r = 'rt'
            self.w = 'wt'
        else:
            self.r = 'rb'
            self.w = 'wb'

    def from_stream(self, filename=None):
        """  read the data from filename/stdin and create a stream
        
        :param filename: the filename in, defaults to None
        :type  filename: str, optional 
        
        """
        

        # check if file or stdin
        if filename:
            # if string it is a filename
            if type(filename) == str:
                with open(filename, self.r) as fp:

                    if self.text:
                        return io.StringIO(fp.read())
                    else:
                        return io.BytesIO(fp.read())
            elif isinstance(filename,io.StringIO) or isinstance(filename,io.BytesIO):
                return filename
            else:
                raise TypeError("Unepected Object passed as file/stream")
        else:

            if self.text:
                return io.StringIO(sys.stdin.read())
            else:
                return io.BytesIO(sys.stdin.buffer.read())

    def to_stream(self, streamin, filename=None):
        """ Write data to file
        
        :param streamin: the stream to save
        :type  streamin: StringOI/BytesIO
        
        :param filename: the filename to write to, defaults to None
        :type  filename: str, optional 
        
        """
        
        output = streamin.getvalue()
        if self.text and isinstance(output,bytes):
            output = output.encode('utf-8')

        # if it is a filename then write to file
        if filename:
            if type(filename) == str:
                with open(filename, self.w) as fp:
                    fp.write(output)
            elif isinstance(filename,io.StringIO) or isinstance(filename,io.BytesIO):
                filename.write(output)
            else:
                raise TypeError("Unepected Object passed as file/stream")
        else: # else write to stdin
            if self.text:
                sys.stdout.write(output)
            else:
                sys.stdout.buffer.write(output)

    def __enter__(self):
        """ Context manager. Automatically opens input 
        """
        
        return self

    def run(self, func, **kwargs):
        """ Context manager, write and close the file
        
        :param func: the function to run
        :type  func: function
        
        :param **kwargs: extra arguments
        :type  **kwargs: dict
        
        """
        
        self.data = func(self.data, **kwargs)


    def iterate(self, funcs):
        """ execute the functions sequentially
        
        :param funcs: list of functions to be run sequentially
        :type  funcs: list
        
        """
        

        # iterate and execute functions
        for p in funcs:
            data = (*p,{})
            self.run(data[0],**data[1])
        


    def __exit__(self, exc_type, exc_val, traceback):
        """ Context manager, write and close the file
        
        :param exc_type: exception type
        
        :param exc_val: exception value
        
        :param traceback: traceback
        
        """
        
        self.to_stream(self.data, self.fileout)
