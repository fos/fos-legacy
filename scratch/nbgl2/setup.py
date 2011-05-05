from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension("FosWindow", ["FosWindow.pyx"], libraries=["glut","GLU"]),
    Extension("RequestInfo", ["RequestInfo.pyx"]),
    Extension("nbglutManager", ["nbglutManager.pyx"], libraries=["glut","GLU"])
    ]

setup(
  name = 'nbgl',
  ext_modules = cythonize(ext_modules),
)
 
