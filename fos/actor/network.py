import numpy as np

from fos.core.world import World
from fos.lib.pyglet.gl import *
from fos.core.actor import Actor
from .primitives.network_primitives import NodeGLPrimitive, EdgeGLPrimitive
        
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
        
        edge_width_granularity
            Idea: Subdivide the weight histogram into different
            bins with their own line width
        
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
#        print "dt", dt
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
        
        

        

            
        
        