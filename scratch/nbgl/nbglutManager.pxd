cdef struct WindowInfo:
    int id
    char title[256]
    int x
    int y
    int w
    int h
    void* data    
    void (*initRendering)()
    void (*handleResize)(int w, int h)
    void (*handleKeypress)(unsigned char key, int x, int y)
    void (*drawScene)()
    void (*update)(int arg)

cdef struct RequestInfo:
    int request
    WindowInfo* data 

cdef void _sendDestroyMessageToWindow(int id)

cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void *malloc(size_t size)
    void free(void *pointer)

cdef extern from "pthread.h":
    ctypedef void *pthread_t
    int pthread_create(pthread_t *thread, void *attr,void *(*start_routine)(void*), void *arg)
    int pthread_join(pthread_t, void **)


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

    # Matrix Mode 
    int GL_MATRIX_MODE
    int GL_MODELVIEW
    int GL_PROJECTION
    int GL_TEXTURE

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


cdef extern from "GL/glu.h":
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


cdef extern from "GL/freeglut.h":
    # GLUT API macro definitions -- the display mode definitions
    int GLUT_RGB
    int GLUT_RGBA
    int GLUT_INDEX
    int GLUT_SINGLE
    int GLUT_DOUBLE
    int GLUT_ACCUM
    int GLUT_ALPHA
    int GLUT_DEPTH
    int GLUT_STENCIL
    int GLUT_MULTISAMPLE
    int GLUT_STEREO
    int GLUT_LUMINANCE


    # Additional GLUT Key definitions for the Special key function
    int GLUT_KEY_NUM_LOCK
    int GLUT_KEY_BEGIN
    int GLUT_KEY_DELETE

    # GLUT API Extension macro definitions -- behaviour when the user clicks on an "x" to close a window
    int GLUT_ACTION_EXIT
    int GLUT_ACTION_GLUTMAINLOOP_RETURNS
    int GLUT_ACTION_CONTINUE_EXECUTION

    # Create a new rendering context when the user opens a new window?
    int GLUT_CREATE_NEW_CONTEXT
    int GLUT_USE_CURRENT_CONTEXT

    # GLUT API Extension macro definitions -- the glutGet parameters
    int GLUT_INIT_STATE
    int GLUT_ACTION_ON_WINDOW_CLOSE
    int GLUT_WINDOW_BORDER_WIDTH
    int GLUT_WINDOW_HEADER_HEIGHT
    int GLUT_VERSION
    int GLUT_RENDERING_CONTEXT
    int GLUT_DIRECT_RENDERING
    int GLUT_FULL_SCREEN

    # Initialization functions, see fglut_init.c
    void glutInit( int* pargc, char** argv )
    void glutInitWindowPosition( int x, int y )
    void glutInitWindowSize( int width, int height )
    void glutInitDisplayMode( unsigned int displayMode )
    void glutInitDisplayString( char* displayMode )

    # Process loop function, see freeglut_main.c
    void glutMainLoop( )

    # Window management functions, see freeglut_window.c
    int  glutCreateWindow( char* title )
    int  glutCreateSubWindow( int window, int x, int y, int width, int height )
    void glutDestroyWindow( int window )
    void glutSetWindow( int window )
    int  glutGetWindow( )
    void glutSetWindowTitle( char* title )
    void glutSetIconTitle( char* title )
    void glutReshapeWindow( int width, int height )
    void glutPositionWindow( int x, int y )
    void glutShowWindow( )
    void glutHideWindow( )
    void glutIconifyWindow( )
    void glutPushWindow( )
    void glutPopWindow( )
    void glutFullScreen( )

    # Display-connected functions, see freeglut_display.c
    void glutPostWindowRedisplay( int window )
    void glutPostRedisplay( )
    void glutSwapBuffers( )

    # Mouse cursor functions, see freeglut_cursor.c
    void glutWarpPointer( int x, int y )
    void glutSetCursor( int cursor )

    # Overlay stuff, see freeglut_overlay.c
    void glutEstablishOverlay( )
    void glutRemoveOverlay( )
    void glutUseLayer( GLenum layer )
    void glutPostOverlayRedisplay( )
    void glutPostWindowOverlayRedisplay( int window )
    void glutShowOverlay( )
    void glutHideOverlay( )

    # Menu stuff, see freeglut_menu.c
    int  glutCreateMenu( void (* callback)( int menu ) )
    void glutDestroyMenu( int menu )
    int  glutGetMenu( )
    void glutSetMenu( int menu )
    void glutAddMenuEntry( char* label, int value )
    void glutAddSubMenu( char* label, int subMenu )
    void glutChangeToMenuEntry( int item, char* label, int value )
    void glutChangeToSubMenu( int item, char* label, int value )
    void glutRemoveMenuItem( int item )
    void glutAttachMenu( int button )
    void glutDetachMenu( int button )

    # Global callback functions, see freeglut_callbacks.c
    void glutTimerFunc( unsigned int time, void (* callback)( int ), int value )
    void glutIdleFunc( void (* callback)( ) )

    # Window-specific callback functions, see freeglut_callbacks.c
    void glutKeyboardFunc( void (* callback)( unsigned char, int, int ) )
    void glutSpecialFunc( void (* callback)( int, int, int ) )
    void glutReshapeFunc( void (* callback)( int, int ) )
    void glutVisibilityFunc( void (* callback)( int ) )
    void glutDisplayFunc( void (* callback)( ) )
    void glutMouseFunc( void (* callback)( int, int, int, int ) )
    void glutMotionFunc( void (* callback)( int, int ) )
    void glutPassiveMotionFunc( void (* callback)( int, int ) )
    void glutEntryFunc( void (* callback)( int ) )

    void glutKeyboardUpFunc( void (* callback)( unsigned char, int, int ) )
    void glutSpecialUpFunc( void (* callback)( int, int, int ) )
    void glutJoystickFunc( void (* callback)( unsigned int, int, int, int ), int pollInterval )
    void glutMenuStateFunc( void (* callback)( int ) )
    void glutMenuStatusFunc( void (* callback)( int, int, int ) )
    void glutOverlayDisplayFunc( void (* callback)( ) )
    void glutWindowStatusFunc( void (* callback)( int ) )

    void glutSpaceballMotionFunc( void (* callback)( int, int, int ) )
    void glutSpaceballRotateFunc( void (* callback)( int, int, int ) )
    void glutSpaceballButtonFunc( void (* callback)( int, int ) )
    void glutButtonBoxFunc( void (* callback)( int, int ) )
    void glutDialsFunc( void (* callback)( int, int ) )
    void glutTabletMotionFunc( void (* callback)( int, int ) )
    void glutTabletButtonFunc( void (* callback)( int, int, int, int ) )

    # State setting and retrieval functions, see freeglut_state.c
    int  glutGet( GLenum query )
    int  glutDeviceGet( GLenum query )
    int  glutGetModifiers( )
    int  glutLayerGet( GLenum query )

    # Font stuff, see freeglut_font.c
    void glutBitmapCharacter( void* font, int character )
    int  glutBitmapWidth( void* font, int character )
    void glutStrokeCharacter( void* font, int character )
    int  glutStrokeWidth( void* font, int character )
    int  glutBitmapLength( void* font, unsigned char* string )
    int  glutStrokeLength( void* font, unsigned char* string )

    # Geometry functions, see freeglut_geometry.c
    void glutWireCube( GLdouble size )
    void glutSolidCube( GLdouble size )
    void glutWireSphere( GLdouble radius, GLint slices, GLint stacks )
    void glutSolidSphere( GLdouble radius, GLint slices, GLint stacks )
    void glutWireCone( GLdouble base, GLdouble height, GLint slices, GLint stacks )
    void glutSolidCone( GLdouble base, GLdouble height, GLint slices, GLint stacks )

    void glutWireTorus( GLdouble innerRadius, GLdouble outerRadius, GLint sides, GLint rings )
    void glutSolidTorus( GLdouble innerRadius, GLdouble outerRadius, GLint sides, GLint rings )
    void glutWireDodecahedron( )
    void glutSolidDodecahedron( )
    void glutWireOctahedron( )
    void glutSolidOctahedron( )
    void glutWireTetrahedron( )
    void glutSolidTetrahedron( )
    void glutWireIcosahedron( )
    void glutSolidIcosahedron( )

    # Teapot rendering functions, found in freeglut_teapot.c
    void glutWireTeapot( GLdouble size )
    void glutSolidTeapot( GLdouble size )

    # Game mode functions, see freeglut_gamemode.c
    void glutGameModeString( char* string )
    int  glutEnterGameMode( )
    void glutLeaveGameMode( )
    int  glutGameModeGet( GLenum query )

    # Video resize functions, see freeglut_videoresize.c
    int  glutVideoResizeGet( GLenum query )
    void glutSetupVideoResizing( )
    void glutStopVideoResizing( )
    void glutVideoResize( int x, int y, int width, int height )
    void glutVideoPan( int x, int y, int width, int height )

    # Colormap functions, see freeglut_misc.c
    void glutSetColor( int color, GLfloat red, GLfloat green, GLfloat blue )
    GLfloat glutGetColor( int color, int component )
    void glutCopyColormap( int window )

    # Misc keyboard and joystick functions, see freeglut_misc.c
    void glutIgnoreKeyRepeat( int ignore )
    void glutSetKeyRepeat( int repeatMode )
    void glutForceJoystickFunc( )

    # Misc functions, see freeglut_misc.c
    int  glutExtensionSupported( char* extension )
    void glutReportErrors( )

    # freeglut_ext.h
    # Process loop function, see freeglut_main.c
    void glutMainLoopEvent( )
    void glutLeaveMainLoop( )
    void glutExit         ( )

    # Window management functions, see freeglut_window.c
    void glutFullScreenToggle( )

    # Window-specific callback functions, see freeglut_callbacks.c
    void glutMouseWheelFunc( void (* callback)( int, int, int, int ) )
    void glutCloseFunc( void (* callback)( ) )
    void glutWMCloseFunc( void (* callback)( ) )
    # A. Donev: Also a destruction callback for menus 
    void glutMenuDestroyFunc( void (* callback)( ) )

    # State setting and retrieval functions, see freeglut_state.c
    void glutSetOption ( GLenum option_flag, int value )
    int*  glutGetModeValues(GLenum mode, int * size)
    # A.Donev: User-data manipulation 
    void* glutGetWindowData( )
    void glutSetWindowData(void* data)
    void* glutGetMenuData( )
    void glutSetMenuData(void* data)

    # Font stuff, see freeglut_font.c
    int  glutBitmapHeight( void* font )
    GLfloat glutStrokeHeight( void* font )
    void glutBitmapString( void* font, unsigned char *string )
    void glutStrokeString( void* font, unsigned char *string )

    # Geometry functions, see freeglut_geometry.c
    void glutWireRhombicDodecahedron( )
    void glutSolidRhombicDodecahedron( )
    void glutWireSierpinskiSponge ( int num_levels, GLdouble offset[3], GLdouble scale )
    void glutSolidSierpinskiSponge ( int num_levels, GLdouble offset[3], GLdouble scale )
    void glutWireCylinder( GLdouble radius, GLdouble height, GLint slices, GLint stacks)
    void glutSolidCylinder( GLdouble radius, GLdouble height, GLint slices, GLint stacks)

    # Extension functions, see freeglut_ext.c
    #typedef void (* GLUTproc)()
    #GLUTproc glutGetProcAddress( char *procName )

    # Initialization functions, see freeglut_init.c
    void glutInitContextVersion( int majorVersion, int minorVersion )
    void glutInitContextFlags( int flags )
    void glutInitContextProfile( int profile )

