from fos.lib.pyglet.gl import *
from fos.core.managed_window import ManagedWindow
from fos.lib import pyglet
from fos.lib.pyglet.window import key,mouse
from fos.core.interactor import Interaction
from fos.actor.volslicer import ConnectedSlices

from threading import RLock
import numpy as np

        
class FosWindow(ManagedWindow):
    
    def __init__(self, **kwargs):
        super(FosWindow, self).__init__(**kwargs)
        
        
        self.actors = []
        self.mouse_x, self.mouse_y = 0,0
        self._render_lock = RLock()
        
    def setup(self):
        
        #glClearColor(1.0, 1.0, 0.0, 0.0)
        #glClearDepth(1.0)
#
#        glDepthFunc(GL_LESS)
#        glEnable(GL_DEPTH_TEST)

        #glEnable(GL_BLEND)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE#_MINUS_SRC_ALPHA)
        pass
        
        
    def update(self, dt):
        pass
    ''''
        for a in actors:
            try:
                a.update()
            except:
                pass
'''
            
    def draw(self):   
        #print "draw in fos_window"
        self._render_lock.acquire()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
        glLoadIdentity()
    
        eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=cam_rot.lookat
        gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
        glMultMatrixf(cam_trans.matrix)
        glMultMatrixf(cam_rot.matrix)
#
#        quadratic = gluNewQuadric()
#        #gluQuadricNormals(quadratic, GLU_SMOOTH)
#        #gluQuadricTexture(quadratic, GLU_TRUE)
#        glPushMatrix()
#        glScalef(20.0, 20.0, 20.0)
#        #glTranslatef(20.0, 10.0, -1.5)
#        #gluCylinder(quadratic, 1.0, 1.0, 3.0, 32, 32)
#        gluSphere(quadratic, 10.3, 32, 32)
#        glPopMatrix()
#        gluDeleteQuadric(quadratic)
        
        for a in self.actors:
            try:
                a.draw()
            except:
                pass
            
        self._render_lock.release()
    
              
    def on_resize(self, width, height):
        print "test", width, height
        
        
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 2000.)
        glMatrixMode(GL_MODELVIEW)
        #self.set_size(width, height)
        
#        return pyglet.event.EVENT_HANDLED


    def on_key_press(self, symbol,modifiers):

        if symbol == key.R:
            cam_rot.reset()
            cam_trans.reset()
        
        if symbol == key.H:
            self.set_size(900, 600)
            
        if symbol == key.P:                
            x,y=self.mouse_x,self.mouse_y
            nx,ny,nz=screen_to_model(x,y,0)
            fx,fy,fz=screen_to_model(x,y,1)        
            near=(nx,ny,nz)
            far=(fx,fy,fz)
            #print near,far
            #print'x',x,'y',y
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
                cam_rot.rotate( dx*cam_rot.mouse_speed,0,1,0)
                cam_rot.rotate(-dy*cam_rot.mouse_speed,1,0,0)
                
        if buttons & mouse.RIGHT:
            #print('right dragging')
            tx=dx*cam_trans.mouse_speed
            ty=dy*cam_trans.mouse_speed        
            cam_trans.translate(tx,ty,0)
    
        if buttons & mouse.MIDDLE:
            #print('middle dragging')
            tz=dy*cam_trans.mouse_speed
            cam_trans.translate(0,0,tz)
    
    def on_mouse_scroll(self, x,y,scroll_x,scroll_y):
    #    print('scrolling...')   
        cam_trans.translate(0,0,scroll_y*cam_trans.scroll_speed)

    def on_close(self):
        """
        Closes the Fos window.
        """
        self.has_exit = True
        self.close()
        
#    def close(self):
#        '''Close the window.
#
#        After closing the window, the GL context will be invalid.  The
#        window instance cannot be reused once closed (see also `set_visible`).
#
#        The `pyglet.app.EventLoop.on_window_close` event is dispatched on
#        `pyglet.app.event_loop` when this method is called.
#        '''
#        from fos.lib.pyglet import app
#        if not self._context:
#            return
#        
#        app.windows.remove(self)
#        self._context.destroy()
#        self._config = None
#        self._context = None
#        
#        if app.event_loop:
#            app.event_loop.dispatch_event('on_window_close', self)
#            



def schedule(update,dt=None):
    if dt==None:
        pyglet.clock.schedule(update)
    else:
        pyglet.clock.schedule_interval(update,dt)
        

#    def draw(self):
#        pass
#        self._render_lock.acquire()
#
#        self._self.mouse_xlock.release()

#Global variables
#mouse_x,mouse_y=0,0
#actors=[]
#cam_rot = Interaction()
#cam_trans = Interaction()
#
#a=np.random.random( ( 100, 100, 100) )
#aff = np.eye(4)
#cds = ConnectedSlices(aff,a)
#actors.append(cds)


if __name__ == '__main__':
    w = FosWindow(#width=1024,
             #height=768,
             caption='The Light Machine',
             resizable=True,
             vsync=False)
    
    cam_rot = Interaction()
    cam_trans = Interaction()
    
    # connected slices actor
    a=np.random.random( ( 100, 100, 100) )
    aff = np.eye(4)
    cds = ConnectedSlices(aff,a)
    w.actors.append(cds)

#    from fos.actor.network import AttributeNetwork
#    # network actor
#    pos = np.random.random( (10,3) )
#    net = AttributeNetwork(pos)
#    w.actors.append(net)
    
    