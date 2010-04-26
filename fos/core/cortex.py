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



class CorticalSurface(object):

    def __init__(self,fname):

       
        self.fname = fname
        
        self.position  = [0.0, 0.0, 0.0]

        self.scale     = None #[100., 50., 20.]

        
        self.ambient   = [0.55, 0.44, 0.36, 1.]
        
        self.diffuse   = [0.55, 0.44, 0.36, 1.]
        
        self.specular  = [0.55, 0.44, 0.36, 1.]

        #self.shininess = 5.

        #self.emission  = [0.1, 0.1, 0.1, 1.]
       
        
        self.list_index = None
        
        self.name_index = None

        self.pts = None

        self.polys = None

        self.normals = None
        


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


    def calculate_normals(self):
        
        p=self.pts

        normals=[]

        for l in self.polys: #[:50000]:

            normal=np.cross(p[l[0]]-p[l[1]],p[l[1]]-p[l[2]])

            normals.append(normal)


        self.normals=np.array(normals,np.float32)

        print self.normals.shape
        
        

    def init2(self):

        self.load_polydata()

        self.calculate_normals()

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glEnable(gl.GL_NORMALIZE)  

        gl.glEnable(gl.GL_BLEND)
      
        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)  

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)

        gl.glVertexPointerf(self.pts)

        #print 'oops'

        gl.glNormalPointerf(self.normals)

        #print 'normals'

        gl.glDrawElements(gl.GL_TRIANGLES,3*4,gl.GL_INT,np.ravel(self.polys).tostring())
    

        #print 'draw'

        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
        
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()

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

        #gl.glEnable(gl.GL_COLOR_MATERIAL)
        
        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, self.specular )

        #gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        #gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)


        gl.glEnable(gl.GL_BLEND)
      
        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        

        gl.glEnable(gl.GL_NORMALIZE)

        gl.glBegin(gl.GL_TRIANGLES)

        for l in self.polys: #[:50000]:

            normal=np.cross(p[l[0]]-p[l[1]],p[l[1]]-p[l[2]])                

            #n(p[l[0]])
            
            n(normal)

            v(p[l[0]])

            #n(p[l[1]])

            n(normal)
            
            v(p[l[1]])

            #n(p[l[2]])

            n(normal)

            v(p[l[2]])        

        gl.glEnd()        
       
        gl.glEndList()

        print 'triangles ready in', time.clock()-time1, 'secs'


    
    def display(self,mode=gl.GL_RENDER):


        #gl.glPushMatrix()

        gl.glCallList(self.list_index)
    
        #gl.glPopMatrix()




    


