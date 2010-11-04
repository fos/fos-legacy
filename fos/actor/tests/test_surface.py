import numpy as np

ftriangles='/home/eg309/Data/surface/triangles.npy'
fvertices='/home/eg309/Data/surface/vertices.npy'
flowres ='/home/eg309/Data/surface/labellowres.npy'
fhighres='/home/eg309/Data/surface/labelhighres.npy'

vertices=np.load(fvertices).astype(np.float32)
faces=np.load(ftriangles).astype(np.uint32)
highres=np.load(fhighres).astype(np.float32)
highres=np.interp(highres,[highres.min(),highres.max()],[.3,1.]).astype(np.float32)

highres.shape+=(1,)

colors=np.ones((len(vertices),4))
colors[:,0]=highres.T

colors=colors.astype(np.float32)

print colors.shape, colors.min(),colors.max(),colors.mean()

#exit(0)

#eds=np.load('/home/eg309/Devel/dipy/dipy/core/matrices/evenly_distributed_sphere_362.npz')
#vertices=eds['vertices']
#faces=eds['faces']

vertices=vertices.astype(np.float32)
faces=faces.astype(np.uint32)        

len(vertices)
print 'vertices.shape', vertices.shape, vertices.dtype
print 'faces.shape', faces.shape,faces.dtype

'''
vertices=np.array([[0,   100,-1],
                   [-100,0,-1],
                   [100, 0,-1],
                   [100, 100,-1],
                   [0,   0,-1],
                   [200, 0,-1]],dtype=np.float32)

faces=np.array([[0,1,2],[3,4,5]],dtype=np.uint32)
'''

def auto_normals(vertices,faces):
    
    normals=np.zeros((len(vertices),3))
    trinormals=np.cross(vertices[faces[:,0]]-vertices[faces[:,1]],\
                                vertices[faces[:,1]]-vertices[faces[:,2]],\
                                axisa=1,axisb=1)
    for (i,face) in enumerate(faces):
        normals[face]+=trinormals[i]            
        
    div=np.sqrt(np.sum(normals**2,axis=1))     
    div=div.reshape(len(div),1)
    normals=(normals/div)
            
    return normals.astype(np.float32)
    
normals=auto_normals(vertices,faces)
print 'normals.shape',normals.shape

'''
normals=np.array([ [0,   0, 1],
                   [0,   0, 1],
                   [0,   0, 1],
                   [0,   0, 1],
                   [0,   0, 1],
                   [0,   0, 1]],dtype=np.float32)


colors=np.array([  [0,   0, 1., 1],
                   [0,   0, 1., 1],
                   [0,   0, 1., 1],
                   [0,   0, 1., 1],
                   [0,   0, 1., 1],
                   [0,   0, 1., 1]],dtype=np.float32)
'''

#colors=np.repeat(np.array([[1.,0.,0.,1.]]),len(vertices),axis=0).astype(np.float32)
print 'colors.shape',colors.shape

#vertices=vertices*10

#print vertices
#print faces
#print colors
#print normals


print vertices.min(),vertices.max(),vertices.mean()
print normals.min(),normals.max(), normals.mean()

print vertices.dtype,faces.dtype, colors.dtype, normals.dtype

from fos.actor.surf import Surface

s=Surface(vertices,faces,normals,colors)

from fos.core.world import World
w=World(0)
w.add(s)

from fos.core.camera import DefaultCamera
cam=DefaultCamera()
w.add(cam)

from fos.core.fos_window import FosWindow
wi=FosWindow()
wi.attach(w)


