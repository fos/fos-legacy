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


import numpy as np
from fos.core.machine import Machine, batch, mouse_x,mouse_y,actors
import pyglet
from pyglet.gl import *
from pyglet.image import Animation, AnimationFrame
import os

ang=0

class SmoothLineGroup(pyglet.graphics.Group):

     def set_state(self):
         #glClearColor(1,0.1,0.9,1)
         glEnable(GL_DEPTH_TEST)
         glEnable(GL_BLEND)
         glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

         glEnable(GL_LINE_SMOOTH)
         #glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
         glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
         glLineWidth(3.)
         
     def unset_state(self):
         glDisable(GL_DEPTH_TEST)
         glDisable(GL_BLEND)
         glDisable(GL_LINE_SMOOTH)
         glLineWidth(1.)


class InteractiveCurves(object):

    def __init__(self,curves,colors,batch,group=None):

        self.vertex_list=lno*[None]

        for curve in curves:            
            curve=curve.astype('f')            
            vertices=lines.ravel().tolist()
            self.vertex_list[i] = batch.add(len(curve),GL_LINE_STRIP,group,\
                                         ('v3f/static',vertices))
            
    def update(self):
        pass

    def delete(self):
        pass

def load_animation(image_name,columns,rows):
 
    effect_seq = pyglet.image.ImageGrid(pyglet.image.load(image_name), rows, columns)
    
    effect_frames = []
    for row in range(rows, 0, -1):
        end = row * columns
        start = end - (columns -1) -1
        for effect_frame in effect_seq[start:end:1]:
            effect_frames.append(AnimationFrame(effect_frame, 0.1))
    
    effect_frames[(rows * columns) -1].duration = None
        
    return Animation(effect_frames)
    
         

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
        def vec(*args):
            return (GLfloat * len(args))(*args)
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

    def __init__(self,odfs,vertices,faces,batch,group=None):


        J=0

        self.odfs_no=J
        self.vertex_list=(odfs.shape[0]*odfs.shape[1])*[None]
        
        for index in np.ndindex(odfs.shape[:2]):

            values=odfs[index]        
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

        

#'''
            
import dipy.core
import nibabel as ni
from dipy.io import dicomreaders as dcm
import dipy.core.generalized_q_sampling as gq


mat_path='/home/eg01/Devel/dipy/dipy/core/matrices/evenly_distributed_sphere_362.npz'

eds=np.load(mat_path)
directions=eds['vertices']
faces=eds['faces']
values=np.random.rand(len(directions))

dname =  '/home/eg01/Data_Backup/Data/Frank_Eleftherios/frank/20100511_m030y_cbu100624/08_ep2d_advdiff_101dir_DSI'

data,affine,bvals,gradients=dcm.read_mosaic_dir(dname)
print data.shape


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

odf_slice=ODF_Slice(odfs,directions,faces,batch=batch,group=csg)

actors.append(odf_slice)

'''


#'''
signals=data[48,48,28]
slg=SmoothLineGroup()
actors.append(Dandelion(signals,gradients,batch=batch,group=slg))

anim=load_animation('effects/_LPE__Healing_Circle_by_LexusX2.png', 5, 10)
#'''
sprite=pyglet.sprite.Sprite(anim)
sprite.position = (-sprite.width/2, - sprite.height/2)

actors.append(sprite)

Machine().run()
#'''

