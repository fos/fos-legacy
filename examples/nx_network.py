import networkx as nx
import numpy as np

n = 100

g=nx.gnp_random_graph(n,0.3)
edges = np.array(g.edges())

ret = nx.spring_layout(g, 3)

e=np.zeros( (n,3))

for i in range(n):
    e[i,:] = ret[i]

from fos import Window
from fos.actor.network import AttributeNetwork

wi = Window()
w = wi.get_world()

cu = AttributeNetwork(node_position=e*100,
                      scale_factor = 1.,
                      #global_node_size = 0.01,
                      edge_connectivity = edges
                      )

w.add(cu)