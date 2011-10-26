import numpy as np

from fos import Actor
import fos.lib.pyglet as pyglet
from fos.lib.pyglet.gl import *
import fos.core.collision as cll
from fos.actor.primitives import AABBPrimitive

class InteractiveCurves(Actor):

    def __init__(self,curves,colors=None,line_width=2.,affine=None):
            
        if affine is None:
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine
        
        self.vertex_list =len(curves)*[None]
        self.len_vl=len(curves)
        self.range_vl=range(len(curves))
        self.selected=[]
        self.current=None        
        self.main_color=None
        self.updated=False
        self.line_width = line_width

        ccurves=np.concatenate(curves)
        self.min=np.min(ccurves,axis=0)
        self.max=np.max(ccurves,axis=0)
        self.mean=np.mean(ccurves,axis=0)
        self.position=(0,0,0)
                
        coord1 = np.array([ccurves[:,0].min(),
                           ccurves[:,1].min(),
                           ccurves[:,2].min()], dtype = np.float32)
        
        coord2 = np.array([ccurves[:,0].max(),
                           ccurves[:,1].max(),
                           ccurves[:,2].max()], dtype = np.float32)
        
        self.make_aabb((coord1,coord2),10)
         #self.aabb=AABBPrimitive(np.array([-1000,-1000,1000]),np.array([1000,1000,-1000]),margin=0)
        print 'MBytes',ccurves.nbytes/2.**20
        self.curves_nbytes=ccurves.nbytes         
        self.curves=curves
        self.add_tracks(curves,colors)        
        
    def add_tracks(self,curves,colors=None):
        print 'adding tracks'
        if colors==None:
            main_color=np.array([1,1,1,1])
        for i,curve in enumerate(curves):
            curve=curve.astype('f')
            vertices=tuple(curve.ravel().tolist())
            if colors==None:
                color=np.tile(main_color,(len(curve),1)).astype('f')
            else:
                color=np.tile(colors[i],(len(curve),1)).astype('f')
            color=255*color
            color=np.round(color).astype('ubyte')
            color=tuple(color.ravel().tolist())                             
            self.vertex_list[i]= fos.lib.pyglet.graphics.vertex_list(len(curve),('v3f/static',vertices),('c4B/static',color))
        self.range_vl=range(len(curves))
        #print self.range_vl                
        self.compile_gl()
        
    def compile_gl(self):            
        index=glGenLists(1)
        glNewList( index,GL_COMPILE)
        [self.vertex_list[i].draw(GL_LINE_STRIP) for i in self.range_vl]
        glEndList()
        self.list_index=index       

    def draw(self):        
        self.set_state()        
        glCallList(self.list_index)        
        self.draw_aabb()
        self.unset_state()        
                  
    def update(self,dt):        
        cr=self.current
        if cr!=None:            
            if self.selected.count(cr)==0:
                self.selected.append(cr)
                color=self.vertex_list[cr].colors[:4]                
                r,g,b,a=color                
                ncolors=len(self.curves[cr])*(255,255,255,a)
                self.vertex_list[cr].colors=ncolors            
            if self.selected.count(cr)>0:                
                color=self.vertex_list[cr].colors[:4]
                r,g,b,a=color               
                ncolors=len(self.curves[cr])*(150,0,0,a)
                self.vertex_list[cr].colors=ncolors
            self.current=None
            self.updated=True

    def process_pickray(self,near,far):        
                        
        min_dist_info=[ cll.mindistance_segment2track_info(near,far,xyz) \
                for xyz in self.curves]
        A = np.array(min_dist_info)        
        dist=10**(-3)
        np.where(A[:,0]<dist)
        iA=np.where(A[:,0]<dist)
        minA=A[iA]
        if len(minA)==0:            
            iA=np.where(A[:,0]==A[:,0].min())
            minA = A[iA]        
        miniA=minA[:,1].argmin()        
        print 'track_id',iA[0][miniA]        
        self.current=iA[0][miniA]        
        if self.selected.count(self.current)==0:            
            self.selected.append(self.current)
        if self.selected.count(self.current)>0:
            self.selected.remove(self.current)
            
    def process_keys(self,symbol,modifiers):        
        #print symbol
        pass
        
    def process_mouse_motion(self,x,y,dx,dy):
        #print x,y
        pass
       
    def set_state(self):        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)        
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(self.line_width)
        
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDisable(GL_LINE_SMOOTH)
        glLineWidth(self.line_width)

    def delete(self):
        for i in range(len(self.vertex_list)):
            self.vertex_list[i].delete()
