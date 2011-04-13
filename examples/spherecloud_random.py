import numpy as np

from fos import Window
from fos.actor.spherecloud import SphereCloud

n = 100

# the positions for the sphere
positions = np.random.random( (n,3) ).astype( np.float32 ) * 500

# the radii for the spheres
radii = np.random.random( (n,) ).astype( np.float32 ) * 10

# the color for the spheres
colors = np.random.random( (n,4) ).astype( np.float32 ) * 10
colors[:,3] = 1.0

sc = SphereCloud( positions = positions, radii=radii, colors=colors )

wi = Window()
w = wi.get_world()
w.add(sc)
