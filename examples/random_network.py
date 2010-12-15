import numpy as np

from fos import World, Window, WindowManager

from fos.actor.network import AttributeNetwork

w = World("myworld")    

# node positions
s = 1000
pos = np.random.random( (s,3)).astype(np.float32) * 100
col = np.random.random_integers( 0, 255, (s,4) ).astype(np.ubyte)
col[:, 3] = 255

size = np.array( [1.0, 10.0], dtype = np.float32 )
size = np.random.random( (s,1) ).astype(np.float32)

ss = 500
edg = np.array( [ [0,1]], dtype = np.uint8 )
edg_weight = np.array( [1.5], dtype = np.float32 )
edg_col = np.array( [ [255, 0, 0, 255]], dtype = np.ubyte )

edg = np.random.random_integers(0, s-1, (ss, 2)).astype(np.uint32)
edg_weight = np.random.random( (ss,1)).astype(np.float32)

edg_col = np.random.random_integers( 0, 255-1, (ss,4) ).astype(np.ubyte)
#edg_col[:, 3] = np.random.random_integers(0,1, (ss,)).astype(np.ubyte).ravel()

aff = np.eye(4, dtype = np.float32)
aff[:3,3] = [0,0,0]

cu = AttributeNetwork(affine = aff,
                      force_centering = True,
                      node_position = pos,
                      node_size = size,
                      node_color = col,
                      edge_connectivity = edg,
                      edge_weight = edg_weight,
                      edge_color = edg_col,
                      global_edge_width = 3.5
                      )
w.add(cu)
#w.delete(cu)

wi = Window()
wi.attach(w)

cu.start()

wm = WindowManager()
wm.add(wi)
wm.run()