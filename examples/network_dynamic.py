import numpy as np

from fos import Window, WindowManager, World
from fos.actor.network import AttributeNetwork,DynamicNetwork

# time steps
ts = 20000

# node positions
s = 100
pos = np.zeros( (s,3,ts)).astype(np.float32)
pos[:,:,0] = np.random.random( (s,3)).astype(np.float32) * 200 - 100
for i in xrange(1,ts):
    pos[:,:,i] = pos[:,:,i-1] + np.random.random( (s,3)).astype(np.float32) * 4 - 2
col = np.random.random_integers( 0, 255-1, (s,4,ts) ).astype(np.ubyte)
#col[:, 3, :] = 255
size = np.random.random( (s ,ts) ).astype(np.float32)
ss = 500
edg = np.random.random_integers(0, s-1, (ss, 2,ts)).astype(np.uint32)
edg_weight = np.random.random( (ss,1,ts)).astype(np.float32)
edg_col = np.random.random_integers( 0, 255-1, (ss,4,ts) ).astype(np.ubyte)
aff = np.eye(4, dtype = np.float32)

aff[:3,3] = [0,0,0]
nlabs = {0 : { 'label'  : 'Node 1',
               'size'   : 20,
               'font'   : 'Times New Roman',
               'color'  : ( 255, 0, 0, 255 ) },
              1 : { 'label' : 'Node 2'}
              }

class DynNet(DynamicNetwork):
    def update(self, dt):
        super(DynNet,self).update(dt)

dn = DynNet(affine = aff,
                      node_position = pos,
                      node_size = size,
                      node_color = col,
                      node_label = nlabs,
                      edge_connectivity = edg,
                      edge_color = edg_col,
                      global_edge_width = 3.5
                      )
w = World()
w.add(dn)

wi = Window(caption = "Dynamic Network with Fos")
wi.attach(w)
dn.start()
wm = WindowManager()
wm.add(wi)
wm.run()
