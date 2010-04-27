import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut


class Pyramid(object):


    def __init__(self):

        self.position = [0,0,0]

        self.near_pick = None

        self.far_pick = None

        self.pts = 100*np.array([[0,0,0],[1,1,0],[2,0,0],[1,0.5,1]],np.float32)

        p=self.pts

        self.triangles=np.array([[p[0],p[1],p[2]], [p[0],p[1],p[3]], [p[1],p[2],p[3]], [p[2],p[0],p[3]] ],np.int)

        self.colours = np.array([[255,0,0,255],[0,255,0,255],[0,0,255,255],[127,127,127,255]],np.int)

    def init(self):

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glDisable(gl.GL_LIGHTING)

        gl.glColor3fv([1,0,0])
        
        gl.glBegin(gl.GL_TRIANGLES)

        #


        for (num, tri) in enumerate(self.triangles):
            
            #gl.glColor4iv(self.colours[num])

            for vert in tri:
            
                gl.glVertex3fv(vert)

            #gl.glVertex3fv(tri[1])

            #gl.glVertex3fv(tri[2])
                


        #
        gl.glEnd()

        gl.glEnable(gl.GL_LIGHTING)

        gl.glEndList()





    def display(self):
        
        gl.glCallList(self.list_index)




        
