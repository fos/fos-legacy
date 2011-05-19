import numpy as np
import h5py

import fos
from fos import SimpleWindow as Window
from fos.lib.pyglet.gl import *
from fos.actor.tree import Tree
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
s=500
# tune it up
# this is very inefficient, because it copies the position arrays
for i in range(1000):
    pos2 = pos.copy()
    pos2[:,0] = pos2[:,0] + (randn()-0.5)*s
    pos2[:,1] = pos2[:,1] + (randn()-0.5)*s
    # random width array
    #wid = np.random.randn(1, 5, (len(pos2),) )
    wid = np.random.rand( len(pos2) ) * 2
    ac.append( Tree(vertices = pos2,
                       connectivity = parents,
                       colors = colors,
                       vertices_width = wid)
    )

for e in ac:
    window.add_actor_to_world(e)

fos.run()