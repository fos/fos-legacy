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




import mouse 

MS=1000


def center(x,y):

    return ((int(1024-x)/2),int((768-y)/2))

'''
def make_angle_table(lists):

    #angle_table = make_angle_table([[[0,0,0],[90,0,0],30],[[90,0,0],[90,90,0],30]])

    table = []
    for list in lists:
        start,finish,n = list
        sx,sy,sz = start
        fx,fy,fz = finish
        cx = np.linspace(sx,fx,n)
        cy = np.linspace(sy,fy,n)
        cz = np.linspace(sz,fz,n)
        if table == []:
            table = np.column_stack((cx,cy,cz))
        else:
            table = np.vstack((table,np.column_stack((cx,cy,cz))))
    print 'angle table has length %d' % table.shape[0]
    return table


angle_table = make_angle_table([[[0,0,0],[-90,0,0],200],
                                        [[-90,0,0],[-90,-90,0],200],
                                        [[-90,-90,0],[-90,-90,90],200],
                                        [[-90,-90,90],[0,-90,-90],400]])


'''


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

        #devel07
        csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'
       
        csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'


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

        #devel07
        tb1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

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

        #devel07
        csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'
       
        csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'


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

        #devel07
        tb1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'
       

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

        #devel07

        b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

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


        global b1

        #devel07

        b1_fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain2/brain2_scan1_fiber_track_mni.trk'

         
        
        b1=tracks.Tracks(b1_fname,subset=[0,200])

        b1.angular_speed = 0.

        b1.picking_example = True

        b1.min_length = 20.

        b1.opacity = 0.8

        b1.manycolors = False

        b1.brain_color = [0, 0, 0]


        b1.init()




        global texim


        #devel07

        fname = '/home/eg01/Devel/Fos/fos/core/tests/data/Streaks4.bmp'

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
                 

        


    


        
