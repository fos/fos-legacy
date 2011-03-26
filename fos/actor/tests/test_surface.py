import numpy as np
from fos.comp_geom.gen_normals import auto_normals


from fos.data import get_sphere

eds=np.load(get_sphere('symmetric362'))# problem with 642 
vertices=eds['vertices']
faces=eds['faces']

vertices=50*vertices.astype('f4')
faces=faces.astype(np.uint32)
colors=np.ones((len(vertices),4)).astype('f4')
#colors[0]=np.array([1.,0.,0.,1.]).astype('f4')
colors[:,:3]=np.random.rand(len(vertices),3).astype('f4')

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
#aff[0,3] = 30

s=Surface(vertices,faces,colors,normals=normals,affine = None,force_centering=True,add_lights=False)

#vertices2=vertices+np.array([10,0,0],dtype=vertices.dtype)
#s2=Surface(vertices2,faces,colors, affine = aff, normals=normals)

w=World()
w.add(s)
#w.add(s2)

cam=DefaultCamera()
w.add(cam)

wi=Window(bgcolor=(1.,0.,1.,1.),width=1000,height=1000)
wi.attach(w)


