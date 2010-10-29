from math import sin, cos,sqrt
import numpy as np

#pyglet.options['debug_gl']=False

from fos.core.fos_window import FosWindow
import fos.core.collision as cll


class Engine():

    def __init__(self):        
        self._window = None
        
    
    def run(self):
        
        self._window = FosWindow(width=1024,
                                 height=768,
                                 caption='The Light Machine',
                                 resizable=True,
                                 vsync=False)
        
        # pyglet.window.Window
#        self._window = FosWindow(width=self.width,\
#                              height=self.height,\
#                              caption='The Light Machine',\
#                              resizable=True,\
#                              vsync=False)
#                              #config=self.config)
        

#
#        schedule(update)
#                
#        print('NeoFos started')
#        # call the event loop of FosWindow, which subclasses
#        # ManagedWindow that implements its own event loop
#        pyglet.app.run()
        

    def show(self):
        """
        Creates and displays window, or activates it
        (gives it focus) if it has already been created.
        """
        print "in show"
        if self._window and not self._window.has_exit:
            self._window.activate()
        else:
            self._win_args['visible'] = True
            self.axes.reset_resources()
            
            #self._window = PlotWindow(self, **self._win_args)
            

Engine().run()
# show the one and only window for now
#Engine().show()


