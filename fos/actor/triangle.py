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
        self.tri_vert_ptr = self.triangle_vertices.ctypes.data #get the pointer        
      
        self.triangle_vertices2 = self.triangle_vertices + np.array( [100,0,0], dtype = np.float32)        
        self.tri_vertex_array = np.vstack( (self.triangle_vertices, self.triangle_vertices2) )
        self.tri_vertex_array_ptr = self.tri_vertex_array.ctypes.data 
                
        self.tri_vert_ptr = self.triangle_vertices.ctypes.data
       

        self.triangle_face = np.array( [[0,1,2]], dtype = np.uint32)
        self.tri_face_ptr = self.triangle_face.ctypes.data        
        
#        self.tri_vert_ptr2 = self.triangle_vertices2.ctypes.data
        self.triangle_face2 = np.array( [[3,4,5]], dtype = np.uint32)
        self.tri_face_ptr2 = self.triangle_face2.ctypes.data

    
    def draw_test(self):
        
        # GLsizei which is ctypes.c_int
        self.count_arr = np.array( [3,3], dtype = np.int32)
        self.count_arr_ptr=self.count_arr.ctypes.data
                        
        self.index = np.vstack( (self.triangle_face, self.triangle_face2) )        
        print 'index',self.index
        
        from fos.core.cython_gl import get_ppointer
        
        #return all the vertices 
        get_ppointer(self.index)
        
        get_pointer(self.count_arr_ptr)
        
        '''
        
        index = index.astype(np.uint32)
        
        iptr = ctypes.POINTER(ctypes.c_uint32)        
        print "len index", len(index)
        self.index_ptr = (iptr*len(index))(*[row.ctypes.data_as(iptr) for row in index])
        print "last value", self.index_ptr,self.index_ptr[0][0],self.index_ptr[1][2]
        print 'count_arr_ptr',self.count_arr_ptr        
        print 'tri_face_ptr',self.tri_face_ptr        
        #np.array([tri_face_ptr2])
        
        '''
        
    def draw(self):
       
        #self.multi_draw_elements()
        self.draw_elements()
        
    def mutlti_draw_elements(self):
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.tri_vertex_array_ptr)        
        #glColorPointer(4, GL_UNSIGNED_BYTE, 0, glyph.glcolors)
        #glNormalPointer(GL_FLOAT, 0, glyph.glnormals)
        glMultiDrawElements(GL_TRIANGLE, self.count_arr_ptr, GL_UNSIGNED_INT, self.index_ptr, 2)
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
        glVertexPointer(3, GL_FLOAT, 0, self.tri_vert_ptr)        
        glDrawElements(GL_TRIANGLES, 3,GL_UNSIGNED_INT, self.tri_face_ptr)
        glDisableClientState(GL_VERTEX_ARRAY)    
                                       
    
    def update(self, dt):
        pass