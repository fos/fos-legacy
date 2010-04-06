import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut




class Collection(object):

    def __init__(self):

        self.position  = [0.0, 0.0, 0.0]

        self.scale     = None #[100., 50., 20.]

        self.ambient   = [0.0, 0.0, 0.2, 1.]
        
        self.diffuse   = [0.0, 0.0, 0.7, 1.]
        
        self.specular  = [0.5, 0.5, 0.5, 1.]

        self.shininess = 50.

        self.emission  = [0.2, 0.2, 0.2, 0]

        self.list_index = None

        self.name_index = None

        self.gridx = None
        
        self.gridy = None
        
        self.gridz = None


    def init(self):


        self.list_index = gl.glGenLists(4)

        print self.list_index

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()
        
        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        #x,y,z = self.scale

        #gl.glScalef(x,y,z)
        
        glut.glutSolidCube(50.0)

        gl.glPopMatrix()

        gl.glEndList()

        x,y,z=np.mgrid[-200:200:5j,-200:200:5j, -200:200:5j]

        self.gridx=x.ravel()
        
        self.gridy=y.ravel()
        
        self.gridz=z.ravel()

        print self.list_index


    def glyph(self,x,y,z):

        gl.glPushMatrix()
    
        #gl.glLoadIdentity()

        #x,y,z=self.position
        
        gl.glTranslatef(x,y,z)
        
        gl.glRotatef(30*np.random.rand(1)[0],0.,1.,0.)
    
        gl.glCallList(self.list_index)
    
        gl.glPopMatrix()
        

    def display(self):

        for i in range(len(self.gridx)):

            x=self.gridx[i]
            
            y=self.gridy[i]
            
            z=self.gridz[i]

            self.glyph(x,y,z)

            

       
        
       
'''

def load_pot():

    #global primno

    global pot
    
    pot=gl.glGenLists(1)

    gl.glNewList(pot,gl.GL_COMPILE)
        
    gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, [0.0, 0.0, 0.2, 1] )

    gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, [0.0, 0.0, 0.7, 1] )

    gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, [0.5, 0.5, 0.5, 1] )

    gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, 50 )

    glut.glutSolidTeapot(50.0)

    gl.glEndList()    

        
    
def render_pot():

    gl.glPushMatrix()
    
    #gl.glLoadIdentity()

    gl.glTranslatef(0.,0.,0.)
    
    gl.glCallList(pot)
    
    gl.glPopMatrix()    

    

def render2_pot():

    gl.glPushMatrix()
    
    #gl.glLoadIdentity()
    
    gl.glTranslatef(100.,0.,0.)
    
    gl.glCallList(pot)
    
    gl.glPopMatrix()
    

    

'''

    

    


