import sys
import numpy as np
import nibabel as nib

#from eudx_results import show_tracks
from fos.actor.slicer import Slicer
from fos import Actor,World, Window, WindowManager
from pyglet.gl import *

class Point(Actor):

    def __init__(self,positions,colors=(1.,0,0,1),pointsize=2,affine=None):
        """ Plot points in 3D 

        Parameters
        -----------
        positions : float32, shape (N,3)
        colors : None, cyan colour all points
                tuple, len(4), same colour all points
                array, shape (N,4), a colour for each point
        pointsize : int
        affine : array, shape (4,4), extra transformation

        """
        super(Actor, self).__init__()

        if affine == None:
            # create a default affine
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine
        if colors == None:
            self.colors = np.array( [[0,1,1,1]], 
                    dtype = np.float32).repeat(len(positions),axis=0)        
        try:
            if colors.ndim==2:
                self.colors=colors.astype(np.float32)
        except AttributeError:
            self.colors = np.array( [colors], dtype = np.float32).repeat(len(positions),axis=0) 
            
        self.vertices=np.array([[-100,-100,-100],[100,100,100]])
        self.make_aabb(margin=0)
        self.show_aabb=True
        self.positions = positions.astype(np.float32)
        self.vert_ptr = self.positions.ctypes.data
        self.color_ptr = self.colors.ctypes.data
        self.nopoints=len(self.positions)
        self.pointsize = pointsize

    def update(self,dt):
        pass

    def draw(self):
        self.set_state()
        glPushMatrix()
        #glMultMatrixf(self.glaffine)        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vert_ptr)
        glColorPointer(4, GL_FLOAT, 0, self.color_ptr)
        glPointSize(self.pointsize)
        glDrawArrays(GL_POINTS, 0, self.nopoints )
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()
        self.unset_state()

    def process_mouse_motion(self,x,y,dx,dy):
        self.mouse_x=x
        self.mouse_y=y

    def process_keys(self,symbol,modifiers):
        pass

    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unset_state(self):
        glDisable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)


if __name__=='__main__':

    pos1=100*np.random.rand(100,3) -50
    cloud1 = Point(pos1,colors=(1,0,0,1.),pointsize=2.)

    pos2=100*np.random.rand(100,3) -50   
    cloud2 = Point(pos2,colors=np.random.rand(100,4),pointsize=5.)

    w=World()
    w.add(cloud1)
    w.add(cloud2)

    wi = Window(caption="Fos",\
                bgcolor=(.3,.3,.6,1.),\
                width=1600,\
                height=900)
    wi.attach(w)

    wm = WindowManager()
    wm.add(wi)
    wm.run()


    


















