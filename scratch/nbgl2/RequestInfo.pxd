from FosWindow cimport FosWindow

cdef class RequestInfo:
    cdef FosWindow fosWindow
    cdef int request
