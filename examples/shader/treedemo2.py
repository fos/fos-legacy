import numpy as np
import h5py

from fos import Actor, World, Window
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

wi = Window(width = 1400, height = 900)
w = wi.get_world()

ac=[]
s=800
# tune it up
# this is very inefficient, because it copies the position arrays
for i in range(100):
    pos2 = pos.copy()
    pos2[:,0] = pos2[:,0] + (randn()-0.5)*s
    pos2[:,1] = pos2[:,1] + (randn()-0.5)*s

    ac.append( Tree(vertices = pos2,
                       connectivity = parents,
                       colors = colors)
    )

for e in ac:
    w.add(e)
