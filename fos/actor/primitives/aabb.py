""" The Primitive for the axis-aligned bounding box """

import numpy as np

from fos.lib.pyglet.gl import GL_QUADS, GL_UNSIGNED_INT

class AABBPrimitive():

    vertices = None
    vertices_ptr = None
    vertices_nr = 0
    
    color_ptr = None
    colors = None
    normal_ptr = None
    
    mode = None
    type = None
    
    nr_nodes = None
    indices_ptr = None
    indices = None
    indices_nr = 0
    
    def __init__(self, coord1, coord2):
        
        self.mode = GL_QUADS
        self.type = GL_UNSIGNED_INT
        
        # make box
        self._make_box(coord1, coord2)
            
    def _make_box(self, c1, c2):
        
        dx = abs(coord2[0] - coord1[0])
        dy = abs(coord2[1] - coord1[1])
        dz = abs(coord2[2] - coord1[2])
        
        self.vertices = np.array([
               [-0.5, -0.5, -0.5],
               [c1[0], c1[1], c1[2]],
               [-0.5,  0.5, -0.5],
               [-0.5,  0.5,  0.5],
               [ 0.5, -0.5, -0.5],
               [ 0.5, -0.5,  0.5],
               [c2[0], c2[1], c2[2]],
               [0.5,  0.5,  0.5]], dtype = np.float32)

        self.vertices = np.array([
               [-0.5, -0.5, -0.5],
               [-0.5, -0.5,  0.5],
               [-0.5,  0.5, -0.5],
               [-0.5,  0.5,  0.5],
               [ 0.5, -0.5, -0.5],
               [ 0.5, -0.5,  0.5],
               [ 0.5,  0.5, -0.5],
               [ 0.5,  0.5,  0.5]], dtype = np.float32)
        
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

        
    def draw(self):
        pass
        # enable wireframe
        # set color to yellow
        