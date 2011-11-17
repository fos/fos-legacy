#!/usr/bin/env python
''' Installation script for the fos package '''


from os.path import join as pjoin
from glob import glob
from distutils.core import setup
from distutils.extension import Extension
import numpy as np

from build_helpers import make_cython_ext

# we use cython to compile the module if we have it
try:
    import Cython
except ImportError:
    has_cython = False
else:
    has_cython = True
    
col_ext, cmdclass = make_cython_ext(
    'fos.core.collision',
    has_cython,
    include_dirs = [np.get_include()])

cgl_ext, cmdclass = make_cython_ext(
    'fos.core.cython_gl',
    has_cython,
    include_dirs = [np.get_include()])

setup(name='fos',
      version='0.2',
      description='Scientific 3d Engine',
      author='Fos Team',
      author_email='garyfallidis@gmail.com',
      url='http://github.com/Garyfallidis/Fos',
      packages=['fos','fos.core','fos.actor'],
      ext_modules = [col_ext],
      cmdclass    = cmdclass,
      )

