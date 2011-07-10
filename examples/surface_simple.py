import numpy as np
from fos.comp_geom.gen_normals import auto_normals 
from fos.data import get_sphere
from fos.actor.surf import Surface
from fos import Window, WindowManager, World, DefaultCamera
from fos.core.color import red,green,blue,white,black
from fos.core.material import Material
from fos.core.light import Light

eds=np.load(get_sphere())
vertices=eds['vertices']
faces=eds['faces']

vertices=100*vertices.astype(np.float32)
faces=faces.astype(np.uint32)        

print('vertices.shape %s' % vertices.dtype)
print('faces.shape %s' % faces.dtype)

colors=np.random.rand(len(vertices),4)
colors=colors.astype('f4')
colors[:,3]=1
   
normals=auto_normals(vertices,faces)
print('normals.shape %d %d' % normals.shape)
print('colors.shape %d %d' % colors.shape)
print(vertices.dtype,faces.dtype, colors.dtype, normals.dtype)

aff = np.eye(4,dtype='f4')
aff[:3,3] = [0,0,0]

s=Surface(vertices,faces,colors,normals=None, material=None, light=None, affine=aff)

aff2=aff.copy()
aff2[:3,3]=[250,0,0]

l2=Light(position=np.array((1, 0, .5, 0),'f4'),ambient=(.0,.5,.5,1.),diffuse=(.5,.5,.5,1),specular=(.5,.5,.5,1))
m2=Material(diffuse=red,emissive=None,specular=(.9,.9,.9,1.),shininess=100,color=False)
s2=Surface(vertices,faces,colors,normals, material = m2, light = l2, affine=aff2)

aff3=aff.copy()
aff3[:3,3]=[500,0,0]

l3=Light(position=np.array((1, 0, .5, 0),'f4'),ambient=(.0,.5,.5,1.),diffuse=(.5,.5,.5,1),specular=(.5,.5,.5,1))
m3=Material(diffuse=blue,emissive=(.4,.4,.4,1.),specular=(.9,.9,.9,1.),shininess=100,color=False)
s3=Surface(vertices,faces,colors,normals, material = m3, light = l3, affine=aff3)

w=World()
w.add(s)
w.add(s2)
w.add(s3)

cam=DefaultCamera()
w.add(cam)
 
wi=Window()
wi.attach(w)

wm = WindowManager()
wm.add(wi)
wm.run()

"""
import os.path as op
pa = '/home/stephan/Downloads/Gifti/'

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

