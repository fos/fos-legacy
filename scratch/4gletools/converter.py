# using gletools, i would like to display brain meshes
# here you see how to convert gifti brain meshes to a format consumable by gletools
# http://codeflow.org/entries/2009/jul/31/gletools-advanced-pyglet-utilities/
# and calculate the normals

import numpy as np
from fos.comp_geom.gen_normals import *

a=gi.read('fsaverage.gii')
np.savetxt('/home/stephan/vertices', a.darrays[0].data, delimiter=' ')
np.savetxt('/home/stephan/faces', a.darrays[1].data, fmt='%5i', delimiter=' ')
n=auto_normals(v,w)
np.savetxt('/home/stephan/normals', n, delimiter=' ')
