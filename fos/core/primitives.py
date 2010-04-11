import os
import time
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import Image
import PIL.ImageOps as iops
from fos.core.utils import list_indices as lind
from os.path import join as pjoin

data_path = pjoin(os.path.dirname(__file__), 'data')


class Tracks3D(object):

    def __init__(self):

        self.position = (-100,-100,0)

        self.fname = '/home/eg309/Data/Eleftherios/dti_FACT.trk'

        #self.fname =
        #'/home/eg309/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

        self.manycolors = True
        
        self.bbox = None

        self.list_index = None

        self.affine = None

        self.data = None

        self.list_index = None

        self.rot_angle=0

        self.ambient   = [0.0, 0.0, 0.2, 1.]
        
        self.diffuse   = [0.0, 0.0, 0.7, 1.]
        
        self.specular  = [0.2, 0.2, 0.7, 1.]

        self.shininess = 50.

        self.emission  = [0.2, 0.2, 0.2, 0]

        

        

    def init(self):

        import dipy.io.trackvis as tv

        lines,hdr = tv.read(self.fname)

        ras = tv.aff_from_hdr(hdr)

        self.affine=ras

        tracks = [l[0] for l in lines]

        print 'tracks loaded'

        self.data = tracks#[:10000]

        del lines

        if self.manycolors:

            self.multiple_colors()
            #self.line_test()

        else:

            self.one_color()

               
 

    def display(self):

        gl.glPushMatrix()
    
        #gl.glLoadIdentity()

        x,y,z=self.position
        
        gl.glTranslatef(x,y,z)        
            
        gl.glCallList(self.list_index)
    
        gl.glPopMatrix()


    def one_color(self):

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()

        #'''

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        #'''

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glPopMatrix()

        gl.glEndList()

    


    def multiple_colors(self):

        colors=np.random.rand(1,3).astype(np.float32)

        print colors

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        #gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        for d in self.data:

            gl.glColor3fv(np.random.rand(1,3))

            gl.glVertexPointerd(d)

            #gl.glColorPointerd(colors)
            
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        #gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnable(gl.GL_LIGHTING)
        
        gl.glPopMatrix()

        gl.glEndList()
 


        '''


        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()

        colors=np.float32( np.random.rand( 10,3 ))

        colorsin=np.round( 10*np.random.rand( len( self.data ) ) ).astype(np.ubyte)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glColorPointer( 3, gl.GL_FLOAT, 0, colors.tostring( ) )

        #gl.glColorPointerd(colors)

        colorsins=colorsin.tostring()

        print 

        for i,d in enumerate(self.data):
 
            gl.glVertexPointer( 3, gl.GL_FLOAT, 0, d.tostring( ) )

            #gl.glVertexPointerd(d)

            gl.glDrawElements(gl.GL_LINE_STRIP , len(d), gl.GL_UNSIGNED_BYTE, colorsins[i] )
        

        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        
        gl.glPopMatrix()

        gl.glEndList()
  
        '''

    def poly_test(self):

        n=50

        a=np.arange(0,n)

        vertices = np.transpose(
            np.reshape(np.array((np.cos(2*np.pi*a/float(n)), np.sin(3*2*np.pi*a/float(n)))),(2, n)))

        colors=np.ones((n, 3))

        colors[0]=[1,0,0]

        colors[25]=[1,1,0]

        colors.shape = (n, 3)

        

        glClearColor(0.5, 0.5, 0.5, 0)
        
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glOrtho(-1,1,-1,1,-1,1)
        
	glDisable(gl.GL_LIGHTING)
        
	glDrawArrays(gl.GL_LINE_LOOP, 0, n)
        
	glEnable(gl.GL_LIGHTING)

        glVertexPointerd(vertices)
        
	glColorPointerd(colors)
        
	glEnableClientState(GL_VERTEX_ARRAY)
        
	glEnableClientState(GL_COLOR_ARRAY)

        
        gl.glPopMatrix()

        gl.glEndList()



    def line_test(self):
       
        scalar=1.0

        lines=self.data

        colors=None


        if colors!=None:        

            lit=iter(colors)

        else:

            colors=np.random.rand(len(lines),3)

            lit=iter(colors)
    

        self.list_index = gl.glGenLists(1)
        
        gl.glNewList(self.list_index, gl.GL_COMPILE)
        
        nol=0

        gl.glDisable(gl.GL_LIGHTING)

               

        for Line in lines:
        

            inw=True

            mit=iter(Line)

            nit=iter(Line)

            nit.next()
        
            scalar=lit.next()

            gl.glBegin(gl.GL_LINE_STRIP)    

            gl.glColor4f(scalar[0],scalar[1],scalar[2],1.)
            

            while(inw):            

                try:

                    m=mit.next()                                        

                    gl.glVertex3f(m[0], m[1], m[2]) # point                   

                except StopIteration:
                    

                    break


            gl.glEnd()                                
        
            nol+=1

            if nol%1000==0:
                
                print(nol,'Lines Loaded')
        

        gl.glEnable(gl.GL_LIGHTING)
        
        gl.glEndList()
        





class Image2D(object):

    def __init__(self):


        self.position = [0,0,0]

        self.fname = pjoin(os.path.dirname(__file__), 'tests/data/small_latex1.png')

        print self.fname

        #'/home/eg01/Desktop/small_latex1.png'

        self.size = None

        self.win_size = None

        self.data = None

        self.alpha = 50 #None # 0 - 255

        self.rm_blackish = True

        pass

    def init(self):

        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        #x,y,width,height = gl.glGetDoublev(gl.GL_VIEWPORT)
        
	#width,height = int(width),int(height)

        img = Image.open(self.fname)

        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        self.size = img.size

        rgbi=iops.invert(img.convert('RGB'))

        rgbai=rgbi.convert('RGBA')

        if self.alpha != None:

            rgbai.putalpha(self.alpha)

        
        if self.rm_blackish:


            for x,y in np.ndindex(self.size[0],self.size[1]):

                r,g,b,a=rgbai.getpixel((x,y))

                if r<50 and g<50 and b < 50:

                    rgbai.putpixel((x,y),(0,0,0,0))
    
        #for x,y in

        
        self.data=rgbai.tostring()

        x,y,width,height = gl.glGetDoublev(gl.GL_VIEWPORT)
        
	width,height = int(width),int(height)

        self.win_size=(width,height)

        print self.win_size
    

    def display(self):

        #gl.glRasterPos2i(100,0)

        x,y,width,height = gl.glGetDoublev(gl.GL_VIEWPORT)
        
	width,height = int(width),int(height)

        self.win_size=(width,height)

        #print self.win_size
        
        gl.glWindowPos3iv(self.position)

        w,h=self.size

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_ONE,gl.GL_DST_COLOR)

        gl.glDrawPixels(w, h,gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.data)

        gl.glDisable(gl.GL_BLEND)

        
    

class BrainSurface(object):

    def __init__(self):

        self.fname='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'

        #self.fname='/home/eg309/Desktop/rh.pial.vtk'
        
        self.position  = [0.0, 0.0, 0.0]

        self.scale     = None #[100., 50., 20.]

        '''

        self.ambient   = [0.0, 0.0, 0.2, 1.]
        
        self.diffuse   = [0.0, 0.0, 0.7, 1.]
        
        self.specular  = [0.2, 0.2, 0.7, 1.]

        self.shininess = 50.

        self.emission  = [0.2, 0.2, 0.2, 0]

        '''

        '''

        self.ambient   = [0.0, 0.0, 0.2, 1.]
        
        self.diffuse   = [0.0, 0.0, 0.5, 1.]
        
        self.specular  = [0.2, 0.2, 0.2, 1.]

        self.shininess = 10.

        self.emission  = [0., 0., 0.2, 0]

        '''
        
        self.ambient   = [0.55, 0.44, 0.36, 1.]
        
        self.diffuse   = [0.55, 0.44, 0.36, 1.]
        
        self.specular  = [0.1, 0.1, 0.6, 1.]

        self.shininess = 5.

        self.emission  = [0.1, 0.1, 0.1, 1.]
        
        
        
        self.list_index = None
        
        self.name_index = None

        self.pts = None

        self.polys = None
        


    def load_polydata(self):

        f=open(self.fname,'r')
        
        lines=f.readlines()

        taglines=[l.startswith('POINTS') or l.startswith('POLYGONS')  for l in lines]

        pts_polys_tags=[i for i in lind(taglines,True)]

        if len(pts_polys_tags)<2:

            NameError('This must be the wrong file no polydata in.')

        #read points
            
        pts_index = pts_polys_tags[0]
              
        pts_tag = lines[pts_index].split()

        pts_no = int(pts_tag[1])

        pts=lines[pts_index+1:pts_index+pts_no+1]

        self.pts=np.array([np.array(p.split(),dtype=np.float32) for p in pts])

        #read triangles
        
        polys_index = pts_polys_tags[1]

        #print polys_index

        polys_tag = lines[polys_index].split()

        polys_no = int(polys_tag[1])

        polys=lines[polys_index+1:polys_index+polys_no+1]

        self.polys=np.array([np.array(pl.split(),dtype=np.int) for pl in polys])[:,1:]

                

    def init(self):        


        self.load_polydata()

        n=gl.glNormal3fv
        
        v=gl.glVertex3fv

        p=self.pts

        print 'adding triangles'

        time1=time.clock()
        
        #print pts.shape, polys.shape
        
        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()
        
        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnable(gl.GL_NORMALIZE)

        gl.glBegin(gl.GL_TRIANGLES)

        for l in self.polys[:50000]:

            n(p[l[0]])

            v(p[l[0]])

            n(p[l[1]])
            
            v(p[l[1]])

            n(p[l[2]])           

            v(p[l[2]])        

        gl.glEnd()        

        gl.glPopMatrix()

        gl.glEndList()

        print 'triangles ready in', time.clock()-time1, 'secs'


    
    def display(self,mode=gl.GL_RENDER):


        gl.glPushMatrix()
    
        #gl.glLoadIdentity()

        #x,y,z=self.position
        
        #gl.glTranslatef(x,y,z)
        
        #gl.glRotatef(30*np.random.rand(1)[0],0.,1.,0.)
    
        gl.glCallList(self.list_index)
    
        gl.glPopMatrix()

    


    def load_polydata_using_mayavi(self):

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
        
        gl.glRotatef(30*np.random.rand(1)[0],0.,1.,0.)
    
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
            

            

       

    


