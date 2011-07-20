#!/usr/bin/env python

import numpy as np

from fos import World, Window, WindowManager
from fos.actor.axes import Axes

window = Window(resizable=True, vsync=False, width=500, height=500, caption = "Axes")

ax = Axes(scale=100)

w = World()
w.add(ax)
window.attach(w)
wm = WindowManager()
wm.add(window)
wm.run()
