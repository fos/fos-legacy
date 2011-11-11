import numpy as np
from fos.lib.pyglet.gl import *
from fos import Actor, World
from fos.lib.pyglet.lib import load_library
glib=load_library('GL')
from fos.actor.axes import Axes


class Line(Actor):
    """Generate n randomm lines of pts points.

    This is useful to test peformances of the draw() method.
    """

    def __init__(self, scale = 1.0, line_width=2., pts=12, n=10000):

        self.vertices = np.ascontiguousarray(np.random.randn(pts*n,3).astype('f4'))
        self.vertices *= scale
        
        self.colors = np.ascontiguousarray(np.random.rand(pts*n,3).astype('f4'))
        
        self.vptr=self.vertices.ctypes.data
        self.cptr=self.colors.ctypes.data        
        
        self.count=np.random.permutation(np.array([pts]*n, dtype=np.int32))[:10]
        self.first=np.random.permutation(np.arange(0,pts*n,pts, dtype=np.int32))[:10]
        
        self.firstptr=self.first.ctypes.data
        self.countptr=self.count.ctypes.data
        
        self.line_width=line_width
        self.items=10
       
        # self.index=self.compile_gl()        
                
        self.show_aabb = False        
        self.make_aabb((np.array([-scale,-scale,-scale]),np.array([scale,scale,scale])),margin = 0)
        
    
    def update(self, dt):
        pass


    def draw(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        glVertexPointer(3,GL_FLOAT,0,self.vptr)
        glColorPointer(4,GL_FLOAT,0,self.cptr)
        glLineWidth(self.line_width)
        glPushMatrix()
        glib.glMultiDrawArrays(GL_LINE_STRIP, self.firstptr,self.countptr, self.items)
        glPopMatrix()
        
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)      
        glLineWidth(1.)



if __name__ == '__main__':

    from fos import World, Window, WindowManager

    ax = Line(100)
    
    w=World()
    w.add(ax)
        
    #windowing    
    wi = Window(caption="Spaghetti by Free On Shades (fos.me)",bgcolor=(0,0.,0.2,1),width=800,height=600)
    wi.attach(w)
    wm = WindowManager()
    wm.add(wi)
    wm.run()
    
