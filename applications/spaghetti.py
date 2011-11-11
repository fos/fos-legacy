import numpy as np
import nibabel as nib
import os.path as op

import fos.lib.pyglet
# debug = True
# fos.lib.pyglet.options['debug_lib'] = debug
# fos.lib.pyglet.options['debug_gl'] = debug
# fos.lib.pyglet.options['debug_gl_trace'] = debug
# fos.lib.pyglet.options['debug_gl_trace_args'] = debug
# fos.lib.pyglet.options['debug_graphics_batch'] = debug
# fos.lib.pyglet.options['shadow_window'] = debug


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
from slicer import Slicer

if __name__ == '__main__':

    
    #load the volume
    #img = nib.load('/usr/share/fsl/data/standard/FMRIB58_FA_1mm.nii.gz')
    img = nib.load('data/subj_05/MPRAGE_32/T1_flirt_out.nii.gz')
    #img = nib.load('/home/eg309/Desktop/out.nii.gz')
    data = img.get_data()
    affine = img.get_affine()
    
    #load the tracks
    #fdpyw ='/home/eg309/Data/devel09_13_Oct_2011/PROC_MR10032/subj_03/101_32/GQI/lsc_QA_ref.dpy'
    fdpyw = 'data/subj_05/101_32/DTI/tracks_gqi_1M_linear.dpy'
    
    dpr = Dpy(fdpyw, 'r')
    T = dpr.read_tracks()
    dpr.close()
    
    #T=T[:50000]
    #T=[t-np.array(data.shape)/2. for t in T]
    
    fpkl = 'data/subj_05/101_32/DTI/qb_gqi_1M_linear_20.pkl'
    #qb=QuickBundles(T,10.,12)

    qb=load_pickle(fpkl)
    #visualisation part        
    tl = TrackLabeler(qb,qb.downsampled_tracks(),vol_shape=data.shape,tracks_alpha=1)
    sl = Slicer(affine,data,alpha=255)    
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
    wi = Window(caption="Spaghetti by Free On Shades (fos.me)",bgcolor=(0,0.,0.2,1),width=800,height=600)
    wi.attach(w)
    wm = WindowManager()
    wm.add(wi)
    wm.run()
    
