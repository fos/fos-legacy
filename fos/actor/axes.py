import numpy as np

from fos.lib.pyglet.gl import *
from fos import Actor, World
from fos.shader.vsml import vsml
from fos.shader import Shader, get_simple_shader

class Axes(Actor):

    def __init__(self, scale = 1.0):
        """ Draw three axes
        """
        super(Axes, self).__init__()

        self.scale = scale

        self.shader = get_simple_shader()


    def update(self, dt):
        pass


    def draw(self):

        if vsml.DEBUG:
            print "draw axes", self.scale
            print "vsml modelview is ", vsml.modelview
            print "vsml projection is ", vsml.projection

        #self.shader.bind()
#
#        vsml.pushMatrix(vsml.MatrixTypes.MODELVIEW)
        
        glPushMatrix()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glLoadMatrix(vsml.get_modelview())

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glLoadMatrix(vsml.get_projection())

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
        
        glPopMatrix()
#        vsml.popMatrix(vsml.MatrixTypes.MODELVIEW)
#
#        self.shader.unbind()