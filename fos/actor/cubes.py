import numpy as np
from itertools import chain, islice, product, repeat, cycle, izip

from fos.core.world import World
from fos.lib.pyglet.gl import *

from fos.lib.pyglet.graphics import Batch
from fos.core.actor import Actor
from fos.geometry.vec3 import Vec3


def glarray(gltype, seq, length):
    '''
    Convert a list of lists into a flattened ctypes array, eg:
    [ (1, 2, 3), (4, 5, 6) ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
    '''
    arraytype = gltype * length
    return arraytype(*seq)


def tessellate(face):
    '''
    Return the given face broken into a list of triangles, wound in the
    same direction as the original poly. Does not work for concave faces.
    e.g. [0, 1, 2, 3, 4] -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    return (
        [face[0], face[index], face[index + 1]]
        for index in xrange(1, len(face) - 1)
    )

def face_normal(vertices, face):
    '''
    Return the unit normal vector (at right angles to) this face.
    Note that the direction of the normal will be reversed if the
    face's winding is reversed.
    '''
    v0 = vertices[face[0]]
    v1 = vertices[face[1]]
    v2 = vertices[face[2]]
    a = v0 - v1
    b = v2 - v1
    return b.cross(a).normalized()

class GLPrimitive(object):
    
    def __init__(self):
        self.num_glvertices = None
        self.glvertices = None
        self.glindex_type = None
        self.glindices = None
        self.glcolors = None
        self.glnormals = None


    def get_num_glvertices(_, faces):
        return len(list(chain(*faces)))


    def get_glvertices(self, vertices, faces):
        glverts = chain.from_iterable(
            vertices[index]
            for face in faces
            for index in face
        )
        self.num_glvertices = self.get_num_glvertices(faces)
        return glarray(gl.GLfloat, glverts, self.num_glvertices * 3)


    def get_glindex_type(self):
        '''
        The type of the glindices array depends on how many vertices there are
        '''
        if self.num_glvertices < 256:
            index_type = gl.GLubyte
        elif self.num_glvertices < 65536:
            index_type = gl.GLushort
        else:
            index_type = gl.GLuint
        return index_type


    def get_glindices(self, faces):
        glindices = []
        face_offset = 0
        for face in faces:
            indices = xrange(face_offset, face_offset + len(face))
            glindices.extend(chain(*tessellate(indices)))
            face_offset += len(face)
        self.glindex_type = self.get_glindex_type()
        return glarray(self.glindex_type, glindices, len(glindices))


    def get_glcolors(self, faces, face_colors):
        glcolors = chain.from_iterable(
            repeat(color, len(face))
            for face, color in izip(faces, face_colors)
        )
        return glarray(gl.GLubyte, chain(*glcolors), self.num_glvertices * 4) 
        

    def get_glnormals(self, vertices, faces):
        normals = (
            face_normal(vertices, face)
            for face in faces
        )
        glnormals = chain.from_iterable(
            repeat(normal, len(face))
            for face, normal in izip(faces, normals)
        )
        return glarray(
            gl.GLfloat, chain(*glnormals), self.num_glvertices * 3)


    def from_shape(self, vertices, faces, face_colors):
        self.glvertices = self.get_glvertices(vertices, faces)
        self.glindices = self.get_glindices(faces)
        self.glcolors = self.get_glcolors(faces, face_colors)
        self.glnormals = self.get_glnormals(vertices, faces)
        
class Polyhedron(object):
    '''
    Defines a polyhedron, a 3D shape with flat faces and straight edges.
    Each vertex defines a point in 3d space. Each face is a list of indices
    into the vertex array, forming a coplanar convex ring defining the face's
    edges. Each face has its own color.
    '''
    def __init__(self, vertices, faces, face_colors=None):
        
        if len(vertices) > 0 and not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]
        self.vertices = vertices

        for face in faces:
            assert len(face) >= 3
            for index in face:
                assert 0 <= index < len(vertices)
        self.faces = faces

        if face_colors is None:
            face_colors = repeat((255, 0, 0, 255))
        
#        if face_colors is None:
#            face_colors = white
#        if isinstance(face_colors, Color):
#            face_colors = repeat(face_colors)

        # TODO: colors of koch_cube/tetra break if we remove this 'list'
        # and set face_colors to the return of 'islice'. Don't know why.
        
        # returns a list of tuples of len self.faces of the given facecolors
        self.face_colors = list(islice(cycle(face_colors), len(self.faces)))
        
    def get_glprimitive(self):
        glprimitive = GLPrimitive()
        glprimitive.from_shape(self.vertices, self.faces, self.face_colors)
        return glprimitive
        

class Cubes(Actor):
    
    def __init__(self, location):
        
        self.batch=Batch()
        
        # just one cube
        e2 = 10. / 2
        verts = list(product(*repeat([-e2, +e2], 3)))
        faces = [
            [0, 1, 3, 2], # left
            [4, 6, 7, 5], # right
            [7, 3, 1, 5], # front
            [0, 2, 6, 4], # back
            [3, 7, 6, 2], # top
            [1, 0, 4, 5], # bottom
        ]
        
        oc = Polyhedron(verts, faces)
        glprim = oc.get_glprimitive()

        self.vertex_list = self.batch.add_indexed(len(glprim.glvertices) / 3,\
                                                 GL_TRIANGLES,\
                                                 None,\
                                                 list(glprim.glindices),\
                                                 ('v3f/static',list(glprim.glvertices)),\
                                                 ('n3f/static',list(glprim.glnormals)),\
                                                 ('c4B/static',list(glprim.glcolors))
                                                  \
                                                 )
        
    def draw(self):

        self.batch.draw()
        
    def delete(self):
        self.vertex_list.delete()
        
        
if __name__ == '__main__':
    
    
    mycubes = Cubes( np.array([0.0,0.0,0.0]) )
    
    