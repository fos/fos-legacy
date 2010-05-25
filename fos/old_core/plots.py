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
import fos.core.label as label

import dipy.core.track_metrics as tm
from dipy.core import track_learning as tl
from dipy.io import trackvis as tv
import dipy.core.track_performance as pf



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

  
        tracks.angle_table_index=0

        tracks.anglex = 0.

        tracks.angley = 0.

        tracks.anglez = 0.

        global csurf

        #devel06
        csurfr ='/home/ian/Data/dipy/rh.pial.vtk'
       
        csurfl ='/home/ian/Data/dipy/lh.pial.vtk'

        #devel07
        #csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'
       
        #csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'


        csurfr = cortex.CorticalSurface(csurfr, angle_table=tracks.angle_table)
        
        csurfl = cortex.CorticalSurface(csurfl, angle_table=tracks.angle_table)

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

        
        csurfr.position[2]+=20
        
        csurfl.position[2]+=20
        

        csurfr.init()

        csurfl.init()
        #'''
        

        global tb1

        #devel06
        tb1_fname='/home/ian/Data/dipy/brain2_scan1_fiber_track_mni.trk'

        #devel07
        #tb1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

        #tb1=tracks.ChromoTracks(tb1_fname,shrink=0.99)

        tb1=tracks.Tracks(tb1_fname,ang_table=True,shrink=0.99,subset=[0,20000])

        tb1.angular_speed = 0.

        tb1.fade_demo = True
        
        tb1.opacity = 0.1

        tb1.opacity_rate = -0.01
        
        #tb1.fadeout = True

        #tb1.fadeout_speed = 0.001

        tb1.position = -tb1.mean

        tb1.position[0] += 5.

        tb1.position[2] += 20.

        tb1.manycolors = False #True

        #tb1.material_color = True

        tb1.orbit_demo = True #False          

        tb1.orbit_anglez_rate = 1.
                
        tb1.orbit_anglex_rate = -.1   
        

        tb1.init()


        global t1; t1 = self.hidden_tracks(tb1_fname,0.1*0.1,angle_table=True, data_ext=tb1.data)
        
        global ct1; ct1 = self.hidden_tracks(tb1_fname,0.1*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        global ct6; ct6 = self.hidden_tracks(tb1_fname,1*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        #global ct7; ct7 = self.hidden_tracks(tb1_fname,0.7,angle_table=True,many_colors=True, data_ext=tb1.data)

        '''
        global t1; t1 = self.hidden_tracks(tb1_fname,1*0.1,angle_table=True, data_ext=tb1.data)

        global t2; t2 = self.hidden_tracks(tb1_fname,.1*0.1,angle_table=True, data_ext=tb1.data)

        global t3; t3 = self.hidden_tracks(tb1_fname,.05*0.1,angle_table=True, data_ext=tb1.data)
        
        global t4; t4 = self.hidden_tracks(tb1_fname,.01*0.1,angle_table=True, data_ext=tb1.data)

        #global t5; t5 = self.hidden_tracks(tb1_fname,.005*0.1,angle_table=True, data_ext=tb1.data)
        

        #global ct1; ct1 = self.hidden_tracks(tb1_fname,.005*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        global ct2; ct2 = self.hidden_tracks(tb1_fname,.01*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        global ct3; ct3 = self.hidden_tracks(tb1_fname,.05*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)
        
        global ct4; ct4 = self.hidden_tracks(tb1_fname,.1*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        global ct5; ct5 = self.hidden_tracks(tb1_fname,.5*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        global ct6; ct6 = self.hidden_tracks(tb1_fname,1*0.1,angle_table=True,many_colors=True, data_ext=tb1.data)

        '''

        empty = tracks.Empty()

        empty.init()
        
        ghost = tracks.Ghost()

        ghost.init()
        

        #'''

        delay = 5*MS

        self.slots={00:{'actor':empty, 'slot':(0, delay)},

                    05:{'actor':ghost,'slot':( 0*MS+delay, 800*MS+delay )},

                    10:{'actor':tb1,'slot':( 0*MS+delay, 40*MS+delay )},                   

                    
                    11:{'actor':csurfl,'slot':( 0*MS+delay, 40*MS+delay )},
                    
                    12:{'actor':csurfr,'slot':( 0*MS+delay, 40*MS+delay )},
                    
                    
                    21:{'actor':t1,'slot':( 40*MS+delay, 41*MS+delay )},

                    22:{'actor':t1,'slot':( 40*MS+delay, 42*MS+delay )},

                    23:{'actor':t1,'slot':( 40*MS+delay, 43*MS+delay )},

                                
                    31:{'actor':ct1,'slot':( 42*MS+delay, 47*MS+delay )},

                    32:{'actor':ct1,'slot':( 42*MS+delay, 46*MS+delay )},

                    33:{'actor':ct1,'slot':( 42*MS+delay, 45*MS+delay )},
                    

                    34:{'actor':ct6,'slot':( 47*MS+delay, 800*MS+delay )}

                    #35:{'actor':ct7,'slot':( 48*MS, 800*MS )}


                    }
        #'''

        '''

        self.slots={10:{'actor':tb1,'slot':( 0, 3*40*MS )},

                    
                    11:{'actor':csurfl,'slot':( 0,3*40*MS )},
                    
                    12:{'actor':csurfr,'slot':( 0,3*40*MS )},
                    
                    
                    21:{'actor':t1,'slot':( 3*40*MS,  3*41*MS )},

                    22:{'actor':t1,'slot':( 3*40*MS,  3*42*MS )},

                    23:{'actor':t1,'slot':(  3*40*MS,  3*43*MS )},

                                
                    31:{'actor':ct1,'slot':( 3*42*MS, 3*47*MS )},

                    32:{'actor':ct1,'slot':( 3*42*MS, 3*46*MS )},

                    33:{'actor':ct1,'slot':(  3*42*MS,3*45*MS )},
                    

                    34:{'actor':ct6,'slot':(  3*47*MS, 3*48*MS )},

                    35:{'actor':ct7,'slot':(  3*48*MS, 800*MS )}


                    }


        '''            
        global last_time

        last_time = glut.glutGet(glut.GLUT_ELAPSED_TIME)




                    

        

    def hidden_tracks(self,t1_fname,opacity,angle_table,many_colors=False,data_ext=None):


        t1=tracks.Tracks(t1_fname,ang_table=angle_table,shrink=0.99,subset=[0,20000],data_ext=data_ext)

        t1.angular_speed = 0.

        t1.fade_demo = True
        
        t1.opacity = opacity #0.1

        #t1.opacity_rate = -0.01
        
        #tb1.fadeout = True

        #tb1.fadeout_speed = 0.001

        t1.position = -tb1.mean

        t1.position[0] += 5.

        t1.position[2] += 20.

        t1.manycolors = many_colors #False #True

        #tb1.material_color = True

        t1.orbit_demo = True#False          

        t1.orbit_anglez_rate = 0.#1.
                
        t1.orbit_anglex_rate = 0.#-.1        
        
        t1.init()

        return t1

          
    def display(self):

        global last_time

        current_time = glut.glutGet(glut.GLUT_ELAPSED_TIME)

        Dt = current_time - last_time

        #print Dt
        
        now = self.time

        #if Dt < 40:

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()

                

        last_time = current_time



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick





class PlotStuff():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None


    def init(self):


        angle_table = make_angle_table([
                [[0,0,90],[90,0,90],200],
                [[90,0,90],[90,90,90],200],
                [[90,90,90],[90,90,360],200]
                ])
        '''
        angle_table = make_angle_table([[[0,0,0],[-90,0,0],200],
                                        [[-90,0,0],[-90,-90,0],200],
                                        [[-90,-90,0],[-90,-90,90],200],
                                        [[-90,-90,90],[0,-90,-90],400]])
        '''
        
        global csurfr
        global csurfl

        #devel06
        csurfr ='/home/ian/Data/dipy/rh.pial.vtk'
       
        csurfl ='/home/ian/Data/dipygr/lh.pial.vtk'

        #devel07
        #csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'
       
        #csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'


        csurfr = cortex.CorticalSurfaceStuff(csurfr,angle_table)
        
        csurfl = cortex.CorticalSurfaceStuff(csurfl,angle_table)

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

        #devel06
        tb1_fname='/home/ian/Data/dipy/brain2_scan1_fiber_track_mni.trk'
       
        #devel07
        #tb1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'
       

        #tb1=tracks.ChromoTracks(tb1_fname,shrink=0.99,thinning=100,angle_table=angle_table)

        colored=tracks.ChromoTracks(tb1_fname,shrink=0.99,thinning=100,angle_table=angle_table,
                                    manycolors=True)
        '''
        buff=tracks.ChromoTracks(tb1_fname,shrink=0.99,thinning=100,angle_table=angle_table,
                                 manycolors=False,brain_color=[.941,.862,.510])
        white=tracks.ChromoTracks(tb1_fname,shrink=0.99,thinning=100,angle_table=angle_table,
                                  manycolors=False)
        '''

        colored.fade_demo = True
        colored.orbit_demo = True
        colored.opacity = 1.0
        colored.opacity_rate = -0.02
        colored.angular_speed = 0.
        colored.position = -colored.mean
        
        '''
        buff.fade_demo = False
        buff.orbit_demo = False
        buff.opacity = 1.0
        buff.opacity_rate = -0.02
        buff.angular_speed = 0.
        buff.position = -buff.mean
        '''
        
        tb1 = colored
        tb1.angular_speed = 0.
        tb1.fade_demo = True
        tb1.opacity = 1.0
        tb1.opacity_rate = -0.01
        tb1.position = -tb1.mean
        
        #tb1.fadeout = True

        #tb1.fadeout_speed = 0.001

        #white.position = tb1.position
        
        #buff.position = tb1.position

        tb1.position[0] += 0.

        #tb1.position[0] += 250.

        #tb1.position[0] += 150.

        tb1.manycolors = False

        #tb1.material_color = True

        tb1.orbit_demo = True          

        tb1.orbit_anglez_rate = 0.
                
        tb1.orbit_anglex_rate = 0.
        
        

        tb1.init()

#        self.slots={00:{'actor':tb1,'slot':( 0, 800*MS )}}
#                    #01:{'actor':csurfl,'slot':( 0, 800*MS )},
#                    #02:{'actor':csurfr,'slot':( 0, 800*MS )}
        

        
        self.slots={000:{'actor':tb1,'slot':( 0, 800*MS )},
                    010:{'actor':csurfl,'slot':( 0, 800*MS )},
                    020:{'actor':csurfr,'slot':( 0, 800*MS )}}#,
                    #030:{'actor':buff, 'slot':( 0,800*MS )}}
        


          
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

        #devel06

        b1_fname='/home/ian/Data/dipy/brain2_scan1_fiber_track_mni.trk'

        #devel07

        #b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

        #elfthin

        #b1_fname='/home/eg309/Desktop/DataNew/garyfallidis/brain2/brain2_scan1_fiber_track_mni.trk'

        
        
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


        self.slots={0:{'actor':pyr,'slot':( 0,  8000*MS )},

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



        
     
class PlotTextureIan():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        #self.fname = fname

        self.offset = None
        

    def init(self, given_tracks=None):


        global b1

        global b2

        #devel06

        #b1_fname='/home/ian/Data/dipy/brain2_scan1_fiber_track_mni.trk'

        #devel07

        b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

         
        
        b1=tracks.TracksModified(b1_fname,subset=[0,1000])

        b1.angular_speed = 0.

        b1.picking_example = True

        b1.min_length = 15.

        b1.opacity = 0.1

        b1.manycolors = False

        b1.brain_color = [1, 1, 1]

        b1.init()


        global texim


        #devel06

        #fname = '/home/ian/Data/dipy/Streaks4.bmp'

        #devel07

        fname = '/home/eg01/Devel/Fos/fos/core/tests/data/Streaks4.bmp'

        texim = texture.Texture_Demo(fname,red=False,green=True, blue=False)

        #texim.orbit = b1.data[4246]


        number_of_spritetracks = 30
        random_inx=np.floor(len(b1.data)*np.random.rand(number_of_spritetracks)).astype(np.int)
        systematic_inx = range(0,len(b1.data),len(b1.data)/number_of_spritetracks)

        #texim.orbits = [b1.data[4246],b1.data[3000],b1.data[2000],b1.data[1000]]

        texim.orbits =[]

        #indices = random_inx
        indices = systematic_inx
        
        for i in indices:

            #print i

            if tm.length(b1.data[i]) > 20.:

                #print i

                texim.orbits.append(b1.data[i])

        global b2


        b2=tracks.TracksModified(None,line_width=2,tracks=[b1.data[i] for i in indices],colormap=False,text='M')

        b2.angular_speed = 0.

        b2.picking_example = True

        b2.min_length = 15.

        b2.opacity = 0.9

        b2.manycolors = False

        b2.brain_color = [0.2, 0.8, 0.4]


        b2.init()
        

        texim.orbits_index = np.zeros((len(texim.orbits),),np.int)
        
        texim.init()

        #'''

        self.slots={0:{'actor':texim,'slot':( 0*MS, 20*MS )},
                    1:{'actor':b1,'slot':(0*MS, 200*MS)},
                    2:{'actor':b2,'slot':(15*MS, 2000*MS)}}

        #'''

        '''
        self.slots={0:{'actor':texim,'slot':( 0*MS, 20*MS )},
                    #1:{'actor':b1,'slot':(0*MS, 200*MS)},
                    2:{'actor':b2,'slot':(0*MS, 2000*MS)}}
        '''
        
          
    def display(self):

        now = self.time

        #'''

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



        '''
        gl.glDisable(gl.GL_LIGHTING)
        
        gl.glColor3f(1.,0.,0.)

        gl.glRasterPos3f(0.,0.,0.)

        label = 'HELLO'

        #print label

        for c in label:

            #print c

            glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

        gl.glEnable(gl.GL_LIGHTING)

        '''
        

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


        global b1

        #devel06

        b1_fname='/home/ian/Data/dipy/brain2_scan1_fiber_track_mni.trk'

        #devel07

        #b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

         
        
        b1=tracks.Tracks(b1_fname,subset=[0,200])

        b1.angular_speed = 0.

        b1.picking_example = True

        b1.min_length = 20.

        b1.opacity = 0.8

        b1.manycolors = False

        b1.brain_color = [0, 0, 0]


        b1.init()




        global texim


        #devel06

        fname = '/home/ian/Data/dipy/Streaks4.bmp'

        #devel07

        #fname = '/home/eg01/Devel/Fos/fos/core/tests/data/Streaks4.bmp'

        texim = texture.Texture_Demo(fname,red=False,green=False, blue=True)

        #texim.orbit = b1.data[4246]

        #print 'len(b1.data)', len(b1.data)

        random_inx=np.trunc(len(b1.data)*np.random.rand(200)).astype(np.int)
        #print random_inx

        #texim.orbits = [b1.data[4246],b1.data[3000],b1.data[2000],b1.data[1000]]

        texim.orbits =[]
        
        for i in random_inx:

            #print i

            if tm.length(b1.data[i]) > 20.:

                #print i

                texim.orbits.append(b1.data[i])

                
        

        texim.orbits_index = np.zeros((len(texim.orbits),),np.int)
        
        texim.init()

        self.slots={0:{'actor':texim,'slot':( 0, 800*MS )}}#,
                    #1:{'actor':b1,'slot':(0, 800*MS)}}

        
          
    def display(self):

        now = self.time

        #'''

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



        #'''
        gl.glDisable(gl.GL_LIGHTING)
        
        gl.glColor3f(1.,0.,0.)

        gl.glRasterPos3f(0.,0.,0.)

        '''
        label = 'HELLO'

        #print label

        for c in label:

            #print c

            glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

        gl.glEnable(gl.GL_LIGHTING)

        '''

        #'''
        

    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick





class PlotLabelExample():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        #self.fname = fname

        

    def init(self):


        '''
        global b1

        #devel07

        #b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

        #elfthin

        b1_fname='/home/eg309/Desktop/DataNew/garyfallidis/brain2/brain2_scan1_fiber_track_mni.trk'

        
        
        b1=tracks.Tracks(b1_fname)

        b1.angular_speed = 0.

        b1.picking_example = True

        b1.min_length = 20.

        b1.opacity=0.1


        b1.init()




        global texim

        #elfthin

        fname = '/home/eg309/Devel/Fos/fos/core/tests/data/Streaks4.bmp'

        #devel07

        #fname = '/home/eg01/Devel/Fos/fos/core/tests/data/Streaks4.bmp'

        texim = texture.Texture_Demo(fname)

        #texim.orbit = b1.data[4246]

        random_inx=np.round(19000*np.random.rand(30)).astype(np.int)
        

        #texim.orbits = [b1.data[4246],b1.data[3000],b1.data[2000],b1.data[1000]]

        texim.orbits =[]
        for i in random_inx:

            if tm.length(b1.data[i]) > 20.:

                print i

                texim.orbits.append(b1.data[i])

                
        

        texim.orbits_index = np.zeros((20,),np.int)
        
        texim.init()

        '''

        points = np.array([[0.,0.,0.],[100.,0.,0],[-100.,0.,0.],[100.,100.,100.]]).astype(np.float32)

        labels = ['testa','testb','testc','testd']
        

        colors = np.array([[1.,0,0],[1.,0.,0.],[0.,1.,0],[0.,0.,1.]]).astype(np.float32)

        #lab = label.Label([[0.,0.,0.],[100.,]],['test'],[[1.,0.,0.]])

        lab = label.Label(points,labels,colors)
        
        lab.init()

        self.slots={#0:{'actor':texim,'slot':( 0, 800*MS ) },
                    #1:{'actor':b1,'slot':(0, 800*MS) },
                    2:{'actor':lab,'slot':(0, 800*MS) }}

        
          
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
                 

        
class PlotMultipleBrains():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        #self.fname = fname

        

    def init(self):


        br1path='/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk'

        br2path='/home/eg01/Data_Backup/Data/Eleftherios/CBU090134_METHODS/20090227_154122/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk'

        br3path='/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_RK2.trk'


        min_len=20

        down=20

        rand_tracks=-1 #default 10 min_search_len=70
        
        min_search_len=70
        
        max_search_len=140


        corr_mat_demo=np.array([[ 1, 10560,  3609],[ 2, 17872, 15377],[ 3,  6447,  3897], [4, 18854,  6409], [ 5, 14416,  4515], [ 7,  9956, 13913], [8, 10853, 15572], [ 9, 13280,  8461], [ 0, 11275,  9224]])


        print 'Minimum track length', min_len, 'mm'
        print 'Number of segments for downsampling',down
        print 'Number of tracks for detection',rand_tracks
        print 'Minimum searched track length', min_search_len, 'mm'
        print 'Maximum searched track length', max_search_len, 'mm'

        tracks1,hdr1=tv.read(br1path)

        tracks2,hdr2=tv.read(br2path)

        tracks3,hdr3=tv.read(br3path)

        #Load only track points, no scalars or parameters.

        tracks1=[t[0] for t in tracks1]

        tracks2=[t[0] for t in tracks2]

        tracks3=[t[0] for t in tracks3]

        print 'Before thresholding'

        print len(tracks1)

        print len(tracks2)

        print len(tracks3)

        print hdr1['dim']

        print hdr2['dim']

        print hdr3['dim']

        #Apply thresholds

        tracks1=[t for t in tracks1 if tm.length(t) > min_len]

        tracks2=[t for t in tracks2 if tm.length(t) > min_len]

        tracks3=[t for t in tracks3 if tm.length(t) > min_len]

        print 'After thresholding'

        print len(tracks1)
        print len(tracks2)
        print len(tracks3)

        print 'Downsampling'

        tracks1z=[tm.downsample(t,down) for t in tracks1]

        tracks2z=[tm.downsample(t,down) for t in tracks2]

        tracks3z=[tm.downsample(t,down) for t in tracks3] 

        print 'Detecting random tracks'

        lt1=len(tracks1)

        lt2=len(tracks2)

        lt3=len(tracks3)

        if rand_tracks==-1:
            
	    #use already stored indices
            t_ind=corr_mat_demo[:,1]
            
				
	t_ind=np.array(t_ind)

        print 'Indices of tracks for detection', t_ind

        print 'Finding corresponding tracks'

        global track2track        
        track2track= self.corresponding_tracks(t_ind,tracks1z,tracks2z)

        global track2track2
        track2track2=self.corresponding_tracks(t_ind,tracks1z,tracks3z)

        print 'First Correspondance Matrix'
        print track2track

        print 'Second Correspondance Matrix'
        print track2track2

        print 'first brain'
        print track2track[:,1].T

        print 'second brain'
        print track2track[:,2].T

        print 'third brain'
        print track2track2[:,2].T


        #fos.add(r,fos.line(tracks1,fos.red,opacity=0.01))
        #fos.add(r,fos.line(tracks2,fos.cyan,opacity=0.01))

        tracks1zshift = tracks1z
        tracks2zshift = tracks2z
        tracks3zshift = tracks3z

        m1z=np.concatenate(tracks1zshift).mean(axis=0)
        
        m2z=np.concatenate(tracks2zshift).mean(axis=0)

        m3z=np.concatenate(tracks3zshift).mean(axis=0)

        #tracks1zshift=[t+np.array([-70,0,0]) for t in tracks1z]

        #tracks2zshift=[t+np.array([70,0,0]) for t in tracks2z]

        tracks1zshift=[t-m1z for t in tracks1z]
        
        tracks2zshift=[t-m2z for t in tracks2z]
          
        tracks3zshift=[t-m3z for t in tracks3z]


        global t1

        #devel07

        t1=tracks.Tracks(None,data_ext=tracks1zshift)

        t1.angular_speed = 0.1

        t1.brain_color=[1,0,0]

        t1.manycolors=False

        t1.opacity = 0.01

        t1.orbit_demo=True

        t1.orbit_anglez_rate = 0.
                
        t1.orbit_anglex_rate = 0.

        t1.orbit_angley_rate = .2

        

        t1.init()

        t1.position = np.array([-120,0,-30])

        print 't1p',t1.position

        

        global t2

        #devel07

        t2=tracks.Tracks(None,data_ext=tracks2zshift)

        t2.angular_speed = 0.1

        t2.brain_color=[0,1,1]

        t2.manycolors=False

        t2.opacity = 0.01

        t2.orbit_demo=True

        t2.orbit_anglez_rate = 0.
                
        t2.orbit_anglex_rate = 0.

        t2.orbit_angley_rate = .2

        t2.init()
        
        t2.position = np.array([0,0,-30])

        print 't2p', t2.position
        
        

        global t3

        #devel07

        t3=tracks.Tracks(None,data_ext=tracks3zshift)

        t3.angular_speed = 0.1

        t3.manycolors=False

        t3.brain_color=[0,0,1]

        t3.opacity = 0.01

        t3.orbit_demo=True

        t3.orbit_anglez_rate = 0.
                
        t3.orbit_anglex_rate = 0.

        t3.orbit_angley_rate = .2        

        t3.init()
        
        #t3.position = -
        #np.concatenate(tracks3zshift).mean(axis=0)+np.array([70,0,0])

        t3.position = np.array([120,0,-30])

        print 't3p', t3.position
        
        

        self.slots={0:{'actor':t1,'slot':( 0, 800*MS ) },
                    1:{'actor':t2,'slot':( 0, 800*MS ) },
                    2:{'actor':t3,'slot':( 0, 800*MS ) }}
                   
                   

        
          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()


        global track2track

        global track2track2

 
        for i in track2track:

            t1.display_one_track(i[1], np.array([1,1,0,1],np.float32))
            t2.display_one_track(i[2], np.array([1,1,0,1],np.float32))

        for i in track2track2:                                     

            t3.display_one_track(i[2], np.array([1,1,0,1],np.float32))                      

                                                          

        '''    
            
        gl.glDisable(gl.GL_LIGHTING)
        
        gl.glColor3f(1.,0.,0.)

        gl.glRasterPos3f(0.,0.,0.)

        
        label = 'HELLO'

        #print label

        for c in label:

            #print c

            glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

        gl.glEnable(gl.GL_LIGHTING)

        '''



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick
                 

    def corresponding_tracks(self,indices,tracks1,tracks2):
	''' Detect similar tracks in different brains
	'''
    
	li=len(indices)
	track2track=np.zeros((li,3))
	cnt=0
	for i in indices:        
        
		rt=[pf.zhang_distances(tracks1[i],t,'avg') for t in tracks2]
		rt=np.array(rt)               

		track2track[cnt-1]=np.array([cnt,i,rt.argmin()])        
		cnt+=1
        
	return track2track.astype(int)
    

class PlotBundlesExample():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        #self.fname = fname

        

    def init(self):

        import pbc

        G,hdr,R = pbc.load_approximate_training_set('/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/')

        tl=[]

        self.slots={}

        colors=np.array([[1.,1.,1.],
                         [0.5, 0, 0],
                         [0.29411765, 0., 0.50980392],
                         [0, 0.5, 0],
                         [0., 0.49, 1.],
                         [ 0.498, 1., 0.83 ],
                         [1.  ,  0.84,  0. ],
                         [0.74901961, 1., 0.],
                         [0.49803922, 1. , 0. ]])

        data=G[0]['tracks']

        d1z=np.concatenate(data).mean(axis=0)
        
        
        for g in [0,1,2,3,4,5,6,7,8]:

            data=G[g]['tracks']

            print g, G[g]['label_name']

            global t

            #d1z=np.concatenate(data).mean(axis=0)
        
            data=[t-d1z for t in data]
              
            t=tracks.Tracks(None,data_ext=data)

            t.angular_speed = 0.1

            t.brain_color=colors[g]

            t.manycolors = False

            t.opacity = 0.1

            t.orbit_demo = True

            t.orbit_anglez_rate = 0.
                
            t.orbit_anglex_rate = 0.

            t.orbit_angley_rate = 1.

            t.init()
        
            t.position = np.array([0,0,10])

            print 'tp', t.position

            tl.append(t)

            if g==0:

                self.slots[g]={'actor':tl[g],'slot':( 0, 5*MS ) }

            else:

                self.slots[g]={'actor':tl[g],'slot':( 0, 10*MS ) }
       
                   

        #full arcuate
                
        arcuate=G[1]['tracks']

        amean=np.concatenate(arcuate).mean(axis=0)
        
        data=[t-amean for t in arcuate]
        

        t=tracks.Tracks(None,data_ext=data)

        t.angular_speed = 0.1

        t.brain_color=colors[1]

        t.manycolors = False

        t.opacity = 0.1

        t.orbit_demo = True

        t.orbit_anglez_rate = 0.
                
        t.orbit_anglex_rate = 0.

        t.orbit_angley_rate = -1.

        t.init()
        
        t.position = np.array([-20,0,60])
        
        self.slots[g+1]={'actor':t,'slot':( 12*MS, 800*MS ) }

        #broken arcuate - injury

        dataa,datab=self.break_bundle(data, [-3000,3000,0], [-3000,-3000,0], [3000, -3000,0])


        #dataa=[t+np.array([100,0,0],np.float32) for t in dataa]
        
        #datab=[t+np.array([100,0,0],np.float32) for t in datab]
        
        
        t1=tracks.Tracks(None,data_ext=dataa)

        t1.angular_speed = 0.1

        t1.brain_color=[1.,0.,0.]

        t1.manycolors = False

        t1.opacity = 0.1

        t1.orbit_demo = True

        t1.orbit_anglez_rate = 0.
                
        t1.orbit_anglex_rate = 0.

        t1.orbit_angley_rate = -1.

        t1.init()
        
        t1.position = np.array([20,0,60])
        

        #datab=[t+np.array([0,20,0]) for t in datab]
        
        t2=tracks.Tracks(None,data_ext=datab)

        t2.angular_speed = 0.1

        t2.brain_color=[1.,0.,0.]

        t2.manycolors = False

        t2.opacity = 0.1

        t2.orbit_demo = True

        t2.orbit_anglez_rate = 0.
                
        t2.orbit_anglex_rate = 0.

        t2.orbit_angley_rate = -1.

        t2.init()
        
        t2.position = np.array([20,0,60])
        
        
        self.slots[g+2]={'actor':t1,'slot':( 12*MS, 800*MS ) }

        self.slots[g+3]={'actor':t2,'slot':( 12*MS, 800*MS ) }
        

        
          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()

                                                         

        '''    
            
        gl.glDisable(gl.GL_LIGHTING)
        
        gl.glColor3f(1.,0.,0.)

        gl.glRasterPos3f(0.,0.,0.)

        
        label = 'HELLO'

        #print label

        for c in label:

            #print c

            glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

        gl.glEnable(gl.GL_LIGHTING)

        '''



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick
                 

    def break_bundle(self,tracks, p1, p2, p3):


        import fos.core.collision as cll

        tracksa=[]

        tracksb=[]

        for t in tracks:

            for i in range(len(t)-1):

                success, per, p = cll.intersect_segment_plane(t[i],t[i+1], p1, p2, p3)

                if success:

                    #print t, i

                    tracksa.append(t[:i-1])

                    tracksb.append(t[i+1:-1])

        return tracksa, tracksb

        
        



