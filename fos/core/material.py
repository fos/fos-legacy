import numpy as np
import fos.lib.pyglet as pyglet
from fos.lib.pyglet.gl import *
from fos.lib.pyglet.gl import GLfloat
from fos.core.utils import vec

class Material():
    
    def __init__(self,diffuse,emissive,specular,shininess,color=False):       
        
        self.diffuse=diffuse
        self.specular=specular
        self.emissive=emissive
        self.shininess=shininess 
        
    def set_material(self):
        
        if self.diffuse !=None:
            glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,vec(*self.diffuse))
        if self.specular !=None:
            glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR, vec(*self.specular))
        if self.emissive != None:        
            glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION,vec(*self.emissive))
        if self.shininess !=None:            
            glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS, self.shininess)
        
    
