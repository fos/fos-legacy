""" Test for the SphereCloud actor """

from nose.tools import assert_true, assert_false, \
     assert_equal, assert_raises

from numpy.testing import assert_array_equal, assert_array_almost_equal

import numpy as np

def test_spherecloud():
    
    from fos.actor.spherecloud import SphereCloud
    
    # the positions for the sphere
    positions = np.array( [[0,0,0],
                           [1,1,1],
                           [10,10,10]], dtype = np.float32 )
    
    # the radii for the spheres
    radii = np.array( [1.0, 1.0, 2.0], dtype = np.float32 )
    
    # the color for the spheres
    colors = np.ones((len(positions),4)).astype('f4')
    colors[:,:3] = np.random.rand(len(positions),3).astype('f4')
    
    sc = SphereCloud( positions = positions, radii=radii, colors=colors )

    
    
if __name__ == '__main__':
    
    test_spherecloud()
