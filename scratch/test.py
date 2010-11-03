import numpy as np

from fos.core.world import World
from fos.core.fos_window import FosWindow
from fos.core.camera import DefaultCamera
from fos.actor.volslicer import ConnectedSlices
from fos.actor.triangle import Triangle

w = World(0)    
cam = DefaultCamera()
w.add(cam)

#a=np.random.random( (100, 100, 100) )
#aff = np.eye(4)
#cds = ConnectedSlices(aff,a)
#w.add(cds)

tri = Triangle()
w.add(tri)

wi = FosWindow()
wi.attach(w)
