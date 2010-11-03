import numpy as np

from fos.lib.pyglet.gl import *
from fos.core.managed_window import ManagedWindow
from fos.lib import pyglet
from fos.lib.pyglet.window import key,mouse
from fos.lib.pyglet.clock import Clock
from fos.lib.pyglet.window import FPSDisplay
from fos.core import color

class FosWindow(ManagedWindow):
    
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
        
        self.update_dt = 1.0/60
        
        super(FosWindow, self).__init__(**kwargs)
        
        if bgcolor==None:
            self.bgcolor=color.black
        else:
            self.bgcolor=bgcolor        
        
        self.mouse_x, self.mouse_y = 0,0
        
        # the world that is attached to this window
        self._world = None
        
        # the frame rate display from pyglet
        self.fps_display = FPSDisplay(self)
        
        
    def setup(self):           
                
        r,g,b,a = self.bgcolor
        glClearColor(r,g,b,a)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
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

    
    def attach(self, world):
        """ Attach a FosWindow to a world. The world needs
        to have at least one camera. The first camera is used
        for the window. You can change the camera for a window
        by using set_current_camera()
        
        """
        world._render_lock.acquire()
#        # can not attach a window to a world that has not cameras
        if len(world.get_cameras()) == 0:
            raise Exception("Can not attach window to a world with no cameras")
        
        self._world = world
        
        # just take the first camera
        self.current_camera = self._world.get_cameras()[0]
        world._render_lock.release()
            
    def draw(self):   
        self._world._render_lock.acquire()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
        glLoadIdentity()
    
        self.current_camera.draw()
    
        for a in self._world.ag.actors:
            try:
                a.draw()
            except:
                pass
        
        self.fps_display.draw()
        
        self._world._render_lock.release()
    
              
    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 2000.)
        glMatrixMode(GL_MODELVIEW)
        
        return pyglet.event.EVENT_HANDLED


    def on_key_press(self, symbol,modifiers):

        # how to propagate the events to the actors and camera?
            
        if symbol == key.R:
            self.current_camera.cam_rot.reset()
            self.current_camera.cam_trans.reset()
        
        if symbol == key.H:
            self.set_size(900, 600)
        if modifiers & key.MOD_CTRL:
            if symbol == key.PLUS:
                neww = self.width + self.width / 10
                newh = self.height + self.height / 10
                self.set_size(neww, newh)
            elif symbol == key.MINUS:
                neww = self.width - self.width / 10
                newh = self.height - self.height / 10
                self.set_size(neww, newh)
                 
        if symbol == key.P:          
                  
            x,y=self.mouse_x,self.mouse_y
            nx,ny,nz=screen_to_model(x,y,0)
            fx,fy,fz=screen_to_model(x,y,1)        
            near=(nx,ny,nz)
            far=(fx,fy,fz)
            for a in actors:
                try:
                    a.process_pickray(near,far)
                except:
                    pass
            

    def on_mouse_motion(self, x,y,dx,dy):
        self.mouse_x, self.mouse_y=x,y
        
    def on_mouse_drag(self, x,y,dx,dy,buttons,modifiers):
        if buttons & mouse.LEFT:
            if modifiers & key.MOD_CTRL:
                print('ctrl dragging')
            else:
                self.current_camera.cam_rot.rotate( dx*self.current_camera.mouse_speed,0,1,0)
                self.current_camera.cam_rot.rotate(-dy*self.current_camera.mouse_speed,1,0,0)
                
        if buttons & mouse.RIGHT:
            tx=dx*self.current_camera.mouse_speed
            ty=dy*self.current_camera.mouse_speed        
            self.current_camera.cam_trans.translate(tx,ty,0)
    
        if buttons & mouse.MIDDLE:
            tz=dy*self.current_camera.mouse_speed
            self.current_camera.cam_trans.translate(0,0,tz)
    
    def on_mouse_scroll(self, x,y,scroll_x,scroll_y):
        self.current_camera.cam_trans.translate(0,0,scroll_y*self.current_camera.scroll_speed)

    def on_close(self):
        """
        Closes the Fos window.
        """
        self.has_exit = True
        self.close()

    