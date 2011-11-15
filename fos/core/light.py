import numpy as np
import pyglet as pyglet
from pyglet.gl import *
from pyglet.gl import GLfloat
from fos.core.utils import vec

class Light():
    
    def __init__(self,position,ambient,diffuse,specular):       
        
        self.position=position
        self.specular=specular
        self.ambient=ambient
        self.diffuse=diffuse
        
    def set_light(self):       
    
        glLightfv(GL_LIGHT0, GL_POSITION, vec(*self.position))
        if self.specular!=None:        
            glLightfv(GL_LIGHT0, GL_SPECULAR, vec(*self.specular))
        if self.ambient!=None:
            glLightfv(GL_LIGHT0, GL_AMBIENT, vec(*self.ambient))
        if self.diffuse!=None:
            glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(*self.diffuse));
        
