cdef extern from "GL/gl.h":
    # Datatypes
    ctypedef unsigned int GLenum
    ctypedef unsigned char GLboolean
    ctypedef unsigned int GLbitfield
    ctypedef void GLvoid
    ctypedef signed char     GLbyte   # 1-byte signed 
    ctypedef short           GLshort  # 2-byte signed 
    ctypedef int             GLint    # 4-byte signed 
    ctypedef unsigned char   GLubyte  # 1-byte unsigned 
    ctypedef unsigned short  GLushort # 2-byte unsigned 
    ctypedef unsigned int    GLuint   # 4-byte unsigned 
    ctypedef int             GLsizei  # 4-byte signed 
    ctypedef float           GLfloat  # single precision float 
    ctypedef float           GLclampf # single precision float in [0,1] 
    ctypedef double          GLdouble # double precision float 
    ctypedef double          GLclampd # double precision float in [0,1] 

    # Boolean values 
    int GL_FALSE
    int GL_TRUE

    # Data types 
    int GL_BYTE
    int GL_UNSIGNED_BYTE
    int GL_SHORT
    int GL_UNSIGNED_SHORT
    int GL_INT
    int GL_UNSIGNED_INT
    int GL_FLOAT
    int GL_2_BYTES
    int GL_3_BYTES
    int GL_4_BYTES
    int GL_DOUBLE

    # Primitives 
    int GL_POINTS
    int GL_LINES
    int GL_LINE_LOOP
    int GL_LINE_STRIP
    int GL_TRIANGLES
    int GL_TRIANGLE_STRIP
    int GL_TRIANGLE_FAN
    int GL_QUADS
    int GL_QUAD_STRIP
    int GL_POLYGON

    # Vertex Arrays 
    int GL_VERTEX_ARRAY
    int GL_NORMAL_ARRAY
    int GL_COLOR_ARRAY
    int GL_INDEX_ARRAY
    int GL_TEXTURE_COORD_ARRAY
    int GL_EDGE_FLAG_ARRAY
    int GL_VERTEX_ARRAY_SIZE
    int GL_VERTEX_ARRAY_TYPE
    int GL_VERTEX_ARRAY_STRIDE
    int GL_NORMAL_ARRAY_TYPE
    int GL_NORMAL_ARRAY_STRIDE
    int GL_COLOR_ARRAY_SIZE
    int GL_COLOR_ARRAY_TYPE
    int GL_COLOR_ARRAY_STRIDE
    int GL_INDEX_ARRAY_TYPE
    int GL_INDEX_ARRAY_STRIDE
    int GL_TEXTURE_COORD_ARRAY_SIZE
    int GL_TEXTURE_COORD_ARRAY_TYPE
    int GL_TEXTURE_COORD_ARRAY_STRIDE
    int GL_EDGE_FLAG_ARRAY_STRIDE
    int GL_VERTEX_ARRAY_POINTER
    int GL_NORMAL_ARRAY_POINTER
    int GL_COLOR_ARRAY_POINTER
    int GL_INDEX_ARRAY_POINTER
    int GL_TEXTURE_COORD_ARRAY_POINTER
    int GL_EDGE_FLAG_ARRAY_POINTER
    int GL_V2F
    int GL_V3F
    int GL_C4UB_V2F
    int GL_C4UB_V3F
    int GL_C3F_V3F
    int GL_N3F_V3F
    int GL_C4F_N3F_V3F
    int GL_T2F_V3F
    int GL_T4F_V4F
    int GL_T2F_C4UB_V3F
    int GL_T2F_C3F_V3F
    int GL_T2F_N3F_V3F
    int GL_T2F_C4F_N3F_V3F
    int GL_T4F_C4F_N3F_V4F

    # Matrix Mode 
    int GL_MATRIX_MODE
    int GL_MODELVIEW
    int GL_PROJECTION
    int GL_TEXTURE

    # Points 
    int GL_POINT_SMOOTH
    int GL_POINT_SIZE
    int GL_POINT_SIZE_GRANULARITY
    int GL_POINT_SIZE_RANGE

    # Lines 
    int GL_LINE_SMOOTH
    int GL_LINE_STIPPLE
    int GL_LINE_STIPPLE_PATTERN
    int GL_LINE_STIPPLE_REPEAT
    int GL_LINE_WIDTH
    int GL_LINE_WIDTH_GRANULARITY
    int GL_LINE_WIDTH_RANGE

    # Polygons 
    int GL_POINT
    int GL_LINE
    int GL_FILL
    int GL_CW
    int GL_CCW
    int GL_FRONT
    int GL_BACK
    int GL_POLYGON_MODE
    int GL_POLYGON_SMOOTH
    int GL_POLYGON_STIPPLE
    int GL_EDGE_FLAG
    int GL_CULL_FACE
    int GL_CULL_FACE_MODE
    int GL_FRONT_FACE
    int GL_POLYGON_OFFSET_FACTOR
    int GL_POLYGON_OFFSET_UNITS
    int GL_POLYGON_OFFSET_POINT
    int GL_POLYGON_OFFSET_LINE
    int GL_POLYGON_OFFSET_FILL

    # Display Lists 
    int GL_COMPILE
    int GL_COMPILE_AND_EXECUTE
    int GL_LIST_BASE
    int GL_LIST_INDEX
    int GL_LIST_MODE

    # Depth buffer 
    int GL_NEVER
    int GL_LESS
    int GL_EQUAL
    int GL_LEQUAL
    int GL_GREATER
    int GL_NOTEQUAL
    int GL_GEQUAL
    int GL_ALWAYS
    int GL_DEPTH_TEST
    int GL_DEPTH_BITS
    int GL_DEPTH_CLEAR_VALUE
    int GL_DEPTH_FUNC
    int GL_DEPTH_RANGE
    int GL_DEPTH_WRITEMASK
    int GL_DEPTH_COMPONENT

    # Lighting 
    int GL_LIGHTING
    int GL_LIGHT0
    int GL_LIGHT1
    int GL_LIGHT2
    int GL_LIGHT3
    int GL_LIGHT4
    int GL_LIGHT5
    int GL_LIGHT6
    int GL_LIGHT7
    int GL_SPOT_EXPONENT
    int GL_SPOT_CUTOFF
    int GL_CONSTANT_ATTENUATION
    int GL_LINEAR_ATTENUATION
    int GL_QUADRATIC_ATTENUATION
    int GL_AMBIENT
    int GL_DIFFUSE
    int GL_SPECULAR
    int GL_SHININESS
    int GL_EMISSION
    int GL_POSITION
    int GL_SPOT_DIRECTION
    int GL_AMBIENT_AND_DIFFUSE
    int GL_COLOR_INDEXES
    int GL_LIGHT_MODEL_TWO_SIDE
    int GL_LIGHT_MODEL_LOCAL_VIEWER
    int GL_LIGHT_MODEL_AMBIENT
    int GL_FRONT_AND_BACK
    int GL_SHADE_MODEL
    int GL_FLAT
    int GL_SMOOTH
    int GL_COLOR_MATERIAL
    int GL_COLOR_MATERIAL_FACE
    int GL_COLOR_MATERIAL_PARAMETER
    int GL_NORMALIZE

    # User clipping planes 
    int GL_CLIP_PLANE0
    int GL_CLIP_PLANE1
    int GL_CLIP_PLANE2
    int GL_CLIP_PLANE3
    int GL_CLIP_PLANE4
    int GL_CLIP_PLANE5

    # Accumulation buffer 
    int GL_ACCUM_RED_BITS
    int GL_ACCUM_GREEN_BITS
    int GL_ACCUM_BLUE_BITS
    int GL_ACCUM_ALPHA_BITS
    int GL_ACCUM_CLEAR_VALUE
    int GL_ACCUM
    int GL_ADD
    int GL_LOAD
    int GL_MULT
    int GL_RETURN

    # Alpha testing 
    int GL_ALPHA_TEST
    int GL_ALPHA_TEST_REF
    int GL_ALPHA_TEST_FUNC

    # Blending 
    int GL_BLEND
    int GL_BLEND_SRC
    int GL_BLEND_DST
    int GL_ZERO
    int GL_ONE
    int GL_SRC_COLOR
    int GL_ONE_MINUS_SRC_COLOR
    int GL_SRC_ALPHA
    int GL_ONE_MINUS_SRC_ALPHA
    int GL_DST_ALPHA
    int GL_ONE_MINUS_DST_ALPHA
    int GL_DST_COLOR
    int GL_ONE_MINUS_DST_COLOR
    int GL_SRC_ALPHA_SATURATE

    # Render Mode 
    int GL_FEEDBACK
    int GL_RENDER
    int GL_SELECT

    # Feedback 
    int GL_2D
    int GL_3D
    int GL_3D_COLOR
    int GL_3D_COLOR_TEXTURE
    int GL_4D_COLOR_TEXTURE
    int GL_POINT_TOKEN
    int GL_LINE_TOKEN
    int GL_LINE_RESET_TOKEN
    int GL_POLYGON_TOKEN
    int GL_BITMAP_TOKEN
    int GL_DRAW_PIXEL_TOKEN
    int GL_COPY_PIXEL_TOKEN
    int GL_PASS_THROUGH_TOKEN
    int GL_FEEDBACK_BUFFER_POINTER
    int GL_FEEDBACK_BUFFER_SIZE
    int GL_FEEDBACK_BUFFER_TYPE

    # Selection 
    int GL_SELECTION_BUFFER_POINTER
    int GL_SELECTION_BUFFER_SIZE

    # Fog 
    int GL_FOG
    int GL_FOG_MODE
    int GL_FOG_DENSITY
    int GL_FOG_COLOR
    int GL_FOG_INDEX
    int GL_FOG_START
    int GL_FOG_END
    int GL_LINEAR
    int GL_EXP
    int GL_EXP2

    # Logic Ops 
    int GL_LOGIC_OP
    int GL_INDEX_LOGIC_OP
    int GL_COLOR_LOGIC_OP
    int GL_LOGIC_OP_MODE
    int GL_CLEAR
    int GL_SET
    int GL_COPY
    int GL_COPY_INVERTED
    int GL_NOOP
    int GL_INVERT
    int GL_AND
    int GL_NAND
    int GL_OR
    int GL_NOR
    int GL_XOR
    int GL_EQUIV
    int GL_AND_REVERSE
    int GL_AND_INVERTED
    int GL_OR_REVERSE
    int GL_OR_INVERTED

    # Stencil 
    int GL_STENCIL_BITS
    int GL_STENCIL_TEST
    int GL_STENCIL_CLEAR_VALUE
    int GL_STENCIL_FUNC
    int GL_STENCIL_VALUE_MASK
    int GL_STENCIL_FAIL
    int GL_STENCIL_PASS_DEPTH_FAIL
    int GL_STENCIL_PASS_DEPTH_PASS
    int GL_STENCIL_REF
    int GL_STENCIL_WRITEMASK
    int GL_STENCIL_INDEX
    int GL_KEEP
    int GL_REPLACE
    int GL_INCR
    int GL_DECR

    # Buffers, Pixel Drawing/Reading 
    int GL_NONE
    int GL_LEFT
    int GL_RIGHT
    #int GL_FRONT
    #int GL_BACK
    #int GL_FRONT_AND_BACK
    int GL_FRONT_LEFT
    int GL_FRONT_RIGHT
    int GL_BACK_LEFT
    int GL_BACK_RIGHT
    int GL_AUX0
    int GL_AUX1
    int GL_AUX2
    int GL_AUX3
    int GL_COLOR_INDEX
    int GL_RED
    int GL_GREEN
    int GL_BLUE
    int GL_ALPHA
    int GL_LUMINANCE
    int GL_LUMINANCE_ALPHA
    int GL_ALPHA_BITS
    int GL_RED_BITS
    int GL_GREEN_BITS
    int GL_BLUE_BITS
    int GL_INDEX_BITS
    int GL_SUBPIXEL_BITS
    int GL_AUX_BUFFERS
    int GL_READ_BUFFER
    int GL_DRAW_BUFFER
    int GL_DOUBLEBUFFER
    int GL_STEREO
    int GL_BITMAP
    int GL_COLOR
    int GL_DEPTH
    int GL_STENCIL
    int GL_DITHER
    int GL_RGB
    int GL_RGBA

    # Implementation limits 
    int GL_MAX_LIST_NESTING
    int GL_MAX_EVAL_ORDER
    int GL_MAX_LIGHTS
    int GL_MAX_CLIP_PLANES
    int GL_MAX_TEXTURE_SIZE
    int GL_MAX_PIXEL_MAP_TABLE
    int GL_MAX_ATTRIB_STACK_DEPTH
    int GL_MAX_MODELVIEW_STACK_DEPTH
    int GL_MAX_NAME_STACK_DEPTH
    int GL_MAX_PROJECTION_STACK_DEPTH
    int GL_MAX_TEXTURE_STACK_DEPTH
    int GL_MAX_VIEWPORT_DIMS
    int GL_MAX_CLIENT_ATTRIB_STACK_DEPTH

    # Gets 
    int GL_ATTRIB_STACK_DEPTH
    int GL_CLIENT_ATTRIB_STACK_DEPTH
    int GL_COLOR_CLEAR_VALUE
    int GL_COLOR_WRITEMASK
    int GL_CURRENT_INDEX
    int GL_CURRENT_COLOR
    int GL_CURRENT_NORMAL
    int GL_CURRENT_RASTER_COLOR
    int GL_CURRENT_RASTER_DISTANCE
    int GL_CURRENT_RASTER_INDEX
    int GL_CURRENT_RASTER_POSITION
    int GL_CURRENT_RASTER_TEXTURE_COORDS
    int GL_CURRENT_RASTER_POSITION_VALID
    int GL_CURRENT_TEXTURE_COORDS
    int GL_INDEX_CLEAR_VALUE
    int GL_INDEX_MODE
    int GL_INDEX_WRITEMASK
    int GL_MODELVIEW_MATRIX
    int GL_MODELVIEW_STACK_DEPTH
    int GL_NAME_STACK_DEPTH
    int GL_PROJECTION_MATRIX
    int GL_PROJECTION_STACK_DEPTH
    int GL_RENDER_MODE
    int GL_RGBA_MODE
    int GL_TEXTURE_MATRIX
    int GL_TEXTURE_STACK_DEPTH
    int GL_VIEWPORT

    # Evaluators 
    int GL_AUTO_NORMAL
    int GL_MAP1_COLOR_4
    int GL_MAP1_INDEX
    int GL_MAP1_NORMAL
    int GL_MAP1_TEXTURE_COORD_1
    int GL_MAP1_TEXTURE_COORD_2
    int GL_MAP1_TEXTURE_COORD_3
    int GL_MAP1_TEXTURE_COORD_4
    int GL_MAP1_VERTEX_3
    int GL_MAP1_VERTEX_4
    int GL_MAP2_COLOR_4
    int GL_MAP2_INDEX
    int GL_MAP2_NORMAL
    int GL_MAP2_TEXTURE_COORD_1
    int GL_MAP2_TEXTURE_COORD_2
    int GL_MAP2_TEXTURE_COORD_3
    int GL_MAP2_TEXTURE_COORD_4
    int GL_MAP2_VERTEX_3
    int GL_MAP2_VERTEX_4
    int GL_MAP1_GRID_DOMAIN
    int GL_MAP1_GRID_SEGMENTS
    int GL_MAP2_GRID_DOMAIN
    int GL_MAP2_GRID_SEGMENTS
    int GL_COEFF
    int GL_ORDER
    int GL_DOMAIN

    # Hints 
    int GL_PERSPECTIVE_CORRECTION_HINT
    int GL_POINT_SMOOTH_HINT
    int GL_LINE_SMOOTH_HINT
    int GL_POLYGON_SMOOTH_HINT
    int GL_FOG_HINT
    int GL_DONT_CARE
    int GL_FASTEST
    int GL_NICEST

    # Scissor box 
    int GL_SCISSOR_BOX
    int GL_SCISSOR_TEST

    # Pixel Mode / Transfer 
    int GL_MAP_COLOR
    int GL_MAP_STENCIL
    int GL_INDEX_SHIFT
    int GL_INDEX_OFFSET
    int GL_RED_SCALE
    int GL_RED_BIAS
    int GL_GREEN_SCALE
    int GL_GREEN_BIAS
    int GL_BLUE_SCALE
    int GL_BLUE_BIAS
    int GL_ALPHA_SCALE
    int GL_ALPHA_BIAS
    int GL_DEPTH_SCALE
    int GL_DEPTH_BIAS
    int GL_PIXEL_MAP_S_TO_S_SIZE
    int GL_PIXEL_MAP_I_TO_I_SIZE
    int GL_PIXEL_MAP_I_TO_R_SIZE
    int GL_PIXEL_MAP_I_TO_G_SIZE
    int GL_PIXEL_MAP_I_TO_B_SIZE
    int GL_PIXEL_MAP_I_TO_A_SIZE
    int GL_PIXEL_MAP_R_TO_R_SIZE
    int GL_PIXEL_MAP_G_TO_G_SIZE
    int GL_PIXEL_MAP_B_TO_B_SIZE
    int GL_PIXEL_MAP_A_TO_A_SIZE
    int GL_PIXEL_MAP_S_TO_S
    int GL_PIXEL_MAP_I_TO_I
    int GL_PIXEL_MAP_I_TO_R
    int GL_PIXEL_MAP_I_TO_G
    int GL_PIXEL_MAP_I_TO_B
    int GL_PIXEL_MAP_I_TO_A
    int GL_PIXEL_MAP_R_TO_R
    int GL_PIXEL_MAP_G_TO_G
    int GL_PIXEL_MAP_B_TO_B
    int GL_PIXEL_MAP_A_TO_A
    int GL_PACK_ALIGNMENT
    int GL_PACK_LSB_FIRST
    int GL_PACK_ROW_LENGTH
    int GL_PACK_SKIP_PIXELS
    int GL_PACK_SKIP_ROWS
    int GL_PACK_SWAP_BYTES
    int GL_UNPACK_ALIGNMENT
    int GL_UNPACK_LSB_FIRST
    int GL_UNPACK_ROW_LENGTH
    int GL_UNPACK_SKIP_PIXELS
    int GL_UNPACK_SKIP_ROWS
    int GL_UNPACK_SWAP_BYTES
    int GL_ZOOM_X
    int GL_ZOOM_Y

    # Texture mapping 
    int GL_TEXTURE_ENV
    int GL_TEXTURE_ENV_MODE
    int GL_TEXTURE_1D
    int GL_TEXTURE_2D
    int GL_TEXTURE_WRAP_S
    int GL_TEXTURE_WRAP_T
    int GL_TEXTURE_MAG_FILTER
    int GL_TEXTURE_MIN_FILTER
    int GL_TEXTURE_ENV_COLOR
    int GL_TEXTURE_GEN_S
    int GL_TEXTURE_GEN_T
    int GL_TEXTURE_GEN_MODE
    int GL_TEXTURE_BORDER_COLOR
    int GL_TEXTURE_WIDTH
    int GL_TEXTURE_HEIGHT
    int GL_TEXTURE_BORDER
    int GL_TEXTURE_COMPONENTS
    int GL_TEXTURE_RED_SIZE
    int GL_TEXTURE_GREEN_SIZE
    int GL_TEXTURE_BLUE_SIZE
    int GL_TEXTURE_ALPHA_SIZE
    int GL_TEXTURE_LUMINANCE_SIZE
    int GL_TEXTURE_INTENSITY_SIZE
    int GL_NEAREST_MIPMAP_NEAREST
    int GL_NEAREST_MIPMAP_LINEAR
    int GL_LINEAR_MIPMAP_NEAREST
    int GL_LINEAR_MIPMAP_LINEAR
    int GL_OBJECT_LINEAR
    int GL_OBJECT_PLANE
    int GL_EYE_LINEAR
    int GL_EYE_PLANE
    int GL_SPHERE_MAP
    int GL_DECAL
    int GL_MODULATE
    int GL_NEAREST
    int GL_REPEAT
    int GL_CLAMP
    int GL_S
    int GL_T
    int GL_R
    int GL_Q
    int GL_TEXTURE_GEN_R
    int GL_TEXTURE_GEN_Q

    # Utility 
    int GL_VENDOR
    int GL_RENDERER
    int GL_VERSION
    int GL_EXTENSIONS

    # Errors 
    int GL_NO_ERROR
    int GL_INVALID_ENUM
    int GL_INVALID_VALUE
    int GL_INVALID_OPERATION
    int GL_STACK_OVERFLOW
    int GL_STACK_UNDERFLOW
    int GL_OUT_OF_MEMORY

    # glPush/PopAttrib bits 
    int GL_CURRENT_BIT
    int GL_POINT_BIT
    int GL_LINE_BIT
    int GL_POLYGON_BIT
    int GL_POLYGON_STIPPLE_BIT
    int GL_PIXEL_MODE_BIT
    int GL_LIGHTING_BIT
    int GL_FOG_BIT
    int GL_DEPTH_BUFFER_BIT
    int GL_ACCUM_BUFFER_BIT
    int GL_STENCIL_BUFFER_BIT
    int GL_VIEWPORT_BIT
    int GL_TRANSFORM_BIT
    int GL_ENABLE_BIT
    int GL_COLOR_BUFFER_BIT
    int GL_HINT_BIT
    int GL_EVAL_BIT
    int GL_LIST_BIT
    int GL_TEXTURE_BIT
    int GL_SCISSOR_BIT
    int GL_ALL_ATTRIB_BITS

    # Miscellaneous
    cdef void glClearIndex( GLfloat c )

    void glClearColor( GLclampf red, GLclampf green, GLclampf blue, GLclampf alpha )

    void glClear( GLbitfield mask )

    void glIndexMask( GLuint mask )

    void glColorMask( GLboolean red, GLboolean green, GLboolean blue, GLboolean alpha )

    void glAlphaFunc( GLenum func, GLclampf ref )

    void glBlendFunc( GLenum sfactor, GLenum dfactor )

    void glLogicOp( GLenum opcode )

    void glCullFace( GLenum mode )

    void glFrontFace( GLenum mode )

    void glPointSize( GLfloat size )

    void glLineWidth( GLfloat width )

    void glLineStipple( GLint factor, GLushort pattern )

    void glPolygonMode( GLenum face, GLenum mode )

    void glPolygonOffset( GLfloat factor, GLfloat units )

    void glPolygonStipple( GLubyte *mask )

    void glGetPolygonStipple( GLubyte *mask )

    void glEdgeFlag( GLboolean flag )

    void glEdgeFlagv( GLboolean *flag )

    void glScissor( GLint x, GLint y, GLsizei width, GLsizei height)

    void glClipPlane( GLenum plane, GLdouble *equation )

    void glGetClipPlane( GLenum plane, GLdouble *equation )

    void glDrawBuffer( GLenum mode )

    void glReadBuffer( GLenum mode )

    void glEnable( GLenum cap )

    void glDisable( GLenum cap )

    GLboolean glIsEnabled( GLenum cap )


    void glEnableClientState( GLenum cap )  # 1.1 

    void glDisableClientState( GLenum cap )  # 1.1 


    void glGetBooleanv( GLenum pname, GLboolean *params )

    void glGetDoublev( GLenum pname, GLdouble *params )

    void glGetFloatv( GLenum pname, GLfloat *params )

    void glGetIntegerv( GLenum pname, GLint *params )


    void glPushAttrib( GLbitfield mask )

    void glPopAttrib( )


    void glPushClientAttrib( GLbitfield mask )  # 1.1 

    void glPopClientAttrib( )  # 1.1 


    GLint glRenderMode( GLenum mode )

    GLenum glGetError( )

    GLubyte * glGetString( GLenum name )

    void glFinish( )

    void glFlush( )

    void glHint( GLenum target, GLenum mode )


    # Depth Buffer

    void glClearDepth( GLclampd depth )

    void glDepthFunc( GLenum func )

    void glDepthMask( GLboolean flag )

    void glDepthRange( GLclampd near_val, GLclampd far_val )


    # Accumulation Buffer

    void glClearAccum( GLfloat red, GLfloat green, GLfloat blue, GLfloat alpha )

    void glAccum( GLenum op, GLfloat value )


    # Transformation

    void glMatrixMode( GLenum mode )

    void glOrtho( GLdouble left, GLdouble right,
                                 GLdouble bottom, GLdouble top,
                                 GLdouble near_val, GLdouble far_val )

    void glFrustum( GLdouble left, GLdouble right,
                                   GLdouble bottom, GLdouble top,
                                   GLdouble near_val, GLdouble far_val )

    void glViewport( GLint x, GLint y,
                                    GLsizei width, GLsizei height )

    void glPushMatrix( )

    void glPopMatrix( )

    void glLoadIdentity( )

    void glLoadMatrixd( GLdouble *m )
    void glLoadMatrixf( GLfloat *m )

    void glMultMatrixd( GLdouble *m )
    void glMultMatrixf( GLfloat *m )

    void glRotated( GLdouble angle,
                                   GLdouble x, GLdouble y, GLdouble z )
    void glRotatef( GLfloat angle,
                                   GLfloat x, GLfloat y, GLfloat z )

    void glScaled( GLdouble x, GLdouble y, GLdouble z )
    void glScalef( GLfloat x, GLfloat y, GLfloat z )

    void glTranslated( GLdouble x, GLdouble y, GLdouble z )
    void glTranslatef( GLfloat x, GLfloat y, GLfloat z )

    # Display Lists

    GLboolean glIsList( GLuint list )

    void glDeleteLists( GLuint list, GLsizei range )

    GLuint glGenLists( GLsizei range )

    void glNewList( GLuint list, GLenum mode )

    void glEndList( )

    void glCallList( GLuint list )

    void glCallLists( GLsizei n, GLenum type, GLvoid *lists )

    void glListBase( GLuint base )


    # Drawing Functions

    void glBegin( GLenum mode )

    void glEnd( )


    void glVertex2d( GLdouble x, GLdouble y )
    void glVertex2f( GLfloat x, GLfloat y )
    void glVertex2i( GLint x, GLint y )
    void glVertex2s( GLshort x, GLshort y )

    void glVertex3d( GLdouble x, GLdouble y, GLdouble z )
    void glVertex3f( GLfloat x, GLfloat y, GLfloat z )
    void glVertex3i( GLint x, GLint y, GLint z )
    void glVertex3s( GLshort x, GLshort y, GLshort z )

    void glVertex4d( GLdouble x, GLdouble y, GLdouble z, GLdouble w )
    void glVertex4f( GLfloat x, GLfloat y, GLfloat z, GLfloat w )
    void glVertex4i( GLint x, GLint y, GLint z, GLint w )
    void glVertex4s( GLshort x, GLshort y, GLshort z, GLshort w )

    void glVertex2dv( GLdouble *v )
    void glVertex2fv( GLfloat *v )
    void glVertex2iv( GLint *v )
    void glVertex2sv( GLshort *v )

    void glVertex3dv( GLdouble *v )
    void glVertex3fv( GLfloat *v )
    void glVertex3iv( GLint *v )
    void glVertex3sv( GLshort *v )

    void glVertex4dv( GLdouble *v )
    void glVertex4fv( GLfloat *v )
    void glVertex4iv( GLint *v )
    void glVertex4sv( GLshort *v )


    void glNormal3b( GLbyte nx, GLbyte ny, GLbyte nz )
    void glNormal3d( GLdouble nx, GLdouble ny, GLdouble nz )
    void glNormal3f( GLfloat nx, GLfloat ny, GLfloat nz )
    void glNormal3i( GLint nx, GLint ny, GLint nz )
    void glNormal3s( GLshort nx, GLshort ny, GLshort nz )

    void glNormal3bv( GLbyte *v )
    void glNormal3dv( GLdouble *v )
    void glNormal3fv( GLfloat *v )
    void glNormal3iv( GLint *v )
    void glNormal3sv( GLshort *v )


    void glIndexd( GLdouble c )
    void glIndexf( GLfloat c )
    void glIndexi( GLint c )
    void glIndexs( GLshort c )
    void glIndexub( GLubyte c )  # 1.1 

    void glIndexdv( GLdouble *c )
    void glIndexfv( GLfloat *c )
    void glIndexiv( GLint *c )
    void glIndexsv( GLshort *c )
    void glIndexubv( GLubyte *c )  # 1.1 

    void glColor3b( GLbyte red, GLbyte green, GLbyte blue )
    void glColor3d( GLdouble red, GLdouble green, GLdouble blue )
    void glColor3f( GLfloat red, GLfloat green, GLfloat blue )
    void glColor3i( GLint red, GLint green, GLint blue )
    void glColor3s( GLshort red, GLshort green, GLshort blue )
    void glColor3ub( GLubyte red, GLubyte green, GLubyte blue )
    void glColor3ui( GLuint red, GLuint green, GLuint blue )
    void glColor3us( GLushort red, GLushort green, GLushort blue )

    void glColor4b( GLbyte red, GLbyte green,
                                   GLbyte blue, GLbyte alpha )
    void glColor4d( GLdouble red, GLdouble green,
                                   GLdouble blue, GLdouble alpha )
    void glColor4f( GLfloat red, GLfloat green,
                                   GLfloat blue, GLfloat alpha )
    void glColor4i( GLint red, GLint green,
                                   GLint blue, GLint alpha )
    void glColor4s( GLshort red, GLshort green,
                                   GLshort blue, GLshort alpha )
    void glColor4ub( GLubyte red, GLubyte green,
                                    GLubyte blue, GLubyte alpha )
    void glColor4ui( GLuint red, GLuint green,
                                    GLuint blue, GLuint alpha )
    void glColor4us( GLushort red, GLushort green,
                                    GLushort blue, GLushort alpha )


    void glColor3bv( GLbyte *v )
    void glColor3dv( GLdouble *v )
    void glColor3fv( GLfloat *v )
    void glColor3iv( GLint *v )
    void glColor3sv( GLshort *v )
    void glColor3ubv( GLubyte *v )
    void glColor3uiv( GLuint *v )
    void glColor3usv( GLushort *v )

    void glColor4bv( GLbyte *v )
    void glColor4dv( GLdouble *v )
    void glColor4fv( GLfloat *v )
    void glColor4iv( GLint *v )
    void glColor4sv( GLshort *v )
    void glColor4ubv( GLubyte *v )
    void glColor4uiv( GLuint *v )
    void glColor4usv( GLushort *v )


    void glTexCoord1d( GLdouble s )
    void glTexCoord1f( GLfloat s )
    void glTexCoord1i( GLint s )
    void glTexCoord1s( GLshort s )

    void glTexCoord2d( GLdouble s, GLdouble t )
    void glTexCoord2f( GLfloat s, GLfloat t )
    void glTexCoord2i( GLint s, GLint t )
    void glTexCoord2s( GLshort s, GLshort t )

    void glTexCoord3d( GLdouble s, GLdouble t, GLdouble r )
    void glTexCoord3f( GLfloat s, GLfloat t, GLfloat r )
    void glTexCoord3i( GLint s, GLint t, GLint r )
    void glTexCoord3s( GLshort s, GLshort t, GLshort r )

    void glTexCoord4d( GLdouble s, GLdouble t, GLdouble r, GLdouble q )
    void glTexCoord4f( GLfloat s, GLfloat t, GLfloat r, GLfloat q )
    void glTexCoord4i( GLint s, GLint t, GLint r, GLint q )
    void glTexCoord4s( GLshort s, GLshort t, GLshort r, GLshort q )

    void glTexCoord1dv( GLdouble *v )
    void glTexCoord1fv( GLfloat *v )
    void glTexCoord1iv( GLint *v )
    void glTexCoord1sv( GLshort *v )

    void glTexCoord2dv( GLdouble *v )
    void glTexCoord2fv( GLfloat *v )
    void glTexCoord2iv( GLint *v )
    void glTexCoord2sv( GLshort *v )

    void glTexCoord3dv( GLdouble *v )
    void glTexCoord3fv( GLfloat *v )
    void glTexCoord3iv( GLint *v )
    void glTexCoord3sv( GLshort *v )

    void glTexCoord4dv( GLdouble *v )
    void glTexCoord4fv( GLfloat *v )
    void glTexCoord4iv( GLint *v )
    void glTexCoord4sv( GLshort *v )


    void glRasterPos2d( GLdouble x, GLdouble y )
    void glRasterPos2f( GLfloat x, GLfloat y )
    void glRasterPos2i( GLint x, GLint y )
    void glRasterPos2s( GLshort x, GLshort y )

    void glRasterPos3d( GLdouble x, GLdouble y, GLdouble z )
    void glRasterPos3f( GLfloat x, GLfloat y, GLfloat z )
    void glRasterPos3i( GLint x, GLint y, GLint z )
    void glRasterPos3s( GLshort x, GLshort y, GLshort z )

    void glRasterPos4d( GLdouble x, GLdouble y, GLdouble z, GLdouble w )
    void glRasterPos4f( GLfloat x, GLfloat y, GLfloat z, GLfloat w )
    void glRasterPos4i( GLint x, GLint y, GLint z, GLint w )
    void glRasterPos4s( GLshort x, GLshort y, GLshort z, GLshort w )

    void glRasterPos2dv( GLdouble *v )
    void glRasterPos2fv( GLfloat *v )
    void glRasterPos2iv( GLint *v )
    void glRasterPos2sv( GLshort *v )

    void glRasterPos3dv( GLdouble *v )
    void glRasterPos3fv( GLfloat *v )
    void glRasterPos3iv( GLint *v )
    void glRasterPos3sv( GLshort *v )

    void glRasterPos4dv( GLdouble *v )
    void glRasterPos4fv( GLfloat *v )
    void glRasterPos4iv( GLint *v )
    void glRasterPos4sv( GLshort *v )


    void glRectd( GLdouble x1, GLdouble y1, GLdouble x2, GLdouble y2 )
    void glRectf( GLfloat x1, GLfloat y1, GLfloat x2, GLfloat y2 )
    void glRecti( GLint x1, GLint y1, GLint x2, GLint y2 )
    void glRects( GLshort x1, GLshort y1, GLshort x2, GLshort y2 )


    void glRectdv( GLdouble *v1, GLdouble *v2 )
    void glRectfv( GLfloat *v1, GLfloat *v2 )
    void glRectiv( GLint *v1, GLint *v2 )
    void glRectsv( GLshort *v1, GLshort *v2 )

    
    # Vertex Arrays  (1.1)

    void glVertexPointer( GLint size, GLenum type,
                                       GLsizei stride, GLvoid *ptr )

    void glNormalPointer( GLenum type, GLsizei stride,
                                       GLvoid *ptr )

    void glColorPointer( GLint size, GLenum type,
                                      GLsizei stride, GLvoid *ptr )

    void glIndexPointer( GLenum type, GLsizei stride,
                                      GLvoid *ptr )

    void glTexCoordPointer( GLint size, GLenum type,
                                         GLsizei stride, GLvoid *ptr )

    void glEdgeFlagPointer( GLsizei stride, GLvoid *ptr )

    void glGetPointerv( GLenum pname, GLvoid **params )

    void glArrayElement( GLint i )

    void glDrawArrays( GLenum mode, GLint first, GLsizei count )

    void glDrawElements( GLenum mode, GLsizei count,
                                      GLenum type, GLvoid *indices )

    void glInterleavedArrays( GLenum format, GLsizei stride,
                                           GLvoid *pointer )

   
    # Lighting

    void glShadeModel( GLenum mode )

    void glLightf( GLenum light, GLenum pname, GLfloat param )
    void glLighti( GLenum light, GLenum pname, GLint param )
    void glLightfv( GLenum light, GLenum pname,
                                 GLfloat *params )
    void glLightiv( GLenum light, GLenum pname,
                                 GLint *params )

    void glGetLightfv( GLenum light, GLenum pname,
                                    GLfloat *params )
    void glGetLightiv( GLenum light, GLenum pname,
                                    GLint *params )

    void glLightModelf( GLenum pname, GLfloat param )
    void glLightModeli( GLenum pname, GLint param )
    void glLightModelfv( GLenum pname, GLfloat *params )
    void glLightModeliv( GLenum pname, GLint *params )

    void glMaterialf( GLenum face, GLenum pname, GLfloat param )
    void glMateriali( GLenum face, GLenum pname, GLint param )
    void glMaterialfv( GLenum face, GLenum pname, GLfloat *params )
    void glMaterialiv( GLenum face, GLenum pname, GLint *params )

    void glGetMaterialfv( GLenum face, GLenum pname, GLfloat *params )
    void glGetMaterialiv( GLenum face, GLenum pname, GLint *params )

    void glColorMaterial( GLenum face, GLenum mode )


    # Raster functions

    void glPixelZoom( GLfloat xfactor, GLfloat yfactor )

    void glPixelStoref( GLenum pname, GLfloat param )
    void glPixelStorei( GLenum pname, GLint param )

    void glPixelTransferf( GLenum pname, GLfloat param )
    void glPixelTransferi( GLenum pname, GLint param )

    void glPixelMapfv( GLenum map, GLsizei mapsize,
                                    GLfloat *values )
    void glPixelMapuiv( GLenum map, GLsizei mapsize,
                                     GLuint *values )
    void glPixelMapusv( GLenum map, GLsizei mapsize,
                                     GLushort *values )

    void glGetPixelMapfv( GLenum map, GLfloat *values )
    void glGetPixelMapuiv( GLenum map, GLuint *values )
    void glGetPixelMapusv( GLenum map, GLushort *values )

    void glBitmap( GLsizei width, GLsizei height,
                                GLfloat xorig, GLfloat yorig,
                                GLfloat xmove, GLfloat ymove,
                                GLubyte *bitmap )

    void glReadPixels( GLint x, GLint y,
                                    GLsizei width, GLsizei height,
                                    GLenum format, GLenum type,
                                    GLvoid *pixels )

    void glDrawPixels( GLsizei width, GLsizei height,
                                    GLenum format, GLenum type,
                                    GLvoid *pixels )

    void glCopyPixels( GLint x, GLint y,
                                    GLsizei width, GLsizei height,
                                    GLenum type )


    # Stenciling

    void glStencilFunc( GLenum func, GLint ref, GLuint mask )

    void glStencilMask( GLuint mask )

    void glStencilOp( GLenum fail, GLenum zfail, GLenum zpass )

    void glClearStencil( GLint s )



    # Texture mapping

    void glTexGend( GLenum coord, GLenum pname, GLdouble param )
    void glTexGenf( GLenum coord, GLenum pname, GLfloat param )
    void glTexGeni( GLenum coord, GLenum pname, GLint param )

    void glTexGendv( GLenum coord, GLenum pname, GLdouble *params )
    void glTexGenfv( GLenum coord, GLenum pname, GLfloat *params )
    void glTexGeniv( GLenum coord, GLenum pname, GLint *params )

    void glGetTexGendv( GLenum coord, GLenum pname, GLdouble *params )
    void glGetTexGenfv( GLenum coord, GLenum pname, GLfloat *params )
    void glGetTexGeniv( GLenum coord, GLenum pname, GLint *params )


    void glTexEnvf( GLenum target, GLenum pname, GLfloat param )
    void glTexEnvi( GLenum target, GLenum pname, GLint param )

    void glTexEnvfv( GLenum target, GLenum pname, GLfloat *params )
    void glTexEnviv( GLenum target, GLenum pname, GLint *params )

    void glGetTexEnvfv( GLenum target, GLenum pname, GLfloat *params )
    void glGetTexEnviv( GLenum target, GLenum pname, GLint *params )


    void glTexParameterf( GLenum target, GLenum pname, GLfloat param )
    void glTexParameteri( GLenum target, GLenum pname, GLint param )

    void glTexParameterfv( GLenum target, GLenum pname,
                                          GLfloat *params )
    void glTexParameteriv( GLenum target, GLenum pname,
                                          GLint *params )

    void glGetTexParameterfv( GLenum target,
                                           GLenum pname, GLfloat *params)
    void glGetTexParameteriv( GLenum target,
                                           GLenum pname, GLint *params )

    void glGetTexLevelParameterfv( GLenum target, GLint level,
                                                GLenum pname, GLfloat *params )
    void glGetTexLevelParameteriv( GLenum target, GLint level,
                                                GLenum pname, GLint *params )


    void glTexImage1D( GLenum target, GLint level,
                                    GLint internalFormat,
                                    GLsizei width, GLint border,
                                    GLenum format, GLenum type,
                                    GLvoid *pixels )

    void glTexImage2D( GLenum target, GLint level,
                                    GLint internalFormat,
                                    GLsizei width, GLsizei height,
                                    GLint border, GLenum format, GLenum type,
                                    GLvoid *pixels )

    void glGetTexImage( GLenum target, GLint level,
                                     GLenum format, GLenum type,
                                     GLvoid *pixels )


    # 1.1 functions 

    void glGenTextures( GLsizei n, GLuint *textures )

    void glDeleteTextures( GLsizei n, GLuint *textures)

    void glBindTexture( GLenum target, GLuint texture )

    void glPrioritizeTextures( GLsizei n,
                                            GLuint *textures,
                                            GLclampf *priorities )

    GLboolean glAreTexturesResident( GLsizei n,
                                                  GLuint *textures,
                                                  GLboolean *residences )

    GLboolean glIsTexture( GLuint texture )


    void glTexSubImage1D( GLenum target, GLint level,
                                       GLint xoffset,
                                       GLsizei width, GLenum format,
                                       GLenum type, GLvoid *pixels )


    void glTexSubImage2D( GLenum target, GLint level,
                                       GLint xoffset, GLint yoffset,
                                       GLsizei width, GLsizei height,
                                       GLenum format, GLenum type,
                                       GLvoid *pixels )


    void glCopyTexImage1D( GLenum target, GLint level,
                                        GLenum internalformat,
                                        GLint x, GLint y,
                                        GLsizei width, GLint border )


    void glCopyTexImage2D( GLenum target, GLint level,
                                        GLenum internalformat,
                                        GLint x, GLint y,
                                        GLsizei width, GLsizei height,
                                        GLint border )


    void glCopyTexSubImage1D( GLenum target, GLint level,
                                           GLint xoffset, GLint x, GLint y,
                                           GLsizei width )


    void glCopyTexSubImage2D( GLenum target, GLint level,
                                           GLint xoffset, GLint yoffset,
                                           GLint x, GLint y,
                                           GLsizei width, GLsizei height )


    # Evaluators

    void glMap1d( GLenum target, GLdouble u1, GLdouble u2,
                               GLint stride,
                               GLint order, GLdouble *points )
    void glMap1f( GLenum target, GLfloat u1, GLfloat u2,
                               GLint stride,
                               GLint order, GLfloat *points )

    void glMap2d( GLenum target,
		     GLdouble u1, GLdouble u2, GLint ustride, GLint uorder,
		     GLdouble v1, GLdouble v2, GLint vstride, GLint vorder,
		     GLdouble *points )
    void glMap2f( GLenum target,
		     GLfloat u1, GLfloat u2, GLint ustride, GLint uorder,
		     GLfloat v1, GLfloat v2, GLint vstride, GLint vorder,
		     GLfloat *points )

    void glGetMapdv( GLenum target, GLenum query, GLdouble *v )
    void glGetMapfv( GLenum target, GLenum query, GLfloat *v )
    void glGetMapiv( GLenum target, GLenum query, GLint *v )

    void glEvalCoord1d( GLdouble u )
    void glEvalCoord1f( GLfloat u )

    void glEvalCoord1dv( GLdouble *u )
    void glEvalCoord1fv( GLfloat *u )

    void glEvalCoord2d( GLdouble u, GLdouble v )
    void glEvalCoord2f( GLfloat u, GLfloat v )

    void glEvalCoord2dv( GLdouble *u )
    void glEvalCoord2fv( GLfloat *u )

    void glMapGrid1d( GLint un, GLdouble u1, GLdouble u2 )
    void glMapGrid1f( GLint un, GLfloat u1, GLfloat u2 )

    void glMapGrid2d( GLint un, GLdouble u1, GLdouble u2,
                                   GLint vn, GLdouble v1, GLdouble v2 )
    void glMapGrid2f( GLint un, GLfloat u1, GLfloat u2,
                                   GLint vn, GLfloat v1, GLfloat v2 )

    void glEvalPoint1( GLint i )

    void glEvalPoint2( GLint i, GLint j )

    void glEvalMesh1( GLenum mode, GLint i1, GLint i2 )

    void glEvalMesh2( GLenum mode, GLint i1, GLint i2, GLint j1, GLint j2 )



    # Fog

    void glFogf( GLenum pname, GLfloat param )

    void glFogi( GLenum pname, GLint param )

    void glFogfv( GLenum pname, GLfloat *params )

    void glFogiv( GLenum pname, GLint *params )



    # Selection and Feedback

    void glFeedbackBuffer( GLsizei size, GLenum type, GLfloat *buffer )

    void glPassThrough( GLfloat token )

    void glSelectBuffer( GLsizei size, GLuint *buffer )

    void glInitNames( )

    void glLoadName( GLuint name )

    void glPushName( GLuint name )

    void glPopName( )


