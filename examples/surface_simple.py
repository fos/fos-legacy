import numpy as np
from fos.comp_geom.gen_normals import auto_normals 
from fos.data import get_sphere
from fos.actor.surf import Surface
from fos import Window, WindowManager, World, DefaultCamera

#import os.path as op
#pa = '/home/stephan/Downloads/Gifti/'

"""
pa = op.join(op.dirname(__file__))
ftriangles=op.join(pa,'triangles.npy')
fvertices=op.join(pa,'vertices.npy')
fhighres=op.join(pa,'labels.npy')

vertices=np.load(fvertices).astype(np.float32)
faces=np.load(ftriangles).astype(np.uint32)
highres=np.load(fhighres).astype(np.float32)
highres=np.interp(highres,[highres.min(),highres.max()],[.3,1.]).astype(np.float32)

highres.shape+=(1,)

colors=np.ones((len(vertices),4))
colors[:,0]=highres.T

colors=colors.astype(np.float32)

print colors.shape, colors.min(),colors.max(),colors.mean()
"""


eds=np.load(get_sphere())
vertices=eds['vertices']
faces=eds['faces']

vertices=100*vertices.astype(np.float32)
faces=faces.astype(np.uint32)        

print 'vertices.shape', vertices.shape, vertices.dtype
print 'faces.shape', faces.shape,faces.dtype

colors=np.random.rand(len(vertices),4)
colors=colors.astype('f4')
   
normals=auto_normals(vertices,faces)
print('normals.shape %d %d' % normals.shape)

print('colors.shape %d %d' % colors.shape)
print(vertices.dtype,faces.dtype, colors.dtype, normals.dtype)

aff = np.eye(4, dtype = np.float32)
aff[:3,3] = [150,0,0]

s=Surface(vertices,faces,colors, affine = aff, add_lights = True, normals = normals)

w=World()
w.add(s)

cam=DefaultCamera()
w.add(cam)
 
wi=Window()
wi.attach(w)

wm = WindowManager()
wm.add(wi)
wm.run()


