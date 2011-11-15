import numpy as np
import pyglet as pyglet
from pyglet.gl import *
from pyglet.gl import GLfloat

from fos.core.actor import Actor
from fos.core.utils import vec

class Surface(Actor):
    
    def __init__(self,vertices,faces,colors,
                 normals = None,
                 material = None,
                 light = None,                
                 affine = None):
        
        super(Surface, self).__init__()
        
        # store a reference to vertices for bounding box computation
        self.vertices = vertices
        #if force_centering:
        #    self.vertices = self.vertices - np.mean(self.vertices, axis = 0)
            
        self.vert_ptr=self.vertices.ctypes.data
        self.face_ptr=faces.ctypes.data        
        self.color_ptr=colors.ctypes.data
        self.material=material
        self.light=light
    
        self.el_count=len(faces)*3

        if affine == None:
            # create a default affine
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine
            
        self._update_glaffine()
        
        if normals!=None or colors==None:
            self.norm_ptr=normals.ctypes.data
            self.draw = self.draw_withlight
        else:
            self.draw = self.draw_sanslight
        
        self.show_aabb = True
        self.make_aabb(margin = 0)
    
    
    def draw_withlight(self):
        
        
        glPushMatrix()
        self.set_state()
        glMultMatrixf(self.glaffine)   
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        #glEnableClientState(GL_COLOR_ARRAY)        
        glVertexPointer(3, GL_FLOAT, 0, self.vert_ptr)                          
        glNormalPointer(GL_FLOAT, 0, self.norm_ptr)        
        #glColorPointer(4, GL_FLOAT, 0, self.color_ptr)
        glDrawElements(GL_TRIANGLES, self.el_count, GL_UNSIGNED_INT, self.face_ptr)
        #glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        self.unset_state()
        glEnable(GL_DEPTH_TEST)
        if self.show_aabb:
            self.draw_aabb()
        glPopMatrix()
        

        
    def draw_sanslight(self):
        glPushMatrix()
        glMultMatrixf(self.glaffine)
        #glEnable (GL_BLEND) 
        #glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)        
        glVertexPointer(3, GL_FLOAT, 0, self.vert_ptr)                             
        glColorPointer(4, GL_FLOAT, 0, self.color_ptr)
        glDrawElements(GL_TRIANGLES, self.el_count, GL_UNSIGNED_INT, self.face_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        if self.show_aabb:
            self.draw_aabb()        
        glPopMatrix()
        
    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)        
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        #glShadeModel(GL_SMOOTH)
        glLineWidth(3.)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        #glEnable(GL_LIGHT1)
        #Define a simple function to create ctypes arrays of floats:
        
        self.light.set_light()
        self.material.set_material()
        
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glLineWidth(1.)
        
        glDisable(GL_LIGHTING)
        #glDisable(GL_LIGHT0)   
    
    def update(self, dt):
        #print 'dt',dt
        pass
    