import OpenGL.GL as gl

import OpenGL.GLU as glu

import OpenGL.GLUT as glut


class Label(object):

    def __init__(self,points,labels,colors):

        self.list_index = None

        self.points = points

        self.labels = labels

        self.colors = colors


    def init(self):


        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index, gl.GL_COMPILE)

        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        #gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)

        gl.glDisable(gl.GL_LIGHTING)

        gl.glColor3f(1,1,0)
        
        glut.glutSolidSphere(50.,50,50)
        
        for i in range(len(self.points)):


            r,g,b = self.colors[i]

            print r,g,b

            gl.glColor3f(r,g,b)

            x,y,z = self.points[i]

            print x,y,z

            gl.glRasterPos3f(x,y,z)

            label = self.labels[i]

            print label

            for c in label:

                print c

                glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

        gl.glEnable(gl.GL_LIGHTING)

        gl.glEnd()


    def display(self):

        #gl.glPushMatrix()

        print self.list_index

        #gl.glLoadIdentity()

        gl.glCallList(self.list_index)

        #gl.glPopMatrix()



