from enthought.mayavi.tools.sources import open
from enthought.mayavi import mlab
import enthought.mayavi.tools.sources as sources
src=sources.open('/home/eg309/Desktop/rh.pial.vtk')
surf=mlab.pipeline.surface(src)
pd=src.outputs[0]
pd[0]
#?pd.points.to_array
pts=pd.points.to_array()
polys=pd.polys.to_array()
polys.shape
pts.shape
polys.shape
lpol=len(polys)/4
polys=polys.reshape(lpol,4)


