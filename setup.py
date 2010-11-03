#!/usr/bin/env python
''' Installation script for fos package '''


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
      version='0.1a',
      description='Scientific 3d Engine',
      author='Fos Team',
      author_email='garyfallidis@gmail.com',
      url='http://github.com/Garyfallidis/Fos',
      packages=['fos','fos.core'],
      #package_data={'dipy.io': ['tests/data/*', 'tests/*.py']},
      ext_modules = [col_ext], #,cgl_ext],
      cmdclass    = cmdclass,      
      scripts=glob('scripts/*.py')
      )

