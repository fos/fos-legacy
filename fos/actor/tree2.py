import numpy as np

from fos.lib.pyglet.gl import *

from fos import Actor

class Tree(Actor):
    
    def __init__(self, vertices,
                 connectivity,
                 colors = None,
                 affine = None,
                 force_centering = False,
                 *args, **kwargs):
        """ A tree
        
        vertices : Nx3
            3D Coordinates x,y,z
        connectivity : Mx1
            Tree topology
        colors : Nx4 or 1x4
            Per vertex color, or actor color
        affine : 4x4
            Affine transformation of the actor

        """
        super(Tree, self).__init__()
        
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
            if len(colors) == 1:
                self.colors = np.array( [colors], dtype = np.ubyte).repeat(len(self.vertices),axis=0)            
            else:
                assert(len(colors) == len(self.vertices))
                self.colors = colors
            
        self.make_aabb(margin = 0)
        
        # create indicies, seems to be slow with nested loops
        self.indices = connectivity.astype( np.uint32 )
        self.indices_ptr = self.indices.ctypes.data
        self.indices_nr = self.indices.size
        
        # duplicate colors to make it "per vertex"
        self.colors = self.colors.repeat(2, axis = 0)
        self.colors_ptr = self.colors.ctypes.data
        
        self.vertices_ptr = self.vertices.ctypes.data
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

