# A port of VSML
# http://www.lighthouse3d.com/very-simple-libs/vsml/vsml-in-action/
# to support matrix operations

# Singleton class from
# http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern

# also see http://sourceforge.net/projects/libmymath/files/libmymath%20v1.3.1/

from fos.lib.pyglet.gl import *
import gletools
import numpy as np

class MatrixTypes(object):
    MODELVIEW = 0
    PROJECTION = 1


def normalize(vectarr):
    return vectarr / np.linalg.norm( vectarr )


class VSML(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VSML, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.projection = np.eye(4)
        self.modelview = np.eye(4)

    def get_projection(self):
        # todo: do we need .T ?
        return gletools.Mat4(*self.projection.ravel().tolist())

    def get_modelview(self):
        return gletools.Mat4(*self.modelview.ravel().tolist())

    def initUniformLocs(sefl, modelviewLoc, projLoc):
        """
        /** Call this function to init the library for a particular
          * program shader if using uniform variables
          *
          * \param modelviewLoc location of the uniform variable
          * for the modelview matrix
          *
          * \param projLoc location of the uniform variable
          * for the projection matrix
        */
        void initUniformLocs(GLuint modelviewLoc, GLuint projLoc);
        """
        pass

    def initUniformBlock(self, buf, modelviewOffset, projOffset):
        """
        /** Call this function to init the library for a particular
          * program shader if using uniform blocks
          *
          * \param buffer index of the uniform buffer
          * \param modelviewOffset offset within the buffer of
          * the modelview matrix
          * \param projOffset offset within the buffer of
          * the projection matrix
        */
        void initUniformBlock(GLuint buffer, GLuint modelviewOffset, GLuint projOffset);
        """
        pass

    def translate(self, aType, x, y, z):
        """
        /** Similar to glTranslate*. Can be applied to both MODELVIEW
          * and PROJECTION matrices.
          *
          * \param aType either MODELVIEW or PROJECTION
          * \param x,y,z vector to perform the translation
        */
        void translate(MatrixTypes aType, float x, float y, float z);
        """
        pass

    def translate(self, x, y, z):
        """
        /** Similar to glTranslate*. Applied to MODELVIEW only.
          *
          * \param x,y,z vector to perform the translation
        */
        void translate(float x, float y, float z);
        """
        pass

    def scale(self, aType, x, y, z):
        """
        /** Similar to glScale*. Can be applied to both MODELVIEW
          * and PROJECTION matrices.
          *
          * \param aType either MODELVIEW or PROJECTION
          * \param x,y,z scale factors
        */
        void scale(MatrixTypes aType, float x, float y, float z);
        """
        pass

    def scale(self, x, y, z):
        """
        /** Similar to glScale*. Applied to MODELVIEW only.
          *
          * \param x,y,z scale factors
        */
        void scale(float x, float y, float z);
        """
        pass

    def rotate(self, aType, angle, x, y, z):
        """
        /** Similar to glTotate*. Can be applied to both MODELVIEW
          * and PROJECTION matrices.
          *
          * \param aType either MODELVIEW or PROJECTION
          * \param angle rotation angle in degrees
          * \param x,y,z rotation axis in degrees
        */
        void rotate(MatrixTypes aType, float angle, float x, float y, float z);
        """
        pass

    def rotate(self, angle, x, y, z):
        """
        /** Similar to glRotate*. Applied to MODELVIEW only.
          *
          * \param angle rotation angle in degrees
          * \param x,y,z rotation axis in degrees
        */
        void rotate(float angle, float x, float y, float z);
        """
        pass

    def loadIdentity(self, aType):
        """
        /** Similar to glLoadIdentity.
          *
          * \param aType either MODELVIEW or PROJECTION
        */
        void loadIdentity(MatrixTypes aType);
        """
        pass

    def multMatrix(self, aType, aMatrix):
        """
        /** Similar to glMultMatrix.
          *
          * \param aType either MODELVIEW or PROJECTION
          * \param aMatrix matrix in column major order data, float[16]
        */
        void multMatrix(MatrixTypes aType, float *aMatrix);
        """
        pass

    def loadMatrix(self, aType, aMatrix):
        """
        /** Similar to gLoadMatrix.
          *
          * \param aType either MODELVIEW or PROJECTION
          * \param aMatrix matrix in column major order data, float[16]
        */
        void loadMatrix(MatrixTypes aType, float *aMatrix);
        """
        pass

    def pushMatrix(self, aType):
        """
        /** Similar to glPushMatrix
          *
          * \param aType either MODELVIEW or PROJECTION
        */
        void pushMatrix(MatrixTypes aType);
        """
        pass

    def popMatrix(self, aType):
        """
        /** Similar to glPopMatrix
          *
          * \param aType either MODELVIEW or PROJECTION
        */
        void popMatrix(MatrixTypes aType);
        """
        pass

#    def lookAt(self, xPos, yPos, zPos, xLook, yLook, zLook, xUp, yUp, zUp):
        """
        /** Similar to gluLookAt
          *
          * \param xPos, yPos, zPos camera position
          * \param xLook, yLook, zLook point to aim the camera at
          * \param xUp, yUp, zUp camera's up vector
        */
        void lookAt(float xPos, float yPos, float zPos,
                    float xLook, float yLook, float zLook,
                    float xUp, float yUp, float zUp);
        """

    def lookAt(self, xPos, yPos, zPos, xLook, yLook, zLook, xUp, yUp, zUp):

        dir = np.array( [xLook - xPos, yLook - yPos, zLook - zPos], dtype = np.float32)
        dir = normalize(dir)

        up = np.array( [xUp, yUp, zUp], dtype = np.float32 )

        right = np.cross(dir, up)
        right = normalize(right)

        up = np.cross(right,dir)
        up = normalize(up)

        # build the matrix
        out = np.zeros( (4,4), dtype = np.float32 )
        out[0,:3] = right
        out[1,:3] = up
        out[2,:3] = -dir

        out[0,3] = -xPos
        out[1,3] = -yPos
        out[2,3] = -zPos
        out[3,3] = 1.0
        print out
        print "out order?",  out.ravel()

        # mulitply on the matrix stack
        self.modelview = out * self.modelview
        # self.modelview = gletools.Mat4(*out.T.ravel().tolist())
    

    def perspective(self, fov, ratio, nearp, farp):
        """
        /** Similar to gluPerspective
          *
          * \param fov vertical field of view
          * \param ratio aspect ratio of the viewport or window
          * \param nearp,farp distance to the near and far planes
        */
        void perspective(float fov, float ratio, float nearp, float farp);
        """
        out = np.eye( 4, dtype = np.float32 )

        f = 1.0 / np.tan (fov * (np.pi / 360.0) )

        out[0,0] = f / ratio
        out[1,1] = f
        out[2,2] = (farp + nearp) / (nearp - farp)
        out[2,3] = (2.0 * farp * nearp) / (nearp - farp)
        out[3,2] = -1.0;
        out[3,3] = 0.0

        print "perspective", out
        self.projection = out * self.projection

    
    def ortho(self, left, right, bottom, top, nearp=-1.0, farp=1.0):
        """
        /** Similar to glOrtho and gluOrtho2D (just leave the last two params blank).
          *
          * \param left,right coordinates for the left and right vertical clipping planes
          * \param bottom,top coordinates for the bottom and top horizontal clipping planes
          * \param nearp,farp distance to the near and far planes
        */
        void ortho(float left, float right, float bottom, float top, float nearp=-1.0f, float farp=1.0f);
        """
        pass

    def frustum(self, left, right, bottom, top, nearp, farp):
        """
        /** Similar to glFrustum
          *
          * \param left,right coordinates for the left and right vertical clipping planes
          * \param bottom,top coordinates for the bottom and top horizontal clipping planes
          * \param nearp,farp distance to the near and far planes
        */
        void frustum(float left, float right, float bottom, float top, float nearp, float farp);
        """
        pass

    def get(self, aType):
        """
        /** Similar to glGet
          *
          * \param aType either MODELVIEW or PROJECTION
          * \returns pointer to the matrix (float[16])
        */
        float *get(MatrixTypes aType);
        """
        pass

    def matrixToBuffer(self, aType):
        """
        /** Updates the uniform buffer data
          *
          * \param aType  either MODELVIEW or PROJECTION
        */
        void matrixToBuffer(MatrixTypes aType);
        """
        pass

    def matrixToUniform(self, aType):
        """
        /** Updates the uniform variables
          *
          * \param aType  either MODELVIEW or PROJECTION
        */
        void matrixToUniform(MatrixTypes aType);
        """
        pass

    def matrixToGL(self, aType):
        """
        /** Updates either the buffer or the uniform variables
          * based on which init* function was called last
          *
          * \param aType  either MODELVIEW or PROJECTION
        */
        void matrixToGL(MatrixTypes aType);
        """
        pass

    # protected:

    #    /// Has an init* function been called?
    #    bool mInit;
    mInit = False

    #    /// Using uniform blocks?
    #    bool mBlocks;
    mBlocks = False

    #    ///brief Matrix stacks for modelview and projection matrices
    #    std::vector<float *> mMatrixStack[2];
    mMatrixStack = []

    #    /// The storage for the two matrices
    #    float mMatrix[2][16];
    mMatrix = []

    #    /// Storage for the uniform locations
    #    GLuint mUniformLoc[2];
    mUniformLoc = []

    #    /// Storage for the buffer index
    #    GLuint mBuffer;
    mBuffer = None

    #    /// Storage for the offsets within the buffer
    #    GLuint mOffset[2];
    mOffset = []

    def setIdentityMatrix(self, mat, size=4):
        """
        /** Set a float* to an identity matrix
          *
          * \param size the order of the matrix
        */
        void setIdentityMatrix( float *mat, int size=4);
        """
        pass

    def crossProduct(self, a, b, res):
        """
        /** vector cross product
          *
          * res = a x b
        */
        void crossProduct( float *a, float *b, float *res);
        """
        pass

    def normalize(self, a):
        """
        /// normalize a vec3
        void normalize(float *a);
        """
        pass


# self.glaffine = (GLfloat * 16)(*tuple(self.affine.T.ravel()))


# Test it
vsml = VSML()
#print id(s1), s1.normalize(None)
#
#s2 = VSML()
#print id(s2), s2.normalize(None)
#
