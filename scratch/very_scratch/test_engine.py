
from nose.tools import assert_true, assert_false, \
     assert_equal, assert_raises

from numpy.testing import assert_array_equal, assert_array_almost_equal

import numpy as np

import pyglet as pyglet
from fos.core.world import World
from fos.actor.volslicer import ConnectedSlices
from fos.core.fos_window import FosWindow
from fos.core.camera import DefaultCamera
from fos.core.engine import Engine

def test_engine2windows():
    
    eng = Engine()
    eng.run()
    # create a world
    w = World(0)
    
    # create default camera
    cam = DefaultCamera()
    
    # add camera
    w.add(cam)
    
    # create image viewr
    a=np.random.random( ( 100, 100, 100) )
    aff = np.eye(4)
    cds = ConnectedSlices(aff,a)
    
    # add cds to world
    w.add(cds)
    
    # add world to engine
    eng.add(w)
    
    # create a window
    wi = FosWindow()
    
    # attach window to world
    wi.attach(w)
    
    wi2 = FosWindow()
    # attach window to world
    wi2.attach(w)
    
    
def test_engine2windows2cameras():
    
    eng = Engine()
    eng.run()
    # create a world
    w = World(0)
    w2 = World(1)
    
    # create default camera
    cam = DefaultCamera()
    cam2 = DefaultCamera()
    
    # add camera
    w.add(cam)
    w2.add(cam2)
    
    # create image viewr
    a=np.random.random( ( 100, 100, 100) )
    aff = np.eye(4)
    cds = ConnectedSlices(aff,a)
    
    # add cds to world
    w.add(cds)
    w2.add(cds)
    
    # add world to engine
    eng.add(w)
    eng.add(w2)
    
    # create a window
    wi = FosWindow()
    wi.attach(w)
    
    wi2 = FosWindow()
    # attach window to world
    wi2.attach(w2)
    
    
