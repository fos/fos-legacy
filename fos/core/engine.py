import numpy as np

from fos.lib import pyglet
from fos.core.world import World
from fos.actor.volslicer import ConnectedSlices
from fos.core.fos_window import FosWindow
from fos.core.camera import DefaultCamera

class Engine():

    def __init__(self):        
        self.worlds = []
    
    def run(self):
        pyglet.clock.schedule(self.update, 1/60.0)
                
    def add(self, world):
        self.worlds.append(world)
        
    def update(self, dt):
        print "dt", dt    
        # this should call the update of all the actors
        # in a world
                    
if __name__ == '__main__':
    
    eng = Engine()
    
    # create a world
    w = World(0)
    
    # create default camera
    cam = DefaultCamera()
    
    # add camera
    w.add(cam)
    
    # create image viewr
    a=np.random.random( ( 100, 100, 100) )
    aff = np.eye(4)
    cds = ConnectedSlices(aff,a)
    
    # add cds to world
    w.add(cds)
    
    # add world to engine
    eng.add(w)
    
    # create a window
    wi = FosWindow()
    
    # attach window to world
    wi.attach(w)
    
    wi2 = FosWindow()
    # attach window to world
    wi2.attach(w)
    
    # run the engine
    eng.run()
    

    