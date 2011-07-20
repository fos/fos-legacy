import numpy as np

from fos.lib.pyglet.gl import *
from fos import Actor, World
from fos.shader.vsml import vsml

class Axes(Actor):

    def __init__(self, scale = 1.0):
        """ Draw three axes
        """
        super(Axes, self).__init__()

        self.scale = scale

    def draw(self):
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