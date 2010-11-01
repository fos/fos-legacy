import numpy as np
from ctypes import c_void_p
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
        self.triangle_vertices2 = self.triangle_vertices + np.array( [100,0,0], dtype = np.float32)
        
        self.tri_vertex_array = np.vstack( (self.triangle_vertices, self.triangle_vertices2) )
        self.tri_vertex_array_ptr = self.tri_vertex_array.ctypes.data 
        
#        self.tri_vert_ptr = self.triangle_vertices.ctypes.data
        self.triangle_face = np.array( [[0,1,2]], dtype = np.uint32)
        self.tri_face_ptr = self.triangle_face.ctypes.data
        
#        self.tri_vert_ptr2 = self.triangle_vertices2.ctypes.data
        self.triangle_face2 = np.array( [[0,1,2]], dtype = np.uint32)
        self.tri_face_ptr2 = self.triangle_face2.ctypes.data
        
        # GLsizei which is ctypes.c_int
        self.count_arr_ptr = np.array( [3,3], dtype = np.int32).ctypes.data
        

        
        index = np.vstack( (self.triangle_face, self.triangle_face2) )
        index = index.astype(np.uint32)
        
        iptr = ctypes.POINTER(ctypes.c_uint32)
        print "len index", len(index)
        self.index_ptr = (iptr*len(index))(*[row.ctypes.data_as(iptr) for row in index])
        print "last value", self.index_ptr[1][2]
        
        
    def draw(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glPushMatrix()
#        glTranslatef()
#        glMultMatrixf()
        glVertexPointer(3, GL_FLOAT, 0, self.tri_vertex_array_ptr)
        
#        glColorPointer(4, GL_UNSIGNED_BYTE, 0, glyph.glcolors)
#        glNormalPointer(GL_FLOAT, 0, glyph.glnormals)
        
        glMultiDrawElements(GL_TRIANGLE, self.count_arr_ptr, GL_UNSIGNED_INT, self.index_ptr, 2)
        glPopMatrix()
        glDisableClientState(GL_VERTEX_ARRAY)
        
#        glMultiDrawElements(
#            GL_TRIANGLE, # primitive type
#            self.count_arr_ptr, # count is an array of how many vertices are found in 
#            #                   # each respective array element list
#            GL_UNSIGNED_INT, # type (data type) the same as they are in glDrawElements, indicating the data type of the indices array
#            self.index_ptr, # indices is an array of pointers to lists of array elements
#            2) # calls a sequence of primecount (a number of) glDrawElements commands
         

    def draw_elements(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glPushMatrix()
        glVertexPointer(3, GL_FLOAT, 0, self.tri_vert_ptr)

        glDrawElements(
            GL_TRIANGLES,
            3,
            GL_UNSIGNED_BYTE,
            self.tri_face_ptr)
        
        glPopMatrix()
        glDisableClientState(GL_VERTEX_ARRAY)    
                                       
    
    def update(self, dt):
        pass