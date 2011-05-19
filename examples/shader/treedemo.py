#!/usr/bin/env python


import numpy as np

import fos.lib.pyglet as pyglet
from fos.lib.pyglet.gl import *
from fos.lib.pyglet.window import key

from fos.actor.tree import Tree
from fos import SimpleWindow
from fos.actor.axes import Axes

mycpt = "Treedemo - Fos.me"
try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,depth_size=16, double_buffer=True,)
    window = SimpleWindow(resizable=True, config=config, vsync=False, width=1000, height=800, caption = mycpt) # "vsync=False" to check the framerate
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = SimpleWindow(resizable=True, caption = mycpt)


# sample tree data
# ####
vert = np.array( [ [0,0,0],
                   [5,5,0],
                   [5,10,0],
                   [10,5,0]], dtype = np.float32 )

conn = np.array( [ 0, 1, 1, 2, 1, 3 ], dtype = np.uint32 )

cols = np.array( [ [0, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 1, 0.5] ] , dtype = np.float32 )

vert_width = np.array( [1, 5, 5, 1, 5, 1], dtype = np.float32 )

ax = Axes()
window.add_actor_to_world(ax)

act = Tree(vertices = vert, connectivity = conn, colors = cols, vertices_width = vert_width)
window.add_actor_to_world(act)

fos.run()
