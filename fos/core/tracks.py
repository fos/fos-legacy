import numpy as np
import OpenGL.GL as gl


from fos.core.scene  import Scene
from fos.core.actors import Actor
from fos.core.plots  import Plot
from fos.core.primitives import Empty

import fos.core.collision as cll


class Tracks(Actor):

    def __init__(self,data,colors,line_width=3.):

        Actor.__init__(self)
        
        self.data=data

        self.cdata=None

        self.colors=colors

        self.line_width=line_width

        self.list_index = None

        self.near_pick_prev = None

        self.near_pick = None

        self.far_pick_prev = None

        self.far_pick = None
        
        self.picked_track = None

    def init(self):

        self.init_default()
        

    def init_default(self):


        counts=[len(d) for d in self.data]

        cdata=np.concatenate(self.data)

        first=np.array(counts).cumsum()

        first=list(np.hstack((np.array([0]),first[:-1])))
        
        ccolors=np.concatenate(self.colors)

        self.min=np.min(cdata,axis=0)

        self.max=np.max(cdata,axis=0)

        self.mean=np.mean(cdata,axis=0)

        
        cdata = cdata - self.mean

        self.cdata = cdata

        self.list_index = gl.glGenLists(1)
 
        gl.glNewList( self.list_index,gl.GL_COMPILE)
        

        gl.glDisable(gl.GL_LIGHTING)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glEnable(gl.GL_BLEND)
        

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glLineWidth(self.line_width)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
       
        
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


        '''
        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)                
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
        '''

        print self.near_pick

        print self.far_pick


        self.process_picking(self.near_pick, self.far_pick)                
        self.near_pick_prev = self.near_pick

        self.far_pick_prev = self.far_pick
        

        gl.glPushMatrix()

        x,y,z = self.position

        gl.glTranslatef(x,y,z)

        gl.glCallList(self.list_index)

        gl.glPopMatrix()



    def process_picking(self,near,far):

        print('process picking')

        #min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        #min_dist=np.array(min_dist)

        #print min_dist

        #self.picked_track=min_dist.argmin()

        #print 'min index',self.picked_track

        
        print 'near',near
        print 'far', far
        

        if near!=None:

            print cll.mindistance_segment2track_info(near,far,self.data[0]-self.mean)

            print cll.mindistance_segment2track_info(near,far,self.data[1]-self.mean)

        '''

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        A = np.array(min_dist_info)

        dist=10**(-3)

        iA=np.where(A[:,0]<dist)

        minA=A[iA]

        print 'minA ', minA

        miniA=minA[:,1].argmin()

        print 'final min index ',iA[0][miniA]

        self.picked_track=iA[0][miniA]

        '''
    


    
