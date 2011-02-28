cimport nbglutManager
from nbglutManager cimport WindowInfo

cimport windowLinkedList
cimport requestLinkedList
cimport trialDraw

# Global Variables
cdef int hasBeenInitialized = False
cdef pthread_t eventLoopThread
cdef int continueRunning
cdef int waitForTermination = False
cdef pthread_mutex_t mutexRequest
cdef pthread_mutex_t mutexSharedMemory
cdef pthread_cond_t noWindowsCondition

# Requests to event handler thread
cdef int REQUEST_NOTHING = 0
cdef int REQUEST_CREATE = 1
cdef int REQUEST_DESTROY = 2
cdef int REQUEST_RESIZE = 3

def initialize(in_args):
    global hasBeenInitialized
    global mutexSharedMemory
    global noWindowsCondition
    global windowLinkedList
    global requestLinkedList
    
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

    pthread_mutex_init(&mutexRequest, NULL)
    pthread_mutex_init(&mutexSharedMemory, NULL)
    pthread_cond_init(&noWindowsCondition, NULL)

    hasBeenInitialized = True
    
def destroy():
    global mutexSharedMemory
    global noWindowsCondition
    global mutexRequest 
    global requestLinkedList

    requestLinkedList.makeEmpty()

    terminateEventLoopThread()
    pthread_mutex_destroy(&mutexRequest)
    pthread_mutex_destroy(&mutexSharedMemory)
    pthread_cond_destroy(&noWindowsCondition)
    

def createEventLoopThread():
    global mutexSharedMemory
    global windowLinkedList

    pthread_mutex_lock(&mutexSharedMemory) # Protect shared memory from other threads
  
    if (windowLinkedList.size() <= 0):   
        _createEventLoopThread()

    pthread_mutex_unlock(&mutexSharedMemory)

def terminateEventLoopThread():
    global continueRunning
    global noWindowsCondition
    global eventLoopThread 
    global windowLinkedList

    closeAllWindows()
    while(windowLinkedList.size() > 0):
        pass

    pthread_mutex_lock(&mutexSharedMemory)
    continueRunning = False
    pthread_mutex_unlock(&mutexSharedMemory)
    pthread_cond_signal(&noWindowsCondition)    
    #pthread_detach(eventLoopThread)
    pthread_join(eventLoopThread, NULL)


def openWindow(char* title, int x, int y, int w, int h, int scn):  
    global mutexRequest    
    global noWindowsCondition
    global requestLinkedList

         
    cdef RequestInfo* requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
    requestInfo.request = REQUEST_CREATE
    requestInfo.data = _setWindowParameters(0, title, x, y, w, h, scn)

    pthread_mutex_lock(&mutexRequest) 
    requestLinkedList.addLast(requestInfo)
    pthread_mutex_unlock(&mutexRequest)

    pthread_cond_signal(&noWindowsCondition)
    
    

def closeWindow(int id):
    global mutexRequest
    global mutexSharedMemory
    global requestLinkedList

    pthread_mutex_lock(&mutexSharedMemory) # Protect shared memory from other threads that produce data for visualization
    cdef int idExists = (windowLinkedList.size() > 0) and (windowLinkedList.find(id) != NULL)   
    pthread_mutex_unlock(&mutexSharedMemory)

    cdef RequestInfo* requestInfo

    if (idExists): 
        
        requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
         
        requestInfo.request = REQUEST_DESTROY
        requestInfo.data = _setWindowParameters(id, "", 0, 0, 0, 0, 0)
        
        pthread_mutex_lock(&mutexRequest)
        requestLinkedList.addLast(requestInfo)
        pthread_mutex_unlock(&mutexRequest) 


def closeAllWindows():
    global mutexRequest
    global requestLinkedList
    global windowLinkedList

    cdef RequestInfo* requestInfo

    pthread_mutex_lock(&mutexSharedMemory)
    cdef WindowInfo* windowInfo = windowLinkedList.first()
    pthread_mutex_unlock(&mutexSharedMemory)   

    while(windowInfo != NULL):
        requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
         
        requestInfo.request = REQUEST_DESTROY
        requestInfo.data = _setWindowParameters(windowInfo.id, "", 0, 0, 0, 0, 0)
        pthread_mutex_lock(&mutexRequest)
        requestLinkedList.addLast(requestInfo)
        pthread_mutex_unlock(&mutexRequest) 

        pthread_mutex_lock(&mutexSharedMemory)
        windowInfo = windowLinkedList.next()
        pthread_mutex_unlock(&mutexSharedMemory)   
        
    

    

def printNumWindows():
    global windowLinkedList

    print windowLinkedList.size()
         

def changeWindowSize(int id, int w, int h):
    global mutexRequest
    global mutexSharedMemory
    global requestLinkedList

    pthread_mutex_lock(&mutexSharedMemory) # Protect shared memory from other threads that produce data for visualization
    cdef int idExists = (windowLinkedList.size() > 0) and (windowLinkedList.find(id) != NULL) 
    pthread_mutex_unlock(&mutexSharedMemory)

    cdef RequestInfo* requestInfo

    if (idExists):
        requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))

        requestInfo.request = REQUEST_RESIZE
        requestInfo.data = _setWindowParameters(id, "", 0, 0, w, h, 0) 

        pthread_mutex_lock(&mutexRequest)
        requestLinkedList.addLast(requestInfo)
        pthread_mutex_unlock(&mutexRequest)
        
    


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

    cdef int thread_args = 0  
    pthread_create(&eventLoopThread, NULL, TaskCode, <void *> &thread_args)


cdef void *TaskCode(void *argument):
    global continueRunning
    global mutexRequest
    global mutexSharedMemory
    global noWindowsCondition
    global requestLinkedList
    global windowLinkedList
   
    cdef RequestInfo* requestInfo
    cdef WindowInfo* windowInfo

    cdef int i 

    continueRunning = True

    while (continueRunning):
        # First, handle drawing and window management requests
        if (requestLinkedList.size() > 0): 
            pthread_mutex_lock(&mutexRequest) 
            requestInfo = requestLinkedList.removeFirst()
            pthread_mutex_unlock(&mutexRequest)

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
            
        for i from 0 <= i < 5:
            glutMainLoopEvent()  # dispatch events

        if (windowLinkedList.size() <= 0):
            # To drain the event loop before the thread terminates 
            for i from 0 <= i < 2000:
                glutMainLoopEvent()
            pthread_mutex_lock(&mutexSharedMemory)  
            if ((windowLinkedList.size() <= 0) and continueRunning):  
                pthread_cond_wait(&noWindowsCondition, &mutexSharedMemory)
            pthread_mutex_unlock(&mutexSharedMemory) 
 

    pthread_mutex_lock(&mutexRequest)
    requestLinkedList.makeEmpty()
    pthread_mutex_unlock(&mutexRequest) 

    # To drain the event loop before the thread terminates 
    for i from 0 <= i < 2000:
        glutMainLoopEvent()

    return NULL


cdef void _createWindow(WindowInfo* windowInfo):
    global mutexSharedMemory

    glutInitWindowSize(windowInfo.w, windowInfo.h)
    glutInitWindowPosition(windowInfo.x, windowInfo.y)

    windowInfo.id = glutCreateWindow(windowInfo.title)
    pthread_mutex_lock(&mutexSharedMemory)  
    windowLinkedList.addFirst(windowInfo)
    pthread_mutex_unlock(&mutexSharedMemory)  

    windowInfo.initRendering()
            
    # Set handler functions
    if (windowInfo.handleResize):
        glutReshapeFunc(windowInfo.handleResize)
    if (windowInfo.handleKeypress):
        glutKeyboardFunc(windowInfo.handleKeypress)
    if (windowInfo.drawScene != NULL):
        glutDisplayFunc(windowInfo.drawScene)
    if (windowInfo.update != NULL):
        pthread_mutex_lock(&mutexSharedMemory)  
        if (windowLinkedList.size() == 1):
            glutTimerFunc(25, windowInfo.update, 1) # Add a timer 
        pthread_mutex_unlock(&mutexSharedMemory)  

    glutCloseFunc(_close)
             

cdef void _sendDestroyMessageToWindow(int id):
    global mutexSharedMemory

    pthread_mutex_lock(&mutexSharedMemory)  
    cdef int idExists = (windowLinkedList.size() > 0) and (windowLinkedList.find(id) != NULL)
    pthread_mutex_unlock(&mutexSharedMemory)  

    if (idExists): 
        pthread_mutex_lock(&mutexSharedMemory)  
        glutDestroyWindow(id)
        pthread_mutex_unlock(&mutexSharedMemory)  
            

cdef void _close():
    global mutexSharedMemory 

    cdef int id
    cdef WindowInfo* windowInfo

    pthread_mutex_lock(&mutexSharedMemory) 
    if (windowLinkedList.size() > 0):
        id = glutGetWindow()    
        windowInfo = windowLinkedList.remove(id)
        if (windowInfo != NULL):  
            free(windowInfo)   
    pthread_mutex_unlock(&mutexSharedMemory)
           
     

cdef void _changeWindowSize(int id, int w, int h):
    global mutexSharedMemory 

    pthread_mutex_lock(&mutexSharedMemory) 
    if (windowLinkedList.find(id) != NULL):
        glutSetWindow(id)
        glutReshapeWindow(w, h)    
    pthread_mutex_unlock(&mutexSharedMemory) 

         
cdef void _lockMutexSharedMemory():
    global mutexSharedMemory

    pthread_mutex_lock(&mutexSharedMemory) 


cdef void _unlockMutexSharedMemory():
    global mutexSharedMemory

    pthread_mutex_unlock(&mutexSharedMemory) 
    

