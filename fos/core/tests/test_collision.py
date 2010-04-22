import numpy as np

from nose.tools import assert_true, assert_false, assert_equal, assert_almost_equal

from numpy.testing import assert_array_equal, assert_array_almost_equal

import fos.core.collision as cll


def test_mindistance_segment2track():

    print 'touching one segment only'

    print cll.mindistance_segment2track([1,0,0],[0,1,0],np.array([[1,0,0],[0,1,1],[3,3,3]]))

    print 'cross with the second'

    print cll.mindistance_segment2track([0,0,0],[1,0,0],np.array([[3,3,3],[0.5,1,0],[0.5,-1,0]]))
    

def test_segment2segment():


    print '#intersecting at 0'
    
    print cll.closest_points_2segments([-10,0,0],[10,0,0],[0,1,0],[0,-1,0])

    print

    print '#parallel'
    
    print cll.closest_points_2segments([-10,0,0],[10,0,0],[0,1,0],[3,1,0])

    print

    print '#parallel 2'
    
    print cll.closest_points_2segments([-3,0,0],[-1,0,0],[0,1,0],[3,1,0])

    print

    print '#aligned'
    
    print cll.closest_points_2segments([-10,0,0],[10,0,0],[0,0,0],[3,0,0])

    print

    print '#nose 2 nose touching'
    
    print cll.closest_points_2segments([0,0,0],[1,1,0],[1,1,0],[2,0,0])

    print

    print '#nose 2 nose outside segments'
    
    print cll.closest_points_2segments([0,0,0],[1,1,0],[2,1,0],[3,0,0])

    print

    print '#vertical in distance'

    print cll.closest_points_2segments([0,0,0],[1,0,0],[0.5,-1,1],[0.5,1,1])

    print

    print '#touch vertically'

    print cll.closest_points_2segments([0,0,0],[1,0,0],[0.5,1,0],[0.5,0,0])

    print

    print '#touch vertically - opposite'

    print cll.closest_points_2segments([0.5,1,0],[0.5,0,0],[0,0,0],[1,0,0])

    print
    

    print '#intersect vertically - no touching'

    print cll.closest_points_2segments([0.5,1,0],[0.5,0,0],[0,-1,0],[1,-1,0])

    print
    



    

    
