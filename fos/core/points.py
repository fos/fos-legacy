import numpy as np
import OpenGL.GL as gl
from OpenGL.arrays import vbo
from fos.core.actors import Actor

class Points(Actor):

    def __init__(self,data,colors,point_size=3.,lists=True):

        Actor.__init__(self)

        self.data=data
        self.cdata=None
        self.colors=colors
        self.point_size=point_size
        self.list_index = None
        self.near_pick_prev = None
        self.near_pick = None
        self.far_pick_prev = None
        self.far_pick = None        
        self.picked_track = None
        self.picked_tracks = []
        self.vbo = None
        self.lists = lists

        
    def init(self):

        self.init_default()
       

    def init_default(self):

        self.counts=[len(d) for d in self.data]
        cdata=np.concatenate(self.data)
        first=np.array(self.counts).cumsum()
        self.first=list(np.hstack((np.array([0]),first[:-1])))        
        ccolors=np.concatenate(self.colors)
        self.min=np.min(cdata,axis=0)
        self.max=np.max(cdata,axis=0)
        self.mean=np.mean(cdata,axis=0)        
        cdata = cdata - self.mean
        self.cdata = cdata
        
        stack=np.hstack((cdata,ccolors))
        stack=stack.astype('float32')
        self.vbo = vbo.VBO(stack,usage='GL_STATIC_DRAW')

        #print self.counts, self.first

        if self.lists:
            
            self.list_index = gl.glGenLists(1)
            gl.glNewList( self.list_index,gl.GL_COMPILE)
            self._execute_vbos()
            gl.glEndList()

    def _execute_vbos(self):

        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)
        #gl.glLineWidth(self.line_width)
        gl.glPointSize(self.point_size)
        
        self.vbo.bind()

        try:

            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glEnableClientState(gl.GL_COLOR_ARRAY)
            #gl.glVertexPointerf(cdata)
            gl.glVertexPointer(3, gl.GL_FLOAT, 28, self.vbo )
            gl.glColorPointer(4, gl.GL_FLOAT, 28, self.vbo+12 )
            gl.glMultiDrawArrays(gl.GL_POINTS,\
                                 self.first,self.counts,len(self.counts)) 

        finally:

            self.vbo.unbind()

        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisable(gl.GL_BLEND)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_DEPTH_TEST)


    def display(self):

        if self.near_pick!= None:
            
            #print self.near_pick
            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:                
                self.process_picking(self.near_pick, self.far_pick)
                self.near_pick_prev = self.near_pick
                self.far_pick_prev = self.far_pick
        
        gl.glPushMatrix()
        x,y,z = self.position
        gl.glTranslatef(x,y,z)

        if self.lists:
            gl.glCallList(self.list_index)
        else:
            self._execute_vbos()
        
        gl.glPopMatrix()

    def process_picking(self,near,far):

        pass
