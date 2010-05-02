import sys
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

#import fos.core.primitives as prim
import fos.core.text as text
import fos.core.cortex as cortex
import fos.core.pyramid as pyramid
import fos.core.tracks as tracks
import fos.core.texture as texture


import mouse 

MS=1000


def center(x,y):

    return ((int(1024-x)/2),int((768-y)/2))



class Plot():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        

    def init(self):

        global csurf

        #devel07
        #csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'
       
        #csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'

        #elfthin
        csurfr = '/home/eg309/Desktop/DataNew/rh.pial.vtk'
       
        csurfl = '/home/eg309/Desktop/DataNew/lh.pial.vtk'

        csurfr = cortex.CorticalSurface(csurfr)
        
        csurfl = cortex.CorticalSurface(csurfl)

        csurfr.fadeout = True

        csurfl.fadeout = True

        
        csurfr.fadeout_speed = 0.001        

        csurfl.fadeout_speed = 0.001

        
        csurfr.orbit_demo = True          

        csurfr.orbit_anglez_rate = 1.
        
        
        csurfl.orbit_demo = True
        
        csurfl.orbit_anglez_rate = 1.
        
        csurfr.orbit_anglex_rate = -.1
        
        csurfl.orbit_anglex_rate = -.1
        
        

        csurfr.init()

        csurfl.init()


        global tb1

        #devel07
        #tb1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

        #elfthin
        tb1_fname='/home/eg309/Desktop/DataNew/garyfallidis/brain2/brain2_scan1_fiber_track_mni.trk'

        tb1=tracks.Tracks(tb1_fname,shrink=0.99)

        tb1.angular_speed = 0.

        tb1.opacity = .1
        
        #tb1.fadeout = True

        #tb1.fadeout_speed = 0.001

        tb1.position = -tb1.mean

        tb1.position[0] += 5.

        tb1.manycolors = True

        #tb1.material_color = True

        tb1.orbit_demo = True          

        tb1.orbit_anglez_rate = 1.
                
        tb1.orbit_anglex_rate = -.1
        

        
        
        

        tb1.init()



        self.slots={00:{'actor':tb1,'slot':( 0, 800*MS )},
                    01:{'actor':csurfl,'slot':( 0, 800*MS )},
                    02:{'actor':csurfr,'slot':( 0, 800*MS )}}
        


          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick







class PlotPickingExample():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        #self.fname = fname

        

    def init(self):

        '''

        global csurf

        csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'

        #csurf_fname ='/home/eg309/Desktop/rh.pial.vtk'
        
        csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'

        #csurfr = cortex.CorticalSurface(csurfr)
        
        #csurfl = cortex.CorticalSurface(csurfl)

        #csurfr.init()

        #csurfl.init()

        '''

        global b1

        #devel07

        #b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

        #elfthin

        b1_fname='/home/eg309/Desktop/DataNew/garyfallidis/brain2/brain2_scan1_fiber_track_mni.trk'

        
        
        b1=tracks.Tracks(b1_fname)

        b1.angular_speed = 0.

        b1.picking_example = True

        b1.min_length = 0.

        b1.init()



        self.slots={0:{'actor':b1,'slot':( 0,   800*MS )}}

        '''
       
        self.slots={0:{'actor':csurfr,'slot':( 0,   800*MS )},
                    1:{'actor':csurfl,'slot':( 0,   800*MS )}}                 

        '''

        
        
          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick




class PlotIan():


    def __init__(self):


        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None


    def init(self):

        global pyr

        pyr = pyramid.Pyramid()

        pyr.init()

        global pyr2

        pyr2 = pyramid.Pyramid()

        pyr2.init()

        pyr.position=[100,0,0]

        pyr2.position=[-100,0,0]


        self.slots={0:{'actor':pyr,'slot':( 0,   800*MS )},

                    1:{'actor':pyr2,'slot':( 0,   800*MS )}
                    }                 


    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick



        
     
class PlotTextureExample():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        #self.fname = fname

        

    def init(self):


        global texim

        fname = '/home/eg309/Downloads/ztv121/Art/Streaks4.bmp'

        texim = texture.Texture(fname)

        texim.init()

        self.slots={0:{'actor':texim,'slot':( 0,   800*MS )}}

        
          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick
                 



        



        
