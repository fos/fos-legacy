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
from labeler import TrackLabeler
from fos.actor.slicer import Slicer
#dipy modules
from dipy.segment.quickbundles import QuickBundles
from dipy.io.dpy import Dpy
from dipy.io.pickles import load_pickle,save_pickle
from dipy.viz.colormap import orient2rgb
import copy


if __name__ == '__main__':

    subject = 5
    seeds = 1
    qb_dist = 30
    
    #load T1 volume registered in MNI space    
    img = nib.load('data/subj_'+("%02d" % subject)+'/MPRAGE_32/T1_flirt_out.nii.gz')
    data = img.get_data()
    affine = img.get_affine()    
    #load the tracks registered in MNI space 
    fdpyw = 'data/subj_'+("%02d" % subject)+'/101_32/DTI/tracks_gqi_'+str(seeds)+'M_linear.dpy'    
    dpr = Dpy(fdpyw, 'r')
    T = dpr.read_tracks()
    dpr.close()    
    #load initial QuickBundles with threshold 30mm
    fpkl = 'data/subj_'+("%02d" % subject)+'/101_32/DTI/qb_gqi_'+str(seeds)+'M_linear_'+str(qb_dist)+'.pkl'
    #qb=QuickBundles(T,30.,12)    
    qb=load_pickle(fpkl)
    #create the interaction system for tracks 
    tl = TrackLabeler(qb,qb.downsampled_tracks(),vol_shape=data.shape,tracks_alpha=1)   
    #add a interactive slicing/masking tool
    sl = Slicer(affine,data)    
    #add one way communication between tl and sl
    tl.slicer=sl
    #OpenGL coordinate system axes    
    ax = Axes(100)
    x,y,z=data.shape
    #add the actors to the world    
    w=World()
    w.add(tl)
    w.add(sl)
    w.add(ax)
    #create a window
    wi = Window(caption="Interactive Spaghetti using Diffusion Imaging in Python (dipy.org) and Free On Shades (fos.me)",\
                bgcolor=(0.3,0.3,0.6,1),width=1200,height=800)    
    #attach the world to the window
    wi.attach(w)
    #create a manager which can handle multiple windows
    wm = WindowManager()
    wm.add(wi)    
    wm.run()
    print('Everything is running ;-)')
    
