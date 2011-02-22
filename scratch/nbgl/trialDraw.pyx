from nbglutManager cimport *

cimport windowLinkedList

    

# Global Variables Private 
cdef float angle = 30.0
cdef float cameraAngle = 0.0

# Initializes 3D rendering 
cdef void initRendering():
    glEnable(GL_DEPTH_TEST)

# Called when the window is resized 
cdef void handleResize(int w, int h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, <double> w / <double> h, 1.0, 200.0)
    glMatrixMode(GL_MODELVIEW)

# Called when a key is pressed 
cdef void handleKeypress(unsigned char key, int x, int y):
    if (key == 27): # Escape key 
        _sendDestroyMessageToWindow(glutGetWindow())
    
# Draws the 3D scene 
cdef void drawScene1():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
    glMatrixMode(GL_MODELVIEW) # Switch to the drawing perspective 
    glLoadIdentity() # Reset the drawing perspective 
    glRotatef(-cameraAngle, 0.0, 1.0, 0.0) # Rotate the camera 
    glTranslatef(0.0, 0.0, -5.0) # Move forward 5 units 
	
    glPushMatrix() # Save the transformations performed thus far 
    glTranslatef(0.0, -1.0, 0.0) # Move to the center of the trapezoid 
    glRotatef(angle, 0.0, 0.0, 1.0) # Rotate about the z-axis 
	
    glBegin(GL_QUADS)
	
    # Trapezoid 
    glVertex3f(-0.7, -0.5, 0.0)
    glVertex3f(0.7, -0.5, 0.0)
    glVertex3f(0.4, 0.5, 0.0)
    glVertex3f(-0.4, 0.5, 0.0)
	
    glEnd()
	
    glPopMatrix() # Undo the move to the center of the trapezoid 
    glPushMatrix() # Save the current state of transformations 
    glTranslatef(1.0, 1.0, 0.0) # Move to the center of the pentagon 
    glRotatef(angle, 0.0, 1.0, 0.0) # Rotate about the y-axis 
    glScalef(0.7, 0.7, 0.7) # Scale by 0.7 in the x, y, and z directions 
	
    glBegin(GL_TRIANGLES)
	
    # Pentagon
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f(0.5, -0.5, 0.0)
    glVertex3f(-0.5, 0.0, 0.0)
	
    glVertex3f(-0.5, 0.0, 0.0)
    glVertex3f(0.5, -0.5, 0.0)
    glVertex3f(0.5, 0.0, 0.0)
	
    glVertex3f(-0.5, 0.0, 0.0)
    glVertex3f(0.5, 0.0, 0.0)
    glVertex3f(0.0, 0.5, 0.0)
	
    glEnd()
	
    glPopMatrix() # Undo the move to the center of the pentagon 
    glPushMatrix() # Save the current state of transformations 
    glTranslatef(-1.0, 1.0, 0.0) # Move to the center of the triangle 
    glRotatef(angle, 1.0, 2.0, 3.0) # Rotate about the the vector (1, 2, 3) 
	
    glBegin(GL_TRIANGLES)
	
    # Triangle 
    glVertex3f(0.5, -0.5, 0.0)
    glVertex3f(0.0, 0.5, 0.0)
    glVertex3f(-0.5, -0.5, 0.0)
	
    glEnd()
	
    glPopMatrix() # Undo the move to the center of the triangle 
	
    glutSwapBuffers()


# Draws the 3D scene 
cdef void drawScene2():
    glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
 
    gluLookAt(5.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
	
 
    # Draw the cube, rotated and scaled. 
    glPushMatrix()
    glTranslatef(-1.0, 0.0, 0.0)
	
    glRotatef(angle, 0.0, 0.0, 1.0)
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


cdef void update(int arg):
    global angle

    angle += 2.0
    if (angle > 360): 
        angle -= 360
	
    cdef WindowInfo* windowInfo = windowLinkedList.first()

    while(windowInfo != NULL):
        glutSetWindow(windowInfo.id) # This is important 
        glutPostRedisplay() # Tell GLUT that the display has changed 
        windowInfo = windowLinkedList.next()
    
    # Tell GLUT to call update again in 25 milliseconds 
    glutTimerFunc(25, update, 0)


   
    






