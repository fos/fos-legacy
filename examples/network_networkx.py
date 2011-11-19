import networkx as nx
import numpy as np

from fos import Window, WindowManager, World
from fos.actor.network import AttributeNetwork

n = 100
g=nx.gnp_random_graph(n,0.3)
edges = np.array(g.edges())
ret = nx.spring_layout(g, 3)
e=np.zeros( (n,3))

for i in range(n):
    e[i,:] = ret[i]

wi = Window()
w = World()

cu = AttributeNetwork(node_position=e,
                      scale_factor = 1.,
                      edge_connectivity = edges
                      )

w.add(cu)
wi.attach(w)
wm = WindowManager()
wm.add(wi)
wm.run()
