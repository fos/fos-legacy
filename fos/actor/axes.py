import numpy as np

from fos.lib.pyglet.gl import *
from fos import Actor, World
from fos.shader.vsml import vsml
from fos.shader.shaderlib import get_simple_shader
import numpy as np

class Axes(Actor):

    def __init__(self, scale = 1.0):
        """ Draw three axes
        """
        super(Axes, self).__init__()

        self.scale = scale

        self.mode = GL_LINES
        self.type = GL_UNSIGNED_INT

        self.vertices = np.array( [ [0,0,0],[5,10,0]], dtype = np.float32 )
        self.connectivity = np.array( [ 0, 1], dtype = np.uint32 )
        self.colors = np.array( [ [0, 1, 0, 1.0], [1, 0, 1, 1.0] ] , dtype = np.float32 )

        self.vertices_ptr = self.vertices.ctypes.data
        self.colors_ptr = self.colors.ctypes.data
        self.indices = self.connectivity
        self.indices_ptr = self.indices.ctypes.data
        self.indices_nr = self.indices.size

        self.vertex_vbo = GLuint(0)
        glGenBuffers(1, self.vertex_vbo)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.vertices.size, self.vertices_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        self.colors_vbo = GLuint(0)
        glGenBuffers(1, self.colors_vbo)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.colors.size, self.colors_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        self.indices_vbo = GLuint(0)
        glGenBuffers(1, self.indices_vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        # uint32 has 4 bytes
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.indices_nr, self.indices_ptr, GL_STATIC_DRAW)

        self.shader = get_simple_shader()


    def draw(self):
        self.shader.bind()

        self.shader.uniform_matrixf( 'projMatrix', vsml.get_projection())
        self.shader.uniform_matrixf( 'modelviewMatrix', vsml.get_modelview())

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        # bind the indices buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)

        glDrawElements(self.mode,self.indices_nr,self.type,0)

        self.shader.unbind()

    def draw2(self):

        glPushMatrix()

        glLineWidth(2.0)

        glBegin (GL_LINES)
        # x axes
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(self.scale,0.0,0.0)
        # y axes
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0,0.0,0.0)
        glVertex3f(0.0,self.scale,0.0)
        # z axes
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0,0.0,0.0)
        glVertex3f(0.0,0.0,self.scale)
        glEnd()
        
        glPopMatrix()