import numpy as np

import fos.lib.pyglet as pyglet
#pyglet.options['debug_gl'] = True
#pyglet.options['debug_gl_trace'] = True
#pyglet.options['debug_gl_trace_args'] = True
#pyglet.options['debug_graphics_batch'] = True
#pyglet.options['shadow_window'] = False

#print pyglet.options

from fos.lib.pyglet.gl import *
import fos.lib.pyglet.window
from fos.lib.pyglet.window import key,mouse
from fos.lib.pyglet.clock import Clock, ClockDisplay
from fos.lib.pyglet.window import FPSDisplay


from fos import World

from fos.core.window.window_text  import WindowText
from fos.core import color
from fos.core.handlers.window import FosWinEventHandler

class SimpleWindow(fos.lib.pyglet.window.Window):

    def __init__(self, bgcolor=None, **kwargs):
        """ Create a FosWindow. All parameters are optional.

        Parameters
        ----------
        `bgcolor` : tuple
            Specify the background color as 4-tuple with values
            between 0 and 1
        `width` : int
            Width of the window, in pixels.  Defaults to 640, or the
            screen width if `fullscreen` is True.
        `height` : int
            Height of the window, in pixels.  Defaults to 480, or the
            screen height if `fullscreen` is True.
        `caption` : str or unicode
            Initial caption (title) of the window.  Defaults to
            ``sys.argv[0]``.
        `fullscreen` : bool
            If True, the window will cover the entire screen rather
            than floating.  Defaults to False.
        `visible` : bool
            Determines if the window is visible immediately after
            creation.  Defaults to True.  Set this to False if you
            would like to change attributes of the window before
            having it appear to the user.

        """
        super(SimpleWindow, self).__init__(**kwargs)
        
        self.update_dt = 1.0/60

        if bgcolor == None:
            self.bgcolor = color.black
        else:
            self.bgcolor = bgcolor

        self.mouse_x, self.mouse_y = 0,0

        # create an empty world by default
        emptyworld = World("Zero-Point World")
        self.attach(emptyworld)

        # the frame rate display from fos.lib.pyglet
        #self.fps_display = FPSDisplay(self)
        #self.foslabel = WindowText(self, 'fos', x=10 , y=40)
        self.show_logos = False

        # pushing new event handlers
        foswinhandlers = FosWinEventHandler(self)
        self.push_handlers(foswinhandlers)

        self.show_fps = True
        self.fps_display = ClockDisplay()


    def remove_logos(self):
        self.show_logos = False


    def setup(self):
        r,g,b,a = self.bgcolor
        glClearColor(r,g,b,a)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        #glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        return

    def set_current_camera(self, cam):
        """ Set the current camera to cam for this window

        Parameters
        ----------
        cam : Camera
            The camera object
        """

        if cam in self._world.cl.cameras:
            self.current_camera = cam
        else:
            print "camera not found in this world"

    def update(self, dt):
        # update the actors
        for a in self._world.ag.actors:
            try:
                a.update(dt)
            except:
                pass

        # update the cameras
        for c in self._world.cl.cameras:
            try:
                c.update(dt)
            except:
                pass

#        if dt != 0:
#            print "freq", round(1.0/dt)
#            pass

    def add_actor_to_world(self, actor):
        """ Add actor to the world of this window """
        self._world.add(actor)
            
    def get_world(self):
        """ Returns the world that is attached to this window """
        return self._world

    def attach(self, world):
        """ Attach a FosWindow to a world. The world needs
        to have at least one camera. The first camera is used
        for the window. You can change the camera for a window
        by using set_current_camera()

        """

        # can not attach a window to a world that has not cameras
        if len(world.get_cameras()) == 0:
            raise Exception("Can not attach window to a world with no cameras")

        # attach the world as a private attribute
        self._world = world

        # add the world to the list of windows the world is attached to
        self._world.wins.append(self)

        # just take the first camera
        self.current_camera = self._world.get_cameras()[0]

        
    def on_draw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.current_camera.draw()

        for a in self._world.ag.actors:
            try:
                a.draw()
            except:
                pass

        if self.show_fps:
            glLoadIdentity()
            glTranslatef(200, 280, -800)
            self.fps_display.draw()
            
        if self.show_logos:
            self.foslabel.draw()

