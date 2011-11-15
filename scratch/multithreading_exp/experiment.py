import sys
import types
import traceback
import threading
import collections
import IPython.ipapi
import pyglet
from pyglet.gl import *

def call (function, args, kwargs, output=None):
    ''' WARNING: This can be only called from the OpenGL thread '''
    try:
        result = function(*args, **kwargs)
    except:
        traceback.print_exc()
        result = None
    if output:
        output(result) 
        

def post (function, args, kwargs, output):
    ''' Post a function call on the queue. '''
    _lock.acquire()
    _queue.append((function, args, kwargs, output))
    _lock.release() 
    
def __decorate_function_with_result(function):
    ''' Internal decorator for function that needs to get result '''
    class container(object):
        def __init__(self):
            self.value = None
            self.filled = False
        def __call__(self, value=None):
            self.value = value
            self.filled = True
    class proxy(object):
        def __call__(self, *args, **kwargs):
            output = container()
            post(function, args, kwargs, output)
            while not output.filled: pass
            return output.value
    return proxy() 

def __decorate_function_without_result(function):
    ''' Internal decorator for function that does not nedd to get result '''
    class proxy(object):
        def __call__(self, *args, **kwargs):
            post(function, args, kwargs, None)
    return proxy() 

def __decorate_class(klass):
    class proxy(object):
        ''' Internal decorator for class '''
        __protected__ = set(['__init__',
                             '__getattribute__',
                             '__setattr__',
                             '__proxy__'])
        def __init__(self, *args, **kwargs):
            object.__setattr__(self, '__proxy__', None)
            output = lambda result: object.__setattr__(self,'__proxy__', result)
            post(klass, args, kwargs, output)

        def __getattribute__(self, name):
            if name in proxy.__protected__:
                return object.__getattribute__(self, name)
            proxy_ref = self.__proxy__
            value = getattr(proxy_ref, name)
            if isinstance(value, types.MethodType):
                return proxy_function(value)
            else:
                return value
        def __setattr__(self, name, value):
            proxy_ref = self.__proxy__
            if hasattr(proxy_ref, name):
                call(setattr, (proxy_ref, name, value), {})
            else:
                object.__setattr__(self, name, value)
    return proxy 

def proxy(obj):
    ''' '''
    if type(obj) is bool:
        def wrap(function):
            if isinstance(function, types.FunctionType):
                if obj:
                    return __decorate_function_with_result(function)
                else:
                    return __decorate_function_without_result(function)
            elif isinstance(function,types.TypeType):
                return __decorate_class(function)
            else:
                raise NotImplementedError('Cannot make proxy for %s.'%str(obj))
        return wrap
    else:
        if isinstance(obj, types.FunctionType):
            return __decorate_function_without_result(obj)
        elif isinstance(obj,types.TypeType):
            return __decorate_class(obj)
        else:
            raise NotImplementedError('Cannot make proxy for %s.'%str (obj))
        
def process(dt):
    ''' '''
    if not len(_queue): return
    _lock.acquire()
    function, args, kwargs, output = _queue.popleft()
    call (function, args, kwargs, output)
    _lock.release() 
    
def session_start():
    ''' '''
    pyglet.clock.schedule_interval(process, 1/60.)
    namespace = globals().copy()
    for key in namespace.keys():
        if callable(namespace[key]) and key[:2] == 'gl':
            namespace[key] = __decorate_function_with_result(namespace[key])
    IPython.ipapi.launch_new_instance(namespace)
    pyglet.app.exit()

_lock  = threading.Lock()
_queue = collections.deque() 

#@proxy
#class Window(pyglet.window.Window):
#    def __init__(self, *args, **kwargs):
#        self.label = pyglet.text.Label('Hello, world',
#                                       font_name='Times New Roman',
#                                       font_size=36,
#                                       anchor_x='center',anchor_y='center')
#        
#        pyglet.window.Window.__init__(self,*args, **kwargs)
#        
#    def on_resize(self, width, height):
#        pyglet.window.Window.on_resize(self, width, height)
#        self.label.x = self.width//2
#        self.label.y = self.height//2
#        
#    def on_draw(self):
#        self.clear()
#        self.label.draw() 
        
#pyglet.app.run() 

#@proxy
#def clear(r,g,b,a):
#    glClearColor(r,g,b,a)
#
#@proxy(True)   # True means we want to get function result
#def viewport():
#    viewport = (GLint*4)()
#    glGetIntegerv(GL_VIEWPORT, viewport)
#    return viewport[0],viewport[1],viewport[2],viewport[3]
#
#@proxy
#def set_text(window, text):
#    window.label.text = text


import sys
import pyglet
from pyglet.gl import *

window = pyglet.window.Window(visible=False, resizable=True)

@window.event
def on_draw():
    background.blit_tiled(0, 0, 0, window.width, window.height)
    img.blit(window.width // 2, window.height // 2, 0)

filename = 'pyglet.png'

img = pyglet.image.load(filename).get_texture(rectangle=True)
img.anchor_x = img.width // 2
img.anchor_y = img.height // 2

checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
background = pyglet.image.TileableTexture.create_for_image(checks)

# Enable alpha blending, required for image.blit.
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window.width = img.width
window.height = img.height
window.set_visible()

session = threading.Thread(target=session_start)
session.start()

pyglet.app.run()

#while session.isAlive():
#    pyglet.app.run() 