import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor, World
from fos.actor.primitives import NodePrimitive, EdgePrimitive
        
class AttributeNetwork(Actor):
    
    def __init__(self, node_position, affine = None, force_centering = True, *args, **kwargs):
        """ Draw a network
                
        affine : (4,4)
            The affine has a translational and rotational part
        force_centering : bool
            Subtract the mean over node_position from all node positions to center the actor.
        scale_factor : float
            Scaling the actor, scales all the vertices. You might want to multiply
            your node_position array.
        global_node_size : float
            Size for all nodes, used when node_size is None. If None, defaults to 1.0
        global_line_width : float
            The global line width. Defaults to 1.0
        
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
        
        super(AttributeNetwork, self).__init__()
        
        if not node_position is None:
            self.vertices = node_position
        else:
            raise Exception("You have to specify the node_position array")
        
        self.node_glprimitive = NodePrimitive()
        self.edge_glprimitive = EdgePrimitive()
        
        if affine == None:
            # create a default affine
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine
        
        self._update_glaffine()
        
        self.edge_color = None
        if kwargs.has_key('edge_connectivity'):
            self.edge_connectivity = kwargs['edge_connectivity']

            nr_edges = self.edge_connectivity.shape[0]
            
            if kwargs.has_key('edge_color'):
                self.edge_color = kwargs['edge_color']
            else:
                # default edge color
                self.edge_color = np.array( [[255,255,255,255]], dtype = np.ubyte).repeat(nr_edges,axis=0)

        else:
            self.edge_connectivity = None


        if kwargs.has_key('edge_weight'):
            self.edge_weight = kwargs['edge_weight']
        
        if kwargs.has_key('aabb'):
            self.aabb = kwargs['aabb']
        else:
            self.aabb = None
            
        if kwargs.has_key('obb'):
            self.obb = kwargs['obb']
        else:
            self.obb = None
            
        if kwargs.has_key('scale_factor'):
            self.scale_factor = kwargs['scale_factor']
        else:
            self.scale_factor = 1.0

        if kwargs.has_key('global_node_size'):
            self.global_node_size = kwargs['global_node_size']
        else:
            self.global_node_size = 1.0
            
        if kwargs.has_key('global_edge_width'):
            self.global_edge_width = kwargs['global_edge_width']
        else:
            self.global_edge_width = 1.0
            
        if not self.vertices is None:
            nr_nodes = self.vertices.shape[0]
            
            if force_centering:
                self.vertices = self.vertices - np.mean(self.vertices, axis = 0)

            if kwargs.has_key('node_size'):
                self.node_size = kwargs['node_size'].ravel()
            else:
                # default size 1.0
                self.node_size = np.ones( (nr_nodes, 1), dtype = np.float32 ).ravel() * self.global_node_size

            if kwargs.has_key('node_color'):
                self.node_color = kwargs['node_color']
            else:
                # create default colors for nodes
                self.node_color = np.array( [[200,200,200,255]], dtype = np.ubyte).repeat(nr_nodes,axis=0)
            
        # default variables
        self.internal_timestamp = 0.0
        
        # network creation
        ##################
        if not self.vertices is None and not self.node_size is None:
            assert self.vertices.shape[0] == self.node_size.size
            
            self.node_glprimitive._make_cubes(self.vertices, self.node_size)
                
            self.scale(self.scale_factor)
                        
        if not self.node_color is None:
            self.node_glprimitive._make_color(self.node_color)
            
        if not self.edge_connectivity is None:
            
            self.edge_glprimitive._make_edges(self.vertices, self.edge_connectivity)
            
        if not self.edge_color is None:
            self.edge_glprimitive._make_color(self.edge_color)
        
        self.living = False
        
        # create aabb (in actor)
        self.make_aabb(margin = self.node_size.max())


    def update(self, dt):

        if self.living:

            self.internal_timestamp += dt
            
#            if self.internal_timestamp > 50.0:
#                print "you lived 10 seconds. this is enough"
#                self.stop()


            # simulate brownian motion like behaviour
#            self.vertices += np.random.random( (self.vertices.shape) ) * 2
            
            
#            self.node_size = np.random.random( (self.node_size.shape) ) * 2
#            self.node_glprimitive._make_cubes(self.vertices, self.node_size)
#            print "self", self.edge_glprimitive.vertices[0,:]
            
            # this functionality could be implemented with cython

#            nr = self.edge_color.shape[0]
#            ran = np.random.random_integers(0,1, (nr,))
#            self.edge_color[:,3] = np.where(ran > 0, self.edge_color[:,3], 255 - self.edge_color[:,3])
#            self.edge_glprimitive._make_color(self.edge_color)

            # update the edges, e.g. position
#            self.edge_glprimitive._make_edges(self.vertices, self.edge_connectivity)
            
            # update bounding box
            self.make_aabb(margin = self.node_size.max())
        
    def draw(self):
    
        glPushMatrix()
        glMultMatrixf(self.glaffine)
        
        # check if network has edges at all
        pri = self.edge_glprimitive
        if not pri.vertices is None:
            glLineWidth(self.global_edge_width)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, pri.vertices_ptr)
            glColorPointer(4, GL_UNSIGNED_BYTE, 0, pri.color_ptr)
            glDrawElements(pri.mode,pri.indices_nr,pri.type,pri.indices_ptr)
            glDisableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)
        
        # network requires to have nodes
        pri = self.node_glprimitive
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, pri.vertices_ptr)
        glColorPointer(4, GL_UNSIGNED_BYTE, 0, pri.color_ptr)
        glDrawElements(pri.mode,pri.indices_nr,pri.type,pri.indices_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        self.draw_aabb()

        glPopMatrix()

        
        

                
        