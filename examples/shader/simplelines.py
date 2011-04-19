import numpy as np

from fos import World, Window
from fos.actor.curve import InteractiveCurves



w=World()
w.add(cu)

wi = Window(caption="Simple Lines")
wi.attach(w)
