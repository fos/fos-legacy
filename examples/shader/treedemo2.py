import numpy as np
import h5py

from fos import Actor, World, Window
from fos.actor.tree import Tree

f = h5py.File('../neurons/neurons.hdf5', 'r')
pos = f['neurons/positions'].value
parents = f['neurons/parents'].value
print "parents", parents
colors = f['neurons/colors'].value
f.close()

wi = Window(width = 800, height = 500)
w = wi.get_world()

#act = Tree(vertices = vert,
#                   connectivity = conn,
#                   colors = cols)
act = Tree(vertices = pos,
                   connectivity = parents,
                   colors = colors)

w.add(act)
