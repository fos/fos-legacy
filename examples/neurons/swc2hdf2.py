""" This script converts a set of SWC files into an HDF5 file """

import h5py
import numpy as np
from glob import glob

# assumption
# the ids are ordered starting from 1, root node has parent -1

# the swc files are from neuromorpho.org
# http://neuromorpho.org/neuroMorpho/dableFiles/turner/Source-Version/l71.swc
# http://neuromorpho.org/neuroMorpho/dableFiles/turner/Source-Version/l55.swc

fi=glob('l71.swc')

ficon = []
for file in fi:
    print "Working on ", file
    ficon.append( np.loadtxt(file) )

# compute big arrays
# number of vertices
N = 0
for ele in ficon:
    N += len(ele)

big_pos = np.zeros( (N, 3), dtype = np.float32 )
big_lab = np.zeros( (N, ), dtype = np.int32 )
# connectivity without root node connectivity
big_con = np.zeros( ( 2 * ( N - len(ficon) ),), dtype = np.float32 )
print "big_con", big_con.shape
# per line colors
big_col = np.zeros( (N - len(ficon), 4), dtype = np.float32 )
print "big_col", big_col.shape

def swc2linseg(swcarr):
    """ Converts swc topology (1-indexed) to full
    line connectivity. Assuming the first row is root

    e.g
    [-1, 0, 1, 2, 1 ] to [1,0, 2,1, 3,2, 4,1]
    [-1, 1, 2, 3, 4 ] to [0,1, 1,2, 2,3, 3,4]
    """
    assert( swcarr[0] < 0 )

    N = len(swcarr)
    swcarr.shape = ( N, 1 )
    swcarr2 = swcarr.repeat(2, axis = 1).astype( np.int32 )
    swcarr2[:,1] = np.array( range(N) )
    return swcarr2[1:,:].ravel()

# test
#ina = np.array( [-1, 0, 1, 2, 1 ] )
#print swc2linseg(ina)

# vertices offset
off = 0
# line offset
offseg = 0
rad = np.random.random( (1, 3) )

for i,a in enumerate(ficon):

    # number of vertices
    n = len(a)
    print("number of vertices {0}".format(n))
    
    big_lab[off:off+n] = i + 1000
    big_pos[off:off+n,:] = a[:,2:5]

#    big_con[off:off+n]

    print offseg
    print offseg+n-1
    # assume the first vertex is root
    #print a[1:,6] - 1
    print "offset start", offseg
    print "offset end", offseg + (n-1) * 2
    print "offset end col", offseg + (n-1)
    print "n", n
    print "swc", a[:10,6] - 1
    # this is local topology
    #big_con[offseg:offseg + (n-1) * 2] = swc2linseg(a[:,6] - 1)
    # but we want global!
    big_con[offseg:offseg + (n-1) * 2] = swc2linseg(a[:,6] - 1) + int(off)

    #big_col[offseg/2:offseg/2 + n-1,:3] = rad.repeat( n-1, axis = 0)
    big_col[offseg/2:offseg/2 + n-1,:3] = np.random.random( (n - 1, 3) )
    big_col[offseg/2:offseg/2 + n-1,3] = np.ones( (n - 1,) )

    off += n
    offseg += (n-1) * 2
    print big_con[:10], big_con[-20:]

big_con = big_con.astype( np.uint32 )

def create_hdf(pos, parents, labeling, colors):
    # create extendable hdf5 file
    f = h5py.File('neurons2.hdf5', 'w')
    neurons = f.create_group('neurons')
    neurons.create_dataset('position', data=pos)
    neurons.create_dataset('localtopology', data=parents.astype( np.int32 ))
    neurons.create_dataset('labeling', data=labeling)
    neurons.create_dataset('segmentcolors', data=colors)
    f.close()

create_hdf(big_pos, big_con, big_lab, big_col)
