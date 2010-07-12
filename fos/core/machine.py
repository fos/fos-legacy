from math import sin, cos,sqrt
import numpy as np
import pyglet
from pyglet.gl import *
from pyglet.window import key,mouse
from fos.core.utils import get_model_matrix,screen_to_model,get_viewport
import fos.core.collision as cll

#from tracks import Tracks

#Global variables
mouse_x,mouse_y=0,0

batch = pyglet.graphics.Batch()
actors=[]



'''


class Urchine(object):

    def __init__(self,batch,group=None):

       
        lno=100
        self.vertex_list=lno*[None]
        for i in range(lno):
            lines=100*np.random.rand(10,3).astype('f')
            vertices=lines.ravel().tolist()
            self.vertex_list[i] = batch.add(len(lines),GL_LINE_STRIP,group,\
                                         ('v3f/static',vertices))

        self.lno=lno
        
    def update(self):
        #self.vertex_list.vertices[0]+=1
        pass
    def delete(self):
        
        for i in range(self.lno):
            self.vertex_list.delete()
            
        
        #self.vertex_list.delete()

urch=Urchine(batch=batch)
'''

'''
lno=100000
lines=[10*np.random.rand(10,3).astype('f') for i in range(lno)]
colors=[np.random.rand(10,4).astype('f') for i in range(lno)]

trk=Tracks(lines,colors)
trk.init()
'''

class Interaction(object):

    def __init__(self):
        self.matrix=None
        self.lookat=[0,0,40,0,0,0,0,1,0]
        self.scroll_speed=10
        self.mouse_speed=0.1        
        self.reset()
       
    def reset(self):        
        glPushMatrix()
        glLoadIdentity()
        self.matrix=get_model_matrix()                
        glPopMatrix()

    def translate(self,dx,dy,dz):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(dx,dy,dz)
        glMultMatrixf(self.matrix)
        self.matrix=get_model_matrix()
        glPopMatrix()

    def rotate(self,ang,rx,ry,rz):
        glPushMatrix()
        glLoadIdentity()
        glRotatef(ang,rx,ry,rz)
        glMultMatrixf(self.matrix)
        self.matrix=get_model_matrix()
        glPopMatrix()

cam_rot = Interaction()
cam_trans = Interaction()

class Machine(object):

    def __init__(self,width=1024,height=768,config=None):

        self.width=width
        self.height=height
        self.config = Config(sample_buffers=1, samples=4,\
                        depth_size=24,double_buffer=True,\
                        vsync=True)
    
    def run(self):
        window = pyglet.window.Window(width=self.width,\
                                          height=self.height,\
                                          caption='The Light Machine',\
                                          resizable=True, \
                                          config=self.config)
        window.on_resize=on_resize
        window.on_draw=on_draw
        window.on_key_press=on_key_press
        window.on_mouse_drag=on_mouse_drag
        window.on_mouse_motion=on_mouse_motion
        window.on_mouse_scroll=on_mouse_scroll
        
        schedule(update)
        print('NeoFos started')
        pyglet.app.run()
        

def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update(dt):    
    #urch.update()
    for a in actors:
        try:
            a.update()
        except:
            pass

def on_draw():   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=cam_rot.lookat
    gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
    glMultMatrixf(cam_trans.matrix)
    glMultMatrixf(cam_rot.matrix)
    batch.draw()
    
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
        vp=get_viewport()
        x,y=mouse_x,mouse_y
        nx,ny,nz=screen_to_model(x,vp[3]-y,0)
        fx,fy,fz=screen_to_model(x,vp[3]-y,1)
        near=(nx,ny,nz)
        far=(fx,fy,fz)
        print near,far
    
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
    

if __name__ == "__main__":

    Machine().run()

