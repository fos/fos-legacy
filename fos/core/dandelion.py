import numpy as np
from fos.core.machine import Machine, batch, mouse_x,mouse_y,actors
from pyglet.gl import *
import os

class Dandelion(object):
    def __init__(self,points,faces,batch,group=None):
        pass
    def update(self):
        pass
    def delete(self):
        pass

#class 

    
class Surface(object):

    def __init__(self, values,vertices,faces,batch,group=None):
            
        inds=faces.ravel().tolist()
        verx=vertices.ravel().tolist()

        normals=np.zeros((len(vertices),3))
        #colors=np.ones((len(values),3)#.ravel().tolist()
        #colors=np.dot(np.diag(values),vertices)
        #colors=np.vstack((values,np.ones(len(values)),np.ones(len(values))))

        colors=np.random.rand(len(vertices),3)
        colors=colors.ravel().tolist()
        
        p=vertices
        l=faces
            
        trinormals=np.cross(p[l[:,0]]-p[l[:,1]],p[l[:,1]]-p[l[:,2]],axisa=1,axisb=1)
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

           


import dipy.core
import nibabel as ni
from dipy.io import dicomreaders as dcm
import dipy.core.generalized_q_sampling as gq

#'''
mat_path='/home/eg309/Devel/dipy/dipy/core/matrices/evenly_distributed_sphere_362.npz'

eds=np.load(mat_path)

directions=eds['vertices']
faces=eds['faces']
values=np.random.rand(len(directions))
points=np.dot(np.diag(values),directions)
#'''

'''

bvals=np.load('/home/eg309/Devel/dipy/dipy/core/tests/data/small_64D.bvals.npy')
gradients=np.load('/home/eg309/Devel/dipy/dipy/core/tests/data/small_64D.gradients.npy')

img = ni.load('/home/eg309/Devel/dipy/dipy/core/tests/data/small_64D.nii')
data=img.get_data()

print data.shape

values=data[5,5,5]
'''

dname =  '/home/eg309/Data/Frank_Eleftherios/frank/20100511_m030y_cbu100624/08_ep2d_advdiff_101dir_DSI'

data,affine,bvals,gradients=dcm.read_mosaic_dir(dname)

'''
gqs=gq.GeneralizedQSampling(data,bvals,gradients)

QA=gqs.QA
qa=QA[50,50,40]
'''
qa=gradients[:,0]

odf_surf=Surface(qa,directions,faces,batch=batch)

actors.append(odf_surf)
Machine().run()



