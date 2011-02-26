cimport windowLinkedList

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void *malloc(size_t size)
    void free(void *pointer)


# Global Variables
cdef ListNode *header = NULL
cdef int numNodes = 0
cdef ListNode *iteratorPosition


cdef void createEmptyList():
    global header
    global numNodes

    if (header != NULL):
        destroyList()

    header = <ListNode*> malloc(sizeof(ListNode))
    header.data = NULL
    header.next = NULL
    numNodes = 0


cdef void destroyList():
    global header
 
    if (header != NULL):
        makeEmpty( )
        free(header)
        header = NULL


cdef void makeEmpty(): 
    global header
    global numNodes

    cdef ListNode* p = header.next
    cdef ListNode *cur
    while (p != NULL):
        if (p.data != NULL):
            free(p.data)
        cur = p
        p = p.next 
        free(cur)
    
    header.next = NULL
    numNodes = 0 


cdef void addFirst(WindowInfo* data):
    global header
    global numNodes

    cdef ListNode* p = <ListNode*> malloc(sizeof(ListNode))
    p.data = data
    p.next = header.next
    header.next = p
    numNodes += 1


cdef WindowInfo* remove(int id):
    global header
    global numNodes
    global iteratorPosition

    cdef ListNode* p = findPrevious(id)
    cdef ListNode* cur 
    cdef WindowInfo* windowInfo = NULL

    if (p != NULL):
        cur = p.next
        p.next = cur.next
        windowInfo = cur.data  
        if (cur == iteratorPosition):
            iteratorPosition = p 
        free(cur)
        numNodes -= 1
        if (numNodes == 0):
            header.next = NULL

    return windowInfo


cdef WindowInfo* find( int id ):
    global header

    cdef ListNode* p = header.next
    while (p != NULL):
        if (p.data.id == id):
            return p.data
        p = p.next

    return NULL  



cdef ListNode* findPrevious( int id ):
    global header

    cdef ListNode *prev = header
    cdef ListNode *cur = header.next

    while(cur != NULL):
        if (cur.data.id == id):
            return prev

        prev = cur 
        cur = cur.next
    
    return NULL



cdef int size():
    global numNodes

    return numNodes



# The iterator should not be mixed with remove
cdef WindowInfo* first():
    global header
    global iteratorPosition

    iteratorPosition = header.next
    if (iteratorPosition != NULL):
        return iteratorPosition.data

    return NULL



cdef WindowInfo* next():
    global iteratorPosition

    if (iteratorPosition != NULL):
        iteratorPosition = iteratorPosition.next

    if (iteratorPosition != NULL):
        return iteratorPosition.data

    return NULL
