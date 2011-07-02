import numpy as np

from fos import World, Window, WindowManager
from fos.actor.polygonlines import PolygonLines

# sample polygon line data

vert = np.array( [ [0,0,0],
                   [5,5,0],
                   [5,10,0],
                   [10,5,0]], dtype = np.float32 )

conn = np.array( [ 0, 1, 1, 2, 1, 3 ], dtype = np.uint32 )

cols = np.array( [ [0, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 1, 0.5],
                   [1.0, 0.4, 1, 0.5]] , dtype = np.float32 )

act = PolygonLines(vertices = vert, connectivity = conn, colors = cols)
act.show_aabb = True

w = World()
w.add(act)

window = Window()
window.attach(w)

wm = WindowManager()
wm.add(window)
wm.run()