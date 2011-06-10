""" Meaningful composition of shader programs exposed as a library """
__author__ = 'Stephan Gerhard'

from .shaders import Shader
from .lib import get_shader_code
import fos.lib.pyglet.gl as gl

# load the vary-line-width-shader
def get_vary_line_width_shader():
    return Shader( [get_shader_code('propagatevertex130.vert')],
                   [get_shader_code('propagatecolor130.frag')],
                   [get_shader_code('lineextrusion130.geom'), gl.GL_LINES, gl.GL_TRIANGLE_STRIP, 6]
                  )

# load the vary-line-width-shader
def get_simple_shader():
    return Shader( [get_shader_code('propagatevertex130b.vert')],
                   [get_shader_code('propagatecolor130.frag')]
                  )

# load the vary-line-width-shader
def get_propagate_shader():
    return Shader( [get_shader_code('propagatevertex150.vert')],
                   [get_shader_code('propagatecolor150.frag')]
                   #[get_shader_code('lineextrusion130.geom'), gl.GL_LINES, gl.GL_TRIANGLE_STRIP, 6]
                  )
