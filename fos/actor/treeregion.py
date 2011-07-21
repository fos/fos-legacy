
import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor
from fos.shader import Shader, get_vary_line_width_shader, get_propagate_shader

from fos.shader.vsml import vsml

from ctypes import byref
def gen_texture():
    id = GLuint()
    glGenTextures(1, byref(id))
    return id


class TreeRegion(Actor):

    def __init__(self,
                 vertices,
                 connectivity,
                 colors = None,
                 radius = None,
                 affine = None):
        """ A TreeRegion, composed of many trees

        vertices : Nx3
            3D Coordinates x,y,z
        connectivity : Mx1
            Tree topology
        colors : Nx4 or 1x4
            Per connection color
        radius : N
            Per vertex radius
        affine : 4x4
            Affine transformation of the actor

        """
        super(TreeRegion, self).__init__()

        if affine is None:
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine
        #self._update_glaffine()

        self.vertices = vertices
        self.connectivity = connectivity

        # unfortunately, we need to duplicate vertices if we want per line color
        self.vertices = self.vertices[self.connectivity,:]

        # we have a simplified connectivity now
        self.connectivity = np.array( range(len(self.vertices)), dtype = np.uint32 )

        # this coloring section is for per/vertex color
        if colors is None:
            # default colors for each line
            self.colors = np.array( [[1.0, 0.0, 0.0, 1.0]], dtype = np.float32).repeat(len(self.connectivity)/2, axis=0)
        else:
            # colors array is half the size of the connectivity array
            assert( len(self.connectivity)/2 == len(colors) )
            self.colors = colors

        # we want per line color
        # duplicating the color array, we have the colors per vertex
        self.colors =  np.repeat(self.colors, 2, axis=0)

        # the sample 1d texture data array
        if not radius is None:
            self.mytex = radius.astype( np.float32 )
        else:
            self.mytex = np.ones( len(self.vertices), dtype = np.float32 )
           # self.mytex = np.random.randint(1,5, (len(self.vertices),)).astype(np.float32)

        print "number of vertex rows", self.vertices.shape
        print "number of color rows", self.colors.shape
        print "number of width rows", self.mytex.shape
        print "number of indices rows", self.connectivity.shape

        # create indicies, seems to be slow with nested loops
        self.indices = self.connectivity
        self.indices_ptr = self.indices.ctypes.data
        self.indices_nr = self.indices.size

        # duplicate colors to make it "per vertex"
        self.colors_ptr = self.colors.ctypes.data

        self.vertices_ptr = self.vertices.ctypes.data
        self.mode = GL_LINES
        self.type = GL_UNSIGNED_INT

        # VBO related
        self.vertex_vbo = GLuint(0)
        glGenBuffers(1, self.vertex_vbo)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.vertices.size, self.vertices_ptr, GL_STATIC_DRAW)

        # /* Specify that our coordinate data is going into attribute index 0, and contains three floats per vertex */
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        # for colors
        self.colors_vbo = GLuint(0)
        glGenBuffers(1, self.colors_vbo)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.colors.size, self.colors_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        # for indices
        self.indices_vbo = GLuint(0)
        glGenBuffers(1, self.indices_vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        # uint32 has 4 bytes
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.indices_nr, self.indices_ptr, GL_STATIC_DRAW)

        self.shader = get_vary_line_width_shader()

        # check if we allow to enable texture for radius information
        self.tex_size = int( np.sqrt( self.mytex.size ) ) + 1
        print "required squared size for texture", self.tex_size

        # maximum 2d texture
        myint = GLint(0)
        glGetIntegerv(GL_MAX_TEXTURE_SIZE, myint)
        self.max_tex = myint.value

        if self.tex_size < self.max_tex:
            self.mytex_ptr = self.mytex.ctypes.data
            self.use_tex = True
            self.mytex.resize( self.tex_size )
            self.mytex_ptr = self.mytex.ctypes.data
            self.init_texture_2d()
            print("Initialized texture 2d")
        else:
            raise Exception("Too many vertices to use texture for radius mapping")


    def init_texture(self):
        # self.tex_unit = gen_texture()
        self.tex_unit = GLuint()
        glGenTextures(1, byref(self.tex_unit))

        glBindTexture(GL_TEXTURE_1D, self.tex_unit)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # target, level, internalformat, width, border, format, type, pixels
        glTexImage1D(GL_TEXTURE_1D, 0, GL_LUMINANCE32F_ARB, self.mytex.size, 0, GL_LUMINANCE, GL_FLOAT, self.mytex_ptr)
        glBindTexture(GL_TEXTURE_1D, 0)

    def init_texture_2d(self):
        # self.tex_unit = gen_texture()
        self.tex_unit = GLuint()
        glGenTextures(1, byref(self.tex_unit))

        glBindTexture(GL_TEXTURE_2D, self.tex_unit)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # target, level, internalformat, width, border, format, type, pixels
        glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE32F_ARB, self.tex_size, self.tex_size, 0, GL_LUMINANCE, GL_FLOAT, self.mytex_ptr)
        glBindTexture(GL_TEXTURE_2D, 0)

    def update(self, dt):
        pass


    def draw_vbo(self):

        import pdb; pdb.set_trace()

        # bind the shader
        self.shader.bind()

        self.shader.uniform_matrixf( 'projMatrix', vsml.get_projection())
        self.shader.uniform_matrixf( 'modelviewMatrix', vsml.get_modelview())

        self.shader.uniformi( 'textureWidth', self.tex_size)
        self.shader.uniformi( 'widthSampler', 0)

        # load uniform variables defined as sampler types
        # 0 denotes texture unit 0
        #glUniform1i(self.shader.width_sampler, 0)

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnable(GL_TEXTURE_2D)

        if self.use_tex:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.tex_unit)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        # bind the indices buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)

        glDrawElements(self.mode,self.indices_nr,self.type,0)

        # unbind the shader
        self.shader.unbind()

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisable(GL_TEXTURE_2D)

    def draw(self):

        self.draw_vbo()

    def draw_all(self):
#        import pdb; pdb.set_trace()
        # bind the shader
        self.shader.bind()

        self.shader.uniform_matrixf( 'projMatrix', vsml.get_projection())
        self.shader.uniform_matrixf( 'modelviewMatrix', vsml.get_modelview())

        self.shader.uniformi( 'textureWidth', self.tex_size)
        
        glUniform1i(self.shader.width_sampler, 0)

        if self.use_tex:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.tex_unit)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        # bind the indices buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)

        glDrawElements(self.mode,self.indices_nr,self.type,0)

        # unbind the shader
        self.shader.unbind()

