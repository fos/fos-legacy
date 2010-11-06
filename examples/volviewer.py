import scipy.ndimage as nd
import nibabel as ni
from fos.actor.volslicer import ConnectedSlices 
from fos import World,Window

f1='/home/eg309/Data/regtest/fiac0/meanafunctional_01.nii'
img=ni.load(f1)

data =img.get_data()
affine=img.get_affine()

cds =ConnectedSlices(affine,data)
#actors.append(cds)

w=World()
w.add(cds)
wi=Window()
wi.attach(w)
