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

    
normals=auto_normals(vertices,faces)



print vertices.min(),vertices.max(),vertices.mean()
print normals.min(),normals.max(), normals.mean()

print vertices.dtype,faces.dtype, colors.dtype, normals.dtype

from fos.actor.surf import Surface
from fos import Window, World, DefaultCamera

aff = np.eye(4, dtype = np.float32)
aff[0,3] = 30

s=Surface(vertices,faces,colors,normals=normals, affine = aff,)

vertices2=vertices+np.array([10,0,0],dtype=vertices.dtype)
s2=Surface(vertices2,faces,colors, affine = aff, normals=normals)

w=World()
w.add(s)
w.add(s2)

cam=DefaultCamera()
w.add(cam)

wi=Window()
wi.attach(w)


