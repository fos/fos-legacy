from nbglutManager cimport RequestInfo

ctypedef struct ListNode:
    RequestInfo *data
    ListNode *next


cdef void create()

cdef void destroy()

cdef void makeEmpty()

cdef int addLast(RequestInfo* w)

cdef RequestInfo* removeFirst()

cdef int size()

'''
The functions first and next are neither thread safe nor can be safely 
'''

cdef RequestInfo* first()

cdef RequestInfo* next()
