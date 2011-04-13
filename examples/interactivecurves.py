import numpy as np
import nibabel as nib

from fos import World, Window
from fos.actor.curve import InteractiveCurves

# file
fname = 'streamline.trk'
streams,hdr = nib.trackvis.read(fname)

T=[s[0] for s in streams]
Trk=np.array(T, dtype=np.object)
print "loaded file"

cu = InteractiveCurves(curves = T)

w=World()
w.add(cu)

wi = Window(caption="Interactive Curves")
wi.attach(w)
