from fos.lib.pyglet.gl import *
from fos.core.managed_window import ManagedWindow
from fos.lib import pyglet
from fos.lib.pyglet.window import key,mouse

from threading import RLock
import numpy as np

        
class FosWindow(ManagedWindow):
    
    def __init__(self, **kwargs):
        super(FosWindow, self).__init__(**kwargs)
        
        self.mouse_x, self.mouse_y = 0,0
        self._render_lock = RLock()

        # the world that is attached to this window
        self._world = None
        
        # we have an update label
        self.uplabel = pyglet.text.Label('0.0', font_size=10,
                                         x=self.width//2, y=self.height//2, 
                                         anchor_x='center', anchor_y='center')
        
    def setup(self):
        
        #glClearColor(1.0, 0.0, 0.0, 0.0)
        #glClearDepth(1.0)
#
#        glDepthFunc(GL_LESS)
#        glEnable(GL_DEPTH_TEST)

        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE#_MINUS_SRC_ALPHA)
        pass
    
    def update(self, dt):
        if dt != 0:
            self.uplabel.text = str(round(1.0/dt))    
        
    
    def attach(self, world):
        self._world = world
            
    def draw(self):   
        self._render_lock.acquire()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
        glLoadIdentity()
    
        self._world.cg.cameras[0].draw()
    
        # draw label
        self.uplabel.draw()
    
        for a in self._world.ag.actors:
            try:
                a.draw()
            except:
                pass
            
        self._render_lock.release()
    
              
    def on_resize(self, width, height):
        print "test", width, height
        '''
        if self._needs_resize:
            self.set_size(width, height)
            self._needs_resize = False
        '''
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 2000.)
        glMatrixMode(GL_MODELVIEW)
        
        return pyglet.event.EVENT_HANDLED


    def on_key_press(self, symbol,modifiers):

        # how to propagate the events to the actors and camera?
            
        if symbol == key.R:
            self._world.cg.cameras[0].cam_rot.reset()
            self._world.cg.cameras[0].cam_trans.reset()
        
        if symbol == key.H:
            self.set_size(900, 600)
            
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
                #print('left dragging...')
                self._world.cg.cameras[0].cam_rot.rotate( dx*self._world.cg.cameras[0].mouse_speed,0,1,0)
                self._world.cg.cameras[0].cam_rot.rotate(-dy*self._world.cg.cameras[0].mouse_speed,1,0,0)
                
        if buttons & mouse.RIGHT:
            #print('right dragging')
            tx=dx*self._world.cg.cameras[0].mouse_speed
            ty=dy*self._world.cg.cameras[0].mouse_speed        
            self._world.cg.cameras[0].cam_trans.translate(tx,ty,0)
    
        if buttons & mouse.MIDDLE:
            #print('middle dragging')
            tz=dy*self._world.cg.cameras[0].mouse_speed
            self._world.cg.cameras[0].cam_trans.translate(0,0,tz)
    
    def on_mouse_scroll(self, x,y,scroll_x,scroll_y):
    #    print('scrolling...')   
        self._world.cg.cameras[0].cam_trans.translate(0,0,scroll_y*self._world.cg.cameras[0].scroll_speed)

    def on_close(self):
        """
        Closes the Fos window.
        """
        self.has_exit = True
        self.close()

    