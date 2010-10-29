
from itertools import chain, izip, repeat

from fos.lib.pyglet.gl import gl

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


class Glyph(object):

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


    def from_shape(self, vertices, faces):
        self.glvertices = self.get_glvertices(vertices, faces)
        self.glindices = self.get_glindices(faces)
        self.glnormals = self.get_glnormals(vertices, faces)

