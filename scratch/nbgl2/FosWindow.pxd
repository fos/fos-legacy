cdef class FosWindow:
    cdef int id
    cdef char title[256]
    cdef int x
    cdef int y
    cdef int w
    cdef int h
    cdef void setup(self)

    cdef float angle  # to be removed
    

cdef void reshapeFunc(int width, int height)
cdef void keyboardFunc(unsigned char key, int x, int y)
cdef void displayFunc()
cdef void update(int dt)


