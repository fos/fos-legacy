from glHeaders cimport *
from gluHeaders cimport *
from freeglutHeaders cimport *
from nbglutManager cimport Manager, _getManager, _lockMutexWindowList, _unlockMutexWindowList

cdef double myangle = 30.0

cdef class FosWindow:

    def __init__(self, bgcolor=None, **kwargs):
        """ Create a FosWindow. All parameters are optional.
        
        Parameters
        ----------
        `bgcolor` : tuple
            Specify the background color as 4-tuple with values
            between 0 and 1
        `width` : int
            Width of the window, in pixels.  Defaults to 640, or the
            screen width if `fullscreen` is True.
        `height` : int
            Height of the window, in pixels.  Defaults to 480, or the
            screen height if `fullscreen` is True.
        `caption` : str or unicode
            Initial caption (title) of the window.  Defaults to
            ``sys.argv[0]``.
        `fullscreen` : bool
            If True, the window will cover the entire screen rather
            than floating.  Defaults to False.
        `visible` : bool
            Determines if the window is visible immediately after
            creation.  Defaults to True.  Set this to False if you
            would like to change attributes of the window before
            having it appear to the user.
            
        
        
        self.update_dt = 1.0/60
        
        if bgcolor == None:
            self.bgcolor = color.black
        else:
            self.bgcolor = bgcolor        
        
        self.mouse_x, self.mouse_y = 0,0
        
        # create an empty world by default
        emptyworld = World("Zero-Point World")
        self.attach(emptyworld)
        
        # the frame rate display from fos.lib.pyglet
        #self.fps_display = FPSDisplay(self)
        #self.foslabel = WindowText(self, 'fos', x=10 , y=40)
        #self.show_logos = False
        """
        self.angle = 0.0
        
        
    cdef void setup(self):           
        '''        
        r,g,b,a = self.bgcolor
        glClearColor(r,g,b,a)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        return
        '''
        glEnable(GL_DEPTH_TEST)   
       

    def update(self, dt):
        self.angle += 2.0
        if (self.angle > 360): 
            self.angle -= 360

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
 
        gluLookAt(5.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
	
 
        # Draw the cube, rotated and scaled. 
        glPushMatrix()
        glTranslatef(-1.0, 0.0, 0.0)
	
        glRotatef(self.angle, 0.0, 0.0, 1.0)
        glColor3f(0.8, 0.0, 0.8)
        glutWireCube(2.0)
        glPopMatrix()
 
        # Draw thre cone, rotated and scaled.
        glPushMatrix()
        glTranslatef(1.0, 0.0, 0.0)
        glRotatef(90.0, 1.0, 0.0, 0.0)
        glRotatef(90.0, 0.0, 1.0, 0.0)

        glTranslatef(0.0, 0.0, -1.0)
        glColor3f(0.0, 0.8, 0.8)
        glutWireCone(1.0, 3.0, 10, 10)
        glPopMatrix()
        glutSwapBuffers()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, <double> width / <double> height, 1.0, 200.0)
        glMatrixMode(GL_MODELVIEW)

    def on_key_press(self, symbol, modifiers):
        pass
     

'''    def set_current_camera(self, cam):
        """ Set the current camera to cam for this window
        
        Parameters
        ----------
        cam : Camera
            The camera object
        """
        
        if cam in self._world.cl.cameras:
            self.current_camera = cam
        else:
            print "camera not found in this world"
            
    def update(self, dt):
        # update the actors
        for a in self._world.ag.actors:
            try:
                a.update(dt)
            except:
                pass
            
        # update the cameras
        for c in self._world.cl.cameras:
            try:
                c.update(dt)
            except:
                pass
         
#        if dt != 0:
#            print "freq", round(1.0/dt)
#            pass

    def get_world(self):
        """ Returns the world that is attached to this window """
        return self._world
    
    def attach(self, world):
        """ Attach a FosWindow to a world. The world needs
        to have at least one camera. The first camera is used
        for the window. You can change the camera for a window
        by using set_current_camera()
        
        """
        #world._render_lock.acquire()
        
        # can not attach a window to a world that has not cameras
        if len(world.get_cameras()) == 0:
            raise Exception("Can not attach window to a world with no cameras")
        
        # attach the world as a private attribute
        self._world = world
        
        # add the world to the list of windows the world is attached to
        self._world.wins.append(self)
        
        # just take the first camera
        self.current_camera = self._world.get_cameras()[0]
        
        #world._render_lock.release()
            
    def draw(self):   
        self._world._render_lock.acquire()
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
        self.current_camera.draw()
    
        for a in self._world.ag.actors:
            try:
                a.draw()
            except:
                pass
        
        if self.show_logos:
            self.fps_display.draw()
            self.foslabel.draw()

        self._world._render_lock.release()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60., width / float(height), .1, 2000.)
        glMatrixMode(GL_MODELVIEW)

    def on_key_press(self, symbol, modifiers):

        # how to propagate the events to the actors and camera?
            
        if symbol == key.R:
            self.window.current_camera.reset()
        
        if symbol == key.H:
            self.window.set_size(1000, 600)
            
        if modifiers & key.MOD_CTRL:
            # make window bigger
            if symbol == key.PLUS:
                neww = self.window.width + self.window.width / 10
                newh = self.window.height + self.window.height / 10
                self.window.set_size(neww, newh)
            # make window smaller
            elif symbol == key.MINUS:
                neww = self.window.width - self.window.width / 10
                newh = self.window.height - self.window.height / 10
                self.window.set_size(neww, newh)
                 
        if symbol == key.P:          
            # generate pickray
            x,y=self.window.mouse_x,self.window.mouse_y
            nx,ny,nz=screen_to_model(x,y,0)
            fx,fy,fz=screen_to_model(x,y,1)        
            near=(nx,ny,nz)
            far=(fx,fy,fz)
            self.window._world.propagate_pickray(near, far)
            
        # with s, select and actor and focus the camera, make the aabb glowing,
        # d to deselect, push new set of events for this actor 
        if symbol == key.S:          
            # select aabb
            x,y=self.window.mouse_x,self.window.mouse_y
            nx,ny,nz=screen_to_model(x,y,0)
            fx,fy,fz=screen_to_model(x,y,1)        
            near=(nx,ny,nz)
            far=(fx,fy,fz)
            found_actor = self.window._world.find_selected_actor(near, far)
            if not found_actor is None:
                print "found an actor that was selected"
                found_actor.show_aabb = not found_actor.show_aabb
                # get the center of the aabb
                ax,ay,az = found_actor.aabb.get_center()
                print "ax,az", ax, ay, az
                self.window.current_camera.set_lookatposition(ax,ay,az)
            else:
                print "no actor found"
'''        

cdef void reshapeFunc(int width, int height):
    '''cdef id = glutGetWindow()
    
    _lockMutexWindowList() 
    cdef FosWindow fosWindow = _findFosWindow(id)    
    _unlockMutexWindowList()  
    if (fosWindow == None):
        return

    fosWindow.on_resize(width, height)
    '''

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, <double> width / <double> height, 1.0, 200.0)
    glMatrixMode(GL_MODELVIEW)

cdef void keyboardFunc(unsigned char key, int x, int y):
    #cdef id = glutGetWindow()
    
    #_lockMutexWindowList() 
    #cdef FosWindow fosWindow = _findFosWindow(id)    
    #_unlockMutexWindowList()
    #if (fosWindow == None):
    #    return

    #fosWindow.on_key_press(symbol, modifiers) ???
    pass

cdef void displayFunc():
    global myangle

    #cdef id = glutGetWindow()
    
    #_lockMutexWindowList() 
    #cdef FosWindow fosWindow = _findFosWindow(id)    
    #_unlockMutexWindowList()
    #if (fosWindow == None):
    #    return

    #fosWindow.draw()

    glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
 
    gluLookAt(5.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
	
 
    # Draw the cube, rotated and scaled. 
    glPushMatrix()
    glTranslatef(-1.0, 0.0, 0.0)
	
    glRotatef(30.0, 0.0, 0.0, 1.0)
    glColor3f(0.8, 0.0, 0.8)
    glutWireCube(2.0)
    glPopMatrix()
 
    # Draw thre cone, rotated and scaled.
    glPushMatrix()
    glTranslatef(1.0, 0.0, 0.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)

    glTranslatef(0.0, 0.0, -1.0)
    glColor3f(0.0, 0.8, 0.8)
    glutWireCone(1.0, 3.0, 10, 10)
    glPopMatrix()
    glutSwapBuffers()


cdef void update(int dt):
    global myangle
 
    cdef Manager manager
    cdef FosWindow fosWindow
    cdef int i    

    manager = _getManager()

    myangle += 2.0
    if (myangle > 360): 
        myangle -= 360

    _lockMutexWindowList()

    for i from 0 <= i < len(manager.windowList):
        fosWindow = manager.windowList[i]
        #fosWindow.update(dt)
        glutSetWindow(fosWindow.id) # This is important 
        glutPostRedisplay() # Tell GLUT that the display has changed 

    _unlockMutexWindowList() 

    # Tell GLUT to call update again in dt milliseconds 
    glutTimerFunc(dt, update, dt)

   
