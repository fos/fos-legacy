import scipy.spatial as sp
import numpy as np

from pyglet.gl import *
from fos import Actor
from fos.core.intersection import ray_aabb_intersection

class PolygonLines(Actor):

    def __init__(self,
                 vertices,
                 connectivity,
                 colors = None,
                 affine = None):
        """ A TreeRegion, composed of many trees

        vertices : Nx3
            Local 3D coordinates x,y,z
        connectivity : Mx2
            Polygon line topology
        colors : Nx4 or 1x4, float [0,1]
            Color per vertex
        affine : 4x4
            Affine transformation of the actor
            including translation

        """
        super(PolygonLines, self).__init__()

        if affine is None:
            self.affine = np.eye(4, dtype = np.float32)
        else:
            self.affine = affine

        self._update_glaffine()

        self.vertices = vertices
        self.connectivity = connectivity.ravel()

        # this coloring section is for per/vertex color
        if colors is None:
            # default colors for each line
            self.colors = np.array( [[1.0, 0.0, 0.0, 1.0]], dtype = np.float32).repeat(len(self.vertices), axis=0)
        else:
            # colors array is half the size of the connectivity array
            assert( len(self.vertices) == len(colors) )
            self.colors = colors

        # create AABB using the vertices
        self.make_aabb(margin=2.0)

        # create kdtree
        self.kdtree = sp.KDTree(self.vertices, 5)

        # create pointers
        self.vertices_ptr = self.vertices.ctypes.data
        self.connectivity_ptr = self.connectivity.ctypes.data
        self.connectivity_nr = self.connectivity.size
        self.colors_ptr = self.colors.ctypes.data

        # VBO related
        self.vertex_vbo = GLuint(0)
        glGenBuffers(1, self.vertex_vbo)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER_ARB, 4 * self.vertices.size, self.vertices_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        
        # for colors
        self.colors_vbo = GLuint(0)
        glGenBuffers(1, self.colors_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.colors_vbo)
        glBufferData(GL_ARRAY_BUFFER, 4 * self.colors.size, self.colors_ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)

        # for connectivity
        self.connectivity_vbo = GLuint(0)
        glGenBuffers(1, self.connectivity_vbo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.connectivity_vbo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * self.connectivity_nr, self.connectivity_ptr, GL_STATIC_DRAW)

    def process_pickray(self,near,far):
        """ Called when picking hit this actor
        """
        # subdivide pickray and index the kdtree to find the indices of the
        # closeby points. do then pickray-linesegment intersection
        print "-------------"
        print "near", near
        print "far", far

        # fine intersection points with aabb
        # assume that intersection exists
        near = np.array(near)
        far = np.array(far)
        
        print 'boundingbox', self.aabb.coord[0], self.aabb.coord[1]
        ab1, ab2 = self.get_aabb_coords()
        re = ray_aabb_intersection(near, far, ab1, ab2)

        print "returned intersection points", re

        # needs to have at least 2
        if len(re) < 2:
            return False
        
        ne = np.array(re[0])
        fa = np.array(re[1])
        print "used near", ne
        print "used far", fa
        d = (fa-ne) / np.linalg.norm(fa-ne)

        # how many subdivisions of the unit vector
        nr_subdiv = 20
        kdtree_sphere_query_radius = 2.0
        
        dt = np.linalg.norm((fa-ne)) / 10
        print "kdtree"
        print self.kdtree.mins, self.kdtree.maxes
        
        # create points
        for i in range(nr_subdiv+1):
            point = ne + (dt*i) * d
            # apply inverse of affine transformation to get back
            # to the original vertices space
            point_inv = np.dot( np.linalg.inv(self.affine), np.array( [point[0], point[1], point[2], 1.0] ) )
            point_inv2 = point_inv[:3]
            ind = self.kdtree.query_ball_point(point_inv2, kdtree_sphere_query_radius)
            if len(ind) > 0:
                print 'change colors'
                self.colors[ ind, 1 ] = 1.0
                self.colors[ ind, 0 ] = 0.0


    def draw(self):
        self.draw2()
        
    def draw1(self):

        glPushMatrix()
        glMultMatrixf(self.glaffine)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.vertex_vbo)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.colors_vbo)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.connectivity_vbo)
        glDrawElements(GL_LINES, self.connectivity_nr, GL_UNSIGNED_INT, 0)

        if self.show_aabb:
            self.draw_aabb()

        glPopMatrix()

    def draw2(self):

        glPushMatrix()
        glMultMatrixf(self.glaffine)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices_ptr)
        glColorPointer(4, GL_FLOAT, 0, self.colors_ptr)
        glDrawElements(GL_LINES, self.connectivity_nr, GL_UNSIGNED_INT, self.connectivity_ptr)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        if self.show_aabb:
            self.draw_aabb()
        glPopMatrix()
