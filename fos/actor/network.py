import numpy as np

from fos.lib.pyglet.gl import *
from fos.core.world import World
from fos.lib.pyglet.gl import GLfloat

from fos.core.actor import Actor
from fos.actor.primitives.network_primitives import NodeGLPrimitive, EdgeGLPrimitive
        
class AttributeNetwork(Actor):
    
    def __init__(self, affine = None, force_centering = True, *args, **kwargs):
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
        
        # open questions
        # - pick a node / edge, show info, etc.
        # - dynamic graph with lifetime on nodes/edges
        # - hierarchic graph

        self.node_glprimitive = NodeGLPrimitive()
        self.edge_glprimitive = EdgeGLPrimitive()
        self.aabb_glprimitive = NodeGLPrimitive()
        
        if affine == None:
            # create a default affine
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine
        
        self.glaffine = self._update_glaffine()
        
        if kwargs.has_key('node_position'):
            self.node_position = kwargs['node_position']
        else:
            raise Exception("You have to specify the node_position array")
        

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
            
        if not self.node_position is None:
            nr_nodes = self.node_position.shape[0]
            
            if force_centering:
                self.node_position = self.node_position - np.mean(self.node_position)

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
        if not self.node_position is None and not self.node_size is None:
            assert self.node_position.shape[0] == self.node_size.size
            
            self.node_glprimitive._make_cubes(self.node_position, self.node_size)

            if self.aabb is None:
                # compute aabb
                self._compute_aabb()
            
            if self.obb is None:
                # compute the obb
                self._compute_obb()
                
            self.scale(self.scale_factor)
                        
        if not self.node_color is None:
            self.node_glprimitive._make_color(self.node_color)
            
        if not self.edge_connectivity is None:
            self.edge_glprimitive._make_edges(self.node_position, self.edge_connectivity)
            
        if not self.edge_color is None:
            self.edge_glprimitive._make_color(self.edge_color)
        
        self.living = False
        
        
    def start(self, tickingtime = 2.0):
        print "the actor is alive"
        self.living = True
        self.internal_timestamp = 0.0
        self.tickingtime = tickingtime
        
    def stop(self):
        print "the actor stops living"
        self.living = False
        
    def cont(self):
        print "continue to live happily"
        self.living = True
    
    def set_affine(self, affine):
        # update the affine
        print "update affine", self.affine
        self.affine = affine
        self._update_glaffine()
    
    def scale(self, scale_factor):    
        """ Scales the actor by scale factor.
        Multiplies the diagonal of the affine for
        the first 3 elements """
        self.affine[0,0] *= scale_factor
        self.affine[1,1] *= scale_factor
        self.affine[2,2] *= scale_factor
        self._update_glaffine()
        
    def translate(self, dx, dy, dz):
        """ Translate the actor.
        Remember the OpenGL has right-handed 
        coordinate system """
        self.affine[0,3] += dx
        self.affine[1,3] += dy
        self.affine[2,3] += dz
        self._update_glaffine()
    
    def set_position(self, x, y, z):
        """ Position the actor.
        Remember the OpenGL has right-handed 
        coordinate system """
        self.affine[0,3] += x
        self.affine[1,3] += y
        self.affine[2,3] += z
        self._update_glaffine()
        
    def update(self, dt):
        
        if self.living:
            self.internal_timestamp += dt
            
            if self.internal_timestamp > 10.0:
                print "you lived 10 seconds. this is enough"
                self.stop()
                
                
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

        glPopMatrix()
            
            
            
    def _update_glaffine(self):
        self.glaffine = (GLfloat * 16)(*tuple(self.affine.T.ravel()))
         
    def _compute_aabb(self):

        # using the node_position, node_size to compute the aabb for the cube
        # make it a bit bigger
        nodep = self.node_position
        nodes = self.node_size.max() / 2.0
        
        # two points
        leftbottom = np.array([[nodep[:,0].min(),nodep[:,1].min(),nodep[:,2].min()]], dtype = np.float32) - nodes
        righttop = np.array([nodep[:,0].max(), nodep[:,1].max(),nodep[:,2].max()], dtype = np.float32) + nodes
        
        # subtract the node size
        leftbottom -= nodes
        
        # add the node size
        righttop += nodes

        self.aabb = (leftbottom, righttop)
        
    def _compute_obb(self):
        
        # just reuse the aabb points
        leftbottom, righttop = self.aabb
        
        center = np.mean( np.vstack( (leftbottom, righttop) ), axis = 0)
        halfwidths = (leftbottom - righttop) / 2.0
        # in our default network, this obb is axis-aligned, thus the
        # obb is the identity
        orientation = np.eye( 3, 3 )
         
        self.obb = (center, halfwidths, orientation)
                
        