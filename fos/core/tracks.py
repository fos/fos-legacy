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

class Tracks(object):

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

        self.data_subset = [0,20000]#None

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

        if self.picking_example==False:


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

            for i in self.yellow_indices:


                self.display_one_track(i)


        gl.glPopMatrix()

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print 'min ',self.picked_track

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        min_dist_info = np.array(min_dist_info)

        print 'min info',min_dist_info

        print 'min info extra',min_dist.min(), min_dist_info[self.picked_track]
        


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

        #gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE,gl.GL_ONE_MINUS_SRC_ALPHA)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        #gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_NICEST)

        gl.glLineWidth(self.line_width)

        #gl.glDepthMask(gl.GL_FALSE)


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

        #gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)
        
        gl.glPopMatrix()

        gl.glEndList()
 
    

   


        




            

       

    


