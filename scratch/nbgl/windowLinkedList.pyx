cimport windowLinkedList

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void *malloc(size_t size)
    void free(void *pointer)


# Global Variables
cdef ListNode *head = NULL
cdef int numNodes = 0
cdef ListNode *iteratorPosition


cdef void create():
    global head
    global numNodes

    if (head != NULL):
        destroy()

    head = <ListNode*> malloc(sizeof(ListNode))
    head.data = NULL
    head.next = NULL
    numNodes = 0


cdef void destroy():
    global head
 
    if (head != NULL):
        makeEmpty( )
        free(head)
        head = NULL


cdef void makeEmpty(): 
    global head
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
    numNodes = 0 


cdef int addFirst(WindowInfo* data):
    global head
    global numNodes

    if (head == NULL):
        return False

    cdef ListNode* p = <ListNode*> malloc(sizeof(ListNode))
    p.data = data
    p.next = head.next
    head.next = p
    numNodes += 1

    return True

cdef WindowInfo* remove(int id):
    global head
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
            head.next = NULL

    return windowInfo


cdef WindowInfo* find( int id ):
    global head

    if (head == NULL):
        return NULL

    cdef ListNode* p = head.next
    while (p != NULL):
        if (p.data.id == id):
            return p.data
        p = p.next

    return NULL  



cdef ListNode* findPrevious( int id ):
    global head

    if (head == NULL):
        return NULL

    cdef ListNode *prev = head
    cdef ListNode *cur = head.next

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
    global head
    global iteratorPosition

    if (head == NULL):
        return NULL

    iteratorPosition = head.next
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
