import os

def get_sphere(name='symmetric362'):
    
    if name=='symmetric362':
        return os.path.join(os.path.dirname(__file__),'evenly_distributed_sphere_362.npz')
    if name=='symmetric642':
        return os.path.join(os.path.dirname(__file__),'evenly_distributed_sphere_642.npz')
    
    
    
    