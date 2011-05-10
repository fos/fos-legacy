import numpy as np
import h5py

from fos import Actor, World, Window
from fos.actor.tree import Tree

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


wi = Window(width = 800, height = 500)
w = wi.get_world()

act = Tree(vertices = pos,
                   connectivity = parents,
                   colors = colors)

w.add(act)
