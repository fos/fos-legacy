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
import fos.core.tracks as tracks

import fos.core.collision as cll

data_path = pjoin(os.path.dirname(__file__), 'data')



class CorticalSurface(object):

    def __init__(self,fname,angle_table=None):

       
        self.fname = fname
        
        self.position  = [0.0, 0.0, 0.0]

        self.scale     = None #[100., 50., 20.]

        
        self.ambient   = [0.58, 0.46, 0.38, 1.]
        
        self.diffuse   = [0.58, 0.46, 0.38, 1.]
        
        self.specular  = [0.58, 0.46, 0.38, 1.]

        self.shininess = 5.

        self.emission  = [0.1, 0.1, 0.1, 1.]
       
        
        self.list_index = None
        
        self.name_index = None

        self.pts = None

        self.polys = None

        self.normals = None

        self.fadein = False

        self.fadeout = False

        self.fadein_speed = 0.0

        self.fadeout_speed = 0.0

        self.orbit_demo = False

        self.orbit_anglez = 0.

        self.orbit_anglez_rate = 10.


        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 0.
        
        self.angle_table = angle_table

        self.angle_table_index = 0

        
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

        print 'polys.shape', self.polys.shape

        print 'polys[0]', self.polys[0]





    def calculate_normals(self):


        p=self.pts

        print 'pts.shape',p.shape
        

        normals=np.zeros((len(self.pts),3),np.float32)


        l=self.polys
        
        trinormals=np.cross(p[l[:,0]]-p[l[:,1]],p[l[:,1]]-p[l[:,2]],axisa=1,axisb=1)
        

        for (i,lp) in enumerate(self.polys):

            normals[lp]+=trinormals[i]
           
            
        div=np.sqrt(np.sum(normals**2,axis=1))
        
        div=div.reshape(len(div),1)        

        self.normals=(normals/div).astype(np.float32)


        

    def calculate_normals2(self):
        
        p=self.pts

        print 'pts.shape',p.shape
        

        normals=np.zeros((len(self.pts),3),np.float32)

        normalscnt=np.zeros((len(self.pts),1),np.float32)
        

        l=self.polys
        
  
        for l in self.polys:

            normal = np.cross( p[l[0]] - p[l[1]], p[l[1]] - p[l[2]] )

            normal = normal/np.linalg.norm(normal)

            normals[l] += normal
            

        div=np.sqrt(np.sum(normals**2,axis=1))
        
        div=div.reshape(len(div),1)        

        self.normals=(normals/div).astype(np.float32)



    def calculate_normals3(self):
    

        self.normals=cll.calculate_triangle_normals(self.pts,self.polys)
        

    def init(self):

        time1=time.clock()

        self.load_polydata()

        print 'load disk',time.clock() - time1

        self.calculate_normals()

        print 'calc normals', time.clock() - time1

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        #gl.glEnable(gl.GL_NORMALIZE)  

        gl.glEnable(gl.GL_BLEND)
      
        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glDisable(gl.GL_LIGHTING)        

        #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)

        gl.glVertexPointerf(self.pts)

        gl.glNormalPointerf(self.normals)

        triangles=np.ravel(self.polys).astype(np.uint)

        gl.glDrawElementsui(gl.GL_TRIANGLES,triangles)
            
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
  
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()


        print 'time ',time.clock()-time1

    
    def display(self):

        #print self.fadeout
        

        if self.fadein :
            
            self.ambient[3]+=self.fadein_speed
        
            self.diffuse[3]+=self.fadein_speed
        
            self.specular[3]+=self.fadein_speed

        
        if self.fadeout :

            self.ambient[3]-=self.fadeout_speed
        
            self.diffuse[3]-=self.fadeout_speed
        
            self.specular[3]-=self.fadeout_speed
                


        #print self.ambient[3]

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_EMISSION, self.emission )



        ''' WORKING
        
        gl.glPushMatrix()

        if self.orbit_demo:

            self.orbit_anglex+=self.orbit_anglex_rate
        
            gl.glRotatef(self.orbit_anglex,1,0,0)
        

        gl.glPushMatrix()

        if self.orbit_demo:
            

            self.orbit_anglez+=self.orbit_anglez_rate

            gl.glRotatef(self.orbit_anglez,0,0,1)
        

        gl.glCallList(self.list_index)


        gl.glPopMatrix()


        gl.glPopMatrix()

        '''
        
        x,y,z=self.position

        if self.orbit_demo and self.angle_table == None:

            gl.glPushMatrix()

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            #x,y,z=self.position


            gl.glRotatef(self.orbit_anglez,0,0,1)

            gl.glTranslatef(x,y,z) 


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

        elif self.orbit_demo == True and self.angle_table != None:


            gl.glPushMatrix()

            #global angle_table_index

            #global angle_table

            #print 'ati ',tracks.angle_table_index

            

            gl.glRotatef(tracks.angle_table[tracks.angle_table_index,0],1,0,0)

            #x,y,z = self.position
            
            gl.glPushMatrix()

            gl.glRotatef(tracks.angle_table[tracks.angle_table_index,1],0,1,0)

            gl.glPushMatrix()

            gl.glRotatef(tracks.angle_table[tracks.angle_table_index,2],0,0,1)

            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            #angle_table_index += 1

            #if self.angle_table_index >= self.angle_table.shape[0]:
                
            #    self.angle_table_index = self.angle_table.shape[0] - 1
            

            '''

            gl.glRotatef(self.angle_table[self.angle_table_index,0],1,0,0)

            #x,y,z = self.position
            
            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,1],0,1,0)

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,2],0,0,1)

            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            self.angle_table_index += 1

            if self.angle_table_index >= self.angle_table.shape[0]:
                
                self.angle_table_index = self.angle_table.shape[0] - 1

            '''

            

        

        

class CorticalSurfaceStuff(object):

    def __init__(self,fname, angle_table=None):

       
        self.fname = fname
        
        self.position  = [0.0, 0.0, 0.0]

        self.scale     = None #[100., 50., 20.]

        
        self.ambient   = [0.58, 0.46, 0.38, 1.]
        
        self.diffuse   = [0.58, 0.46, 0.38, 1.]
        
        self.specular  = [0.58, 0.46, 0.38, 1.]

        self.shininess = 5.

        self.emission  = [0.1, 0.1, 0.1, 1.]
       
        
        self.list_index = None
        
        self.name_index = None

        self.pts = None

        self.polys = None

        self.normals = None

        self.fadein = False

        self.fadeout = False

        self.fadein_speed = 0.0

        self.fadeout_speed = 0.0

        self.orbit_demo = False

        self.orbit_anglez = 0.

        self.orbit_anglez_rate = 10.


        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 0.

        self.angle_table = angle_table
        
        self.angle_table_index = 0

        if angle_table != None:
            print 'Cortex angle_table shape %s' % str(self.angle_table.shape)

        


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

        print 'polys.shape', self.polys.shape

        print 'polys[0]', self.polys[0]





    def calculate_normals(self):


        p=self.pts

        print 'pts.shape',p.shape
        

        normals=np.zeros((len(self.pts),3),np.float32)


        l=self.polys
        
        trinormals=np.cross(p[l[:,0]]-p[l[:,1]],p[l[:,1]]-p[l[:,2]],axisa=1,axisb=1)
        

        for (i,lp) in enumerate(self.polys):

            normals[lp]+=trinormals[i]
           
            
        div=np.sqrt(np.sum(normals**2,axis=1))
        
        div=div.reshape(len(div),1)        

        self.normals=(normals/div).astype(np.float32)


        

    def calculate_normals2(self):
        
        p=self.pts

        print 'pts.shape',p.shape
        

        normals=np.zeros((len(self.pts),3),np.float32)

        normalscnt=np.zeros((len(self.pts),1),np.float32)
        

        l=self.polys
        
  
        for l in self.polys:

            normal = np.cross( p[l[0]] - p[l[1]], p[l[1]] - p[l[2]] )

            normal = normal/np.linalg.norm(normal)

            normals[l] += normal
            

        div=np.sqrt(np.sum(normals**2,axis=1))
        
        div=div.reshape(len(div),1)        

        self.normals=(normals/div).astype(np.float32)



    def calculate_normals3(self):
    

        self.normals=cll.calculate_triangle_normals(self.pts,self.polys)
        

    def init(self):

        time1=time.clock()

        self.load_polydata()

        print 'load disk',time.clock() - time1

        self.calculate_normals()

        print 'calc normals', time.clock() - time1

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        #gl.glEnable(gl.GL_NORMALIZE)  

        gl.glEnable(gl.GL_BLEND)
      
        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glDisable(gl.GL_LIGHTING)        

        #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)

        gl.glVertexPointerf(self.pts)

        gl.glNormalPointerf(self.normals)

        triangles=np.ravel(self.polys).astype(np.uint)

        gl.glDrawElementsui(gl.GL_TRIANGLES,triangles)
            
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
  
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()


        print 'time ',time.clock()-time1

    
    def display(self):

        #print self.fadeout
        

        if self.fadein :
            
            self.ambient[3]+=self.fadein_speed
        
            self.diffuse[3]+=self.fadein_speed
        
            self.specular[3]+=self.fadein_speed

        
        if self.fadeout :

            self.ambient[3]-=self.fadeout_speed
        
            self.diffuse[3]-=self.fadeout_speed
        
            self.specular[3]-=self.fadeout_speed
                


        #print self.ambient[3]

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_AMBIENT, self.ambient )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_DIFFUSE, self.diffuse )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        gl.glMaterialfv( gl.GL_FRONT, gl.GL_EMISSION, self.emission )


        x,y,z=self.position

        if self.orbit_demo and self.angle_table == None:

            gl.glPushMatrix()

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            #x,y,z=self.position


            gl.glRotatef(self.orbit_anglez,0,0,1)

            gl.glTranslatef(x,y,z) 


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

        elif self.orbit_demo == True and self.angle_table != None:

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,0],1,0,0)

            #x,y,z = self.position
            
            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,1],0,1,0)

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,2],0,0,1)

            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            self.angle_table_index += 1

            if self.angle_table_index >= self.angle_table.shape[0]:
                
                self.angle_table_index = self.angle_table.shape[0] - 1

            #print 'self.angle_table_index = %d' % self.angle_table_index


            
        '''
        gl.glPushMatrix()

        if self.orbit_demo:

            #self.orbit_anglex+=self.orbit_anglex_rate
        
            gl.glRotatef(self.orbit_anglex,1,0,0)
        

        gl.glPushMatrix()

        if self.orbit_demo:
            

            #self.orbit_anglez+=self.orbit_anglez_rate


            gl.glRotatef(self.orbit_anglez,0,0,1)

            
        

        gl.glCallList(self.list_index)


        gl.glPopMatrix()


        gl.glPopMatrix()
        '''


    


