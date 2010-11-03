import numpy as np

from fos.core.world import World
from fos.core.fos_window import FosWindow
from fos.core.camera import DefaultCamera
from fos.actor.volslicer import ConnectedSlices
from fos.actor.triangle import Triangle
from fos.actor.network import AttributeNetwork

w = World(0)    
cam = DefaultCamera()
w.add(cam)

tri = Triangle()
w.add(tri)

wi = FosWindow()
wi.attach(w)

    
