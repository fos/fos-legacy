import numpy as np

from pyglet.gl import *

from fos import Actor, World, Window

        
class Maps(Actor):
    
    def __init__(self, *args, **kwargs):
        """ Dynamic maps together with symbolic informatio
        
        nr_of_timepoints : int
            The number of timepoints to display
        
        Display result:
        Row segmented, a number of maps for column
        A triangular mesh for each time point, or one as a scaffold
        Scalar field on the vertices for each timepoint
        A set of symbols together with a [0,1] value mapped as a (colored rectangle)
        
        """
        super(Dummy, self).__init__()
        
        self.affine = np.eye(4, dtype = np.float32)
        self._update_glaffine()
        
        self.vertices = np.random.random( (10,3)).astype(np.float32) * 10

        self.colors = np.array( [[255,255,0,255],
                                [255,255,0,255],
                                [0,255,0,255],
                                [0,255,0,255]], dtype = np.ubyte )
        
        self.indices = np.array( [[0,1], [1,2], [5,6], [8,9]] , dtype = np.uint32).ravel()
        self.vertices = self.vertices[self.indices,:]
        self.indices = np.array( range(len(self.indices)), dtype = np.uint32)
        self.colors = self.colors.repeat(2, axis = 0)
        self.colors_ptr = self.colors.ctypes.data
        
        self.vertices_ptr = self.vertices.ctypes.data
        self.indices_ptr = self.indices.ctypes.data
        self.indices_nr = self.indices.size
        self.mode = GL_LINES
        self.type = GL_UNSIGNED_INT
        
    def update(self, dt):
        pass
        
    def draw(self):
        pass

        glPushMatrix()
        glMultMatrixf(self.glaffine)
        glLineWidth(2.0)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices_ptr)
        glColorPointer(4, GL_UNSIGNED_BYTE, 0, self.colors_ptr)
        glDrawElements(self.mode,self.indices_nr,self.type,self.indices_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()

            
if __name__ == '__main__':
    wi = Window()
    w = wi.get_world()
    act = Dummy()
    w.add(act)
        