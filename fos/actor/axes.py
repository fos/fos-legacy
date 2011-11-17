import numpy as np
from pyglet.gl import *
from fos import Actor, World
from pyglet.lib import load_library
glib=load_library('GL')

class Axes(Actor):

    def __init__(self, scale = 1.0, line_width=2.):
        """ Draw three axes
        """

        self.affine=np.eye(4)
        self.scale = scale        
        self.vertices=np.array([[0,0,0],[0.5,0,0],[1,0,0],\
                           [0,0,0],[0,0.5,0],[0,1,0],\
                           [0,0,0],[0,0,0.5],[0,0,1]],dtype='f4')
        self.vertices=self.scale*self.vertices        
        self.colors=np.array([[1,0,0,1],[1,0,0,1],[1,0,0,1],\
                         [0,1,0,1],[0,1,0,1],[0,1,0,1],\
                         [0,0,1,1],[0,0,1,1],[0,0,1,1]],dtype='f4')
        self.vn=len(self.vertices)
        self.cn=len(self.colors)        
        assert self.vn==self.cn        
        self.vptr=self.vertices.ctypes.data
        self.cptr=self.colors.ctypes.data
        self.count=np.array([3,3,3],dtype=np.int32)
        self.first=np.array([0,3,6],dtype=np.int32)        
        self.firstptr=self.first.ctypes.data
        self.countptr=self.count.ctypes.data        
        self.primcount=len(self.first)
        self.items=3        
        self.line_width=line_width
        self.show_aabb = False        
        self.make_aabb((np.array([-scale,-scale,-scale]),np.array([scale,scale,scale])),margin = 0)    
        
    def update(self, dt):
        pass


    def draw(self):
        glEnable(GL_DEPTH_TEST)        
        glLineWidth(self.line_width)        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3,GL_FLOAT,0,self.vptr)
        glColorPointer(4,GL_FLOAT,0,self.cptr)
        glPushMatrix()
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glib.glMultiDrawArrays(GL_LINE_STRIP, self.firstptr,self.countptr, self.items)
        #Same as
        #glDrawArrays(GL_LINE_STRIP,0,3)
        #glDrawArrays(GL_LINE_STRIP,3,3)
        #glDrawArrays(GL_LINE_STRIP,6,3)        
        #if self.show_aabb:self.draw_aabb()
        #Or same as
        #for i in range(self.items):
        #    glDrawArrays(GL_LINE_STRIP,self.first[i],self.count[i])        
        glPopMatrix()
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)        
        glLineWidth(1.)
        glDisable(GL_DEPTH_TEST)

        
        

if __name__=='__main__':
    pass
    
