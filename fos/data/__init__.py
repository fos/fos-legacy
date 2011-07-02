import os

def get_sphere(name='symmetric362'):
    
    if name=='symmetric362':
        return os.path.join(os.path.dirname(__file__),'evenly_distributed_sphere_362.npz')
    if name=='symmetric642':
        return os.path.join(os.path.dirname(__file__),'evenly_distributed_sphere_642.npz')

def get_track_filename():
    return os.path.join(os.path.dirname(__file__),'tracks300.trk')

def get_volume_filename():
    return os.path.join(os.path.dirname(__file__),'aniso_vox.nii.gz')
