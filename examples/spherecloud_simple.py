import numpy as np

from fos import Window
from fos.actor.spherecloud import SphereCloud

# the positions for the sphere
positions = np.array( [[0,0,0],
                       [1,1,1],
                       [10,10,10]], dtype = np.float32 )

# the radii for the spheres
radii = np.array( [1.0, 0.5, 5.0], dtype = np.float32 )

# the color for the spheres
colors = np.array( [[1, 1, 1, 1],
                    [0, 1, 0, 1],
                    [0, 0, 1, 1]]).astype(np.float32)

sc = SphereCloud( positions = positions, radii=radii, colors=colors )

wi = Window()
w = wi.get_world()
w.add(sc)
