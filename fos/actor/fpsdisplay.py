from fos.lib import pyglet
from fos.core.actor import Actor

class FPSDisplay(Actor):
    
    def __init__(self):
        
        self.fps_display = pyglet.clock.ClockDisplay()
        
    def draw(self):
        self.fps_display.draw()
