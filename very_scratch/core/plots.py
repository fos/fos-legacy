

MS=1000


class Plot():


    def __init__(self,slots=None):

        
        self.slots = slots

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        

    def init(self):        

        for s in self.slots:

            self.slots[s]['actor'].init()

          
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


                                                  
        
        



