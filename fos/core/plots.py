import fos.core.primitives as prim

class Plot():

    def __init__(self):

        self.slots=None

        self.time=0

    def init(self):
        

        global im1

        im1 = prim.Image2D('/home/eg309/Devel/Fos/fos/core/tests/data/small_latex1.png')

        im1.init()

        global im2

        im2 = prim.Image2D('/home/eg309/Devel/Fos/fos/core/tests/data/small_latex1.png')

        im2.init()

        im2.position=[400,400,0]


        self.slots={0:{'actor':im1,'slot':(5000,10000)},
                    1:{'actor':im2,'slot':(15000,20000)}}

          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].display()
        

    def update_time(self,time):

        self.time=time
        

        
                 



        



        
