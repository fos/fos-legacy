import numpy as np

from fos.lib.pyglet.gl import GL_QUADS, GL_UNSIGNED_INT, GL_LINES

class NodeGLPrimitive():

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
    
    def __init__(self):
        
        self.mode = GL_QUADS
        self.type = GL_UNSIGNED_INT
            
    def _make_cubes(self, position, size):
        
        assert position.shape[1] == 3
        size = size.ravel()
        assert position.shape[0] == len(size)
        
        nr = len(position)
        # allocate space for the big array
        if self.vertices == None:
            self.nr_nodes = nr
            self.vertices = np.zeros( (8*self.nr_nodes, 3), dtype = np.float32)
            self.indices = np.zeros( (6*self.nr_nodes, 4), dtype = np.uint32)
            # self.affine = np.zeros( (4,4,self.nr_nodes), dtype = np.float)
        else:
            # number of nodes changed
            if nr != self.nr_nodes:
                # need to reallocate array
                self.nr_nodes = nr
                self.vertices = np.zeros( (8*self.nr_nodes, 3), dtype = np.float32)
                self.indices = np.zeros( (6*self.nr_nodes, 4), dtype = np.uint32)
            # else: you could zero them here
            
        for i in xrange(self.nr_nodes):
            # comment: we might needs this loop only on
            # creation time. user interaction updates directly the vertices
            
            vertices = size[i] * np.array([
                   [-0.5, -0.5, -0.5],
                   [-0.5, -0.5,  0.5],
                   [-0.5,  0.5, -0.5],
                   [-0.5,  0.5,  0.5],
                   [ 0.5, -0.5, -0.5],
                   [ 0.5, -0.5,  0.5],
                   [ 0.5,  0.5, -0.5],
                   [ 0.5,  0.5,  0.5]], dtype = np.float32)
            
            # updating the affine for one cube
            # we do not need this for now because we are drawing
            # with drawelements 
            # for now, just add the position
            vertices += position[i,:]
            
            # select the correct block to store the update vertices data
            self.vertices[8*i:(8*(i+1)),:] = vertices
            
            faces = np.array([ [0,1,5,4],
                               [2,3,7,6],
                               [2,0,1,3],
                               [3,7,5,1],
                               [7,6,4,5],
                               [6,2,0,4] ], dtype = np.uint32)
            
            # offset using i and the number of vertices
            faces += 8*i
            
            # updates the indices with the faces
            self.indices[6*i:(6*(i+1)),:] = faces
        

        self.vertices_nr = self.vertices.shape[0]
        self.indices_nr = self.indices.size
        
        self.vertices_ptr = self.vertices.ctypes.data
        self.indices_ptr = self.indices.ctypes.data

    
    def _make_color(self, color):
        if self.vertices is None:
            return
        assert color.shape[0] == self.nr_nodes
        self.colors = color.repeat(8, axis=0)
        self.color_ptr = self.colors.ctypes.data
        
    
    def _make_normals(self):
        if self.vertices is None or self.indices is None:
            return
        
    
class EdgeGLPrimitive():
    

    vertices = None
    vertices_ptr = None
    vertices_nr = 0
    
    color_ptr = None
    colors = None
    
    mode = None
    type = None
    nr_edges = None
    indices_ptr = None
    indices = None
    indices_nr = 0
    
    def __init__(self):
        
        self.mode = GL_LINES
        self.type = GL_UNSIGNED_INT
        
    def _make_edges(self, position, edges):

        assert position.shape[1] == 3
        assert edges.shape[1] == 2
        
        nr = len(edges)
        # allocate space for the big array
        if self.vertices == None:
            self.nr_edges = nr
            self.vertices = np.zeros( (2*self.nr_edges, 3), dtype = np.float32)
            self.indices = np.zeros( (self.nr_edges, 2), dtype = np.uint32)
        else:
            # number of nodes changed
            if nr != self.nr_lines:
                # need to reallocate array
                self.nr_edges = nr
                self.vertices = np.zeros( (2*self.nr_edges, 3), dtype = np.float32)
                self.indices = np.zeros( (self.nr_edges, 2), dtype = np.uint32)
        
        self.indices[:,:] = edges
        self.vertices[:,:] = position[self.indices.ravel(),:]
        
        self.vertices_nr = self.vertices.shape[0]
        self.indices_nr = self.indices.shape[0] * self.indices.shape[1]
        
        self.vertices_ptr = self.vertices.ctypes.data
        self.indices_ptr = self.indices.ctypes.data
        
    def _make_color(self, color):
        if self.vertices is None:
            return
        assert color.shape[0] == self.nr_edges
        self.colors = color.repeat(2, axis=0)
        self.color_ptr = self.colors.ctypes.data