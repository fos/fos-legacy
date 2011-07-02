import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor, World, Window, WindowManager

from fos.lib.pyglet.text import Label
from fos.lib.pyglet.graphics import Batch
        
        
class Dummy(Actor):
    
    def __init__(self, *args, **kwargs):
        """ Draw a dummy actor for testing
                
        """
        super(Dummy, self).__init__()
        
        self.batch = Batch()
        
        fos.lib.pyglet.text.Label('Hello, world', 
                                  font_name='Times New Roman', 
                                  font_size=36,
                                  dpi=250,
#                                  x=window.width//2, y=window.height//2,
                                  anchor_x='center', anchor_y='center',
                                  batch = self.batch)
        fos.lib.pyglet.text.Label('Hi', 
                                  font_name='Times New Roman', 
                                 font_size=26,
                                  dpi=100,
#                                  x=window.width//2, y=window.height//2,
                                  anchor_x='center', anchor_y='center',
                                  batch = self.batch)
        
        
    def update(self, dt):
        pass
        
    def draw(self):
        pass
        glPushMatrix()
        #glRotatef(5.0, 0, 1, 0)
        glTranslatef(-100,0,0)
        self.batch.draw()
        glPopMatrix()
        

            
if __name__ == '__main__':
    w = World()
    wi = Window()
    act = Dummy()
    w.add(act)
    
    wm = WindowManager()
    wm.add(wi)
    wm.run()
        
