/** ----------------------------------------------------------
 * \class VSML
 *
 * Lighthouse3D
 *
 * VSML - Very Simple Matrix Library
 *
 * Full documentation at
 * http://www.lighthouse3d.com/very-simple-libs
 *
 * This class aims at easing geometric transforms, camera
 * placement and projection definition for programmers
 * working with OpenGL core versions.
 *
 * This lib requires:
 *
 * GLEW (http://glew.sourceforge.net/)
 *
 ---------------------------------------------------------------*/
#ifndef __VSML__
#define __VSML__
 
// uncomment this if you want VSML to always update
// the matrices for you. Otherwise you'll have to call
// a matrixTo* function to get them updated before
// calling OpenGL draw commands
 
//#define VSML_ALWAYS_SEND_TO_OPENGL
 
#include <vector>
#include <GL/glew.h>
 
class VSML {
 
public:
 
    /// Enumeration of the matrix types
    enum MatrixTypes{
            MODELVIEW,
            PROJECTION
    } ;
 
    /// Singleton pattern
    static VSML* gInstance;
 
    /// Call this to get the single instance of VSML
    static VSML* getInstance (void);
 
    ~VSML();
 
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
 
    /** Similar to glTranslate*. Can be applied to both MODELVIEW
      * and PROJECTION matrices.
      *
      * \param aType either MODELVIEW or PROJECTION
      * \param x,y,z vector to perform the translation
    */
    void translate(MatrixTypes aType, float x, float y, float z);
 
    /** Similar to glTranslate*. Applied to MODELVIEW only.
      *
      * \param x,y,z vector to perform the translation
    */
    void translate(float x, float y, float z);
 
    /** Similar to glScale*. Can be applied to both MODELVIEW
      * and PROJECTION matrices.
      *
      * \param aType either MODELVIEW or PROJECTION
      * \param x,y,z scale factors
    */
    void scale(MatrixTypes aType, float x, float y, float z);
 
    /** Similar to glScale*. Applied to MODELVIEW only.
      *
      * \param x,y,z scale factors
    */
    void scale(float x, float y, float z);
 
    /** Similar to glTotate*. Can be applied to both MODELVIEW
      * and PROJECTION matrices.
      *
      * \param aType either MODELVIEW or PROJECTION
      * \param angle rotation angle in degrees
      * \param x,y,z rotation axis in degrees
    */
    void rotate(MatrixTypes aType, float angle, float x, float y, float z);
 
    /** Similar to glRotate*. Applied to MODELVIEW only.
      *
      * \param angle rotation angle in degrees
      * \param x,y,z rotation axis in degrees
    */
    void rotate(float angle, float x, float y, float z);
 
    /** Similar to glLoadIdentity.
      *
      * \param aType either MODELVIEW or PROJECTION
    */
    void loadIdentity(MatrixTypes aType);
 
    /** Similar to glMultMatrix.
      *
      * \param aType either MODELVIEW or PROJECTION
      * \param aMatrix matrix in column major order data, float[16]
    */
    void multMatrix(MatrixTypes aType, float *aMatrix);
 
    /** Similar to gLoadMatrix.
      *
      * \param aType either MODELVIEW or PROJECTION
      * \param aMatrix matrix in column major order data, float[16]
    */
 
    void loadMatrix(MatrixTypes aType, float *aMatrix);
 
    /** Similar to glPushMatrix
      *
      * \param aType either MODELVIEW or PROJECTION
    */
    void pushMatrix(MatrixTypes aType);
 
    /** Similar to glPopMatrix
      *
      * \param aType either MODELVIEW or PROJECTION
    */
    void popMatrix(MatrixTypes aType);
 
    /** Similar to gluLookAt
      *
      * \param xPos, yPos, zPos camera position
      * \param xLook, yLook, zLook point to aim the camera at
      * \param xUp, yUp, zUp camera's up vector
    */
    void lookAt(float xPos, float yPos, float zPos,
                float xLook, float yLook, float zLook,
                float xUp, float yUp, float zUp);
 
    /** Similar to gluPerspective
      *
      * \param fov vertical field of view
      * \param ratio aspect ratio of the viewport or window
      * \param nearp,farp distance to the near and far planes
    */
    void perspective(float fov, float ratio, float nearp, float farp);
 
    /** Similar to glOrtho and gluOrtho2D (just leave the last two params blank).
      *
      * \param left,right coordinates for the left and right vertical clipping planes
      * \param bottom,top coordinates for the bottom and top horizontal clipping planes
      * \param nearp,farp distance to the near and far planes
    */
    void ortho(float left, float right, float bottom, float top, float nearp=-1.0f, float farp=1.0f);
 
    /** Similar to glFrustum
      *
      * \param left,right coordinates for the left and right vertical clipping planes
      * \param bottom,top coordinates for the bottom and top horizontal clipping planes
      * \param nearp,farp distance to the near and far planes
    */
    void frustum(float left, float right, float bottom, float top, float nearp, float farp);
 
    /** Similar to glGet
      *
      * \param aType either MODELVIEW or PROJECTION
      * \returns pointer to the matrix (float[16])
    */
    float *get(MatrixTypes aType);
 
    /** Updates the uniform buffer data
      *
      * \param aType  either MODELVIEW or PROJECTION
    */
    void matrixToBuffer(MatrixTypes aType);
 
    /** Updates the uniform variables
      *
      * \param aType  either MODELVIEW or PROJECTION
    */
    void matrixToUniform(MatrixTypes aType);
 
    /** Updates either the buffer or the uniform variables
      * based on which init* function was called last
      *
      * \param aType  either MODELVIEW or PROJECTION
    */
    void matrixToGL(MatrixTypes aType);
 
protected:
 
    VSML();
 
    /// Has an init* function been called?
    bool mInit;
 
    /// Using uniform blocks?
    bool mBlocks;
 
    ///brief Matrix stacks for modelview and projection matrices
    std::vector<float *> mMatrixStack[2];
 
    /// The storage for the two matrices
    float mMatrix[2][16];
 
    /// Storage for the uniform locations
    GLuint mUniformLoc[2];
 
    /// Storage for the buffer index
    GLuint mBuffer;
 
    /// Storage for the offsets within the buffer
    GLuint mOffset[2];
 
    /** Set a float* to an identity matrix
      *
      * \param size the order of the matrix
    */
    void setIdentityMatrix( float *mat, int size=4);
 
    /** vector cross product
      *
      * res = a x b
    */
    void crossProduct( float *a, float *b, float *res);
 
    /// normalize a vec3
    void normalize(float *a);
 
};
 
#endif
