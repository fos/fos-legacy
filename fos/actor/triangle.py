import numpy as np
from ctypes import c_void_p, cast, POINTER, c_int32, c_int

import ctypes

from fos.lib.pyglet.gl import *
from fos.core.actor import Actor

type_to_enum = {
    GLubyte: GL_UNSIGNED_BYTE,
    GLushort: GL_UNSIGNED_SHORT,
    GLuint: GL_UNSIGNED_INT,
}

class Triangle(Actor):
    
    def __init__(self):
        
        self.triangle_vertices = np.array( [[0,100,-1], [-100,-100,-1], [100,-100,-1] ], dtype = np.float32 )
        self.triangle_vertices2 = self.triangle_vertices + np.array( [200,0,0], dtype = np.float32)
        
        self.tri_vertex_array = np.vstack( (self.triangle_vertices, self.triangle_vertices2) )
        self.tri_vertex_array_ptr = self.tri_vertex_array.ctypes.data 
        
        self.tri_vert_ptr = self.triangle_vertices.ctypes.data
        self.tri_vert_ptr2 = self.triangle_vertices2.ctypes.data

        self.triangle_face = np.array( [[0,1,2],[3,4,5]], dtype = np.uint32)
        self.tri_face_ptr = self.triangle_face.ctypes.data
        self.triangle_face2 = np.array( [[3,4,5]], dtype = np.uint32)
        self.tri_face_ptr2 = self.triangle_face2.ctypes.data

    
    def draw(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.tri_vertex_array_ptr)
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,self.tri_face_ptr)
        glDisableClientState(GL_VERTEX_ARRAY)   
        
    def old_init(self):
        self.vertices = np.array( [[0,100,-1], [-100,-100,-1], [100,-100,-1] ], dtype = np.float32 )
        self.vertices_ptr = self.vertices.ctypes.data
        
        self.face = np.array( [[0,1,2]], dtype = np.uint)
        self.sizes = np.array( [[3,3]], dtype = GLsizei)
        
        self.sizes_ptr = self.sizes.ctypes.data_as( POINTER(GLsizei) )
        self.face_ptr = self.face.ctypes.data
        
#        f4ptr = POINTER(c_float)
#        data = (f4ptr*len(x))(*[row.ctypes.data_as(f4ptr) for row in x])

#        f4ptr = POINTER(c_float)
#        self.starts_dbl_ptr = (f4ptr*len(self.vertices))(*[row.ctypes.data_as(f4ptr) for row in self.vertices])

        # the pyglet way
        self.primcount = 2
        self.mode = GL_TRIANGLES
    def draw_multi(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices_ptr)
        glMultiDrawElements(self.mode, self.sizes_ptr, GL_UNSIGNED_INT, self.starts_dbl_ptr, self.primcount)
        glDisableClientState(GL_VERTEX_ARRAY)
        
        
    def draw_test(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
#        glPushMatrix()
#        glTranslatef()
#        glMultMatrixf()
        
        

#        glColorPointer(4, GL_UNSIGNED_BYTE, 0, glyph.glcolors)
#        glNormalPointer(GL_FLOAT, 0, glyph.glnormals)
        glMultiDrawElements.restype  = ctypes.c_void_p
        glMultiDrawElements.argtypes = [ctypes.c_int32,
                                        ctypes.c_int32 * self.primcount,
                                        ctypes.c_int32,
                                        ctypes.POINTER(ctypes.c_int)*self.primecount,
                                        ctypes.c_int32]

        glMultiDrawElements(self.mode, self.sizes, GL_UNSIGNED_INT, self.starts, self.primcount)
        
#        glMultiDrawElements(GL_TRIANGLE, self.count_arr_ptr, GL_UNSIGNED_INT, self.index_ptr, 2)
#        glPopMatrix()
        glDisableClientState(GL_VERTEX_ARRAY)
        
        
#        glMultiDrawElements(
#            GL_TRIANGLE, # primitive type
#            self.count_arr_ptr, # count is an array of how many vertices are found in 
#            #                   # each respective array element list
#            GL_UNSIGNED_INT, # type (data type) the same as they are in glDrawElements, indicating the data type of the indices array
#            self.index_ptr, # indices is an array of pointers to lists of array elements
#            2) # calls a sequence of primecount (a number of) glDrawElements commands
         

    def draw_test2(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
#        glPushMatrix()
        glVertexPointer(3, GL_FLOAT, 0, self.tri_vert_ptr)

        glDrawElements(
            GL_TRIANGLES,
            3,
            GL_UNSIGNED_INT,
            self.tri_face_ptr)
        
#        glPopMatrix()
        glDisableClientState(GL_VERTEX_ARRAY)    
                                       
    
    def update(self, dt):
        pass