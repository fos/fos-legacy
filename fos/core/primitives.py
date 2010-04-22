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

from dipy.core import track_metrics as tm

import fos.core.collision as cll

data_path = pjoin(os.path.dirname(__file__), 'data')

#=======================================================

class Tracks3D(object):

    def __init__(self,fname,colormap=None, line_width=3.):

        self.position = (0,0,0)

        self.fname = fname
        
        self.manycolors = True
        
        self.bbox = None

        self.list_index = None

        self.affine = None

        self.data = None

        self.list_index = None

        self.rot_angle = 0

        self.colormap = None

        self.ambient   = [0.0, 0.0, 0.2, .1]
        
        self.diffuse   = [0.0, 0.0, 0.7, .1]
        
        self.specular  = [0.2, 0.2, 0.7, .1]

        self.shininess = 50.

        self.emission  = [0.2, 0.2, 0.2, 0]
        
        self.min = None
         
        self.max = None

        self.mean = None

        self.min_length = 20.

        self.angle = 0.

        self.angular_speed = .5

        self.line_width = line_width

        self.opacity = 1.

        self.near_pick = None

        self.far_pick = None

        self.near_pick_prev = None

        self.far_pick_prev = None

        self.picked_track = None

        self.pick_color = [1,1,0]

        self.brain_color = [1,0,0]

        self.yellow_indices = None

        self.dummy_data = False

        self.data_subset = None

        self.picking_example = False

        

    def init(self):

        import dipy.io.trackvis as tv

        lines,hdr = tv.read(self.fname)

        ras = tv.aff_from_hdr(hdr)

        self.affine=ras

        tracks = [l[0] for l in lines]

        if self.yellow_indices != None :

            tracks = [t for t in tracks if tm.length(t) > 20]

        print 'tracks loaded'

        #self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]#tracks[:20000]

        if self.dummy_data:

            self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]

        if self.data_subset!=None:

            self.data = tracks[self.data_subset[0]:self.data_subset[1]]

        else:

            self.data = tracks

        data_stats = np.concatenate(tracks)

        self.min=np.min(data_stats,axis=0)
         
        self.max=np.max(data_stats,axis=0)

        self.mean=np.mean(data_stats,axis=0)

        del data_stats
        
        del lines

        self.multiple_colors()

        #self.material_color()

               
 

    def display(self):


        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)             
              
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
      

        gl.glPushMatrix()
    
        x,y,z=self.position

        if self.picking_example!=True:


            gl.glRotatef(-90,1,0,0)

            gl.glRotatef(self.angle,0,0,1)

            gl.glTranslatef(x,y,z)
    

        if self.angle < 360.:

            self.angle+=self.angular_speed
            
        else:

            self.angle=0.
        
        gl.glCallList(self.list_index)           

        if self.picked_track != None:

            self.display_one_track(self.picked_track)

        

        if self.yellow_indices != None:

            #print len(self.data)
            #print self.data[0].shape

            for i in self.yellow_indices:

                #print len(self.data[i])

                self.display_one_track(i)

            #print
            #print
            #print
            

        

        gl.glPopMatrix()

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]
        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print self.picked_track


    def display_one_track(self,track_index,color4=np.array([1,1,0,1],dtype=np.float32)):
        

        gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        gl.glLineWidth(7.)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        gl.glColor4fv(color4)

        #gl.glColor3fv(color3)

        d=self.data[track_index].astype(np.float32)

        gl.glVertexPointerf(d)
                               
        gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnable(gl.GL_LIGHTING)
        
        gl.glPopMatrix()



    def multiple_colors(self):

        from dipy.viz.colormaps import boys2rgb

        from dipy.core.track_metrics import mean_orientation, length, downsample

        colors=np.random.rand(1,3).astype(np.float32)

        print colors

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        #gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_NICEST)

        gl.glLineWidth(self.line_width)


        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        for d in self.data:

            if length(d)> self.min_length:
            
                #mo=mean_orientation(d)

                if self.manycolors:
                
                    ds=downsample(d,6)

                    mo=ds[3]-ds[2]

                    mo=mo/np.sqrt(np.sum(mo**2))

                    mo.shape=(1,3)
            
                    color=boys2rgb(mo)

                    color4=np.array([color[0][0],color[0][1],color[0][2],self.opacity],np.float32)
                    gl.glColor4fv(color4)

                else:

                    color4=np.array([self.brain_color[0],self.brain_color[1],\
                                         self.brain_color[2],self.opacity],np.float32)

                    gl.glColor4fv(color4)
                    

                gl.glVertexPointerf(d)
                               
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnable(gl.GL_LIGHTING)
        
        gl.glPopMatrix()

        gl.glEndList()
 
    def material_color(self):

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glPushMatrix()

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glPopMatrix()    

        gl.glEndList()

   


        


#=========================================================================


class Image2D(object):

    def __init__(self,fname):


        self.position = [0,0,0]

        self.fname = fname

        #self.fname = pjoin(os.path.dirname(__file__), 'tests/data/small_latex1.png')

        print self.fname

        #'/home/eg01/Desktop/small_latex1.png'

        self.size = None

        self.win_size = None

        self.data = None

        self.alpha = 255 #None # 0 - 255

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
    
#===============================================================

class DummyPlane(object):

    def __init__(self):

        self.position = (0.,0.,0.)

    def init(self):

        self.list_index = gl.glGenLists(1)

        gl.glNewList(self.list_index, gl.GL_COMPILE)

        gl.glPushMatrix()

        d=np.array([[-100,100,0],[100,100,0],[100,-100,0],[-100,-100,0]]).astype(np.float32)

        indices = np.array([0,1,2,3]).astype(np.ubyte)

        gl.glDisable(gl.GL_LIGHTING)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        gl.glColor3fv([1.,0.,0.])

        gl.glVertexPointerd(d)

        gl.glDrawElements(gl.GL_QUADS, 4, gl.GL_UNSIGNED_BYTE, indices)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnable(gl.GL_LIGHTING)

        gl.glPopMatrix()
        

        gl.glEndList()


    def display(self):

        gl.glPushMatrix()
    
        #gl.glLoadIdentity()

        x,y,z=self.position
        
        gl.glTranslatef(x,y,z)        
            
        gl.glCallList(self.list_index)
    
        gl.glPopMatrix()


#===================================================================
    
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
            

            

       

    


