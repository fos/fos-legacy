from glHeaders cimport *

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

