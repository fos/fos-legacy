from FosWindow cimport FosWindow

cdef class Manager:
   cdef list windowList
   cdef list requestList

   cdef void _createEventLoopThread(self)

cdef void _sendDestroyMessageToWindow(FosWindow fosWindow, Manager manager)
cdef void _lockMutexWindowList()
cdef void _unlockMutexWindowList()
cdef FosWindow _findFosWindow(int id, Manager manager)
cdef Manager _getManager()




