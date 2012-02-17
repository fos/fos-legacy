import sys
import numpy as np
import nibabel as nib

from dipy.reconst.dti import Tensor
from dipy.reconst.dni import EquatorialInversion
from dipy.reconst.gqi import GeneralizedQSampling
from dipy.reconst.dsi import DiffusionSpectrum
from dipy.segment.quickbundles import QuickBundles
from dipy.tracking.eudx import EuDX
from dipy.external.fsl import pipe,flirt2aff
#from eudx_results import show_tracks
from fos.actor.slicer import Slicer
from fos.actor.point import Point
from fos import Actor,World, Window, WindowManager
from labeler import TrackLabeler

fmask1='/home/eg309/Data/John_Seg/_RH_premotor.nii.gz'
fmask2='/home/eg309/Data/John_Seg/_RH_parietal.nii.gz'
fmask3='/home/eg309/Data/John_Seg/_LH_premotor.nii.gz'
fmask4='/home/eg309/Data/John_Seg/_LH_parietal.nii.gz'

fmasks=[fmask1,fmask2,fmask3,fmask4]

def expand_seeds(seeds,no=5):
    lseeds=len(seeds)
    seeds2=np.zeros((no*lseeds,3))
    for i in range(no):
        seeds2[i*lseeds:(i+1)*lseeds]=seeds + 1*np.random.rand(lseeds,3) - 0.5
    return seeds2

def transform_tracks(tracks,affine):
            return [(np.dot(affine[:3,:3],t.T).T + affine[:3,3]) for t in tracks]


if __name__=='__main__':

    subject=sys.argv[1]

    fsl_ref = '/usr/share/fsl/data/standard/FMRIB58_FA_1mm.nii.gz'
    img_ref =nib.load(fsl_ref)
    ffa='data/subj_'+subject+'/101_32/DTI/fa.nii.gz'
    fmat='data/subj_'+subject+'/101_32/DTI/flirt.mat'
    img_fa =nib.load(ffa)
    img_ref =nib.load(fsl_ref)
    ref_shape=img_ref.get_data().shape
    mat=flirt2aff(np.loadtxt(fmat),img_fa,img_ref)
    fimat='data/subj_'+subject+'/101_32/DTI/iflirt.mat'
    cmd='convert_xfm -omat '+ fimat + ' -inverse '+ fmat
    pipe(cmd)
    fmasknative='data/subj_'+subject+'/101_32/DTI/LH_premotor_native.nii.gz'
    cmd='flirt -in '+fmask3+ ' -ref '+ffa + ' -out '+ fmasknative + ' -init ' + fimat + ' -applyxfm'  
    pipe(cmd)

    img = nib.load(fmasknative)
    mask = img.get_data()

    mask[mask>0]=1
    mask=mask.astype(np.uint8)

    seeds=np.where(mask>0)
    seeds=np.array(seeds).T
    seeds=seeds.astype(np.float64)
    seeds=expand_seeds(seeds,50)

    fraw='data/subj_'+subject+'/101_32/rawbet.nii.gz'
    fbval='data/subj_'+subject+'/101_32/raw.bval'
    fbvec='data/subj_'+subject+'/101_32/raw.bvec'

    img = nib.load(fraw)
    data = img.get_data()
    affine = img.get_affine()
    bvals = np.loadtxt(fbval)
    gradients = np.loadtxt(fbvec).T

    tensors = Tensor(data, bvals, gradients, thresh=50)
    FA = tensors.fa()
    famask=FA>=.2
    
    gqs=GeneralizedQSampling(data,bvals,gradients,1.2,
                odf_sphere='symmetric642',
                mask=famask,
                squared=False,
                save_odfs=False)
    """ 
    ei=EquatorialInversion(data,bvals,gradients,odf_sphere='symmetric642',\
            mask=famask,\
            half_sphere_grads=True,\
            auto=False,\
            save_odfs=False,\
            fast=True)
    ei.radius=np.arange(0,5,0.4)
    ei.gaussian_weight=0.05
    ei.set_operator('laplacian')
    ei.update()
    ei.fit()

    ds=DiffusionSpectrum(data,bvals,gradients,\
                odf_sphere='symmetric642',\
                mask=famask,\
                half_sphere_grads=True,\
                auto=True,\
                save_odfs=False)
    """

    #ds.PK[FA<.2]=np.zeros(5)
    #euler=EuDX(a=FA,ind=tensors.ind(),seeds=seeds,a_low=.2)
    #euler=EuDX(a=ds.PK,ind=ds.IN,seeds=seeds,odf_vertices=ds.odf_vertices,a_low=.2)
    euler=EuDX(a=gqs.qa(),ind=gqs.ind(),seeds=3*10**6,odf_vertices=gqs.odf_vertices,a_low=.0239)
    #euler=EuDX(a=gqs.qa(),ind=gqs.ind(),seeds=seeds,odf_vertices=gqs.odf_vertices,a_low=.0239)
    
    T=[track for track in euler]

    T=transform_tracks(T,mat)

    shift=(np.array(ref_shape)-1)/2.
    T=[t-shift for t in T]    
    
    print len(T)

    qb=QuickBundles(T,20.,18)

    tl = TrackLabeler(qb,\
                qb.downsampled_tracks(),\
                vol_shape=data.shape[:3],\
                tracks_line_width=3.,\
                tracks_alpha=1)

    fT1 = 'data/subj_'+subject+'/MPRAGE_32/T1_flirt_out.nii.gz'
    img = nib.load(fT1)

    sl = Slicer(img.get_affine(),img.get_data())

    tl.slicer=sl

    #seeds=np.dot(seeds,mat[:3,:3])+mat[:,3]

    seeds=np.dot(mat[:3,:3],seeds.T).T + mat[:3,3]
    seeds=seeds-shift
    
    msk = Point(seeds,colors=(1,0,0,1.),pointsize=2.)

    w=World()
    w.add(tl)
    w.add(msk)
    w.add(sl)

    wi = Window(caption="Fos",\
                bgcolor=(.3,.3,.6,1.),\
                width=1600,\
                height=900)

    wi.attach(w)

    wm = WindowManager()
    wm.add(wi)
    wm.run()



















