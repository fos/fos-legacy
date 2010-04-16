import OpenGL.GL as gl
import fos.core.primitives as prim




class Plot():


    def __init__(self):

        self.slots=None

        self.time=0

    def init(self):
        

        global im1

        im1 = prim.Image2D('/home/eg01/Devel/Fos/fos/core/tests/data/small_latex1.png')

        im1.init()     
             
        global b1


        b1 = prim.Tracks3D('/home/eg01/Data_Backup/Data/Eleftherios/CBU090133_METHODS/20090227_145404/Series_003_CBU_DTI_64D_iso_1000/dtk_dti_out/dti_FACT.trk')

        b1.init()

        #print b1.min, b1.max, b1.mean

        b1.position=tuple(-b1.mean)


        self.slots={ 0:{'actor':im1,'slot':(1000,20000) },
                     1:{'actor':b1, 'slot':(5000,60000) }}

        

          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].display()
        

    def update_time(self,time):

        self.time=time










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
        

        
                 



        



        
