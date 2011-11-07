import numpy as np

from fos.lib.pyglet.gl import *
from fos import Actor, World

class Axes(Actor):

    def __init__(self, scale = 1.0):
        """ Draw three axes
        """
        super(Axes, self).__init__()

        self.scale = scale
        
        self.show_aabb = False        
        self.make_aabb((np.array([-scale,-scale,-scale]),np.array([scale,scale,scale])),margin = 0)
        


    def update(self, dt):
        pass


    def draw(self):

        glPushMatrix()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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
        if self.show_aabb:self.draw_aabb()
        glPopMatrix()
