import numpy as np

from nose.tools import assert_true, assert_false, assert_equal, assert_almost_equal

from numpy.testing import assert_array_equal, assert_array_almost_equal

import fos.core.collision as cll

def test_segment2segment():


    print '#intersecting at 0'
    
    print cll.closest_points_2segments([-10,0,0],[10,0,0],[0,1,0],[0,-1,0])

    print

    print '#aligned'
    
    print cll.closest_points_2segments([-10,0,0],[10,0,0],[0,0,0],[0,3,0])

    print

    print '#nose 2 nose'
    
    print cll.closest_points_2segments([0,0,0],[1,1,0],[1,1,0],[2,0,0])

    print

    print '#nose 2 nose outside segments'
    
    print cll.closest_points_2segments([0,0,0],[1,1,0],[2,1,0],[3,0,0])

    
