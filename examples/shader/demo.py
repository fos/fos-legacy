from sys import exit

from fos.lib.pyglet import app, gl
from fos.lib.pyglet.event import EVENT_HANDLED
from fos.lib.pyglet.window import Window
from fos.shader import Shader
from fos.shader.lib import get_shader_code

# load the shaders
shader = Shader( [get_shader_code('zoomRotate.vert')],
                 [get_shader_code('allGreen.frag')] )
                 
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-width/2, width/2, -height/2, height/2, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    return EVENT_HANDLED


def draw_red_square():
    gl.glColor3ub(127, 0, 0)
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(-10, -10)
    gl.glVertex2f(10, -10)
    gl.glVertex2f(10, 10)
    gl.glVertex2f(-10, 10)
    gl.glEnd()


def on_draw(win):
    win.clear()
    
    # bind the shader
    shader.bind()
    
    draw_red_square()
    
    # unbind the shader
    shader.unbind()
    
def main():
    win = Window(fullscreen=False)
    win.on_resize = on_resize
    
    try:
        win.on_draw = lambda: on_draw(win)
        app.run()
    finally:
        win.close()

if __name__ == '__main__':
    exit(main())
