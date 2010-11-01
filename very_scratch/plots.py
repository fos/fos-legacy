import numpy as np
import OpenGL.GL as gl
import fos.core.primitives as prim
import fos.core.text as text




K=1500


def center(x,y):

    return ((int(1024-x)/2),int((768-y)/2))


class Plot():


    def __init__(self):

        self.slots=None

        self.time=0

        self.near_pick=None

        self.far_pick =None

        

    def init(self):


        global ismrm0

        ismrm0=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/firstpage.png')
        ismrm0.invert=False

        ismrm0.init()


        global ismrm1

        ismrm1=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm1.png')

   
        

        print ismrm1.position
        
        print ismrm1.size        

        px,py=ismrm1.size

        print px,py

        nx,ny=center(px,py)

        print nx,ny

        ismrm1.position=[nx,ny,0]

        print ismrm1.position
        
        ismrm1.init()
        
        

        global ismrm2

        ismrm2=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm2.png')

        #ismrm2.init()

        px,py=ismrm2.size

        nx,ny=center(px,py)

        ismrm2.position=[nx,ny,0]
        
        ismrm2.init()
        

        global ismrm3

        ismrm3=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm3.png')

        

        px,py=ismrm3.size

        nx,ny=center(px,py)

        ismrm3.position=[nx,ny,0]

        ismrm3.init()


        global ismrm4

        ismrm4=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm4.png')

      

        px,py=ismrm4.size

        nx,ny=center(px,py)

        ismrm4.position=[nx,ny,0]

        ismrm4.init()


        global ismrm5

        ismrm5=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm5.png')


        px,py=ismrm5.size

        nx,ny=center(px,py)

        ismrm5.position=[nx,ny,0]

        ismrm5.init()
        

        global ismrm6

        ismrm6=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm6.png')

        ismrm6.init()


        global ismrm7

        ismrm7=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm7.png')



        px,py=ismrm7.size

        nx,ny=center(px,py)

        ismrm7.position=[nx,ny,0]
        
        ismrm7.init()

        

        global ismrm8

        ismrm8=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm8.png')

        px,py=ismrm8.size

        nx,ny=center(px,py)

        ismrm8.position=[nx,ny,0]

        ismrm8.init()


        


        global ismrm9

        ismrm9=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm9.png')



        px,py=ismrm9.size

        nx,ny=center(px,py)

        ismrm9.position=[nx,ny,0]
        
        ismrm9.init()        
        

        global ismrm10

        ismrm10=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm10.png')


        px,py=ismrm10.size

        nx,ny=center(px,py)

        ismrm10.position=[nx,ny,0]
        
        ismrm10.init()        
        

        global ismrm11

        ismrm11=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm11.png')



        px,py=ismrm11.size

        nx,ny=center(px,py)

        ismrm11.position=[nx,ny,0]
        
        ismrm11.init()
        
        
        global ismrm12

        ismrm12=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm12.png')



        px,py=ismrm12.size

        nx,ny=center(px,py)

        ismrm12.position=[nx,ny,0]
        
        ismrm12.init()        


        global ismrm13

        ismrm13=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm13.png')

        px,py=ismrm13.size

        nx,ny=center(px,py)

        #ismrm13.position=[nx,ny,0]
        
        ismrm13.init()

        

        global ismrm14

        ismrm14=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm14.png')

        px,py=ismrm14.size

        nx,ny=center(px,py)

        #ismrm13.position=[nx,ny,0]
        
        ismrm14.init()

        

        global ismrm15

        ismrm15=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm15.png')

        px,py=ismrm15.size

        nx,ny=center(px,py)

        #ismrm13.position=[nx,ny,0]
        
        ismrm15.init()
        


        global ismrm16

        ismrm16=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm16.png')

        px,py=ismrm16.size

        nx,ny=center(px,py)

        #ismrm13.position=[nx,ny,0]
        
        ismrm16.init()

        
        global ismrm17

        ismrm17=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/ismrm17.png')

        px,py=ismrm17.size

        nx,ny=center(px,py)

        #ismrm13.position=[nx,ny,0]
        
        ismrm17.init()
        

        global b1

        b1 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        b1.opacity = 1.

        b1.angular_speed = 0.

        b1.manycolors = True

        b1.data_subset=[0,20000]

        b1.picking_example = True

        b1.init()

        
        

        global redcyan1

        redcyan1=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/redcyan1.png')
        redcyan1.invert=False

        redcyan1.init()
        

        global redcyanblue1

        redcyanblue1=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/redcyanblue1.png')

        redcyanblue1.invert=False

        redcyanblue1.init()


        global redcyanblue2

        redcyanblue2=text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/redcyanblue2.png')

        redcyanblue2.invert=False

        redcyanblue2.init()


        global approximate

        approximate =text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/approximate.png')

        approximate.invert=False

        approximate.init()

        

        global mam

        mam = text.PNG('/home/eg01/Devel/Fos/fos/core/tests/data/MAM.png')

        mam.invert = False

        mam.position = [400,300,0]

        mam.init()
        
        


        global bend

        bend = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        bend.opacity = 1.

        bend.angular_speed = -.5

        bend.init()
        
        bend.position=(-bend.mean[0],-bend.mean[1],-bend.mean[2])


        
        global tex1

        snippet = r'''
Projective plane colourcoding of the mid segments [3].
'''

        tex1=text.TeX('test1',snippet)

        tex1.alpha = 255

        tex1.init()

        tex1.position=[0,0,0]
        
        #when to run

        s=0

       
        self.slots={0:{'actor':ismrm0,'slot':( 0,   8*K ) },
                    
                     
                    1:{'actor':ismrm1,'slot':( 10*K, 20*K ) }, #Key question
                    

                    2:{'actor':ismrm2,'slot':( 22*K, 30*K + 10*K ) },#Requirements
                    

                    3:{'actor':ismrm3,'slot':( 32*K +10*K , 40*K +10*K ) },# Identifying
                   

                    4:{'actor':ismrm4,'slot':( 42*K +10*K, 52*K+10*K ) },# compression


                    41:{'actor':approximate,'slot':( 54*K+10*K, 64*K+10*K ) },# approximate
                    
                    
                    5:{'actor':ismrm5,'slot':( 66*K+10*K, 74*K+20*K ) },# metrics
                    

                    6:{'actor':mam,'slot':( 64*K+32*K, 78*K+32*K ) }, # mam
                    

                    7:{'actor':ismrm6,'slot':( 64*K+32*K, 78*K+32*K ) }, # mam               
                    # explained

                    
                    71:{'actor':ismrm8,'slot':( 80*K+32*K, 88*K+32*K ) },#colourmap
                    
                    
                    711:{'actor':bend,'slot':( 90*K+32*K, 100*K+32*K) },#colourbrain
                    
                    
                    712:{'actor':tex1,'slot':( 90*K+32*K, 100*K+32*K) },#colourbrain
                    #text
                    

                    72:{'actor':ismrm9,'slot':( 102*K+32*K, 110*K+32*K ) },#prior
                    #knowledge
                    

                    8:{'actor':ismrm7,'slot':( 112*K+32*K, 120*K+32*K ) }, # corresponding
                    

                    81:{'actor':b1,'slot':( 122*K+32*K, 142*K+32*K ) }, #picking tracks

                    #here

                    811:{'actor':ismrm13,'slot':( 122*K+32*K, 142*K+32*K ) },#picking
                    #label
                    

                    82:{'actor':redcyan1,'slot':( 144*K+32*K, 154*K+32*K ) }, #red
                    #cyan
                    

                    821:{'actor':ismrm14,'slot':( 144*K+32*K, 154*K+32*K ) }, #red
                    #cyan text
                    
                    
                    83:{'actor':redcyanblue1,'slot':( 156*K+32*K, 166*K+32*K ) },# 3
                    # brains 1
                    

                    831:{'actor':ismrm15,'slot':( 156*K+32*K, 166*K+32*K ) },# 3
                    # brains 1 text

                    
                    
                    84:{'actor':redcyanblue2,'slot':( 168*K+32*K, 178*K+32*K) },# 3
                    # brains 2

                    841:{'actor':ismrm16,'slot':( 168*K+32*K, 178*K+32*K) },# 3
                    # brains 2 tex
                    

                    9:{'actor':ismrm10,'slot':( 180*K+32*K, 192*K+32*K) },# conclusion
                    

                    10:{'actor':ismrm11,'slot':( 194*K+32*K, 210*K+32*K) },# software
                    

                    11:{'actor':ismrm12,'slot':( 212*K+32*K, 220*K+32*K) },# references
                    

                    12:{'actor':bend,'slot':( 223*K+32*K, 250*K+32*K) }, # rotating

                    
                    13:{'actor':ismrm17,'slot':( 223*K+32*K, 250*K+32*K) }} # rotating tex
                   
                    




       

        
          
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




class PlotWorking():


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
        

        
                 



        



        
