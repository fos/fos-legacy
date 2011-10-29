import nibabel as ni

from fos.actor.volslicer import ConnectedSlices 
from fos import World,Window, WindowManager
from fos.data import get_volume_filename

img = ni.load( get_volume_filename() )
data = img.get_data()
affine = img.get_affine()

cds = ConnectedSlices(affine,data)

w = World()
w.add(cds)

wi = Window()
wi.attach(w)

wm = WindowManager()
wm.add(wi)
wm.run()