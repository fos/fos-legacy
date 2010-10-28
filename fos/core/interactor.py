from fos.lib.pyglet.gl import *
from fos.core.utils import get_model_matrix #,screen_to_model,get_viewport

class Interaction(object):

    def __init__(self):
        self.matrix=None
        self.lookat=[0,0,120,0,0,0,0,1,0]
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