
from fos.lib.pyglet.gl import *

class WindowText(object):
    '''Display of a flat text in the window
    '''

    def __init__(self, window, caption, x, y, font_size = 20,
                 bold = True, color = (127, 127, 127, 127)):

        from fos.lib.pyglet.text import Label
        self.label = Label(caption, x=x, y=y, font_size=font_size,
                            bold = bold, color = color)
        
        self.window = window

    def draw(self):
        '''Draw the label.

        The OpenGL state is assumed to be at default values, except
        that the MODELVIEW and PROJECTION matrices are ignored.  At
        the return of this method the matrix mode will be MODELVIEW.
        '''
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.window.width, 0, self.window.height, -1, 1)
        
        self.label.draw()

        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
