""" This script converts a set of SWC files into an HDF5 file """

import h5py
import numpy as np
from glob import glob

# assumption
# the ids are ordered starting from 1, root node has parent -1

# the swc files are from neuromorpho.org
# http://neuromorpho.org/neuroMorpho/dableFiles/turner/Source-Version/l71.swc
# http://neuromorpho.org/neuroMorpho/dableFiles/turner/Source-Version/l55.swc

fi=glob('*.swc')
pos=None
offset=[0]
parents=None

for file in fi:
    print "Working on ", file
    a=np.loadtxt(file)
    if pos == None:
        pos = a[:,2:5]
        parents = a[:,6] - 1
        parents = parents.astype(np.int32)
        col = np.random.random_integers(50, 255, (1,4)).astype(np.ubyte)
        col[0,3] = 255
        col = np.repeat(col, len(a), axis = 0)
        colors = col
    else:
        pos = np.vstack( (pos, a[:,2:5]) )
        parents = np.hstack( (parents, a[:,6] - 1) ).astype(np.int32)
        # another random color without transparency
        col = np.random.random_integers(50, 255, (1,4)).astype(np.ubyte)
        col[0,3] = 255
        col = np.repeat(col, len(a), axis = 0)
        colors = np.vstack( (colors, col)).astype(np.ubyte)
        
    size = len(a) + offset[-1]
    offset.append(size)

offset = np.array(offset, dtype = np.int32)
pos = pos.astype(np.float32)
# in case, add a scaling factor
#pos = pos / 1000.
  
def create_hdf(pos, offset, parents, colors):
    # create extendable hdf5 file
    f = h5py.File('neurons.hdf5', 'w')
    neurons = f.create_group('neurons')
    neurons.create_dataset('positions', data=pos)
    neurons.create_dataset('offset', data=offset)
    neurons.create_dataset('parents', data=parents)
    neurons.create_dataset('colors', data=colors)
    f.close()

create_hdf(pos, offset, parents, colors)
    