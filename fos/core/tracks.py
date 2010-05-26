import numpy as np
import OpenGL.GL as gl


from fos.core.scene  import Scene
from fos.core.actors import Actor
from fos.core.plots  import Plot
from fos.core.primitives import Empty

   


class Tracks(Actor):

    def __init__(self,data,colors,mode='default',line_width=3.):
        
        self.data=data

        self.colors=colors

        self.line_width=line_width

        self.list_index = None

        self.mode = mode

        #self.init()

    def init(self):

        if self.mode == 'default':

            self.init_default()

        else:

            self.init_vbos()
        

    def init_default(self):

        self.list_index = gl.glGenLists(1)
 
        gl.glNewList( self.list_index,gl.GL_COMPILE)


        gl.glDisable(gl.GL_LIGHTING)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glEnable(gl.GL_BLEND)
        

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glLineWidth(self.line_width)

        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        

        counts=[len(d) for d in self.data]

        cdata=np.concatenate(self.data)

        first=np.array(counts).cumsum()

        first=list(np.hstack((np.array([0]),first[:-1])))
        
        ccolors=np.concatenate(self.colors)

        
        
        gl.glVertexPointerf(cdata)

        gl.glColorPointerf(ccolors)
       

        gl.glMultiDrawArrays(gl.GL_LINE_STRIP,first,counts,len(counts)) 


        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)


        gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_DEPTH_TEST)

        gl.glEndList()

    def init_vbos(self):

        pass


    def display(self):

        gl.glCallList(self.list_index)

        gl.glFinish()

    def process_picking(self):

        pass

    


    
