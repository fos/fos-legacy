import numpy as np
import nibabel as nib
import os.path as op

from fos import World, Window, WindowManager
from fos.actor.curve import InteractiveCurves
from fos.data import get_track_filename

# exmple track file
streams,hdr = nib.trackvis.read(get_track_filename())

T=[s[0] for s in streams]
Trk=np.array(T, dtype=np.object)
print "loaded file"

cu = InteractiveCurves(curves = T)

w=World()
w.add(cu)

wi = Window(caption="Interactive Curves")
wi.attach(w)

wm = WindowManager()
wm.add(wi)
wm.run()