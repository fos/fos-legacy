import numpy as np

from fos import Actor, World, Window
from fos.actor.tree import Tree

# sample data
vert = np.array( [ [0,0,0],
                   [50,50,0],
                   [50,100,0],
                   [100,50,0]], dtype = np.float32 )
                   
conn = np.array( [ 0, 1, 1, 2, 1, 3 ], dtype = np.uint32 ) 

# the colors are per line
#cols = np.array( [ [0, 255, 0, 255],
#                   [0, 255, 0, 255],
#                   [0, 0, 255, 255] ] , dtype = np.ubyte )

cols = np.array( [ [0, 1, 0, 1],
                   [0, 1, 0, 0],
                   [0, 0, 1, 1] ] , dtype = np.float32 )

wi = Window(width = 800, height = 500)
w = wi.get_world()

act = Tree(vertices = vert, connectivity = conn, colors = cols)
    
w.add(act)
