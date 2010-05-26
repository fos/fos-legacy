from fos.core.actors import Actor


class Empty(Actor):

    def __init__(self):

        pass

    def init(self):

        pass

    def display(self):

        print 'Near_pick', self.near_pick

        print 'Far_pick', self.far_pick

        

