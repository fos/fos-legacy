import numpy as np
import h5py

import fos
from fos import SimpleWindow as Window
from fos.lib.pyglet.gl import *
from fos.actor.treeregion import TreeRegion
from numpy.random import randn

f = h5py.File('../neurons/neurons2.hdf5', 'r')

pos = f['neurons/position'].value
parents = f['neurons/localtopology'].value
labeling = f['neurons/labeling'].value
colors = f['neurons/segmentcolors'].value
f.close()

print pos
print parents
print labeling
print colors

mycpt = "Treedemo - Fos.me"
try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,depth_size=16, double_buffer=True,)
    window = Window(resizable=True, config=config, vsync=False, width=1000, height=800, caption = mycpt) # "vsync=False" to check the framerate
except fos.lib.pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    print "fallback"
    window = Window(resizable=True, caption = mycpt)

ac=[]
# spread factor
s=500
# duplicator
d = 30

# tune it up
# this is very inefficient, because it copies the position arrays
bigpos = np.zeros( (d*len(pos), 3), dtype = np.float32 )
bigpar = np.zeros( (d*len(parents)), dtype = np.float32 )

print bigpar.shape

off = 0
offpar = 0
poslen = len(pos)
parlen = len(parents)

for i in range(d):
    pos2 = pos.copy()
    # spread in xy plane
    pos2[:,0] = pos2[:,0] + (randn()-0.5)*s
    pos2[:,1] = pos2[:,1] + (randn()-0.5)*s


    
    bigpos[off:off+poslen,:] = pos2.copy()
    bigpar[offpar:offpar+parlen] = parents + off

    print "offset", off
    print bigpos
    print "bigpar,", bigpar[offpar:offpar+parlen]
    
    off += poslen
    offpar += parlen
    # create an globaltopology array


treeregion = TreeRegion(vertices = pos2, connectivity = parents )
window.add_actor_to_world(treeregion)

fos.run()