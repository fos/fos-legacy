from nbglutManager cimport WindowInfo

ctypedef struct ListNode:
    WindowInfo *data
    ListNode *next

cdef void createEmptyList()

cdef void destroyList()

cdef void makeEmpty()

cdef void addFirst(WindowInfo* data)

cdef WindowInfo* remove(int id)

cdef WindowInfo* find( int id )

cdef int size()

cdef WindowInfo* first()

cdef WindowInfo* next()


