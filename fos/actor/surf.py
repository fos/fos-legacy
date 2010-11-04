import numpy as np
import fos.lib.pyglet as pyglet
from fos.lib.pyglet.gl import *
from fos.lib.pyglet.graphics import Batch
from fos.core.actor import Actor

def vec(*args):
    return (GLfloat * len(args))(*args)

class CommonSurfaceGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)        
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3.)
       
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glLineWidth(3.)
        pass
    


class Surface(Actor):
    
    def __init__(self,vertices,faces,normals,colors):
        
       #self.vertices=vertices
       #self.faces=faces 
               
       self.vert_ptr=vertices.ctypes.data
       self.face_ptr=faces.ctypes.data
       self.norm_ptr=normals.ctypes.data
       self.color_ptr=colors.ctypes.data
       
       self.el_count=len(faces)*3
        
        
        
    def draw(self):    
                
#        self.set_state()
                        
        glEnableClientState(GL_VERTEX_ARRAY)
#        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        #try:  
        glVertexPointer(3, GL_FLOAT, 0, self.vert_ptr)                          
#        glNormalPointer(GL_FLOAT, 0, self.norm_ptr)        
        glColorPointer(4, GL_FLOAT, 0, self.color_ptr)
        
        #except GLException, e:
        #    print e
        
            
        glDrawElements(GL_TRIANGLES, self.el_count, GL_UNSIGNED_INT, self.face_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
#        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
#        self.unset_state()              

    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)        
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
        glLineWidth(3.)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        #Define a simple function to create ctypes arrays of floats:
        
        glLightfv(GL_LIGHT0, GL_POSITION, vec(.0, .0, 1, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
        
        glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .0, 0, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 0, 0, 1))

        glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,vec(0.9, 0, 0.3, 1.))
        glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR, vec(1, 1, 1, 1.))
        glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS, 50)
        
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glLineWidth(1.)
        glDisable(GL_LIGHTING)
    
    '''
    def update(self, dt):
        print 'dt',dt
        pass
    '''

'''    

class Surface(Actor):

    def __init__(self,vertices,faces,values,batch,group=None):
        
        
        
        self.batch=batch
            
        inds=faces.ravel().tolist()
        verx=vertices.ravel().tolist()

        normals=np.zeros((len(vertices),3))        
        ones_=np.ones(len(values))
        colors=np.vstack((values,ones_,ones_)).T
        colors=colors.ravel().tolist()
        
        p=vertices
        l=faces
            
        trinormals=np.cross(p[l[:,0]]-p[l[:,1]],\
                                p[l[:,1]]-p[l[:,2]],\
                                axisa=1,axisb=1)
        
        for (i,lp) in enumerate(faces):
            normals[lp]+=trinormals[i]

            div=np.sqrt(np.sum(normals**2,axis=1))     
            div=div.reshape(len(div),1)
            normals=(normals/div)            
            norms=np.array(normals).ravel().tolist()
    
        self.vertex_list = self.batch.add_indexed(len(vertices),\
                                                 GL_TRIANGLES,\
                                                 group,\
                                                 inds,\
                                                 ('v3d/static',verx),\
                                                 ('n3d/static',norms),\
                                                 ('c3d/static',colors))
                                                 
    def draw(self):
        self.batch.draw()
        
    def update(self,dt):
        pass    
        
    def delete(self):
        self.vertex_list.delete()
'''