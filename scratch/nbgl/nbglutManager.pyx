cimport nbglutManager
from nbglutManager cimport WindowInfo

cimport windowLinkedList
cimport requestLinkedList
cimport trialDraw

# Global Variables
cdef int gl_initialized = False
cdef int thread_initialized = False
cdef pthread_t eventLoopThread
cdef int continueRunning
cdef int waitForTermination = False
cdef int lastCreatedWindowID = 0
cdef pthread_mutex_t mutexRequestList
cdef pthread_mutex_t mutexWindowList
cdef pthread_cond_t conditionNoOpenWindows

# Requests to event handler thread
cdef int REQUEST_NOTHING = 0
cdef int REQUEST_CREATE = 1
cdef int REQUEST_DESTROY = 2
cdef int REQUEST_RESIZE = 3

def initialize(in_args):
    global mutexWindowList
    global conditionNoOpenWindows
    global gl_initialized
    global thread_initialized
    global windowLinkedList
    global requestLinkedList
    
    cdef int argc = len(in_args)
    cdef char** argv = NULL
    cdef int i

    # Initialize glut
    if (gl_initialized == False):
        argv = <char **> malloc(argc*sizeof(char**)) # check for better syntax and correctness

        for i from 0 <= i < argc: 
            s = in_args[i]
            argv[i] = s

        glutInit(&argc, argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)

        free(argv) # check for correctness

        gl_initialized = True 

    if (thread_initialized == False):
        windowLinkedList.create()
        requestLinkedList.create()

        pthread_mutex_init(&mutexRequestList, NULL)
        pthread_mutex_init(&mutexWindowList, NULL)
        pthread_cond_init(&conditionNoOpenWindows, NULL)

        _createEventLoopThread()
    
        thread_initialized = True
    
def destroy():
    global mutexWindowList
    global mutexRequestList 
    global conditionNoOpenWindows
    global thread_initialized
    global eventLoopThread 
    global windowLinkedList
    global requestLinkedList
    global continueRunning

    if (thread_initialized): 
        flag = 1

        while(flag): # busy wait until all requests have been considered.
            pthread_mutex_lock(&mutexRequestList)
            flag = requestLinkedList.size() > 0
            pthread_mutex_unlock(&mutexRequestList) 


        closeAllWindows()

        flag = 1

        while(flag): # busy wait until all windows have been closed.
            pthread_mutex_lock(&mutexWindowList)
            flag = (windowLinkedList.size() > 0)
            pthread_mutex_unlock(&mutexWindowList) 

        continueRunning = False

        pthread_cond_signal(&conditionNoOpenWindows)    
        pthread_join(eventLoopThread, NULL)

        requestLinkedList.destroy()
        windowLinkedList.destroy()

        pthread_mutex_destroy(&mutexRequestList)
        pthread_mutex_destroy(&mutexWindowList)
        pthread_cond_destroy(&conditionNoOpenWindows)
         
        thread_initialized = False
    


def openWindow(char* title, int x, int y, int w, int h, int scn):  
    global mutexRequestList    
    global conditionNoOpenWindows
    global requestLinkedList
    global lastCreatedWindowID

         
    cdef RequestInfo* requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
    requestInfo.request = REQUEST_CREATE
    requestInfo.data = _setWindowParameters(0, title, x, y, w, h, scn)

    pthread_mutex_lock(&mutexRequestList) 
    requestLinkedList.addLast(requestInfo)
    pthread_mutex_unlock(&mutexRequestList)

    pthread_cond_signal(&conditionNoOpenWindows)

    lastCreatedWindowID += 1

    return lastCreatedWindowID
    
    

def closeWindow(int id):
    global mutexRequestList
    global requestLinkedList


    cdef RequestInfo* requestInfo

    requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
         
    requestInfo.request = REQUEST_DESTROY
    requestInfo.data = _setWindowParameters(id, "", 0, 0, 0, 0, 0)
        
    pthread_mutex_lock(&mutexRequestList)
    requestLinkedList.addLast(requestInfo)
    pthread_mutex_unlock(&mutexRequestList) 


def closeAllWindows():
    global mutexRequestList
    global requestLinkedList
    global windowLinkedList

    cdef RequestInfo* requestInfo

    pthread_mutex_lock(&mutexWindowList)
    cdef WindowInfo* windowInfo = windowLinkedList.first()   

    while(windowInfo != NULL):
        requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))
         
        requestInfo.request = REQUEST_DESTROY
        requestInfo.data = _setWindowParameters(windowInfo.id, "", 0, 0, 0, 0, 0)
        pthread_mutex_lock(&mutexRequestList)
        requestLinkedList.addLast(requestInfo)
        pthread_mutex_unlock(&mutexRequestList) 

        windowInfo = windowLinkedList.next()
       
    pthread_mutex_unlock(&mutexWindowList)   
        
    

    

def printNumWindows():
    global windowLinkedList

    print windowLinkedList.size()
         

def changeWindowSize(int id, int w, int h):
    global mutexRequestList
    global mutexWindowList
    global requestLinkedList

    cdef RequestInfo* requestInfo

    requestInfo = <RequestInfo*> malloc(sizeof(RequestInfo))

    requestInfo.request = REQUEST_RESIZE
    requestInfo.data = _setWindowParameters(id, "", 0, 0, w, h, 0) 

    pthread_mutex_lock(&mutexRequestList)
    requestLinkedList.addLast(requestInfo)
    pthread_mutex_unlock(&mutexRequestList)
        
    


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
    global mutexRequestList
    global mutexWindowList
    global conditionNoOpenWindows
    global requestLinkedList
    global windowLinkedList
   
    cdef RequestInfo* requestInfo
    cdef WindowInfo* windowInfo

    cdef int i 

    continueRunning = True

    while (continueRunning):
        # First, handle drawing and window management requests
        if (requestLinkedList.size() > 0): 
            pthread_mutex_lock(&mutexRequestList) 
            requestInfo = requestLinkedList.removeFirst()
            pthread_mutex_unlock(&mutexRequestList)

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

        if ((windowLinkedList.size() <= 0) and (requestLinkedList.size() <= 0)):
            # To drain the event loop before the thread waits on condition variable 
            for i from 0 <= i < 5000:
                glutMainLoopEvent()
            pthread_mutex_lock(&mutexWindowList)
            #pthread_mutex_lock(&mutexRequestList)
            if ((windowLinkedList.size() <= 0) and (requestLinkedList.size() <= 0) and continueRunning):  
                pthread_cond_wait(&conditionNoOpenWindows, &mutexWindowList)
            #pthread_mutex_unlock(&mutexRequestList)
            pthread_mutex_unlock(&mutexWindowList) 
 

    pthread_mutex_lock(&mutexRequestList)
    requestLinkedList.makeEmpty()
    pthread_mutex_unlock(&mutexRequestList) 

    # To drain the event loop before the thread terminates 
    for i from 0 <= i < 5000:
        glutMainLoopEvent()

    return NULL


cdef void _createWindow(WindowInfo* windowInfo):
    global mutexWindowList

    glutInitWindowSize(windowInfo.w, windowInfo.h)
    glutInitWindowPosition(windowInfo.x, windowInfo.y)

    windowInfo.id = glutCreateWindow(windowInfo.title)
    pthread_mutex_lock(&mutexWindowList)  
    windowLinkedList.addFirst(windowInfo)
    pthread_mutex_unlock(&mutexWindowList)  

    windowInfo.initRendering()
            
    # Set handler functions
    if (windowInfo.handleResize):
        glutReshapeFunc(windowInfo.handleResize)
    if (windowInfo.handleKeypress):
        glutKeyboardFunc(windowInfo.handleKeypress)
    if (windowInfo.drawScene != NULL):
        glutDisplayFunc(windowInfo.drawScene)
    if (windowInfo.update != NULL):
        pthread_mutex_lock(&mutexWindowList)  
        if (windowLinkedList.size() == 1):
            glutTimerFunc(25, windowInfo.update, 1) # Add a timer 
        pthread_mutex_unlock(&mutexWindowList)  

    glutCloseFunc(_close)
             

cdef void _sendDestroyMessageToWindow(int id):
    global mutexWindowList

    pthread_mutex_lock(&mutexWindowList)  
    cdef int idExists = (windowLinkedList.size() > 0) and (windowLinkedList.find(id) != NULL)
    pthread_mutex_unlock(&mutexWindowList)  

    if (idExists): 
        pthread_mutex_lock(&mutexWindowList)  
        glutDestroyWindow(id)
        pthread_mutex_unlock(&mutexWindowList)  
            

cdef void _close():
    global mutexWindowList 

    cdef int id
    cdef WindowInfo* windowInfo

    pthread_mutex_lock(&mutexWindowList) 
    if (windowLinkedList.size() > 0):
        id = glutGetWindow()    
        windowInfo = windowLinkedList.remove(id)
        if (windowInfo != NULL):  
            free(windowInfo)   
    pthread_mutex_unlock(&mutexWindowList)
           
     

cdef void _changeWindowSize(int id, int w, int h):
    global mutexWindowList 

    pthread_mutex_lock(&mutexWindowList) 
    if (windowLinkedList.find(id) != NULL):
        glutSetWindow(id)
        glutReshapeWindow(w, h)    
    pthread_mutex_unlock(&mutexWindowList) 

         
cdef void _lockMutexWindowList():
    global mutexWindowList

    pthread_mutex_lock(&mutexWindowList) 


cdef void _unlockMutexWindowList():
    global mutexWindowList

    pthread_mutex_unlock(&mutexWindowList) 
    

