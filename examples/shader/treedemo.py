import numpy as np

from fos import Actor, World, Window
from fos.actor.tree import Tree

# sample data
vert = np.array( [ [0,0,0],
                   [50,50,0],
                   [50,100,0],
                   [100,50,0]], dtype = np.float32 )
                   
conn = np.array( [ 0, 1, 1, 2, 1, 3 ], dtype = np.uint32 )

cols = np.array( [ [ 255, 0, 0, 255],
                   [ 0, 255, 0, 255],
                   [255, 255, 0, 255],
                   [0, 0, 255, 255] ] , dtype = np.ubyte )


wi = Window()
w = wi.get_world()

act = Tree(vertices = vert,
                   connectivity = conn,
                   colors = cols)
    
w.add(act)
