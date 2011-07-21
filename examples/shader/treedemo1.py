#!/usr/bin/env python

import numpy as np

import fos.lib.pyglet as pyglet
from fos.lib.pyglet.gl import *

from fos import World, Window, WindowManager
from fos.actor.treeregion import TreeRegion

from fos.actor.tree import Tree
from fos import Window
from fos.actor.axes import Axes

mycpt = "TreeRegion Demo - Fos.me"
try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,depth_size=16, double_buffer=True,)
    window = Window(resizable=True, config=config, vsync=False, width=1000, height=800, caption = mycpt) # "vsync=False" to check the framerate
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = Window(resizable=True, caption = "No Multisampling")

# sample tree data
# ####
vert = np.array( [ [0,0,0],
                   [5,10,0]], dtype = np.float32 )

conn = np.array( [ 0, 1], dtype = np.uint32 )

cols = np.array( [ [0, 1, 0, 1.0] ] , dtype = np.float32 )

vert_width = np.array( [1, 5], dtype = np.float32 )

#ax = Axes(scale=100)
act = TreeRegion(vertices = vert, connectivity = conn, radius = vert_width) #colors = cols,

w = World()
#w.add(ax)
w.add(act)

window.attach(w)

wm = WindowManager()
wm.add(window)
wm.run()
