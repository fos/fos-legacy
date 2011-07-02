import numpy as np
import nibabel as nib

from fos import World, Window, WindowManager
from fos.actor.polygonlines import PolygonLines

# sample polygon line data
from fos.data import get_track_filename
streams,hdr = nib.trackvis.read(get_track_filename())
T=[s[0] for s in streams]
trk=np.array(T, dtype=np.object)

# convert tracks to flat array with full connectivity
nvert = sum([t.shape[0] for t in trk])
vert = np.zeros( (nvert, 3), dtype = np.float32)
lab = np.zeros( (nvert,), dtype = np.uint32 )
con = np.zeros( (nvert, 2), dtype = np.uint32 )
offset = 0
for i,ft in enumerate(trk):
    print 'work on fiber', i
    # index is
    lft = len(ft)
    start = offset
    end = offset+lft

    lab[start:end] = i + 1 # unique label
    vert[start:end] = ft

    con[start:end,0] = np.array(range(lft), dtype = np.uint32) + offset
    con[start:end:,1] = np.array(range(1,lft+1), dtype = np.uint32) + offset

    offset += lft

aff = np.eye( 4 )
aff[0,3] = -20
act = PolygonLines(vertices = vert, connectivity = con, affine = aff)
act.show_aabb = True

w = World()
w.add(act)

window = Window()
window.attach(w)

wm = WindowManager()
wm.add(window)
wm.run()