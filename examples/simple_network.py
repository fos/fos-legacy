import numpy as np

from fos.core.world import World
from fos.core.fos_window import FosWindow
from fos.actor.network import AttributeNetwork

w = World("myworld")    

# node positions
pos = np.array( [ [0,0,0], [10,10,10] ], dtype = np.float32)
siz = np.array( [ [1.0, 1.0 ]], dtype = np.float32 )
col = np.array( [ [255,0,0,255],
                  [0,255,0,255]], dtype = np.ubyte)

cu = AttributeNetwork(node_position = pos,
                      node_size = siz,
                      node_color = col)
w.add(cu)
#w.delete(cu)

wi = FosWindow()
wi.attach(w)