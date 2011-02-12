cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void *malloc(size_t size)
    void free(void *pointer)

cdef extern from "pthread.h":
    ctypedef void *pthread_t
    int pthread_create(pthread_t *thread, void *attr,void *(*start_routine)(void*), void *arg)
    int pthread_join(pthread_t, void **)
    

cdef extern from "GL/freeglut.h":
    ctypedef unsigned int GLenum
    int GLUT_DOUBLE
    int GLUT_RGB
    int GLUT_DEPTH 
    int GLUT_ACTION_ON_WINDOW_CLOSE
    int GLUT_ACTION_CONTINUE_EXECUTION
    void glutInit(int *argcp, char **argv)
    void glutInitDisplayMode(unsigned int mode)
    void glutSetOption(GLenum eWhat, int value)   
    void glutCloseFunc(void(*callback)()) 

cdef extern from "displayWindow.h":
    void setWindowParameters(int id, char* title, int x, int y, int w, int h, int scn)
    void _createWindow()
    void _destroyWindow() 
    void _destroyWindow2(int id)
    void _changeWindowSize(int id, int w, int h)
    int getNumOpenWindows()
    int getChangeRequest()
    void setChangeRequest(int value)
    void setRequest(int value)
    void *TaskCode(void *argument)
    int createEventLoopThread()
    int REQUEST_NOTHING
    int REQUEST_CREATE
    int REQUEST_DESTROY
    int REQUEST_RESIZE

cdef class GLWindowManager:
    
    def __cinit__(self, in_args):

        cdef int argc = len(in_args)
        cdef char** argv = NULL
        cdef int i

        argv = <char **> malloc(argc*sizeof(char**)) # check for better syntax and correctness

        for i from 0 <= i < argc: 
            s = in_args[i]
            argv[i] = s

        # Initialize 
        glutInit(&argc, argv)

        free(argv) # check for correctness

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)
 

    def createWindow(self, title):
        cdef int thread_args = 0
        cdef int rc
        
        if (getNumOpenWindows() <= 0):   
            setWindowParameters(0, title, 10, 10, 300, 300, 1) 
            createEventLoopThread()   
        else : 
            while (getChangeRequest() == 1):
                pass

            setWindowParameters(0, title, getNumOpenWindows()*300 + 10, 10, 300, 300, 2) 
            setRequest(REQUEST_CREATE)
            setChangeRequest(1)

 
    def destroyWindow(self, int id):
        while (getChangeRequest() == 1):
                pass

        setWindowParameters(id, "", 0, 0, 0, 0, 2); 
        setRequest(REQUEST_DESTROY)
        setChangeRequest(1)


    def printNumWindows(self):
        print getNumOpenWindows()
         

    def changeWindowSize(self, int id, int w, int h):
        while (getChangeRequest() == 1):
                pass

        setWindowParameters(id, "", 0, 0, w, h, 2); 
        setRequest(REQUEST_RESIZE)
        setChangeRequest(1)
    







