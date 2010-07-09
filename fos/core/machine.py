import numpy as np
import pyglet
from pyglet.gl import *
from utils import get_model_matrix

batch = pyglet.graphics.Batch()

rx=ry=rz=0

class Urchine(object):

    def __init__(self,batch,group=None):
        lines=10*np.random.rand(1000,3)
        lines=lines-np.mean(lines)
        vertices=lines.ravel().tolist()        

        self.vertex_list = batch.add(len(lines),GL_LINE_STRIP,group,\
                                         ('v3d/static',vertices))

    def update(self):        
        #global rx
        #rx=rx+1
        pass

    def delete(self):
        self.vertex_list.delete()


urch=Urchine(batch=batch)        


class Interaction(object):

    def __init__(self):
        self.matrix=None
        self.reset()
        self.rx=0
        self.ry=0

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

camera = Interaction()
        
class Mouse(object):
    def __init__(self):
        self.x=0
        self.y=0

mouse = Mouse()


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
                                          caption='NeoFos - The Light Machine',\
                                          resizable=True, \
                                          config=self.config)
        window.on_resize=on_resize
        window.on_draw=on_draw
        window.on_key_press=on_key_press
        window.on_mouse_press=on_mouse_press

        print('Application started')
        pyglet.app.run()
        

def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    #print('%d width, %d height' % (width,height))
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    #window.flip()
    return pyglet.event.EVENT_HANDLED

def update(dt):    
    urch.update()    
    #control.update()

def on_draw():
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #global rx,ry,rx

    #'''
    glTranslatef(0, 0, -40)

    '''
    glRotatef(rx, 0, 0, 1)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rx, 1, 0, 0)
    
    '''
    #camera.rotate(camera.ry,0,1,0)
    #camera.rotate(camera.rx,1,0,0)
    glMultMatrixf(camera.matrix)
    #camera.rotate(1,0,1,0)

    batch.draw()

def on_key_press(symbol,modifiers):
    if symbol == key.SPACE:
        pass
    
def on_mouse_press(x, y, button, modifiers):
    if pyglet.window.mouse.LEFT == button:

        
        dx=x - mouse.x
        dy=y - mouse.y

        print x,y, mouse.x,mouse.y, dx,dy
        
        camera.rx=dx*0.1
        camera.ry=dy*0.1
        #camera.rotate(camera.ry,0,1,0)
        camera.rotate(camera.rx,1,0,0)
        
    if pyglet.window.mouse.MIDDLE == button:
        pass
    if pyglet.window.mouse.RIGHT == button:
        pass

    mouse.x=x
    mouse.y=y

#batch = pyglet.graphics.Batch()

def schedule(update):    
    pyglet.clock.schedule(update) 

def schedule_interval(update,dt):
    pyglet.clock.schedule_interval(update,dt)
    

