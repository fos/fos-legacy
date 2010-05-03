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

    def __init__(self,fname,colormap=None, line_width=3., shrink=None):

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

        self.material_color = False

        self.fadeout = False

        self.fadein = False

        self.fadeout_speed = 0.

        self.fadein_speed = 0.

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

        self.brain_color = [1,1,1]

        self.yellow_indices = None

        self.dummy_data = False

        self.data_subset = [0,20000]#None


        self.orbit_demo = False          

        self.orbit_anglez =0.

        self.orbit_anglez_rate = 10.
        

        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 2.

        

        self.shrink = shrink

        self.picking_example = False

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

        if self.shrink != None:

            self.data = [ self.shrink*t  for t in self.data]
            

        data_stats = np.concatenate(tracks)

        self.min=np.min(data_stats,axis=0)
         
        self.max=np.max(data_stats,axis=0)

        self.mean=np.mean(data_stats,axis=0)

        del data_stats
        
        del lines
        
        

    def init(self):

        if self.material_color:

            self.material_colors()

        else:

            self.multiple_colors()



               
 

    def display(self):


        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)             
              
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
      

                
        
    
        x,y,z=self.position

        if self.orbit_demo:

            gl.glPushMatrix()

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            x,y,z=self.position

           

            gl.glRotatef(self.orbit_anglez,0,0,1)

            gl.glTranslatef(x,y,z) 


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            
        else:

            gl.glCallList(self.list_index)




            if self.picked_track != None:

                self.display_one_track(self.picked_track)



            if self.yellow_indices != None:

                for i in self.yellow_indices:


                    self.display_one_track(i)


        

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print 'min index',self.picked_track

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        A = np.array(min_dist_info)

        dist=10**(-3)

        iA=np.where(A[:,0]<dist)

        minA=A[iA]

        print 'minA ', minA

        miniA=minA[:,1].argmin()

        print 'final min index ',iA[0][miniA]

        self.picked_track=iA[0][miniA]

   
        

        
        


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

        #gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)
        
        #!!!gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glDepthFunc(gl.GL_NEVER)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE,gl.GL_ONE_MINUS_SRC_ALPHA)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        #!!!gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

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
                    

                else:

                    color4=np.array([self.brain_color[0],self.brain_color[1],\
                                         self.brain_color[2],self.opacity],np.float32)


                if self.fadein == True:

                    color4[3] += self.fadein_speed

                if self.fadeout == True:

                    color4[3] -= self.fadeout_speed

                gl.glColor4fv(color4)                

                gl.glVertexPointerf(d)
                               
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        #gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)
        
        #gl.glPopMatrix()

        gl.glEndList()
 
    

   


    def material_colors(self):
        

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [1,1,1,.1] )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, [1,1,1,.1] )
        
        
        #gl.glMaterialf( gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 50. )

        #gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_EMISSION, [1,1,1,1.])


        gl.glEnable(gl.GL_LINE_SMOOTH)
               
        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)


        #gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        #gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        #gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()


class ChromoTracks(object):

    def __init__(self,fname,colormap=None, line_width=3., shrink=None):

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

        self.material_color = False

        self.fadeout = False

        self.fadein = False

        self.fadeout_speed = 0.

        self.fadein_speed = 0.

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

        self.brain_color = [1,1,1]

        self.yellow_indices = None

        self.dummy_data = False

        self.data_subset = [0,20000]#None


        self.orbit_demo = False          

        self.orbit_anglez =0.

        self.orbit_anglez_rate = 10.
        

        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 2.

        

        self.shrink = shrink

        self.picking_example = False

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

        if self.shrink != None:

            self.data = [ self.shrink*t  for t in self.data]
            

        data_stats = np.concatenate(tracks)

        self.min=np.min(data_stats,axis=0)
         
        self.max=np.max(data_stats,axis=0)

        self.mean=np.mean(data_stats,axis=0)

        del data_stats
        
        del lines
        
        

    def init(self):

        if self.material_color:

            self.material_colors()

        else:

            self.multiple_colors()



               
 

    def display(self):


        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)             
              
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
      

                
        
    
        x,y,z=self.position

        if self.orbit_demo:

            gl.glPushMatrix()

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            x,y,z=self.position

           

            gl.glRotatef(self.orbit_anglez,0,0,1)

            gl.glTranslatef(x,y,z) 


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            
        else:

            gl.glCallList(self.list_index)




            if self.picked_track != None:

                self.display_one_track(self.picked_track)



            if self.yellow_indices != None:

                for i in self.yellow_indices:


                    self.display_one_track(i)


        

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print 'min index',self.picked_track

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        A = np.array(min_dist_info)

        dist=10**(-3)

        iA=np.where(A[:,0]<dist)

        minA=A[iA]

        print 'minA ', minA

        miniA=minA[:,1].argmin()

        print 'final min index ',iA[0][miniA]

        self.picked_track=iA[0][miniA]

   
        

        
        


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

        gl.glNewList( self.list_index,gl.GL_COMPILE_AND_EXECUTE)

        #gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)
        
        #!!!gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glDepthFunc(gl.GL_NEVER)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE,gl.GL_ONE_MINUS_SRC_ALPHA)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        #!!!gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

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
                    

                else:

                    color4=np.array([self.brain_color[0],self.brain_color[1],\
                                         self.brain_color[2],self.opacity],np.float32)


                if self.fadein == True:

                    color4[3] += self.fadein_speed

                if self.fadeout == True:

                    color4[3] -= self.fadeout_speed

                gl.glColor4fv(color4)                

                gl.glVertexPointerf(d)
                               
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        #gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)
        
        #gl.glPopMatrix()

        gl.glEndList()
 
    

   


    def material_colors(self):
        

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [1,1,1,.1] )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, [1,1,1,.1] )
        
        
        #gl.glMaterialf( gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 50. )

        #gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_EMISSION, [1,1,1,1.])


        gl.glEnable(gl.GL_LINE_SMOOTH)
               
        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)


        #gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        #gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        #gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()




            

       

    


