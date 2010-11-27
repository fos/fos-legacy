from __future__ import with_statement
from contextlib import nested

import pyglet
from gletools import (
    ShaderProgram, FragmentShader, VertexShader, Depthbuffer,
    Texture, Projection, UniformArray, Lighting, Color
)
from gletools.gl import *
from util import Mesh, Processor, Kernel, offsets, gl_init
from gaussian import Gaussian

### setup ###

window = pyglet.window.Window()
projection = Projection(0, 0, window.width, window.height, near=18, far=50)
texture = Texture(window.width, window.height, GL_RGBA32F)
bunny = Mesh('meshes/brain')
processor = Processor(texture)

### Shaders and helpers ###

depth = ShaderProgram(
    VertexShader.open('shaders/normal.vert'),
    FragmentShader.open('shaders/depth.frag'),
)

average = ShaderProgram(
    VertexShader.open('shaders/normal.vert'),
    FragmentShader.open('shaders/convolution.frag'),
    kernel_size = 3*3,
    kernel = UniformArray(float, 1, [
        1,  1,  1,
        1,  1,  1,
        1,  1,  1,
    ]),
    output_factor = 1.0/9.0,
    input_factor = 1.0,
    offsets = offsets(-1, 1, window),
)

laplace = ShaderProgram(
    FragmentShader.open('shaders/convolution.frag'),
    kernel_size = 3*3,
    kernel = UniformArray(float, 1, [
        -1, -1, -1,
        -1,  8, -1,
        -1, -1, -1,
    ]),
    input_factor = 100.0,
    output_factor = 1.0/9.0,
    offsets = offsets(-1, 1, window),
)

invert = ShaderProgram(
    FragmentShader.open('shaders/invert.frag'),
)

### Application code ###

angle = 0.0
def simulate(delta):
    global angle
    angle += 10.0 * delta
pyglet.clock.schedule_interval(simulate, 0.01)


@window.event
def on_draw():
    window.clear()
    
    with nested(processor.renderto(texture), projection, Lighting, Color, depth):
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        glTranslatef(0, 0, -40)
        glRotatef(-65, 1, 0, 0)
        glRotatef(angle, 0.0, 0.0, 1.0)
        glRotatef(90, 1, 0, 0)
        glColor4f(0.5, 0.0, 0.0, 1.0)
        bunny.draw()
        glPopMatrix()

    processor.filter(texture, laplace)
    processor.filter(texture, invert)
    processor.blit(texture)

if __name__ == '__main__':
    gl_init()
    pyglet.app.run()
