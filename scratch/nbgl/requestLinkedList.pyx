cimport requestLinkedList

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void *malloc(size_t size)
    void free(void *pointer)


# Global Variables
cdef ListNode *head = NULL
cdef ListNode *tail = NULL
cdef int numNodes = 0
cdef ListNode *iteratorPosition


cdef void create():
    global head
    global tail
    global numNodes

    if (head != NULL):
        destroy()

    head = <ListNode*> malloc(sizeof(ListNode))
    head.data = NULL
    head.next = NULL
    tail = head
    numNodes = 0


cdef void destroy():
    global head
    global tail
    global iteratorPosition
 
    if (head != NULL):
        makeEmpty( )
        free(head)
        head = NULL
        tail = NULL
        iteratorPosition = NULL


cdef void makeEmpty(): 
    global head
    global tail
    global numNodes

    cdef ListNode* p = head.next
    cdef ListNode *cur
    while (p != NULL):
        if (p.data != NULL):
            free(p.data)
        cur = p
        p = p.next 
        free(cur)
    
    head.next = NULL
    tail = head
    numNodes = 0 


cdef int addLast(RequestInfo* data):
    global tail
    global numNodes

    if (tail == NULL):
        return False

    cdef ListNode* p = <ListNode*> malloc(sizeof(ListNode))
    p.data = data
    p.next = NULL
    tail.next = p
    tail = p
    numNodes += 1

    return True
   

cdef RequestInfo* removeFirst():
    global head
    global tail
    global numNodes
    global iteratorPosition

    cdef ListNode* p = head.next
    cdef RequestInfo* requestInfo = NULL

    if (p != NULL):
        head.next = p.next
        requestInfo = p.data  
        if (iteratorPosition == p):
            iteratorPosition = head  
        free(p)
        numNodes -= 1
        if (numNodes == 0):
            head.next = NULL
            tail = head

    return requestInfo


cdef int size():
    global numNodes

    return numNodes


# Iterator methods

cdef RequestInfo* first():
    global head
    global iteratorPosition

    iteratorPosition = head.next
    if (iteratorPosition != NULL):
        return iteratorPosition.data

    return NULL



cdef RequestInfo* next():
    global iteratorPosition

    if (iteratorPosition != NULL):
        iteratorPosition = iteratorPosition.next

    if (iteratorPosition != NULL):
        return iteratorPosition.data

    return NULL
