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

#a=np.random.random( (100, 100, 100) )
#aff = np.eye(4)
#cds = ConnectedSlices(aff,a)
#w.add(cds)
#    
#
#tri = Triangle()
#w.add(tri)

# node positions
s = 100
pos = np.random.random( (s,3)).astype(np.float32) * 10
col = np.random.random_integers( 0, 255, (s,4) ).astype(np.ubyte)
col[:, 3] = 255

size = np.array( [1.0, 10.0], dtype = np.float32 )
size = np.random.random( (s,1) ).astype(np.float32)

shape = ['cube', 'sphere']
label = ['node1', 'node2']

ss = 20
edg = np.array( [ [0,1]], dtype = np.uint8 )
edg_weight = np.array( [1.5], dtype = np.float32 )
edg_col = np.array( [ [255, 0, 0, 255]], dtype = np.ubyte )

edg = np.random.random_integers(0, s-1, (ss, 2)).astype(np.uint32)
edg_weight = np.random.random( (ss,1)).astype(np.float32)
edg_col = np.random.random_integers( 0, 255, (ss,4) ).astype(np.ubyte)
edg_col[:, 3] = 255

cu = AttributeNetwork(node_position = pos,
                      node_size = size,
                      node_color = col,
                      edge_connectivity = edg,
                      edge_weight = edg_weight,
                      edge_color = edg_col)
w.add(cu)

wi = FosWindow()
wi.attach(w)
#
#for i in xrange(1000):
#    cu.node_position += np.random.random( (cu.node_position.shape) ) * 2
    