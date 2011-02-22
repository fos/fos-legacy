cimport nbglutManager
from nbglutManager cimport WindowInfo

cimport windowLinkedList
cimport requestLinkedList
cimport trialDraw



cdef extern from "pthread.h":
    ctypedef void *pthread_t
    ctypedef struct pthread_mutex_t:
        pass

    int pthread_create(pthread_t *thread, void *attr,void *(*start_routine)(void*), void *arg)
    int pthread_join(pthread_t, void **)
   
    int pthread_mutex_init(pthread_mutex_t *, void *)
    int pthread_mutex_lock(pthread_mutex_t *)
    int pthread_mutex_unlock(pthread_mutex_t *)

cdef extern from "string.h":
    char *strcpy(char *destination, char *source)

# Global Variables
cdef int hasBeenInitialized = False
cdef pthread_t eventLoopThread
cdef int continueRunning
cdef int waitForTermination = False
cdef pthread_mutex_t mutexSharedMemory
cdef pthread_mutex_t mutexSerializeRequests

# Requests to event handler thread
cdef int REQUEST_NOTHING = 0
cdef int REQUEST_CREATE = 1
cdef int REQUEST_DESTROY = 2
cdef int REQUEST_RESIZE = 3

def initialize(in_args):
    global hasBeenInitialized
    global mutexSharedMemory
    
    cdef int argc = len(in_args)
    cdef char** argv = NULL
    cdef int i

    # Initialize glut
    if (hasBeenInitialized == False):
        argv = <char **> malloc(argc*sizeof(char**)) # check for better syntax and correctness

        for i from 0 <= i < argc: 
            s = in_args[i]
            argv[i] = s

        glutInit(&argc, argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)

        free(argv) # check for correctness

    windowLinkedList.createEmptyList()
    requestLinkedList.createEmptyList()

    pthread_mutex_init(&mutexSharedMemory, NULL)

    hasBeenInitialized = True


def createWindow(char* title, int x, int y, int w, int h, int scn):      
    global mutexSharedMemory

    pthread_mutex_lock(&mutexSerializeRequests)
    pthread_mutex_lock(&mutexSharedMemory) # Protect shared memory from other threads that produce data for visualization

      
    if (windowLinkedList.size() <= 0):   
        _createEventLoopThread()   

    cdef RequestInfo* requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
    requestInfo.request = REQUEST_CREATE
    requestInfo.data = _setWindowParameters(0, title, x, y, w, h, scn)

    requestLinkedList.addLast(requestInfo)

    pthread_mutex_unlock(&mutexSharedMemory)
    
    

def destroyWindow(int id):
    global mutexSharedMemory

    pthread_mutex_lock(&mutexSerializeRequests)
    pthread_mutex_lock(&mutexSharedMemory) # Protect shared memory from other threads that produce data for visualization
   
    cdef RequestInfo* requestInfo

    if (windowLinkedList.size() > 0 and (windowLinkedList.find(id) != NULL)): 
        
        requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
         
        if (continueRunning): # The event loop thead is running and can handle the request
            requestInfo.request = REQUEST_DESTROY
            requestInfo.data = _setWindowParameters(id, "", 0, 0, 0, 0, 0)
            requestLinkedList.addLast(requestInfo)

    pthread_mutex_unlock(&mutexSharedMemory) 


def printNumWindows():
    global windowLinkedList

    print windowLinkedList.size()
         

def changeWindowSize(int id, int w, int h):
    global mutexSharedMemory

    pthread_mutex_lock(&mutexSerializeRequests)
    pthread_mutex_lock(&mutexSharedMemory) # Protect shared memory from other threads that produce data for visualization

    cdef RequestInfo* requestInfo

    if (windowLinkedList.size() > 0):
        
        requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))

        if (continueRunning): # The event loop thead is running and can handle the request
            requestInfo.request = REQUEST_RESIZE
            requestInfo.data = _setWindowParameters(id, "", 0, 0, w, h, 0) 
            requestLinkedList.addLast(requestInfo)
        
    pthread_mutex_unlock(&mutexSharedMemory)


# private c functions. They should not be called from outside this module

cdef WindowInfo* _setWindowParameters(int id, char* title, int x, int y, int w, int h, int scn):
    
    cdef WindowInfo* windowInfo = <WindowInfo*> malloc(sizeof(WindowInfo))

    windowInfo.id = id
    strcpy(windowInfo.title, title)
    windowInfo.x = x
    windowInfo.y = y
    windowInfo.w = w
    windowInfo.h = h
    windowInfo.initRendering = trialDraw.initRendering
    windowInfo.handleResize = trialDraw.handleResize
    windowInfo.handleKeypress = trialDraw.handleKeypress
    if (scn == 1):
        windowInfo.drawScene = trialDraw.drawScene1
    else: 
        windowInfo.drawScene = trialDraw.drawScene2 
    windowInfo.update = trialDraw.update

    return windowInfo

cdef void _createEventLoopThread():
    global eventLoopThread
    global waitForTermination

    if (waitForTermination == True):
        pthread_join(eventLoopThread, NULL)
        waitForTermination = False

    cdef int thread_args = 0  
    waitForTermination = pthread_create(&eventLoopThread, NULL, TaskCode, <void *> &thread_args)


cdef void *TaskCode(void *argument):
    global continueRunning
    global mutexSharedMemory
   
    cdef RequestInfo* requestInfo
    cdef WindowInfo* windowInfo

    continueRunning = True

    while (continueRunning):
        if (requestLinkedList.size() > 0):  # handle drawing and window management requests
            pthread_mutex_lock(&mutexSharedMemory) 
 
            requestInfo = requestLinkedList.removeFirst()
            if (requestInfo != NULL):  
                windowInfo = requestInfo.data

                if (requestInfo.request == REQUEST_CREATE):
                    _createWindow(windowInfo)
                elif (requestInfo.request == REQUEST_DESTROY):
                    _sendDestroyMessageToWindow(windowInfo.id)
                elif (requestInfo.request == REQUEST_RESIZE):
                    _changeWindowSize(windowInfo.id, windowInfo.w, windowInfo.h)
            
                if (requestInfo.request != REQUEST_CREATE):
                    free(windowInfo)
                free(requestInfo) 
                pthread_mutex_unlock(&mutexSerializeRequests) 

            pthread_mutex_unlock(&mutexSharedMemory)
            
        glutMainLoopEvent()  # dispatch events
 

    pthread_mutex_lock(&mutexSharedMemory)
    requestLinkedList.makeEmpty()
    pthread_mutex_unlock(&mutexSharedMemory) 

    # To drain the event loop before the thread terminates 
    cdef int i
    for i from 0 <= i < 1000:
        glutMainLoopEvent()

    return NULL


cdef void _createWindow(WindowInfo* windowInfo):

    glutInitWindowSize(windowInfo.w, windowInfo.h)
    glutInitWindowPosition(windowInfo.x, windowInfo.y)

    windowInfo.id = glutCreateWindow(windowInfo.title)
    windowLinkedList.addFirst(windowInfo)

    windowInfo.initRendering()
            
    # Set handler functions
    if (windowInfo.handleResize):
        glutReshapeFunc(windowInfo.handleResize)
    if (windowInfo.handleKeypress):
        glutKeyboardFunc(windowInfo.handleKeypress)
    if (windowInfo.drawScene != NULL):
        glutDisplayFunc(windowInfo.drawScene)
    if (windowInfo.update != NULL):
        if (windowLinkedList.size() == 1):
            glutTimerFunc(25, windowInfo.update, 1) # Add a timer 

    glutCloseFunc(_close)
             

cdef void _sendDestroyMessageToWindow(int id):

    if (windowLinkedList.size() > 0): 
        if (windowLinkedList.find(id) != NULL):  
            glutDestroyWindow(id)
            

cdef void _close():
    global continueRunning
    global mutexSharedMemory 

    cdef int id
    cdef WindowInfo* windowInfo

    if (windowLinkedList.size() > 0):
        id = glutGetWindow()
        windowInfo = windowLinkedList.remove(id) 
        if (windowInfo != NULL):  
            free(windowInfo)   
            if (windowLinkedList.size() == 0):
                continueRunning = False
     

cdef void _changeWindowSize(int id, int w, int h):
    if (windowLinkedList.find(id) != NULL):
        glutSetWindow(id)
        glutReshapeWindow(w, h)    

         
