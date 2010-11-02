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
s = 1000
pos = np.array( [[0,0,0],
                 [10,10,10]], dtype = np.float32)
pos = np.random.random( (s,3)).astype(np.float32) * 100

col = np.array( [[10,10,10,255],
                 [100,0,0,255]], dtype = np.ubyte)

size = np.array( [1.0, 10.0], dtype = np.float32 )
size = np.random.random( (s,1) ).astype(np.float32)

shape = ['cube', 'sphere']
label = ['node1', 'node2']

edg = np.array( [ [0,1]], dtype = np.uint8 )
edg_weight = np.array( [1.5], dtype = np.float32 )

cu = AttributeNetwork(node_position = pos,
                      node_size = size)
w.add(cu)

wi = FosWindow()
wi.attach(w)
#
#for i in xrange(1000):
#    cu.node_position += np.random.random( (cu.node_position.shape) ) * 2
    