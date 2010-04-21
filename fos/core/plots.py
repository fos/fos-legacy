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

        b1.angular_speed = 0        

        #print b1.min, b1.max, b1.mean

        b1.position=tuple(-b1.mean)

        
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
        

        
                 



        



        
