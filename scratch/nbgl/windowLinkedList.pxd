from nbglutManager cimport WindowInfo

ctypedef struct ListNode:
    WindowInfo *data
    ListNode *next

cdef void create()

cdef void destroy()

cdef void makeEmpty()

cdef int addFirst(WindowInfo* data)

cdef WindowInfo* remove(int id)

cdef WindowInfo* find( int id )

cdef int size()

cdef WindowInfo* first()

cdef WindowInfo* next()


