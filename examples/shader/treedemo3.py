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

print "orig pos", pos
print "orig par", parents
#print labeling
#print colors

mycpt = "Treedemo - Fos.me"
try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,depth_size=16, double_buffer=True,)
    window = Window(resizable=True, config=config, vsync=False, width=1000, height=800, caption = mycpt ) # "vsync=False" to check the framerate
except fos.lib.pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    print "fallback"
    window = Window(resizable=True, caption = mycpt)

ac=[]
# spread factor
s=500
# duplicator
d = 2200

# tune it up
# this is very inefficient, because it copies the position arrays
bigpos = np.zeros( (d*len(pos), 3), dtype = np.float32 )
bigpar = np.zeros( (d*len(parents)), dtype = np.int32 )

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

    bigpos[off:off+poslen,:] = pos2
    bigpar[offpar:offpar+parlen] = parents + off

    print "offset: pos/par", off, offpar
    print "from to", off, off+poslen
    print "from to", offpar, offpar + parlen
    print "parents array", (parents+off)[:10]
    
    off += poslen
    offpar += parlen

print "len bipar", len(bigpar), bigpar
rad = np.ones( len(bigpar), dtype = np.float32 )
print "bigpos", bigpos

treeregion = TreeRegion(vertices = bigpos, connectivity = bigpar.astype(np.int32) ) #, radius = rad )
window.add_actor_to_world(treeregion)
#
fos.run()