from math import sin, cos,sqrt
import numpy as np

#pyglet.options['debug_gl']=False


from fos.core.managed_window import ManagedWindow
import fos.core.collision as cll

from fos.lib import pyglet
from fos.lib.pyglet.gl import *
from fos.lib.pyglet.window import key,mouse
from fos.core.interactor import Interaction


class Engine():

    def __init__(self,width=1024,height=768,config=None):

        self.width=width
        self.height=height
        #config broke after upgrating to ubuntu 10.10
        '''
        self.config = Config(sample_buffers=1, samples=4,\
                        depth_size=24,double_buffer=True,\
                        vsync=False)
        '''

        self.config = Config(vsync=False)
        self.fps=pyglet.clock.ClockDisplay()
        actors.append(self.fps)
        
    
    def run(self):
        # pyglet.window.Window
        window = ManagedWindow(width=self.width,\
                              height=self.height,\
                              caption='The Light Machine',\
                              resizable=True,\
                              vsync=False)
                              #config=self.config)
        
                            
        window.on_resize=on_resize
        window.on_key_press=on_key_press
        window.on_mouse_drag=on_mouse_drag
        window.on_mouse_motion=on_mouse_motion
        window.on_mouse_scroll=on_mouse_scroll

        window.draw=draw      
        schedule(update)
                
        print('NeoFos started')
        pyglet.app.run()
        

def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 2000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update(dt):    
    #urch.update()
    for a in actors:
        try:
            a.update()
        except:
            pass

def draw():   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()

    #'''
    eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=cam_rot.lookat
    gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
    glMultMatrixf(cam_trans.matrix)
    glMultMatrixf(cam_rot.matrix)
    batch.draw()
    #'''

    
    
    for a in actors:        
        try:
            a.draw()
        except:
            pass
    

    #trk.display()    
    #print pyglet.clock.get_fps()
    
    

def on_key_press(symbol,modifiers):
    #print('key pressed')
    if symbol == key.R:
        cam_rot.reset()
        cam_trans.reset()
    
    if symbol == key.P:                
        global mouse_x, mouse_y
        x,y=mouse_x,mouse_y
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
    
def on_mouse_motion(x,y,dx,dy):
    #print('mouse moved')
    global mouse_x,mouse_y
    mouse_x,mouse_y=x,y
    
def on_mouse_drag(x,y,dx,dy,buttons,modifiers):    
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

def on_mouse_scroll(x,y,scroll_x,scroll_y):
    #print('scrolling...')   
    cam_trans.translate(0,0,scroll_y*cam_trans.scroll_speed)

def schedule(update,dt=None):
    if dt==None:
        pyglet.clock.schedule(update)
    else:
        pyglet.clock.schedule_interval(update,dt)
    


#Global variables
mouse_x,mouse_y=0,0
batch = pyglet.graphics.Batch()
actors=[]
cam_rot = Interaction()
cam_trans = Interaction()
Engine().run()

