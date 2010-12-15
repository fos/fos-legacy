import numpy as np
from fos.comp_geom.gen_normals import auto_normals 

#pa = '/home/stephan/Downloads/Gifti/'
pa = '/home/eg309/Data/surface/'
ftriangles=pa+'triangles.npy'
fvertices=pa+'vertices.npy'
flowres =pa+'labellowres.npy'
fhighres=pa+'labelhighres.npy'

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
    
normals=auto_normals(vertices,faces)
print 'normals.shape',normals.shape
print 'colors.shape',colors.shape

print vertices.min(),vertices.max(),vertices.mean()
print normals.min(),normals.max(), normals.mean()

print vertices.dtype,faces.dtype, colors.dtype, normals.dtype

from fos.actor.surf import Surface
aff = np.eye(4, dtype = np.float32)
aff[:3,3] = [150,0,0]

s=Surface(vertices,faces,colors, affine = aff, add_lights = True, normals = normals)

#vertices2=vertices+np.array([100,0,0],dtype=vertices.dtype)
#s2=Surface(vertices2,faces,normals,colors)

from fos.core.world import World
w=World()
w.add(s)
#w.add(s2)

from fos.core.camera import DefaultCamera
cam=DefaultCamera()
w.add(cam)

from fos import Window, WindowManager 
wi=Window()
wi.attach(w)

wm = WindowManager()
wm.add(wi)
wm.run()


