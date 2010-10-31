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
        

'''
window = pyglet.window.Window()

def test(dt):
    print "dt", dt
    
pyglet.clock.schedule(test)
fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_draw():
    window.clear()
    fps_display.draw()

pyglet.app.run()
'''
#clock.schedule_interval(self.update, 1/60.)

if __name__ == '__main__':
    
#    eng = Engine()
#    eng.run()
    
    # create a world
    w = World(0)
    
    # create default camera
    cam = DefaultCamera()
    
    # add camera
    w.add(cam)
    
    # create image viewr
    a=np.random.random( (100, 100, 100) )
    aff = np.eye(4)
    cds = ConnectedSlices(aff,a)    
    # add cds to world
    w.add(cds)
#    
    # add world to engine
    #    eng.add(w)
    
    # create a window
    wi = FosWindow()
    
    # attach window to world
    wi.attach(w)
    
#    wi2 = FosWindow()
#    # attach window to world
#    wi2.attach(w)
    
    # run the engine
#    eng.run()
