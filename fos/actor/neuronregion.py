import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor

class NeuronRegion(Actor):
    
    def __init__(self, vertices, connectivity, offset,
                 colors = None,
                 force_centering = False,
                 *args, **kwargs):
        """ Draws a set of static neurons with a scalar value on
        the vertices, or color value and transparency.
        
        global_line_width : float
            Global line width used to draw the polylines
        """
        super(NeuronRegion, self).__init__()
        
        self.affine = np.eye(4, dtype = np.float32)
        self._update_glaffine()
        
        self.vertices = vertices
        if force_centering:
            self.vertices = self.vertices - np.mean(self.vertices, axis = 0)
        self.connectivity = connectivity
        
        if colors == None:
            # default colors
            self.colors = np.array( [[255,255,255,255]], dtype = np.ubyte).repeat(len(self.vertices),axis=0)            
        else:
            self.colors = colors
            
        self.offset = offset
        
        self.make_aabb(margin = 0)
        
        # create indicies, seems to be slow with nested loops
        self.indices = []
        for i in range(len(self.offset)-1):
            con = self.connectivity[self.offset[i]:self.offset[i+1]]
            # offset to add
            off = self.offset[i]
            # skipt the first node (root node)
            for j in range(1, len(con)):
                self.indices.append(con[j]+off)
                self.indices.append(j+off)

        self.indices = np.array(self.indices, dtype = np.uint32)
        self.colors = self.colors.repeat(2, axis = 0)
        self.colors_ptr = self.colors.ctypes.data
        self.vertices_ptr = self.vertices.ctypes.data
        self.indices_ptr = self.indices.ctypes.data
        self.indices_nr = self.indices.size
        self.mode = GL_LINES
        self.type = GL_UNSIGNED_INT
        
    def update(self, dt):
        pass
        
    def draw(self):

        glPushMatrix()
        
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glMultMatrixf(self.glaffine)
        
        glLineWidth(2.0)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices_ptr)
        glColorPointer(4, GL_UNSIGNED_BYTE, 0, self.colors_ptr)
        glDrawElements(self.mode,self.indices_nr,self.type,self.indices_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        
        glDisable(GL_LINE_SMOOTH)
        self.draw_aabb()
        
        glPopMatrix()

