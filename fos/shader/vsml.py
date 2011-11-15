# A port of VSML
# http://www.lighthouse3d.com/very-simple-libs/vsml/vsml-in-action/
# to support matrix operations

# Singleton class from
# http://code.activestate.com/recipes/52558/

# also see http://sourceforge.net/projects/libmymath/files/libmymath%20v1.3.1/

from pyglet.gl import *

class MatrixTypes(object):
    MODELVIEW = 0
    PROJECTION = 1

class VSML:
    """ A python singleton """

    class __impl:
        """ Implementation of the VSML singleton interface """

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

        def lookAt(self, xPos, yPos, zPos, xLook, yLook, zLook, xUp, yUp, zUp):
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
            pass

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
            pass

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

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if VSML.__instance is None:
            # Create and remember instance
            VSML.__instance = VSML.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_VSML__instance'] = VSML.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


# Test it
s1 = VSML()
print id(s1), s1.normalize(None)

s2 = VSML()
print id(s2), s2.normalize(None)

# Sample output, the second (inner) id is constant:
# 8172684 8176268
# 8168588 8176268
