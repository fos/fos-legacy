import numpy as np
import nibabel as nib
import os.path as op

import pyglet
#pyglet.options['debug_gl'] = True
#pyglet.options['debug_x11'] = True
#pyglet.options['debug_gl_trace'] = True
#pyglet.options['debug_texture'] = True

#fos modules
from fos.actor.axes import Axes
from fos import World, Window, WindowManager
#dipy modules
from dipy.segment.quickbundles import QuickBundles
from dipy.io.dpy import Dpy
from dipy.io.pickles import load_pickle,save_pickle
from dipy.viz.colormap import orient2rgb
import copy
#trento modules
from labeler import TrackLabeler
from fos.actor.slicer import Slicer

if __name__ == '__main__':

    
    #load the volume
    #img = nib.load('/usr/share/fsl/data/standard/FMRIB58_FA_1mm.nii.gz')
    img = nib.load('data/subj_05/MPRAGE_32/T1_flirt_out.nii.gz')
    data = img.get_data()
    affine = img.get_affine()    
    #load the tracks
    fdpyw = 'data/subj_05/101_32/DTI/tracks_gqi_1M_linear.dpy'    
    dpr = Dpy(fdpyw, 'r')
    T = dpr.read_tracks()
    dpr.close()    
    #T=T[:50000]
    #T=[t-np.array(data.shape)/2. for t in T]    
    fpkl = 'data/subj_05/101_32/DTI/qb_gqi_1M_linear_30.pkl'
    #qb=QuickBundles(T,10.,12)
    qb=load_pickle(fpkl)
    print 'qb ok'    
    #visualisation part        
    tl = TrackLabeler(qb,qb.downsampled_tracks(),vol_shape=data.shape,tracks_alpha=1)    
    print 'tl ok'    
    sl = Slicer(affine,data)    
    print 'sl ok'        
    #one way connection
    tl.slicer=sl
    #coordinate system axes    
    ax = Axes(100)
    x,y,z=data.shape
    print data.shape    
    w=World()
    w.add(tl)
    w.add(sl)
    w.add(ax)
    #windowing
    wi = Window(caption="Spaghetti by Free On Shades (fos.me)",\
                bgcolor=(0,0.,0.2,1),width=800,height=600)    
    print 'wi ok'
    wi.attach(w)
    print 'w attached ok'
    wm = WindowManager()
    print 'wm created ok'
    wm.add(wi)
    print 'wi attached ok'
    wm.run()
    print 'finished'
    
