'''
batch processing is very important with pyglet. I have some interesting
links below

More Examples
        http://boxfight-python.googlecode.com/svn/trunk/src/listener.py       
        vertices=np.array([[0,0,0],[1,0,0],[0,0,0],[0,1,0]])
        verx=vertices.ravel().tolist()

        Draw 2 axes
        
        self.vertex_list =
        batch.add(4,GL_LINES,group,('v3d/static',verx))

        inds=[0,1,2,3]
        
        self.vertex_list =
        batch.add_indexed(4,GL_LINES,group,inds,('v3d/static',verx))


'''

#import OpenGL.GL as GL
import numpy as np
from fos.core.machine import Machine, batch, mouse_x,mouse_y,actors
from fos.imageviewer.arrayimage import ArrayInterfaceImage
import fos.lib.pyglet
#pyglet.options['debug_gl']=False
from fos.lib.pyglet.gl import *
from fos.lib.pyglet.image import Animation, AnimationFrame
import os
from fos.core import collision as cll
import time

ang=0


def vec(*args):
    return (GLfloat * len(args))(*args)

class SmoothLineGroup(pyglet.graphics.Group):
    def set_state(self):
        #glClearColor(1,0.1,0.9,1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        #glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glLineWidth(1.2)
        
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDisable(GL_LINE_SMOOTH)
        glLineWidth(1.)


class InteractiveCurves(object):

    def __init__(self,curves,colors=None,line_width=2.,centered=True):
        self.vertex_list =len(curves)*[None]
        self.len_vl=len(curves)
        self.range_vl=range(len(curves))
        self.selected=[]
        self.current=None        
        self.main_color=None
        self.updated=False

        ccurves=np.concatenate(curves)
        self.min=np.min(ccurves,axis=0)
        self.max=np.max(ccurves,axis=0)
        self.mean=np.mean(ccurves,axis=0)
        self.position=(0,0,0)

        print 'MBytes',ccurves.nbytes/2**20
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

            colors=np.tile(self.main_color,(len(curve),1)).astype('f')
            colors=255*colors
            colors=np.round(colors).astype('ubyte')
            colors=tuple(colors.ravel().tolist())
                           
            self.vertex_list[i]= \
                pyglet.graphics.vertex_list(len(curve),('v3f/static',vertices),\
                                            ('c4B/static',colors))

        self.compile_gl()
        
    def compile_gl(self):            
        index=glGenLists(1)
        glNewList( index,GL_COMPILE)
        [self.vertex_list[i].draw(GL_LINE_STRIP) for i in self.range_vl]
        glEndList()
        self.list_index=index
        

    def draw(self):
        if self.curves_nbytes < 1500000:
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
                #print('Updated in %d secs' % time.clock()-t1)
                #glDeleteList(prev)
            else:
                glCallList(self.list_index)     
        
                  
    def update(self):
        
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
        if self.centered:
            shift=np.array(self.position)-self.mean
            print shift
        else:
            shift=np.array([0,0,0])        
        min_dist_info=[ \
            cll.mindistance_segment2track_info(near,far,xyz+shift) \
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
        print 'track_center',self.position, 'selected',iA[0][miniA]
        self.current=iA[0][miniA]
        #self.selected.append(self.current)
        #self.selected=list(set(self.selected))
        #pass
       

    def delete(self):
        for i in range(len(self.vertex_list)):
            self.vertex_list[i].delete()

def load_animation(image_name,columns,rows):
 
    frame_seq = pyglet.image.ImageGrid(pyglet.image.load(image_name), rows, columns)
    
    frame_list = []
    for row in range(rows, 0, -1):
        end = row * columns
        start = end - (columns -1) -1
        for frame in frame_seq[start:end:1]:
            frame_list.append(AnimationFrame(frame, .1))
    
    #frame_list[(rows * columns) -1].duration = None        
    return Animation(frame_list)
    
         

class Dandelion(object):
    def __init__(self,signals,directions,batch,group=None):

        ''' Visualize the diffusion signal as a dandelion i.e. 
        multiply the signal for each corresponding gradient direction

        Red denotes the maximum signal
        Blue the minimum signal

        Examples
        --------
        signals=data[48,48,28]
        slg=SmoothLineGroup()
        actors.append(Dandelion(signals,gradients,batch=batch,group=slg))
        Machine().run()
        
        '''
        directions=np.dot(np.diag(signals),directions)
        vertices=np.zeros((len(directions)*2,3))
        vertices[::2]=directions
        vertices[1:len(vertices):2]=-directions                
        verx=vertices.ravel().tolist()        
        colors=np.ones((len(vertices),4)) #np.random.rand(len(vertices),3)
        #colors[:len(vertices)/2,1]=np.interp(signals,[signals.min(),signals.max()],[0,1])
        #colors[len(vertices)/2:,1]=colors[:len(vertices)/2,1]
        #colors[:,0]=0
        #colors[:,2]=0
        mxs=np.argmax(signals)
        mns=np.argmin(signals)

        colors[mxs*2]=np.array([1,0,0,1])
        colors[mns*2]=np.array([0,0,1,1])
        
        cols=colors.ravel().tolist()                
        self.vertex_list = batch.add(len(vertices),GL_LINES,group,\
                                         ('v3d/static',verx),\
                                         ('c4d/static',cols))
    
    def update(self):
        pass
    
    def delete(self):
        self.vertex_list.delete()



class CommonSurfaceGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)        
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3.)
       
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glLineWidth(3.)
        pass
    
class IlluminatedSurfaceGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)        
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(3.)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        #Define a simple function to create ctypes arrays of floats:

        glLightfv(GL_LIGHT0, GL_POSITION, vec(.5, .5, 1, 0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(.5, .5, 1, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(1, 1, 1, 1))
        
        glLightfv(GL_LIGHT1, GL_POSITION, vec(1, 0, .5, 0))
        glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.5, .0, 0, 1))
        glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1, 0, 0, 1))

        glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,vec(0.5, 0, 0.3, 0.5))
        glMaterialfv(GL_FRONT_AND_BACK,GL_SPECULAR, vec(1, 1, 1, 0.5))
        glMaterialf(GL_FRONT_AND_BACK,GL_SHININESS, 50)
        
    def unset_state(self):
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glLineWidth(1.)
        glDisable(GL_LIGHTING)
    

class Surface(object):

    def __init__(self,values,vertices,faces,batch,group=None):
            
        inds=faces.ravel().tolist()
        verx=vertices.ravel().tolist()

        normals=np.zeros((len(vertices),3))        
        ones_=np.ones(len(values))
        colors=np.vstack((values,ones_,ones_)).T
        colors=colors.ravel().tolist()
        
        p=vertices
        l=faces
            
        trinormals=np.cross(p[l[:,0]]-p[l[:,1]],\
                                p[l[:,1]]-p[l[:,2]],\
                                axisa=1,axisb=1)
        
        for (i,lp) in enumerate(faces):
            normals[lp]+=trinormals[i]

        div=np.sqrt(np.sum(normals**2,axis=1))     
        div=div.reshape(len(div),1)
        normals=(normals/div)
            
        norms=np.array(normals).ravel().tolist()
        
        self.vertex_list = batch.add_indexed(len(vertices),\
                                                 GL_TRIANGLES,\
                                                 group,\
                                                 inds,\
                                                 ('v3d/static',verx),\
                                                 ('n3d/static',norms),\
                                                 ('c3d/static',colors))

    def update(self):
        pass
    
    def delete(self):
        self.vertex_list.delete()

class ODF_Slice(object):

    def __init__(self,odfs,vertices,faces,noiso,batch,group=None):


        J=0

        self.odfs_no=J
        self.vertex_list=(odfs.shape[0]*odfs.shape[1])*[None]
        
        for index in np.ndindex(odfs.shape[:2]):

            values=odfs[index]
            if noiso:
                values=np.interp(values,[values.min(),values.max()],[0,.5])
                
            inds=faces.ravel().tolist()
            shift=index+(0,)

            print J,odfs.shape[0]*odfs.shape[1]            
            points=np.dot(np.diag(values),vertices)
            
            points=points+np.array(shift)            
            verx=points.ravel().tolist()

            normals=np.zeros((len(vertices),3))        
            ones_=np.ones(len(values))
            colors=np.vstack((values,ones_,ones_)).T
            colors=colors.ravel().tolist()
        
            p=vertices
            l=faces
            
            trinormals=np.cross(p[l[:,0]]-p[l[:,1]],\
                                p[l[:,1]]-p[l[:,2]],\
                                axisa=1,axisb=1)
        
            for (i,lp) in enumerate(faces):
                normals[lp]+=trinormals[i]
                div=np.sqrt(np.sum(normals**2,axis=1))     
                div=div.reshape(len(div),1)
                normals=(normals/div)
                norms=np.array(normals).ravel().tolist()
        
            self.vertex_list[i] = batch.add_indexed(len(vertices),\
                                                 GL_TRIANGLES,\
                                                 group,\
                                                 inds,\
                                                 ('v3d/static',verx),\
                                                 ('n3d/static',norms),\
                                                 ('c3d/static',colors))

            J+=1
            
    def update(self):
        pass
    
    def delete(self):
        for i in range(self.odfs_no):
            self.vertex_list.delete()

            
import dipy.core
import nibabel as ni
from dipy import load_dcm_dir
import dipy.core.generalized_q_sampling as gq

'''#############

mat_path='/home/eg309/Devel/dipy/dipy/core/matrices/evenly_distributed_sphere_362.npz'

eds=np.load(mat_path)
directions=eds['vertices']
faces=eds['faces']
values=np.random.rand(len(directions))

dname =  '/home/eg01/Data_Backup/Data/Frank_Eleftherios/frank/20100511_m030y_cbu100624/08_ep2d_advdiff_101dir_DSI'

data,affine,bvals,gradients=load_dcm_dir(dname)
print data.shape

'''

'''
gqs=gq.GeneralizedQSampling(data,bvals,gradients)
odf=gqs.odf(data[48,48,28])
odf=odf/odf.max()#gqs.normal_param

#print qa.shape, directions.shape, gradients.shape

points=np.dot(np.diag(odf),directions)
#print odf.shape,points.shape,faces.shape
#print odf.min(),odf.max(),points.min(),points.max(), faces.min(),faces.max()

csg=CommonSurfaceGroup()
#isg=IlluminatedSurfaceGroup()

#odf_surf=Surface(odf,points,faces,batch=batch,group=csg)
#actors.append(odf_surf)

odfs=np.zeros((data.shape[0],data.shape[1],len(directions)))

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        odfs[i,j]=gqs.odf(data[i,j,28])

print 'odfs_nbytes', odfs.nbytes
print odfs.shape

odfs=odfs/gqs.normal_param
odf_slice=ODF_Slice(odfs,directions,faces,noiso=True,batch=batch,group=csg)
actors.append(odf_slice)

'''


'''
signals=data[48,48,28]
slg=SmoothLineGroup()
actors.append(Dandelion(signals,gradients,batch=batch,group=slg))
'''

'''
anim=load_animation('effects/_LPE__Healing_Circle_by_LexusX2.png', 5, 10)
sprite=pyglet.sprite.Sprite(anim)
sprite.position = (-sprite.width/2, - sprite.height/2)
actors.append(sprite)
'''

#'''

import scipy.ndimage as nd
f1='/home/eg309/Data/regtest/fiac0/meanafunctional_01.nii'
img=ni.load(f1)

data =img.get_data()
affine=img.get_affine()


#sprite = pyglet.sprite.Sprite(img, x=0, y=0)
#sprite.position = (-sprite.width/2, - sprite.height/2)
#actors.append(sprite)

class ConnectedSlices():

    def __init__(self,affine,data):

        self.shape=data.shape
        self.data=data
        self.affine=affine
        #volume center coordinates
        self.vxi,self.vxj,self.vxk=self.shape[0]/2,self.shape[1]/2,self.shape[2]/2
        self.update_vox_coords(self.vxi,self.vxj,self.vxk)

    def update_vox_coords(self,vxi,vxj,vxk):

        self.vxi,self.vxj,self.vxk=vxi,vxj,vxk
        #current slices for the 3 axes
        self.sli=self.data[self.vxi,:,:]
        self.slj=self.data[:,self.vxj,:]
        self.slk=self.data[:,:,self.vxk]

        #interpolate for textures
        sli=np.interp(self.sli,[self.sli.min(),self.sli.max()],[0,255]).astype(np.uint8)        
        slj=np.interp(self.slj,[self.slj.min(),self.slj.max()],[0,255]).astype(np.uint8)        
        slk=np.interp(self.slk,[self.slk.min(),self.slk.max()],[0,255]).astype(np.uint8)        
        
        texi = ArrayInterfaceImage(sli).texture
        texj = ArrayInterfaceImage(slj).texture
        texk = ArrayInterfaceImage(slk).texture

        #how far in Z axis is texture projection plane in gl space
        self.z=-1
        #three points are needed to define the projection plane
        self.p0=(0,0,self.z)
        self.p1=(1,0,self.z)
        self.p2=(0,1,self.z)
                       
        spri=pyglet.sprite.Sprite(texi, x=0, y=0)                       
        spri.position=(-spri.width/2, - spri.height/2)
        
        sprj=pyglet.sprite.Sprite(texj, x=0, y=0)                       
        sprj.position=(-sprj.width/2, - sprj.height/2)

        sprk=pyglet.sprite.Sprite(texk, x=0, y=0)                       
        sprk.position=(-sprk.width/2, - sprk.height/2)    

        self.spri=spri
        self.sprj=sprj
        self.sprk=sprk

    def draw(self):
        #print('draw')

  
        glPushMatrix()
        glTranslatef(-self.spri.width/2-self.sprj.width/2,0,self.z)
        glScalef(1, 1., 0)
        self.spri.draw()
        glPopMatrix()         
 
        glPushMatrix()
        glTranslatef(0,0,self.z)
        glScalef(1, 1., 0)
        self.sprj.draw()
        glPopMatrix() 
    
        glPushMatrix()
        glTranslatef(self.sprj.width/2+self.sprk.width/2,0,self.z)
        #glTranslatef(0,0,self.z)
        glScalef(1, 1., 0)
        self.sprk.draw()
        glPopMatrix()        

    def process_pickray(self,near,far):
        #collision with plane
 
        success,t,p= cll.intersect_segment_plane(near,far,self.p0,self.p1,self.p2)

        print success
        print p

        o0_low_left=(-self.spri.width-self.sprj.width/2.,-self.spri.height/2)
        o0_up_right= (-self.sprj.width/2.,self.spri.height/2)       
        if tell_me_if(p,o0_low_left,o0_up_right):
            print 'Object 0'
            pix0=np.round(p[0]-o0_low_left[0]).astype(int)
            pix1=np.round(p[1]-o0_low_left[1]).astype(int)            
            self.update_vox_coords(self.vxi,pix1,pix0)            
            print 'Changed', self.vxi,pix0,pix1            
 
        o1_low_left=(-self.sprj.width/2.,-self.sprj.height/2)
        o1_up_right= (self.sprj.width/2.,self.sprj.height/2)               
        if tell_me_if(p,o1_low_left,o1_up_right):
            print 'Object 1'
            pix0=np.round(p[0]-o1_low_left[0]).astype(int)
            pix1=np.round(p[1]-o1_low_left[1]).astype(int)
            self.update_vox_coords(pix1,self.vxj,pix0)            
            

        o2_low_left=(self.sprj.width/2.,-self.sprk.height/2)
        o2_up_right= (self.sprj.width/2+self.sprk.width,self.spri.height/2)       
        if tell_me_if(p,o2_low_left,o2_up_right):
            print 'Object 2'
            pix0=np.round(p[0]-o2_low_left[0]).astype(int)
            pix1=np.round(p[1]-o2_low_left[1]).astype(int)
            self.update_vox_coords(pix1,pix0,self.vxk)
         
        print np.round(p)

        #self.update_vox_coords()
        
        
        

    def update(self):
        pass
    
def tell_me_if(p,low_left,up_right):
            if low_left[0]  <= p[0] and p[0]<=up_right[0]:
                if low_left[1]  <= p[1] and p[1]<=up_right[1]:
                    return True
            return False


cds =ConnectedSlices(affine,data)
actors.append(cds)


#'''

import nibabel.trackvis as tv

'''
T_, _ = tv.read('/home/eg01/Devel/dipy/dipy/core/bench/data/tracks300.trk.gz')
T=[t[0] for t in T_]
print len(T)

T=T[:4]
'''

#fname='/home/eg01/Data_Backup/Data/PBC/pbc2009icdm/brain1/brain1_scan1_fiber_track_mni.trk'
#fname='/home/eg309/Data/PBC/pbc2009icdm/brain1/brain1_scan1_fiber_track_mni.trk'
fname='/home/eg309/Data/PROC_MR10032/subj_04/101/1312211075232351192010092217591167666934589ep2dadvdiffDSI10125x25x25STs003a001_FA_warp.trk'

'''

print 'Loading file...'
streams,hdr=tv.read(fname)

print 'Copying tracks...'
T=[i[0] for i in streams]

del streams

T2=T[:20000]

import dipy.core.track_performance as pf

T=[pf.approximate_ei_trajectory(t) for t in T]

#slg=SmoothLineGroup()
#'''
ic=InteractiveCurves(T)
actors.append(ic)
#'''

ic=InteractiveCurves(T2)
actors.append(ic)
'''
Machine().run()



