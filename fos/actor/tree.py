import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor

from fos.shader import Shader
from fos.shader.lib import get_shader_code

# load the shaders
shader = Shader( [get_shader_code('propagatevertex.vert')],
                 ##   [get_shader_code('zoomRotate.vert')],
                 [get_shader_code('allRed.frag')],
                 [get_shader_code('LineToTube.geom'), gl.GL_LINES, gl.GL_TRIANGLE_STRIP, 6]
                 #[]
                  )

class Tree(Actor):
    
    def __init__(self, vertices,
                 connectivity,
                 colors = None,
                 affine = None,
                 force_centering = False,
                 *args, **kwargs):
        """ A tree
        
        vertices : Nx3
            3D Coordinates x,y,z
        connectivity : Mx1
            Tree topology
        colors : Nx4 or 1x4
            Per vertex color, or actor color
        affine : 4x4
            Affine transformation of the actor

        """
        super(Tree, self).__init__()
        
        self.affine = np.eye(4, dtype = np.float32)
        self._update_glaffine()
        
        self.vertices = vertices
        if force_centering:
            self.vertices = self.vertices - np.mean(self.vertices, axis = 0)
        self.connectivity = connectivity
        
        if colors == None:
            # default colors
            self.colors = np.array( [[255,255,255,255]], dtype = np.float32).repeat(len(self.vertices),axis=0) / 255.
        else:
            if len(colors) == 1:
                self.colors = np.array( [colors], dtype = np.float32).repeat(len(self.vertices),axis=0) / 255.
            else:
                assert(len(colors) == len(self.vertices))
                self.colors = colors
            
        self.make_aabb(margin = 0)
        
        # create indicies, seems to be slow with nested loops
        self.indices = connectivity.astype( np.uint32 )
        self.indices_ptr = self.indices.ctypes.data
        self.indices_nr = self.indices.size
        
        # duplicate colors to make it "per vertex"
       # self.colors = self.colors.repeat(2, axis = 0)
        self.colors_ptr = self.colors.ctypes.data
        
        self.vertices_ptr = self.vertices.ctypes.data
        self.mode = GL_LINES
        self.type = GL_UNSIGNED_INT
        
        # VBO related
        self.vertex_vbo = GLuint(0)        
        glGenBuffers(1, self.vertex_vbo)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        # copy the vertex data to our buffer
        #glBufferData(GL_ARRAY_BUFFER, ADT.arrayByteCount(circle), ADT.voidDataPointer(circle), GL_STATIC_DRAW_ARB)
        #glBufferData(GL_ARRAY_BUFFER, 8 * sizeof(GLfloat), diamond, GL_STATIC_DRAW);
        # print "vertices size", self.vertices.size
        
        # 4 * because float32 has 4 bytes
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.vertices.size, self.vertices_ptr, GL_STATIC_DRAW)
        
        # /* Specify that our coordinate data is going into attribute index 0, and contains three floats per vertex */
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);

        
        print "vertices", self.vertices
        print "vertices size", self.vertices.size
        print "vertices dtype", self.vertices.dtype

        # for indices
        self.indices_vbo = GLuint(0)
        glGenBuffers(1, self.indices_vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        # uint32 has 4 bytes
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.indices_nr, self.indices_ptr, GL_STATIC_DRAW)

        # for colors
        self.colors_vbo = GLuint(0)        
        glGenBuffers(1, self.colors_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.colors_vbo)
        
        print "colors", self.colors
        print "colors size", self.colors.size
        print "colors dtype", self.colors.dtype
        
        glBufferData(GL_ARRAY_BUFFER, 4 * self.colors.size, self.colors_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, 0);

        # encapsulate vbo
        # http://www.siafoo.net/snippet/185

        
    def update(self, dt):
        pass
        
    def draw_shader(self):

#        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
#        glBindBuffer(GL_ARRAY_BUFFER, self.colors_vbo)

        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(1.0, 1.0, 1.0, 0.0)

        # bind the shader
        shader.bind()
                
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
       # glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, 0)
        
        # bind the indices buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        
        glDrawElements(self.mode,self.indices_nr,self.type,0)
    
        # unbind the shader
        shader.unbind()
        
    def draw_va(self):
        
        glPushMatrix()
    
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glMultMatrixf(self.glaffine)
        
        glLineWidth(2.0)
        glEnableClientState(GL_VERTEX_ARRAY)
        #glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices_ptr)
        #glColorPointer(4, GL_UNSIGNED_BYTE, 0, self.colors_ptr)
        glDrawElements(self.mode,self.indices_nr,self.type,self.indices_ptr)
        #glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        
        glDisable(GL_LINE_SMOOTH)

        glPopMatrix()
        
    def draw_immediate(self):

        glColor3ub(127, 0, 0)
        
        glBegin(gl.GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(100, 100, 0)
        glVertex3f(100, 100, 0)
        glVertex3f(150, 200, 0)
        glEnd()

        
    def draw(self):

        self.draw_shader()


