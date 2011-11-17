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

cdef extern from "pthread.h":  
    ctypedef void *pthread_t
    int pthread_create(pthread_t *thread, void *attr,void *(*start_routine)(void*), void *arg)
    int   pthread_join(pthread_t, void **)
    

# initialize numpy runtime
cnp.import_array()

#numpy pointers
cdef inline float* asfp(cnp.ndarray pt):
    return <float *>pt.data

cdef inline double* asdp(cnp.ndarray pt):
    return <double *>pt.data

@cython.cdivision(True)
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

cdef void *taskcode(void *argument):

    cdef int tid
    cdef int *ptid 
    ptid = <int *> argument
    tid = ptid[0]
    #printf("Hello World! It's me, thread %d!\n", tid);
    print(tid)
    return NULL

DEF NUM_THREADS=5

cdef int test_thread ():

    cdef pthread_t threads[NUM_THREADS]
    cdef int thread_args[NUM_THREADS]
    cdef int rc, i 
      
    for i from 0<=i<NUM_THREADS:
   
      thread_args[i] = i   
      print(i)
      rc = pthread_create(&threads[i], NULL, taskcode, <void *> &thread_args[i]);
      
    for i from 0<=i<NUM_THREADS:    
      rc = pthread_join(threads[i], NULL)
      
def test():
    test_thread()
        
    
   

