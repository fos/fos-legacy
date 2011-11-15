""" The Primitive for the axis-aligned bounding box """

import numpy as np

from pyglet.gl import GL_QUADS, GL_UNSIGNED_INT

class AABBPrimitive():

    vertices = None
    vertices_ptr = None
    vertices_nr = 0
    
    mode = None
    type = None
    
    indices_ptr = None
    indices = None
    indices_nr = 0
    
    def __init__(self, blf = None, trb = None, margin = 20):
        """ Constructs a axis-aligned bounding box primitive
        from bottom-left-front and top-right-back point coordinates """
        
        self.mode = GL_QUADS
        self.type = GL_UNSIGNED_INT
        
        self.coord = (None, None)
        
        self._make_box(blf, trb, margin)
            
    def _make_box(self, c1, c2, margin):

        self.update(c1, c2, margin)

        self.indices = np.array([ [0,1,5,4],
                           [2,3,7,6],
                           [2,0,1,3],
                           [3,7,5,1],
                           [7,6,4,5],
                           [6,2,0,4] ], dtype = np.uint32)
        
        
        self.vertices_nr = self.vertices.shape[0]
        self.indices_nr = self.indices.size
        
        self.vertices_ptr = self.vertices.ctypes.data
        self.indices_ptr = self.indices.ctypes.data

    def update(self, c1, c2, margin):
        # add the margin on all sides
        c1[0] = c1[0] - margin
        c1[1] = c1[1] - margin
        c1[2] = c1[2] - margin
        
        c2[0] = c2[0] + margin
        c2[1] = c2[1] + margin
        c2[2] = c2[2] + margin

        self.coord = (np.array(c1, dtype = np.float32), 
                      np.array(c2, dtype = np.float32))
        
        self.vertices = np.array([
               [c1[0],c1[1],c2[2]],
               [c1[0],c1[1],c1[2]],
               [c1[0],c2[1],c2[2]],
               [c1[0],c2[1],c1[2]],
               [c2[0],c1[1],c2[2]],
               [c2[0],c1[1],c1[2]],
               [c2[0],c2[1],c2[2]],
               [c2[0],c2[1],c1[2]]], dtype = np.float32)
        
    def get_center(self):
        c1 = np.array(self.coord[0]).ravel()
        c2 = np.array(self.coord[1]).ravel()
        return (c1 + c2) * 0.5
    
    def draw(self):
        pass
        # enable wireframe
        # set color to yellow
        