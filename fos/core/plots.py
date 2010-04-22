import numpy as np
import OpenGL.GL as gl
import fos.core.primitives as prim
import fos.core.text as text




class Plot():


    def __init__(self):

        self.slots=None

        self.time=0

        self.near_pick=None

        self.far_pick =None

        

    def init(self):


        global tex1

        snippet = r'''
Tractography Rocks
'''

        tex1=text.TeX('test',snippet)

        tex1.alpha = 255

        tex1.init()

        tex1.position=[0,0,0]


        global slide1

        slide1=text.PNG('/home/eg01/Devel/Fos/test.png')

        slide1.position=[400,400,0]

        slide1.init()



        global b1

        b1 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        b1.opacity = 1.

        b1.angular_speed = 0.

        b1.manycolors = True

        b1.data_subset=[0,20000]

        b1.picking_example = True

        b1.init()               

        #Show the 3 brains together

        global b13
        global b23
        global b33

        b13 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        #b13 = prim.Tracks3D('/home/eg309/Data/Eleftherios/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')
        
        b13.opacity = .05     

        b13.angular_speed = 0.

        b13.manycolors = False

        b13.brain_color = [1,0,0]

        b13.yellow_indices = [17872, 6447, 18854, 14416, 9956, 10853, 13280, 11275, 10560]


        b13.init()
        
        b13.position=(-b13.mean[0]-150.,-b13.mean[1]+100,-b13.mean[2])

        b23 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090134_METHODS/20090227_154122/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        #b23 = prim.Tracks3D('/home/eg309/Data/Eleftherios/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')
        
        
        b23.opacity = .05

        b23.angular_speed = 0.

        b23.manycolors = False

        b23.brain_color = [0,1,1]

        b23.yellow_indices=[15377, 3897, 6409, 4515, 13913, 15572,  8461,  9224,  3609]
        
        
        b23.init()

        b23.position=(-b23.mean[0],-b23.mean[1]+100,-b23.mean[2])
        
        b33 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_RK2.trk')


        #b33 = prim.Tracks3D('/home/eg309/Data/Eleftherios/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')
        
        
        b33.opacity = .05

        b33.angular_speed = 0.

        b33.manycolors = False

        b33.brain_color = [0,1,0]
        
        b33.yellow_indices = [44949, 13165, 42538, 12471, 19442, 42391, 44919, 27775, 26106]

        b33.init()

        b33.position=(-b33.mean[0]+150.,-b33.mean[1]+100,-b33.mean[2])



        global bend

        bend = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        bend.opacity = 1.

        bend.angular_speed = .5

        bend.init()
        
        bend.position=(-bend.mean[0],-bend.mean[1],-bend.mean[2])
        
        
        #when to run
         
        self.slots={0:{'actor':slide1,'slot':(0,160000) },
                    1:{'actor':b1,'slot':(1000,10000) },
                       2:{'actor':b13,'slot':(12000,16000) },
                       3:{'actor':b23,'slot':(12000,16000) },
                       4:{'actor':b33,'slot':(12000,16000) },
                       5:{'actor':bend,'slot':(18000,200000) }}                   
                     

        
          
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




class Plot_JustOne():


    def __init__(self):

        self.slots=None

        self.time=0

        self.near_pick=None

        self.far_pick =None

    def init(self):


        global tex1

        snippet = r'''
\begin{itemize}
  \item[\texttt{bundle}] spino-cortical tract or some such structure
  \item[\texttt{\#tracks}] 100,000+ or so
  \item[\texttt{status}] provisional till \textsc{LARCH} gets to work
\end{itemize}
'''

        tex1=text.TeX('test',snippet)

        tex1.alpha = 255

        tex1.init()

        tex1.position=[0,0,0]

        tex2=text.TeX('test',snippet)

        tex2.alpha = 255

        tex2.init()

        tex2.position=[400,400,0]
                           
        global b1

        b1 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        #b1 = prim.Tracks3D('/home/eg309/Data/Eleftherios/dti_FACT.trk')

        b1.opacity = 1.

        b1.init()

        b1.angular_speed = 0.5        

        #print b1.min, b1.max, b1.mean

        b1.position=tuple(-b1.mean)



        #Scenario ----------------------------------------
        
        self.slots={ 0:{'actor':tex1,'slot':(1000,80000) },
                     1:{'actor':b1, 'slot': (0,800000) },
                     2:{'actor':tex2,'slot': (2000,80000) }}

          
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

        










#===============================================================
class DummyPlot():

    def __init__(self):

        self.slots=None

        self.time=0

    def init(self):
        

        global im1

        im1 = prim.Image2D('/home/eg01/Devel/Fos/fos/core/tests/data/small_latex1.png')

        im1.init()

        global im2

        im2 = prim.Image2D('/home/eg01/Devel/Fos/fos/core/tests/data/small_latex1.png')

        im2.init()

        im2.position=[400,400,0]


        self.slots={0:{'actor':im1,'slot':(5000,10000)},
                    1:{'actor':im2,'slot':(15000,20000)},
                    2:{'actor':im1,'slot':(25000,30000)},
                    3:{'actor':im2,'slot':(25000,30000)}}

          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].display()
        

    def update_time(self,time):

        self.time=time
        

        
                 



        



        
