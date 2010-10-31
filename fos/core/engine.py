import numpy as np

#from fos.lib import pyglet

from fos.core.world import World
from fos.core.fos_window import FosWindow
from fos.core.camera import DefaultCamera
from fos.actor.cubes import Cubes

# actors
from fos.actor.volslicer import ConnectedSlices

class Engine():

    def __init__(self):        
        self.worlds = []
        
#        self.clock = pyglet.clock.Clock()
#        self.clock.schedule(self.update)
                     
    def run(self):
        self.running = True
        
#        while self.running:
#            dt = self.clock.tick()
#            print "dt", dt    
                        
    def add(self, world):
        self.worlds.append(world)
                
    def update(self, dt):
        print "dt", dt    
        # this should call the update of all the actors
        # in a world
        
    def stop(self):
        self.running = False

if __name__ == '__main__':
    
#    eng = Engine()
#    eng.run()
    
    # create a world
    w = World(0)    
    
    # create default camera
    cam = DefaultCamera()
    
    # add camera
    w.add(cam)
    
    
#    from itertools import chain, islice, product, repeat
#    
#    edge=1.
#    e2 = edge / 2
#    verts = list(product(*repeat([-e2, +e2], 3)))
#    faces = [
#        [0, 1, 3, 2], # left
#        [4, 6, 7, 5], # right
#        [7, 3, 1, 5], # front
#        [0, 2, 6, 4], # back
#        [3, 7, 6, 2], # top
#        [1, 0, 4, 5], # bottom
#    ]
#    
    
    vertices=100*np.array([[0,1.,-1],[-1,-1,-1],[-1,1,-1]])
    faces=np.array([[0,1,2]])
    values=255*np.ones(3)                   
        

    from fos.actor.surf import Surface
    from fos.actor.surf import CommonSurfaceGroup, IlluminatedSurfaceGroup
    
    group=CommonSurfaceGroup()#IlluminatedSurfaceGroup()#CommonSurfaceGroup()
    s=Surface(values,vertices,faces,group)
#    w.add(s)

    mycubes = Cubes( np.array([20.0,0.0,0.0]) )
    w.add(mycubes)
    # create image viewr
#    a=np.random.random( (100, 100, 100) )
#    aff = np.eye(4)
#    cds = ConnectedSlices(aff,a)
    
    #add cds to world
    #w.add(cds)
#    

    # create a window
    # attach window to world
    wi = FosWindow()
    wi.attach(w)

