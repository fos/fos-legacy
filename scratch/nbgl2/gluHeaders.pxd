from glHeaders cimport *

cdef extern from "GL/glu.h":
    # Extensions 
    int GLU_EXT_object_space_tess
    int GLU_EXT_nurbs_tessellator

    # Boolean 
    int GLU_FALSE
    int GLU_TRUE

    # Version 
    int GLU_VERSION_1_1
    int GLU_VERSION_1_2
    int GLU_VERSION_1_3

    # StringName 
    int GLU_VERSION
    int GLU_EXTENSIONS

    # ErrorCode 
    int GLU_INVALID_ENUM
    int GLU_INVALID_VALUE
    int GLU_OUT_OF_MEMORY
    int GLU_INCOMPATIBLE_GL_VERSION
    int GLU_INVALID_OPERATION

    # NurbsDisplay 
    # GLU_FILL 
    int GLU_OUTLINE_POLYGON
    int GLU_OUTLINE_PATCH

    # NurbsCallback 
    int GLU_NURBS_ERROR
    int GLU_ERROR
    int GLU_NURBS_BEGIN
    int GLU_NURBS_BEGIN_EXT
    int GLU_NURBS_VERTEX
    int GLU_NURBS_VERTEX_EXT
    int GLU_NURBS_NORMAL
    int GLU_NURBS_NORMAL_EXT
    int GLU_NURBS_COLOR
    int GLU_NURBS_COLOR_EXT
    int GLU_NURBS_TEXTURE_COORD
    int GLU_NURBS_TEX_COORD_EXT
    int GLU_NURBS_END
    int GLU_NURBS_END_EXT
    int GLU_NURBS_BEGIN_DATA
    int GLU_NURBS_BEGIN_DATA_EXT
    int GLU_NURBS_VERTEX_DATA
    int GLU_NURBS_VERTEX_DATA_EXT
    int GLU_NURBS_NORMAL_DATA
    int GLU_NURBS_NORMAL_DATA_EXT
    int GLU_NURBS_COLOR_DATA
    int GLU_NURBS_COLOR_DATA_EXT
    int GLU_NURBS_TEXTURE_COORD_DATA
    int GLU_NURBS_TEX_COORD_DATA_EXT
    int GLU_NURBS_END_DATA
    int GLU_NURBS_END_DATA_EXT

    # NurbsError 
    int GLU_NURBS_ERROR1
    int GLU_NURBS_ERROR2
    int GLU_NURBS_ERROR3
    int GLU_NURBS_ERROR4
    int GLU_NURBS_ERROR5
    int GLU_NURBS_ERROR6
    int GLU_NURBS_ERROR7
    int GLU_NURBS_ERROR8
    int GLU_NURBS_ERROR9
    int GLU_NURBS_ERROR10
    int GLU_NURBS_ERROR11
    int GLU_NURBS_ERROR12
    int GLU_NURBS_ERROR13
    int GLU_NURBS_ERROR14
    int GLU_NURBS_ERROR15
    int GLU_NURBS_ERROR16
    int GLU_NURBS_ERROR17
    int GLU_NURBS_ERROR18
    int GLU_NURBS_ERROR19
    int GLU_NURBS_ERROR20
    int GLU_NURBS_ERROR21
    int GLU_NURBS_ERROR22
    int GLU_NURBS_ERROR23
    int GLU_NURBS_ERROR24
    int GLU_NURBS_ERROR25
    int GLU_NURBS_ERROR26
    int GLU_NURBS_ERROR27
    int GLU_NURBS_ERROR28
    int GLU_NURBS_ERROR29
    int GLU_NURBS_ERROR30
    int GLU_NURBS_ERROR31
    int GLU_NURBS_ERROR32
    int GLU_NURBS_ERROR33
    int GLU_NURBS_ERROR34
    int GLU_NURBS_ERROR35
    int GLU_NURBS_ERROR36
    int GLU_NURBS_ERROR37


    # NurbsProperty 
    int GLU_AUTO_LOAD_MATRIX
    int GLU_CULLING
    int GLU_SAMPLING_TOLERANCE
    int GLU_DISPLAY_MODE
    int GLU_PARAMETRIC_TOLERANCE
    int GLU_SAMPLING_METHOD
    int GLU_U_STEP
    int GLU_V_STEP
    int GLU_NURBS_MODE
    int GLU_NURBS_MODE_EXT
    int GLU_NURBS_TESSELLATOR
    int GLU_NURBS_TESSELLATOR_EXT
    int GLU_NURBS_RENDERER
    int GLU_NURBS_RENDERER_EXT

    # NurbsSampling 
    int GLU_OBJECT_PARAMETRIC_ERROR
    int GLU_OBJECT_PARAMETRIC_ERROR_EXT
    int GLU_OBJECT_PATH_LENGTH
    int GLU_OBJECT_PATH_LENGTH_EXT
    int GLU_PATH_LENGTH
    int GLU_PARAMETRIC_ERROR
    int GLU_DOMAIN_DISTANCE

    # NurbsTrim 
    int GLU_MAP1_TRIM_2
    int GLU_MAP1_TRIM_3

    # QuadricDrawStyle 
    int GLU_POINT
    int GLU_LINE
    int GLU_FILL
    int GLU_SILHOUETTE

    # QuadricCallback 
    # GLU_ERROR 

    # QuadricNormal 
    int GLU_SMOOTH
    int GLU_FLAT
    int GLU_NONE

    # QuadricOrientation 
    int GLU_OUTSIDE
    int GLU_INSIDE

    # TessCallback 
    int GLU_TESS_BEGIN
    int GLU_BEGIN
    int GLU_TESS_VERTEX
    int GLU_VERTEX
    int GLU_TESS_END
    int GLU_END
    int GLU_TESS_ERROR
    int GLU_TESS_EDGE_FLAG
    int GLU_EDGE_FLAG
    int GLU_TESS_COMBINE
    int GLU_TESS_BEGIN_DATA
    int GLU_TESS_VERTEX_DATA
    int GLU_TESS_END_DATA
    int GLU_TESS_ERROR_DATA
    int GLU_TESS_EDGE_FLAG_DATA
    int GLU_TESS_COMBINE_DATA

    # TessContour 
    int GLU_CW
    int GLU_CCW
    int GLU_INTERIOR
    int GLU_EXTERIOR
    int GLU_UNKNOWN

    # TessProperty 
    int GLU_TESS_WINDING_RULE
    int GLU_TESS_BOUNDARY_ONLY
    int GLU_TESS_TOLERANCE

    # TessError 
    int GLU_TESS_ERROR1
    int GLU_TESS_ERROR2
    int GLU_TESS_ERROR3
    int GLU_TESS_ERROR4
    int GLU_TESS_ERROR5
    int GLU_TESS_ERROR6
    int GLU_TESS_ERROR7
    int GLU_TESS_ERROR8
    int GLU_TESS_MISSING_BEGIN_POLYGON
    int GLU_TESS_MISSING_BEGIN_CONTOUR
    int GLU_TESS_MISSING_END_POLYGON
    int GLU_TESS_MISSING_END_CONTOUR
    int GLU_TESS_COORD_TOO_LARGE
    int GLU_TESS_NEED_COMBINE_CALLBACK

    # TessWinding 
    int GLU_TESS_WINDING_ODD
    int GLU_TESS_WINDING_NONZERO
    int GLU_TESS_WINDING_POSITIVE
    int GLU_TESS_WINDING_NEGATIVE
    int GLU_TESS_WINDING_ABS_GEQ_TWO

    ctypedef struct GLUnurbs
    ctypedef struct GLUquadric
    ctypedef struct GLUtesselator

    ctypedef GLUnurbs GLUnurbsObj
    ctypedef GLUquadric GLUquadricObj
    ctypedef GLUtesselator GLUtesselatorObj
    ctypedef GLUtesselator GLUtriangulatorObj

    void gluBeginCurve (GLUnurbs* nurb)
    void gluBeginPolygon (GLUtesselator* tess)
    void gluBeginSurface (GLUnurbs* nurb)
    void gluBeginTrim (GLUnurbs* nurb)
    GLint gluBuild1DMipmapLevels (GLenum target, GLint internalFormat, GLsizei width, GLenum format, GLenum type, GLint level, GLint base, GLint max,  void *data)
    GLint gluBuild1DMipmaps (GLenum target, GLint internalFormat, GLsizei width, GLenum format, GLenum type, void *data)
    GLint gluBuild2DMipmapLevels (GLenum target, GLint internalFormat, GLsizei width, GLsizei height, GLenum format, GLenum type, GLint level, GLint base, GLint max, void *data)
    GLint gluBuild2DMipmaps (GLenum target, GLint internalFormat, GLsizei width, GLsizei height, GLenum format, GLenum type, void *data)
    GLint gluBuild3DMipmapLevels (GLenum target, GLint internalFormat, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, GLint level, GLint base, GLint max, void *data)
    GLint gluBuild3DMipmaps (GLenum target, GLint internalFormat, GLsizei width, GLsizei height, GLsizei depth, GLenum format, GLenum type, void *data)
    GLboolean gluCheckExtension (GLubyte *extName, GLubyte *extString)
    void gluCylinder (GLUquadric* quad, GLdouble base, GLdouble top, GLdouble height, GLint slices, GLint stacks)
    void gluDeleteNurbsRenderer (GLUnurbs* nurb)
    void gluDeleteQuadric (GLUquadric* quad)
    void gluDeleteTess (GLUtesselator* tess)
    void gluDisk (GLUquadric* quad, GLdouble inner, GLdouble outer, GLint slices, GLint loops)
    void gluEndCurve (GLUnurbs* nurb)
    void gluEndPolygon (GLUtesselator* tess)
    void gluEndSurface (GLUnurbs* nurb)
    void gluEndTrim (GLUnurbs* nurb)
    GLubyte * gluErrorString (GLenum error)
    void gluGetNurbsProperty (GLUnurbs* nurb, GLenum property, GLfloat* data)
    GLubyte * gluGetString (GLenum name)
    void gluGetTessProperty (GLUtesselator* tess, GLenum which, GLdouble* data)
    void gluLoadSamplingMatrices (GLUnurbs* nurb, GLfloat *model, GLfloat *perspective, GLint *view)
    void gluLookAt (GLdouble eyeX, GLdouble eyeY, GLdouble eyeZ, GLdouble centerX, GLdouble centerY, GLdouble centerZ, GLdouble upX, GLdouble upY, GLdouble upZ)
    GLUnurbs* gluNewNurbsRenderer ( )
    GLUquadric* gluNewQuadric ( )
    GLUtesselator* gluNewTess ( )
    void gluNextContour (GLUtesselator* tess, GLenum type)
    #void gluNurbsCallback (GLUnurbs* nurb, GLenum which, _GLUfuncptr CallBackFunc)
    void gluNurbsCallbackData (GLUnurbs* nurb, GLvoid* userData)
    void gluNurbsCallbackDataEXT (GLUnurbs* nurb, GLvoid* userData)
    void gluNurbsCurve (GLUnurbs* nurb, GLint knotCount, GLfloat *knots, GLint stride, GLfloat *control, GLint order, GLenum type)
    void gluNurbsProperty (GLUnurbs* nurb, GLenum property, GLfloat value)
    void gluNurbsSurface (GLUnurbs* nurb, GLint sKnotCount, GLfloat* sKnots, GLint tKnotCount, GLfloat* tKnots, GLint sStride, GLint tStride, GLfloat* control, GLint sOrder, GLint tOrder, GLenum type)
    void gluOrtho2D (GLdouble left, GLdouble right, GLdouble bottom, GLdouble top)
    void gluPartialDisk (GLUquadric* quad, GLdouble inner, GLdouble outer, GLint slices, GLint loops, GLdouble start, GLdouble sweep)
    void gluPerspective (GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar)
    void gluPickMatrix (GLdouble x, GLdouble y, GLdouble delX, GLdouble delY, GLint *viewport)
    GLint gluProject (GLdouble objX, GLdouble objY, GLdouble objZ, GLdouble *model, GLdouble *proj, GLint *view, GLdouble* winX, GLdouble* winY, GLdouble* winZ)
    void gluPwlCurve (GLUnurbs* nurb, GLint count, GLfloat* data, GLint stride, GLenum type)
    #void gluQuadricCallback (GLUquadric* quad, GLenum which, _GLUfuncptr CallBackFunc)
    void gluQuadricDrawStyle (GLUquadric* quad, GLenum draw)
    void gluQuadricNormals (GLUquadric* quad, GLenum normal)
    void gluQuadricOrientation (GLUquadric* quad, GLenum orientation)
    void gluQuadricTexture (GLUquadric* quad, GLboolean texture)
    GLint gluScaleImage (GLenum format, GLsizei wIn, GLsizei hIn, GLenum typeIn, void *dataIn, GLsizei wOut, GLsizei hOut, GLenum typeOut, GLvoid* dataOut)
    void gluSphere (GLUquadric* quad, GLdouble radius, GLint slices, GLint stacks)
    void gluTessBeginContour (GLUtesselator* tess)
    void gluTessBeginPolygon (GLUtesselator* tess, GLvoid* data)
    #void gluTessCallback (GLUtesselator* tess, GLenum which, _GLUfuncptr CallBackFunc)
    void gluTessEndContour (GLUtesselator* tess)
    void gluTessEndPolygon (GLUtesselator* tess)
    void gluTessNormal (GLUtesselator* tess, GLdouble valueX, GLdouble valueY, GLdouble valueZ)
    void gluTessProperty (GLUtesselator* tess, GLenum which, GLdouble data)
    void gluTessVertex (GLUtesselator* tess, GLdouble *location, GLvoid* data)
    GLint gluUnProject (GLdouble winX, GLdouble winY, GLdouble winZ, GLdouble *model, GLdouble *proj, GLint *view, GLdouble* objX, GLdouble* objY, GLdouble* objZ)
    GLint gluUnProject4 (GLdouble winX, GLdouble winY, GLdouble winZ, GLdouble clipW, GLdouble *model, GLdouble *proj, GLint *view, GLdouble nearVal, GLdouble farVal, GLdouble* objX, GLdouble* objY, GLdouble* objZ, GLdouble* objW)



