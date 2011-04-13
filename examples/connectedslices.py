import scipy.ndimage as nd
import nibabel as ni
from fos.actor.volslicer import ConnectedSlices 
from fos import World, Window

# your nifti volume
f1 = 'raw_t1_image.nii.gz'
img = ni.load(f1)

data = img.get_data()
affine = img.get_affine()

cds = ConnectedSlices(affine,data)

w = World()
w.add(cds)

wi = Window()
wi.attach(w)
