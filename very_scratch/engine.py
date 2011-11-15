import numpy as np

#from fos.lib import pyglet

from fos.core.world import World
from fos.core.fos_window import FosWindow
from fos.core.camera import DefaultCamera
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
   
    # create a window
    # attach window to world
    wi = FosWindow(bgcolor=color.orange)
    wi.attach(w)

