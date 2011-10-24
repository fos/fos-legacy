import numpy as np

from fos import Actor
import fos.lib.pyglet as pyglet
from fos.lib.pyglet.gl import *
import fos.core.collision as cll
from fos.actor.primitives import AABBPrimitive

class InteractiveCurves(Actor):

    def __init__(self,curves,colors=None,line_width=2.,centered=True,affine=None):
    
        #super(InteractiveCurves, self).__init__()
        
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
        
        #print coord1
        #print coord2
        self.make_aabb((coord1,coord2),10)
        
        #self.aabb=AABBPrimitive(np.array([-1000,-1000,1000]),np.array([1000,1000,-1000]),margin=0)

        print 'MBytes',ccurves.nbytes/2.**20
        self.curves_nbytes=ccurves.nbytes

        if colors==None:
            self.main_color=np.array([1,1,1,1])
            #np.tile(len(ccurves),

        self.curves=curves
        self.centered=centered
        
        for i,curve in enumerate(curves):
            if centered:
                curve=curve-self.mean
            curve=curve.astype('f')
            vertices=tuple(curve.ravel().tolist())

            if colors==None:
                color=np.tile(self.main_color,(len(curve),1)).astype('f')
            else:
                color=np.tile(colors[i],(len(curve),1)).astype('f')
            color=255*color
            color=np.round(color).astype('ubyte')
            color=tuple(color.ravel().tolist())
                           
            self.vertex_list[i]= fos.lib.pyglet.graphics.vertex_list(len(curve),('v3f/static',vertices),('c4B/static',color))

        self.compile_gl()
        
    def compile_gl(self):            
        index=glGenLists(1)
        glNewList( index,GL_COMPILE)
        [self.vertex_list[i].draw(GL_LINE_STRIP) for i in self.range_vl]
        glEndList()
        self.list_index=index
        

    def draw(self):
        
        self.set_state()
        if self.curves_nbytes < 0: #!!!disabled for now
            [self.vertex_list[i].draw(GL_LINE_STRIP) for i in self.range_vl]
        else:        
            if self.updated:
                print('Updating...')
                self.updated=False
                t1=time.clock()
                prev=self.list_index
                self.compile_gl()                
                glCallList(self.list_index)
                print('Updated')
            else:
                glCallList(self.list_index)
        self.unset_state()     
        
                  
    def update(self,dt):
        
        #print 'dt',dt
        cr=self.current
        if cr!=None:
            self.current=None
            #change colors of selected curve
            if self.selected.count(cr)==0:
                self.selected.append(cr)
                color=self.vertex_list[cr].colors[:4]                
                r,g,b,a=color                
                background=(c_float*4)()
                glGetFloatv(GL_COLOR_CLEAR_VALUE,background)
                br,bg,bb,ba=background
                br,bg,bb,ba=int(round(255*br)),int(round(255*bg)),\
                    int(round(255*bb)),int(round(255*ba))                
                ncolors=len(self.curves[cr])*((r+br)/2,(g+bg)/2,(b+bb)/2,a)
                self.vertex_list[cr].colors=ncolors
            
            elif self.selected.count(cr)>0:
                self.selected.remove(cr)
                color=self.vertex_list[cr].colors[:4]
                r,g,b,a=color                
                background=(c_float*4)()
                glGetFloatv(GL_COLOR_CLEAR_VALUE,background)
                br,bg,bb,ba=background
                br,bg,bb,ba=int(round(255*br)),int(round(255*bg)),\
                    int(round(255*bb)),int(round(255*ba))                
                ncolors=len(self.curves[cr])*(2*r-br,2*g-bg,2*b-bb,a)
                self.vertex_list[cr].colors=ncolors

            self.updated=True 

    def process_pickray(self,near,far):
        
        #print 'near',near,'far',far
        
        if self.centered:
            shift=np.array(self.position)-self.mean
            print 'shift', shift
        else:
            shift=np.array([0,0,0])
                
        min_dist_info=[ cll.mindistance_segment2track_info(near,far,xyz+shift) \
                for xyz in self.curves]

        #print'Min distance info'        
        #print min_dist_info
        A = np.array(min_dist_info)
        #print A
        dist=10**(-3)
        np.where(A[:,0]<dist)
        iA=np.where(A[:,0]<dist)
        minA=A[iA]

        if len(minA)==0: 
            #print 'IN'
            iA=np.where(A[:,0]==A[:,0].min())
            minA = A[iA]
            
        #print 'A','minA next',minA, iA
        miniA=minA[:,1].argmin()
        
        #print 'track_center',self.position, 'selected',iA[0][miniA]
        print 'track_id',iA[0][miniA]
        
        self.current=iA[0][miniA]
        #self.selected.append(self.current)
        #self.selected=list(set(self.selected))
        #pass
        
       
    def set_state(self):
        #glClearColor(1,0.1,0.9,1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        #glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
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
