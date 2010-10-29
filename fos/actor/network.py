from itertools import chain, islice, product, repeat

from fos.lib.pyglet.gl import gl
from fos.core.actor import Actor
from fos.geometry.vec3 import Vec3
from fos.geometry.glyph import Glyph

type_to_enum = {
    gl.GLubyte: gl.GL_UNSIGNED_BYTE,
    gl.GLushort: gl.GL_UNSIGNED_SHORT,
    gl.GLuint: gl.GL_UNSIGNED_INT,
}

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
        
        node_label
            Node labels
        
        node_size
            The size of the node
            
        node_shape
            cube, sphere, pyramid, electrodes (cylinders)
            
        node_color : (N,3)
            The color of the nodes
            Either given [0,1] or [0,255]
            (or: cmap, vmin, vmax)
            
        node_alpha
            The node transparency
        
        -> node_color -> RGBA
        
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
            
        edge_color
            The color of the edges
            (or cmap, vmin, vmax)
            
        edge_style
            solid, dashed, dotted, dashdot
            What does OpenGL support natively?
            
        edge_alpha
            The transparency of the edge
            
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
        if kwargs.has_key('node_position'):
            print kwargs['node_position']
            
        size = 100.0
        
        e2 = size / 2
        vertices = list(product(*repeat([-e2, +e2], 3)))
        faces = [
            [0, 1, 3, 2], # left
            [4, 6, 7, 5], # right
            [7, 3, 1, 5], # front
            [0, 2, 6, 4], # back
            [3, 7, 6, 2], # top
            [1, 0, 4, 5], # bottom
        ]
        
        if len(vertices) > 0 and not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]
        self.vertices = vertices

        for face in faces:
            assert len(face) >= 3
            for index in face:
                assert 0 <= index < len(vertices)
        self.faces = faces
        
        # make an actor / glyph
        
        self.glyph = Glyph()
        self.glyph.from_shape(self.vertices, self.faces)
        
    def draw(self):
        
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
    

        gl.glPushMatrix()

#        gl.glTranslatef(*item.position)

#        gl.glMultMatrixf(item.orientation.matrix)

        gl.glScalef(20.0, 20.0, 20.0)
                
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.glyph.glvertices)
        gl.glNormalPointer(gl.GL_FLOAT, 0, self.glyph.glnormals)
        gl.glDrawElements(
            gl.GL_TRIANGLES,
            len(self.glyph.glindices),
            type_to_enum[self.glyph.glindex_type],
            self.glyph.glindices)

        gl.glPopMatrix()
        
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
            
        
        