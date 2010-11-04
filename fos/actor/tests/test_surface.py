import numpy as np
from fos.comp_geom.gen_normals import auto_normals


from fos.data import get_sphere

eds=np.load(get_sphere('symmetric362'))
vertices=eds['vertices']
faces=eds['faces']


vertices=vertices.astype(np.float32)
faces=faces.astype(np.uint32)        
colors=np.ones((len(vertices),4))

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

vertices2=vertices+np.array([10,0,0],dtype=vertices.dtype)
s2=Surface(vertices2,faces,normals,colors)

from fos.core.world import World
w=World()
w.add(s)
w.add(s2)

from fos.core.camera import DefaultCamera
cam=DefaultCamera()
w.add(cam)

from fos import Window 
wi=Window()
wi.attach(w)


