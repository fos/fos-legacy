import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor, World, Window

class NeuronRegion(Actor):
    
    def __init__(self, vertices, connectivity, offset, colors = None, *args, **kwargs):
        """ Draws a set of static neurons with a scalar value on
        the vertices, or color value and transparency.
        
        global_line_width : float
            Global line width used to draw the polylines
        """
        super(NeuronRegion, self).__init__()
        
        self.affine = np.eye(4, dtype = np.float32)
        self._update_glaffine()
        
        self.vertices = vertices
        self.connectivity = connectivity
        self.colors = colors
        self.offset = offset
        
        self.make_aabb()
        
        print range(len(self.offset)-1)
        # create indicies, seems to be slow with nested loops
        self.indices = []
        for i in range(len(self.offset)-1):
            con = self.connectivity[self.offset[i]:self.offset[i+1]]
            # offset to add
            off = self.offset[i]
            # skipt the first node (root node)
            con[0]=0
            for j in range(0,len(con)-1):
                self.indices.append(j+off)
                self.indices.append(con[j]+off)
                
        self.indices = np.array(self.indices, dtype = np.uint)
        print self.indices
       # self.indices = np.array( range(len(self.indices)), dtype = np.uint32)
        
        #self.colors = self.colors.repeat(2, axis = 0)
        #self.colors_ptr = self.colors.ctypes.data
        
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
        #glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices_ptr)
        #glColorPointer(4, GL_UNSIGNED_BYTE, 0, self.colors_ptr)
        glDrawElements(self.mode,self.indices_nr,self.type,self.indices_ptr)
        #glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        
        glDisable(GL_LINE_SMOOTH)
        #self.draw_aabb()
        
        glPopMatrix()

            
if __name__ == '__main__':
    import numpy as np
    pos = np.random.random( (10,3)) * 100
    # connectivity: each vertices has a parent. -1 denotes the root node
    # for each neuron, the parent ids are local
    con = np.array( [-2,0,1,-2,0,2,5,6,3,4], dtype = np.int)
    # offset and size array to segment the individual neurons
    offsi = np.array( [ 0,3,10 ], dtype = np.uint)
    # colors
    col = np.random.random_integers(10, 255, (10,3)).astype(np.ubyte)
    
    wi = Window()
    w = wi.get_world()
    act = NeuronRegion(vertices = pos,
                       connectivity = con,
                       offset = offsi,
                       colors = col)
    w.add(act)
