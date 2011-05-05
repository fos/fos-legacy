from freeglutHeaders cimport *
cimport nbglutManager
import numpy as np
cimport numpy as cnp

from FosWindow cimport FosWindow, reshapeFunc, keyboardFunc, displayFunc, update

from RequestInfo cimport RequestInfo

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void *malloc(size_t size)
    void free(void *pointer)

cdef extern from "pthread.h":
    ctypedef void *pthread_t
    ctypedef union pthread_mutex_t:
        pass

    ctypedef union pthread_cond_t:
        pass

    ctypedef union pthread_condattr_t:
        pass 

    int pthread_create(pthread_t *thread, void *attr, void *(*start_routine)(void*), void *arg)
    int pthread_join(pthread_t, void **)
    int pthread_detach(pthread_t thread)
   
    int pthread_mutex_init(pthread_mutex_t *, void *)
    int pthread_mutex_destroy(pthread_mutex_t *mutex)
    int pthread_mutex_lock(pthread_mutex_t *)
    int pthread_mutex_unlock(pthread_mutex_t *)

    int pthread_cond_init(pthread_cond_t *cond, pthread_condattr_t *attr)
    int pthread_cond_destroy(pthread_cond_t *cond)
    int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex)
    int pthread_cond_signal(pthread_cond_t *cond)

cdef extern from "string.h":
    char *strcpy(char *destination, char *source)

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
cdef Manager managerPtr

# Requests to event handler thread
cdef int REQUEST_NOTHING = 0
cdef int REQUEST_CREATE = 1
cdef int REQUEST_DESTROY = 2
cdef int REQUEST_RESIZE = 3

cdef class Manager:

    def __init__(self):
        self.windowList = []
        self.requestList = []

    def initialize(self, in_args):
        global mutexWindowList
        global mutexRequestList
        global conditionNoOpenWindows
        global gl_initialized
        global thread_initialized
    
        cdef int argc = 0
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
            self.windowList = []
            self.requestList = []
           
            pthread_mutex_init(&mutexRequestList, NULL)
            pthread_mutex_init(&mutexWindowList, NULL)
            pthread_cond_init(&conditionNoOpenWindows, NULL)
            
            self._createEventLoopThread()
    
            thread_initialized = True
            

    
    def destroy(self):
        global mutexRequestList
        global mutexWindowList
        global conditionNoOpenWindows
        global thread_initialized
        global eventLoopThread 
        global continueRunning

        if (thread_initialized): 
            flag = 1

            while(flag): # busy wait until all requests have been considered.
                pthread_mutex_lock(&mutexRequestList)
                flag = len(self.requestList) > 0
                pthread_mutex_unlock(&mutexRequestList) 

            self.closeAllWindows()

            flag = 1

            while(flag): # busy wait until all windows have been closed.
                pthread_mutex_lock(&mutexWindowList)
                flag = len(self.windowList) > 0
                pthread_mutex_unlock(&mutexWindowList) 

            continueRunning = False

            pthread_cond_signal(&conditionNoOpenWindows)    
            pthread_join(eventLoopThread, NULL)

            pthread_mutex_destroy(&mutexRequestList)
            pthread_mutex_destroy(&mutexWindowList)
            pthread_cond_destroy(&conditionNoOpenWindows)
         
            thread_initialized = False
    


    #def openWindow(self, FosWindow fosWindow):  
    def openWindow(self, char* title, int x, int y, int w, int h):
        global mutexRequestList    
        global conditionNoOpenWindows
        global lastCreatedWindowID

        if (thread_initialized == False):
            print "The window manager is not initialized"  
            return -1
         
        cdef FosWindow fosWindow = FosWindow()
        strcpy(fosWindow.title, title)
        fosWindow.x = x
        fosWindow.y = y
        fosWindow.w = w
        fosWindow.h = h

        cdef RequestInfo requestInfo = RequestInfo()
        requestInfo.request = REQUEST_CREATE
        requestInfo.fosWindow = fosWindow

        pthread_mutex_lock(&mutexRequestList) 
        self.requestList.append(requestInfo)
        pthread_mutex_unlock(&mutexRequestList)

        pthread_cond_signal(&conditionNoOpenWindows)

        lastCreatedWindowID += 1

        return lastCreatedWindowID
    
    
    def closeWindow(self, int id):
        global mutexRequestList
        global mutexWindowList

        if (thread_initialized == False):
            print "The window manager is not initialized"  
            return -1

        pthread_mutex_lock(&mutexWindowList) 
        cdef FosWindow fosWindow = _findFosWindow(id, self)   
        pthread_mutex_unlock(&mutexWindowList)  

        if (fosWindow == None):
            return

        cdef RequestInfo requestInfo = RequestInfo()
         
        requestInfo.request = REQUEST_DESTROY
        requestInfo.fosWindow = fosWindow
        
        pthread_mutex_lock(&mutexRequestList)
        self.requestList.append(requestInfo)
        pthread_mutex_unlock(&mutexRequestList) 


    def closeAllWindows(self):
        global mutexRequestList
        global mutexWindowList
    
        if (thread_initialized == False):
            print "The window manager is not initialized"  
            return -1

        cdef RequestInfo requestInfo

        pthread_mutex_lock(&mutexWindowList)
    
        for i from 0 <= i < len(self.windowList):
            requestInfo = RequestInfo()
         
            requestInfo.request = REQUEST_DESTROY
            requestInfo.fosWindow = self.windowList[i]
            pthread_mutex_lock(&mutexRequestList)
            self.requestList.append(requestInfo)
            pthread_mutex_unlock(&mutexRequestList) 
       
        pthread_mutex_unlock(&mutexWindowList)   
         

    def printNumWindows(self):

        print len(self.windowList)

    def printNumRequests(self):
        print len(self.requestList)
         

    def reshapeWindow(self, int id, int w, int h):
        global mutexRequestList
        global mutexWindowList

        if (thread_initialized == False):
            print "The window manager is not initialized"  
            return -1

        pthread_mutex_lock(&mutexWindowList) 
        cdef FosWindow fosWindow = _findFosWindow(id, self)    
        pthread_mutex_unlock(&mutexWindowList)  
        if (fosWindow == None):
            return -1

        fosWindow.w = w
        fosWindow.h = h

        cdef RequestInfo requestInfo = RequestInfo()
        requestInfo.request = REQUEST_RESIZE
        requestInfo.fosWindow = fosWindow

        pthread_mutex_lock(&mutexRequestList)
        self.requestList.append(requestInfo)
        pthread_mutex_unlock(&mutexRequestList)
        

    # private functions. They should not be called from outside this module

    cdef void _createEventLoopThread(self):
        global eventLoopThread

        cdef void* thread_args = <void*> self  
        pthread_create(&eventLoopThread, NULL, TaskCode, thread_args)



cdef void *TaskCode(void *arguments):
    global mutexRequestList
    global mutexWindowList
    global continueRunning
    global conditionNoOpenWindows  
    global managerPtr  
     
    cdef Manager manager = <Manager> arguments 
    cdef RequestInfo requestInfo
    cdef FosWindow fosWindow
    cdef int i 

    managerPtr = manager

    continueRunning = True

    while (continueRunning):
        # First, handle drawing and window management requests
        if (len(manager.requestList) > 0):
            pthread_mutex_lock(&mutexRequestList) 
            requestInfo = manager.requestList.pop(0)
            pthread_mutex_unlock(&mutexRequestList)
            
            fosWindow = requestInfo.fosWindow
            if (requestInfo.request == REQUEST_CREATE):
                _createWindow(fosWindow, manager)
            elif (requestInfo.request == REQUEST_DESTROY):
                _sendDestroyMessageToWindow(fosWindow, manager)
            elif (requestInfo.request == REQUEST_RESIZE):
                _reshapeWindow(fosWindow, manager)    
             
        for i from 0 <= i < 2:
            glutMainLoopEvent()  # dispatch events
        '''
        if ((len(manager.windowList) <= 0) and (len(manager.requestList) <= 0)):
            # To drain the event loop before the thread waits on condition variable 
            for i from 0 <= i < 5000:
                glutMainLoopEvent()

            pthread_mutex_lock(&mutexWindowList)
            if ((len(manager.windowList.size) <= 0) and (len(manager.requestList) <= 0) and continueRunning):  
                pthread_cond_wait(&conditionNoOpenWindows, &mutexWindowList)
            pthread_mutex_unlock(&mutexWindowList) 
        '''
        
    # To drain the event loop before the thread terminates 
    for i from 0 <= i < 5000:
        glutMainLoopEvent()

    return NULL


cdef void _createWindow(FosWindow fosWindow, Manager manager):
    global mutexWindowList

    glutInitWindowSize(fosWindow.w, fosWindow.h)
    glutInitWindowPosition(fosWindow.x, fosWindow.y)

    fosWindow.id = glutCreateWindow(fosWindow.title)
    pthread_mutex_lock(&mutexWindowList)  
    manager.windowList.insert(0,fosWindow)
    pthread_mutex_unlock(&mutexWindowList)  

    fosWindow.setup()
           
    # Set handler functions
    glutReshapeFunc(reshapeFunc)
    #glutKeyboardFunc(keyboardFunc)
    glutDisplayFunc(displayFunc)
    #pthread_mutex_lock(&mutexWindowList)  
    #if (len(manager.windowList) == 1):
    #    glutTimerFunc(50, update, 50) # Add a timer 
    #pthread_mutex_unlock(&mutexWindowList)  

    glutCloseFunc(_close)
        
   

cdef void _sendDestroyMessageToWindow(FosWindow fosWindow, Manager manager):
    global mutexWindowList

    cdef int id = fosWindow.id

    pthread_mutex_lock(&mutexWindowList)  
    cdef int idExists = (_findFosWindow(id, manager) != None)
    pthread_mutex_unlock(&mutexWindowList)  

    if (idExists): 
        glutDestroyWindow(id) 
            

cdef void _close():
    global mutexWindowList 
    global managerPtr

    cdef int id
    cdef FosWindow fosWindow

    pthread_mutex_lock(&mutexWindowList) 
    if (len(managerPtr.windowList) > 0):
        id = glutGetWindow()    
        fosWindow = _findFosWindow(id, managerPtr)
        if (fosWindow != None):  
            managerPtr.windowList.remove(fosWindow)   
    pthread_mutex_unlock(&mutexWindowList)
           
     

cdef void _reshapeWindow(FosWindow fosWindow, Manager manager):
    global mutexWindowList

    pthread_mutex_lock(&mutexWindowList)  
    cdef int idExists = (_findFosWindow(fosWindow.id, manager) != None)

    if (idExists):
        glutSetWindow(fosWindow.id)
        glutReshapeWindow(fosWindow.w, fosWindow.h)    
    pthread_mutex_unlock(&mutexWindowList) 

         
cdef void _lockMutexWindowList():
    global mutexWindowList

    pthread_mutex_lock(&mutexWindowList) 


cdef void _unlockMutexWindowList():
    global mutexWindowList

    pthread_mutex_unlock(&mutexWindowList) 
    

cdef FosWindow _findFosWindow(int id, Manager manager):
    cdef int i

    cdef FosWindow fosWindow

    for i from 0 <= i < len(manager.windowList):
        fosWindow = manager.windowList[i]
        if (fosWindow.id == id):
            return fosWindow

    return None 

cdef Manager _getManager():
    return managerPtr
