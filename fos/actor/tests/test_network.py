from fos.actor.network import AttributeNetwork

from nose.tools import assert_true, assert_false, \
     assert_equal, assert_raises

from numpy.testing import assert_array_equal, assert_array_almost_equal

import numpy as np


def test_networkcreation():
    
    node_position = np.random.random( (10,3) )
    
    attrn = AttributeNetwork({'node_position' : node_position})
    