import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut


class Pyramid(object):


    def __init__(self):

        self.position = [0,0,0]

        self.near_pick = None

        self.far_pick = None

        self.pts = 100*np.array([[0,0,-1],[1,1,-1],[2,0,-1],[1,0.5,-2]],np.float32) -100*np.array([0,0,5],np.float32)

        p=self.pts

        self.triangles=np.array([[p[0],p[1],p[2]], [p[0],p[1],p[3]], [p[1],p[2],p[3]], [p[2],p[0],p[3]] ],np.int)

        self.colours = np.array([[1,0,0,0.2],[0,1,0,0.2],[0,0,1,0.2],[0.75,0.6,0,0.2]],np.float32)

        self.ambient   = [0.55, 0.44, 0.36, 1.]
        
        self.diffuse   = [0.55, 0.44, 0.36, 1.]
        
        self.specular  = [0.55, 0.44, 0.36, 1.]


        
        
    def init(self):

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glDisable(gl.GL_LIGHTING)

        #gl.glColor4fv([1,0,0,1])

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, self.specular )
        
        gl.glBegin(gl.GL_TRIANGLES)

        #


        for (num, tri) in enumerate(self.triangles):
            
            gl.glColor4fv(self.colours[num])

            for vert in tri:
            
                gl.glVertex3fv(vert)

            #gl.glVertex3fv(tri[1])

            #gl.glVertex3fv(tri[2])
                


        #
        gl.glEnd()

        gl.glEnable(gl.GL_LIGHTING)

        gl.glEndList()





    def display(self):

        #glu.gluLookAt(camera[0], camera[1], camera[2], # look from camera XYZ
                  #0, 0, 0, # look at the origin 
                  #0, 1, 0) # positive Y up vector
        
        #gl.glRotatef(orbitDegrees, 0., 1., 0.)
        # orbit the Y axis
        # ...where orbitDegrees is derived from mouse motion  

        self.position[0]+=1

        x,y,z=self.position

        current=gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX )

        gl.glPushMatrix()

        gl.glLoadIdentity()
                
        gl.glTranslatef(x,y,z)

        gl.glRotatef(30.,0,1,0)

        gl.glCallList(self.list_index)

        gl.glPopMatrix()

        gl.glMultMatrixf(current)

             
        
        
        




        
