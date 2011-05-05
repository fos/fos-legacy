Demonstrate the problems that we face when combine Cython objects with pthreads, glut ang open gl

compile: 
python setup.py build_ext --inplace

or

./compile


run:
import nbglutManager as nbgl
manager = nbgl.Manager()
manager.initialize([])
manager.openWindow('a', 1, 1, 300, 300)
manager.openWindow('b', 1, 1, 300, 300)
manager.openWindow('c', 1, 1, 300, 300)
manager.openWindow('d', 1, 1, 300, 300)
....

# sooner or later we get Segmentation fault

manager.destroy()
