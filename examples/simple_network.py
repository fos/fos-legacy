import numpy as np

from fos import Window
from fos.actor.network import AttributeNetwork

#import fos.lib.pyglet
#fos.lib.pyglet.options['debug_gl'] = True

wi = Window()
w = wi.get_world()

# node positions
pos = np.array( [ [0,0,0], [10,10,10] ], dtype = np.float32)
siz = np.array( [ [1.0, 1.0 ]], dtype = np.float32 )
col = np.array( [ [255,0,0,255],
                  [0,255,0,255]], dtype = np.ubyte)
edg = np.array( [ [0,1]], dtype = np.uint32 )

aff = np.eye(4, dtype = np.float32)
aff[:3,3] = [0,0,0]

node_label = {0 : {label:'Node 1',
                   size:20,
                   font:'Times New Roman'},
              1 : {label:'Node 2'}
              }

cu = AttributeNetwork(affine = aff,
                      node_position = pos,
                      node_size = siz,
                      node_color = col,
                      edge_connectivity = edg)

w.add(cu)
cu.start()
#w.delete(cu)
