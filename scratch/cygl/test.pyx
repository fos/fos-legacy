# Cython's openGL definitions (can be replaced with PySoy's)
cdef extern from "GL/gl.h":
    ctypedef int           GLint
    ctypedef unsigned int  GLenum
    ctypedef float    	   GLfloat
    int GL_POINTS
    cdef void glBegin(GLenum mode)
    cdef void glEnd()
    cdef void glVertex3f(GLfloat x, GLfloat y, GLfloat z)
# End of Cython's openGL definitions


cdef int i
cdef float x
glBegin(GL_POINTS)
for i in range(10000):
    x = i/1000.
    glVertex3f(x,x,-x)
glEnd()
