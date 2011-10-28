import numpy as np
import nibabel as nib
import os.path as op
#Fos modules
from fos import Actor
from fos import World, Window, WindowManager
from fos.actor.curve import InteractiveCurves
from fos.data import get_track_filename
from fos.lib.pyglet.window import key
from fos.core.utils import screen_to_model
import fos.core.collision as cll
from fos.lib.pyglet.gl import *
#dipy modules
from dipy.segment.quickbundles import QuickBundles


streams,hdr = nib.trackvis.read(get_track_filename())
#center the data
T=[s[0] for s in streams]
mean_T=np.mean(np.concatenate(T),axis=0)
T=[t-mean_T for t in T]

qb=QuickBundles(T,10.,12)
Tqb=qb.virtuals()
Tqbe,Tqbei=qb.exemplars()

class TrackLabeler(Actor):   
    
    def __init__(self,qb,tracks,colors=None,line_width=2.,affine=None):
        
        self.virtuals=qb.virtuals()
        self.tracks=tracks           
        if affine is None:
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine            
        #aabb - bounding box things
        ccurves=np.concatenate(tracks)
        self.min=np.min(ccurves,axis=0)
        self.max=np.max(ccurves,axis=0)        
        self.position=(0,0,0)
        coord1 = np.array([ccurves[:,0].min(),ccurves[:,1].min(),ccurves[:,2].min()], dtype = 'f4')        
        coord2 = np.array([ccurves[:,0].max(),ccurves[:,1].max(),ccurves[:,2].max()], dtype = 'f4')
        self.make_aabb((coord1,coord2),10)
        print('MBytes %f' % (ccurves.nbytes/2.**20,))
        del ccurves
        #buffer for selected virtual tracks
        self.selected=[]
        self.updated=False
        self.line_width=line_width
                
        #compile GL lists for virtuals
        self.virtuals_index, self.virtuals_list=self.compile_tracks(self.virtuals,None)        
        #compile GL for partitions
        self.part_index=[]
        for i in range(len(self.virtuals)):
            part_tracks=qb.label2tracks(self.tracks,i)
            tmp_index,tmp_list=self.compile_tracks(part_tracks,None)
            self.part_index.append(tmp_index)
        self.part_selected=np.zeros(len(self.virtuals))       
        
    def compile_tracks(self,tracks,colors=None):
        #print 'compile tracks'        
        vertex_list =len(tracks)*[None]        
        for i,curve in enumerate(tracks):
            curve=curve.astype('f')
            vertices=tuple(curve.ravel().tolist())
            if colors==None:
                color=np.tile(np.array([1,1,1,1.]),(len(curve),1)).astype('f')
            else:
                color=np.tile(colors[i],(len(curve),1)).astype('f')
            color=255*color
            color=np.round(color).astype('ubyte')
            color=tuple(color.ravel().tolist())                             
            vertex_list[i]= fos.lib.pyglet.graphics.vertex_list(len(curve),('v3f/static',vertices),('c4B/static',color))
        index=self.compile_gl(vertex_list,range(len(tracks)))
        print('compiled tracks %d' % len(tracks))
        return index,vertex_list
        
    def compile_gl(self,vertex_list,range_vl):                    
        index=glGenLists(1)
        glNewList(index,GL_COMPILE)
        [vertex_list[i].draw(GL_LINE_STRIP) for i in range_vl]        
        glEndList()
        return index

    def draw(self):        
        self.set_state()        
        glCallList(self.virtuals_index)
        for (i,index) in enumerate(self.part_selected):
            if index==1:
                glCallList(self.part_index[i])
        self.unset_state()
    
    def process_mouse_motion(self,x,y,dx,dy):
        self.mouse_x=x
        self.mouse_y=y

    def process_pickray(self,near,far):
        pass
    
    def update(self,dt):
        if self.updated==False:
            print 'compile again'
            self.virtuals_index=self.compile_gl(self.virtuals_list,range(len(self.virtuals)))
            self.updated=True
    
    def process_keys(self,symbol,modifiers):        
        prev_selected=list(self.selected)
        part_selected=list(self.part_selected)                      
        if symbol==key.P:
            print 'P'
            id=self.picking_virtuals(symbol,modifiers)            
            if prev_selected.count(id)==0:
                self.selected.append(id)       
                ncolor=len(self.virtuals[id])*(255,0,0,255)
                self.virtuals_list[id].colors=ncolor                
            if prev_selected.count(id)==1:
                self.selected.remove(id)                       
                ncolor=len(self.virtuals[id])*(255,255,255,255)
                self.virtuals_list[id].colors=ncolor                
            print self.selected       
        if symbol==key.E:
            print 'E'
            id=self.picking_virtuals(symbol,modifiers)
            print id
            if part_selected[id]==0: self.part_selected[id]=1
            if part_selected[id]==1: self.part_selected[id]=0
            print part_selected
            print self.part_selected
        if symbol==key.K:
            print 'K'
        
        self.updated=False
    
    def picking_virtuals(self,symbol,modifiers):
        x,y=self.mouse_x,self.mouse_y
        nx,ny,nz=screen_to_model(x,y,0)
        fx,fy,fz=screen_to_model(x,y,1)        
        near=(nx,ny,nz)
        far=(fx,fy,fz)
        min_dist_info=[ cll.mindistance_segment2track_info(near,far,xyz) \
                for xyz in self.virtuals]
        A = np.array(min_dist_info)        
        dist=10**(-3)
        np.where(A[:,0]<dist)
        iA=np.where(A[:,0]<dist)
        minA=A[iA]
        if len(minA)==0:            
            iA=np.where(A[:,0]==A[:,0].min())
            minA = A[iA]        
        miniA=minA[:,1].argmin()        
        return iA[0][miniA]
    
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

tl = TrackLabeler(qb,qb.downsampled_tracks())

w=World()
w.add(tl)

wi = Window(caption="Tractography Labeler by Free On Shades (http://fos.me)")
wi.attach(w)

wm = WindowManager()
wm.add(wi)
wm.run()

