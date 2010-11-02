import numpy as np

from fos.core.world import World
from fos.lib.pyglet.gl import *
from fos.core.actor import Actor

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
        self.indices_nr = self.indices.shape[0] * self.indices.shape[1]
        
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
        
class AttributeNetwork(Actor):
    
    def __init__(self, *args, **kwargs):
        """
        
        Graph related
        -------------
        
        layout
            The layout algorithm used if node_position
            not given. Default: random
            From NetworkX: circular, random, shell, spring, spectral, fruchterman_reingold
            Else: ...
        
        Node related
        ------------
        node_position : (N,3)
            Node positions as ndarray

        node_size
            The size of the node

        node_label
            Node labels
            
        node_shape
            cube, sphere, pyramid, electrodes (cylinders)
            
        node_color : (N,4)
            The color of the nodes and its alpha value
            Either given [0,1] or [0,255]
            (or: cmap, vmin, vmax)
        
        node_show_labels
            Show all labels on the nodes / 
            only for specified nodes.
            node_label has to be set
        
        Edge related
        ------------
        
        edge_directed : bool
            Interpret `edge_weight` as directed
        
        edge_weight : (M,1)
            The weight determines the width of the line
            
        edge_color : (N,4)
            The color of the edges
            (or cmap, vmin, vmax)
            
        edge_style
            solid, dashed, dotted, dashdot
            What does OpenGL support natively?
            
        edge_label
            The label for the edges
            
        
        Font related (global or per node/edge?)
        ------------
        
        font_size: int
           Font size for text labels (default=12)
    
        font_color: string
           Font color string (default='k' black)
    
        font_weight: string
           Font weight (default='normal')
    
        font_family: string
           Font family (default='sans-serif')
           
        """
        
        # open questions
        # - how to normalize the input node_position distribution
        # - pick a node / edge, show info, etc.
        # - dynamic graph with lifetime on nodes/edges
        # - hierarchic graph

        self.node_glprimitive = NodeGLPrimitive()
        self.edge_glprimitive = EdgeGLPrimitive()
        
        
        if kwargs.has_key('node_position'):
            self.node_position = kwargs['node_position']

            if kwargs.has_key('node_size'):
                self.node_size = kwargs['node_size']
            else:
                # default size 0.5
                self.node_size = np.ones( (self.node_position.shape[0], 1), dtype = np.float32 ) / 2.0
                
            self.node_glprimitive._make_cubes(self.node_position, self.node_size)
        else:
            raise Exception("You have to specify the node_position array")
        
        if kwargs.has_key('node_color'):
            self.node_color = kwargs['node_color']
            self.node_glprimitive._make_color(self.node_color)
            
#        self.node_shape = kwargs['node_shape']
#        self.node_label = kwargs['node_label']

        if kwargs.has_key('edge_connectivity'):
            self.edge_connectivity = kwargs['edge_connectivity']
            self.edge_glprimitive._make_edges(self.node_position, self.edge_connectivity)
            
        if kwargs.has_key('edge_color'):
            self.edge_color = kwargs['edge_color']
            self.edge_glprimitive._make_color(self.edge_color)
            
        if kwargs.has_key('edge_weight'):
            self.edge_weight = kwargs['edge_weight']
          
        

    def update(self, dt):
        pass
        # update the node position and size to make it dynamic
        # only need to update if anything has changed (chaged)
#        self.node_position += np.random.random( (self.node_position.shape) ) * 2
#        self.node_size = np.random.random( (self.node_size.shape) ) * 2
        
        # this functionality could be implemented with cython
#        self.node_glprimitive._make_cubes(self.node_position, self.node_size)
#        self.node_color[:,3] += 1
#        self.node_color[:,3] = self.node_color[:,3] % 255
#        self.node_glprimitive._make_color(self.node_color)
        
    def draw(self):
        pri = self.edge_glprimitive
        glLineWidth(5.0)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, pri.vertices_ptr)
        glColorPointer(4, GL_UNSIGNED_BYTE, 0, pri.color_ptr)
        glDrawElements(pri.mode,pri.indices_nr,pri.type,pri.indices_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
                  
        pri = self.node_glprimitive
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, pri.vertices_ptr)
        glColorPointer(4, GL_UNSIGNED_BYTE, 0, pri.color_ptr)
        glDrawElements(pri.mode,pri.indices_nr,pri.type,pri.indices_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        

        
    def create_node_geometry(self, node_position, node_size, node_shape):
        """ Takes the node attributes and produces the numpy arrays
        in memory that we will use for OpenGL """
        
        # nr of nodes
        nr_nodes = len(node_position)       
        
        # the new vertices array
        # the new quad faces index array
        
        # create an affine array
        self.node_affines = np.array( (4,4, nr_nodes) )
        
        for i in xrange(nr_nodes):
            pass
        
        

        

            
        
        