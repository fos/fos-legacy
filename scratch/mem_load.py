from cStringIO import StringIO
from pyglet.media import avbin
av = avbin.av
from ctypes import *

class URLContext(Structure):
    _fields_ = [
        ("prot", c_void_p),
        ("flags", c_int),
        ("is_streamed", c_int),
        ("max_packet_size", c_int),
        ("priv_data", c_void_p),
        ("filename", c_char_p)
    ]

URL_OPEN = CFUNCTYPE(c_int, POINTER(URLContext), c_char_p, c_int)
URL_READ = CFUNCTYPE(c_int, POINTER(URLContext), c_void_p, c_int)
URL_WRITE = CFUNCTYPE(c_int, POINTER(URLContext), c_void_p, c_int)
URL_SEEK = CFUNCTYPE(c_int64, POINTER(URLContext), c_int64, c_int)
URL_CLOSE = CFUNCTYPE(c_int, POINTER(URLContext))
URL_READ_PAUSE = CFUNCTYPE(c_int, POINTER(URLContext), c_int)
URL_READ_SEEK =  CFUNCTYPE(c_int64, POINTER(URLContext), c_int, c_int64, c_int)
URL_GET_FILE_HANDLE = CFUNCTYPE(c_int, POINTER(URLContext))

class URLProtocol(Structure):
    pass

URLProtocol._fields_ = [
    ("name", c_char_p),
    ("url_open", URL_OPEN),
    ("url_read", URL_READ),
    ("url_write", URL_WRITE),
    ("url_seek", URL_SEEK),
    ("url_close", URL_CLOSE),
    ("next", POINTER(URLProtocol)),
    ("url_read_pause", URL_READ_PAUSE),
    ("url_read_seek", URL_READ_SEEK),
    ("url_get_file_handle", URL_GET_FILE_HANDLE),
]

class ProtocolPrivateData(Structure):
    _fields_ = [
        ('data', py_object)
    ]

memory_protocol = URLProtocol()
data = create_string_buffer('mem')
name = c_char_p(addressof(data))
memory_protocol.name = name

privates = []

current_file = None

def url_open(context, path, flags):
    private_data = ProtocolPrivateData()
    global current_file
    private_data.data = current_file
    current_file = None
    privates.append(private_data)
    context.contents.priv_data = cast(pointer(private_data), c_void_p)
    return 0

def url_read(context, buffer, size):
    io = ProtocolPrivateData.from_address(context.contents.priv_data).data
    read_data = io.read(size)
    memmove(buffer, read_data, len(read_data))
    return len(read_data)

def url_seek(context, pos, whence):
    io = ProtocolPrivateData.from_address(context.contents.priv_data).data
    if whence == 0x10000: # AVSEEK_SIZE:
        pos = io.tell()
        io.seek(0, 2)
        size = io.tell()
        io.seek(pos)
        return size
    io.seek(pos, whence)
    return io.tell()

def url_close(context):
    priv = ProtocolPrivateData.from_address(context.contents.priv_data)
    address = addressof(priv)
    for item in privates[:]:
        if addressof(item) == address:
            privates.remove(item)
            break
    return 0

memory_protocol.url_open = URL_OPEN(url_open)
memory_protocol.url_read = URL_READ(url_read)
memory_protocol.url_seek = URL_SEEK(url_seek)
memory_protocol.url_close = URL_CLOSE(url_close)

av.register_protocol(byref(memory_protocol))

class AVbinMemorySource(avbin.AVbinSource):
    def __init__(self, filename, file = None):
        if file is not None:
            filename = 'mem:'
            global current_file
            current_file = file
        return super(AVbinMemorySource, self).__init__(filename)

avbin.AVbinSource = AVbinMemorySource

if __name__ == '__main__':
    from pyglet.media import load
    foo = load(None, open("test.ogg", 'rb'), 
        streaming = True)
    foo.play()
    import pyglet
    pyglet.app.run()
