import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

from fos.core.utils import list_indices as lind

class BrainSurface(object):

    def __init__(self):

        #self.rname='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'

        self.fname='/home/eg309/./Desktop/rh.pial.vtk'
        
        self.position  = [0.0, 0.0, 0.0]

        self.scale     = None #[100., 50., 20.]

        self.ambient   = [0.0, 0.0, 0.2, 1.]
        
        self.diffuse   = [0.0, 0.0, 0.7, 1.]
        
        self.specular  = [0.2, 0.2, 0.7, 1.]

        self.shininess = 50.

        self.emission  = [0.2, 0.2, 0.2, 0]
        
        self.list_index = None
        
        self.name_index = None


    def load_from_disk_using_mayavi(self):

        try:

            import enthought.mayavi.tools.sources as sources
            
            from enthought.mayavi import mlab

        except:

            ImportError('Sources module from enthought.mayavi is missing')
        
        src=sources.open(self.rname)

        surf=mlab.pipeline.surface(src)
        
        pd=src.outputs[0]
                
        pts=pd.points.to_array()
        
        polys=pd.polys.to_array()

        lpol=len(polys)/4
        
        polys=polys.reshape(lpol,4)

        return pts,polys

    def load_from_disk(self):

        f=open(fname,'r')
        lines=f.readlines()

        

        #iP=[si for si in lind(lines,'POINTS')]

            
        
        st='POINTS 167501 float\n'
        st.split()
        st2='19.154478  -87.738876  -15.894387\n'
        st2.split()
        float(st2.split())
        st
        st.startswith('POINTS')

        open(self.rname)
        

    def init(self):        

        pts,polys=self.load_from_disk()

        print pts.shape, polys.shape
        

        pass

class Collection(object):

    def __init__(self):

        self.position  = [0.0, 0.0, -350.0]

        self.scale     = None #[100., 50., 20.]

        self.ambient   = [0.0, 0.0, 0.2, 1.]
        
        self.diffuse   = [0.0, 0.0, 0.7, 1.]
        
        self.specular  = [0.2, 0.2, 0.7, 1.]

        self.shininess = 50.

        self.emission  = [0.2, 0.2, 0.2, 0]

        self.list_index = None

        self.name_index = None

        self.gridx = None
        
        self.gridy = None
        
        self.gridz = None

        self.is3dgrid = True


    def init(self):


        self.list_index = gl.glGenLists(1)

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

        #glut.glutSolidTeapot(20.0)

        gl.glPopMatrix()

        gl.glEndList()

        if self.is3dgrid:

            x,y,z=np.mgrid[-200:200:5j,-200:200:5j, -200:200:5j]

            self.gridz=z.ravel()
        
        else:

            x,y=np.mgrid[-200:200:5j,-200:200:5j]

        self.gridx=x.ravel()
        
        self.gridy=y.ravel()
        
        
        print self.list_index


    def glyph(self,x,y,z):

        gl.glPushMatrix()
    
        #gl.glLoadIdentity()

        #x,y,z=self.position
        
        gl.glTranslatef(x,y,z)
        
        #gl.glRotatef(30*np.random.rand(1)[0],0.,1.,0.)
    
        gl.glCallList(self.list_index)
    
        gl.glPopMatrix()
        

    def display(self,mode=gl.GL_RENDER):

        gl.glInitNames()
        
        gl.glPushName(0)

        for i in range(len(self.gridx)):

            x=self.gridx[i]
            
            y=self.gridy[i]

            if self.is3dgrid:
            
                z=self.gridz[i]

            else:

                z=0

            if mode == gl.GL_SELECT:

                gl.glLoadName(i+1)

            self.glyph(x+self.position[0],y+self.position[1],z+self.position[2])
            

            

rsurf=BrainSurface()

rsurf.init()        
       

    


