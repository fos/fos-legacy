import numpy as np
from fos.core.scene  import Scene
from fos.core.actors import Actor
from fos.core.plots  import Plot
from fos.core.tracks import Tracks
from fos.core.points import Points


data=200*np.random.rand(1000000,3)
colors=np.random.rand(1000000,4)

print('no of bytes',colors.nbytes + data.nbytes)

tr=Tracks([data],[colors],lists=True)
#slot={0:{'actor':tr,'slot':(0, 800000)}}
#Scene(Plot(slot)).run()

pts=Points([data],[colors],point_size=3.,lists=True)

slot={0:{'actor':tr,'slot':(0, 800000)},
      1:{'actor':pts,'slot':(0, 800000)}}
Scene(Plot(slot)).run()


