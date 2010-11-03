#from fos.actor.network import AttributeNetwork

from nose.tools import assert_true, assert_false, \
     assert_equal, assert_raises

from numpy.testing import assert_array_equal, assert_array_almost_equal

import numpy as np

from fos.actor.network import NodeGLPrimitive

def test_nodeglprimitive_makecube():
    
    node_position = np.array( [[0,0,0],
                               [1,1,1],
                               [10,10,10]], dtype = np.float32 )
    
    node_size = np.array( [1.0, 1.0, 2.0], dtype = np.float32 )
    
    prim = NodeGLPrimitive()
    prim._make_cubes(node_position, node_size)
    
    assert_equal(prim.vertices_nr, 24)
    assert_equal(prim.indices_nr, 18)
    assert_array_equal(prim.vertices[0,:], np.array( [[ -0.5, -0.5, -0.5]],
                                                     dtype = np.float32))
    
    assert_array_equal(prim.vertices[24,:], np.array( [[ 11.,  11., 11. ]],
                                                     dtype = np.float32))
    
    
    
if __name__ == '__main__':
    
    test_nodeglprimitive_makecube()