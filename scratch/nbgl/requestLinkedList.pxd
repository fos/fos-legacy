from nbglutManager cimport RequestInfo

ctypedef struct ListNode:
    RequestInfo *data
    ListNode *next


cdef void createEmptyList()

cdef void destroyList()

cdef void makeEmpty()

cdef void addLast(RequestInfo* w)

cdef RequestInfo* removeFirst()

cdef int size()

'''
The functions first and next are neither thread safe nor can be safely 
'''

cdef RequestInfo* first()

cdef RequestInfo* next()
