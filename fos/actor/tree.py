import numpy as np

from fos.lib.pyglet.gl import *
#from pyglet.gl import *

from fos import Actor
from fos.shader import Shader
from fos.shader.lib import get_shader_code

# load the shaders
def get_shader():
    return Shader( [get_shader_code('propagatevertex130.vert')],
                   [get_shader_code('propagatecolor130.frag')],
                   [get_shader_code('lineextrusion130.geom'), gl.GL_LINES, gl.GL_TRIANGLE_STRIP, 6]
                  )

from ctypes import byref
def gen_texture():
    id = GLuint()
    glGenTextures(1, byref(id))
    return id

class Tree(Actor):
    
    def __init__(self, vertices,
                 connectivity,
                 colors = None,
                 vertices_width = None,
                 affine = None,
                 force_centering = False,
                 *args, **kwargs):
        """ A tree
        
        vertices : Nx3
            3D Coordinates x,y,z
        connectivity : Mx1
            Tree topology
        colors : Nx4 or 1x4
            Per connection color
        vertices_width : N
            Per vertex width
        affine : 4x4
            Affine transformation of the actor

        """
        super(Tree, self).__init__()
        
        self.affine = np.eye(4, dtype = np.float32)
        #self._update_glaffine()
        
        self.vertices = vertices
        if force_centering:
            self.vertices = self.vertices - np.mean(self.vertices, axis = 0)

        self.connectivity = connectivity

        # unfortunately, we need to duplicate vertices if we
        # want per line color
        self.vertices = self.vertices[self.connectivity,:]

        # we want per line color
        # duplicating the color array, we have the colors per vertex
        self.colors =  np.repeat(colors, 2, axis=0)

        # we have a simplified connectivity
        self.connectivity = np.array( range(len(self.vertices)), dtype = np.uint32 )
        

        # this coloring section is for per/vertex color
#        if colors == None:
#            # default colors
#            self.colors = np.array( [[255,255,255,255]], dtype = np.float32).repeat(len(self.vertices),axis=0) / 255.
#        else:
#            if len(colors) == 1:
#                self.colors = np.array( [colors], dtype = np.float32).repeat(len(self.vertices),axis=0) / 255.
#            else:
#                assert(len(colors) == len(self.vertices))
#                self.colors = colors


       # the sample 1d texture data array
        if not vertices_width is None:
            self.mytex = vertices_width.astype( np.float32 )
        else:
            self.mytex = np.ones( len(self.vertices), dtype = np.float32 )

        self.mytex_ptr = self.mytex.ctypes.data
#        self.make_aabb(margin = 0)
        
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
        # copy the vertex data to our buffer
        #glBufferData(GL_ARRAY_BUFFER, ADT.arrayByteCount(circle), ADT.voidDataPointer(circle), GL_STATIC_DRAW_ARB)
        #glBufferData(GL_ARRAY_BUFFER, 8 * sizeof(GLfloat), diamond, GL_STATIC_DRAW);
        # print "vertices size", self.vertices.size
        
        # 4 * because float32 has 4 bytes
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.vertices.size, self.vertices_ptr, GL_STATIC_DRAW)
        
        # /* Specify that our coordinate data is going into attribute index 0, and contains three floats per vertex */
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

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

        glBufferData(GL_ARRAY_BUFFER, 4 * self.colors.size, self.colors_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        print "mytex", self.mytex, self.mytex_ptr, self.mytex.size, self.mytex.dtype
        # texture init
        self.init_texture()

        self.shader = get_shader()

    def init_texture(self):

        self.tex_unit = gen_texture()
        glBindTexture(GL_TEXTURE_1D, self.tex_unit)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage1D(GL_TEXTURE_1D, 0, GL_LUMINANCE32F_ARB, self.mytex.size, 0, GL_LUMINANCE, GL_FLOAT, self.mytex_ptr)

        glBindTexture(GL_TEXTURE_1D, 0)
        
    def update(self, dt):
        pass
        
    def draw(self):

        # bind the shader
        self.shader.bind()

        glUniform1i(self.shader.width_sampler, 0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_1D, self.tex_unit)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)

        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        # bind the indices buffer
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        
        glDrawElements(self.mode,self.indices_nr,self.type,0)

        # unbind the shader
        self.shader.unbind()

