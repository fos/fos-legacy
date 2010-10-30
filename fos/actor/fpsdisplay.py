from fos.lib import pyglet
from fos.core.actor import Actor

class FPSDisplay(Actor):
    
    def __init__(self):
        self.fps_display = pyglet.clock.ClockDisplay()
        print "fps display created", self.fps_display
        
    def draw(self):
        print "draw fps display"
        self.fps_display.draw()
