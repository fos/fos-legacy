# A type of -*- python -*- file
""" Track propagation performance functions
"""

# cython: profile=True
# cython: embedsignature=True

cimport cython

import numpy as np
cimport numpy as cnp

cdef extern from "math.h" nogil:
    double floor(double x)
    float sqrt(float x)
    float fabs(float x)
    double log2(double x)
    double cos(double x)
    double sin(double x)
    float acos(float x )   
    bint isnan(double x)
    double sqrt(double x)
    
    
cdef extern from "GL/gl.h":
    ctypedef unsigned int GLenum
    ctypedef double GLdouble
    ctypedef int GLsizei
    ctypedef float GLfloat
    ctypedef void GLvoid
    int GL_TRIANGLES
    int GL_FLOAT
    int GL_UNSIGNED_BYTE
    cdef void glPushMatrix()
    cdef void glPopMatrix()    
    void glGetDoublev(GLenum pname, GLdouble *params)     
    void glMultiDrawElements(GLenum mode,GLsizei *count, GLenum type, GLvoid **indices, GLsizei primcount)

# initialize numpy runtime
cnp.import_array()

#numpy pointers
cdef inline float* asfp(cnp.ndarray pt):
    return <float *>pt.data

cdef inline double* asdp(cnp.ndarray pt):
    return <double *>pt.data

cdef  long offset(long *indices,long *strides,int lenind, int typesize) nogil:

    '''
    Parameters
    ----------
    indices: long * (int64 *), indices of the array which we want to
    find the offset
    strides: long * strides
    lenind: int, len(indices)
    typesize: int, number of bytes for data type e.g. if double is 8 if
    int32 is 4

    Returns:
    --------
    offset: integer, offset from 0 pointer in memory normalized by dtype
    '''
 
    cdef int i
    cdef long summ=0
    for i from 0<=i<lenind:
        #print('st',strides[i],indices[i])
        summ+=strides[i]*indices[i]        
    summ/=<long>typesize
    return summ

def ndarray_offset(cnp.ndarray[long, ndim=1] indices, \
                 cnp.ndarray[long, ndim=1] strides,int lenind, int typesize):
    ''' find offset in an ndarray using strides

    Parameters
    ----------
    indices: array, shape(N,), indices of the array which we want to
    find the offset
    strides: array, shape(N,), strides
    lenind: int, len(indices)
    typesize: int, number of bytes for data type e.g. if double is 8 if
    int32 is 4
    
    Returns:
    --------
    offset: integer, offset from 0 pointer in memory normalized by dtype
    
    Example
    -------
    >>> import numpy as np
    >>> from dipy.core.reconstruction_performance import ndarray_offset
    >>> I=np.array([1,1])
    >>> A=np.array([[1,0,0],[0,2,0],[0,0,3]])
    >>> S=np.array(A.strides)
    >>> ndarray_offset(I,S,2,8)
    4
    >>> A.ravel()[4]==A[1,1]
    True

    '''

    return offset(<long*>indices.data,<long*>strides.data,lenind, typesize)

def get_vertices_faces(cnp.ndarray[float, ndim=2] verts,cnp.ndarray[unsigned int, ndim=2] faces):

    print 'hello'
    return


def get_ppointer(cnp.ndarray[unsigned int, ndim=2] indices):
    
    #print 'indices'
    #print indices[0][0]
    cdef void* pind=<void *>indices[0].data
    cdef void* pind2=<void *>indices[1].data
    cdef void* ppind[2]
    cdef double** test
    
    ppind[0]=pind
    ppind[1]=pind2
    
    
    
        
        
    return 


  


