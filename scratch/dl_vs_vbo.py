import numpy as np
from fos.core.scene  import Scene
from fos.core.actors import Actor
from fos.core.plots  import Plot
from fos.core.tracks import Tracks
from fos.core.tracks import Points


data=200*np.random.rand(1000,3)
colors=np.random.rand(1000,4)

#tr=Tracks(data,colors)
#slot={0:{'actor':tr,'slot':(0, 800000)}}
#Scene(Plot(slot)).run()

pts=Points([data],[colors])
slot={0:{'actor':pts,'slot':(0, 800000)}}
Scene(Plot(slot)).run()
