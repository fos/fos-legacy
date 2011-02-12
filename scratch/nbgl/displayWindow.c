#include "displayWindow.h"

#include <string.h>
#include <GL/gl.h>
#include <GL/freeglut.h>

/* Global Variables Exported */
int continueRunning = TRUE;
int changeRequest = FALSE;
int _request;
int numOpenWindows = 0;

Window window;

/* Global Variables Private */
float angle = 30.0;
float cameraAngle = 0.0;
pthread_t eventLoopThread = -1;
WindowIDP windowIDsList = NULL;


/* Initializes 3D rendering */
void initRendering() {
    glEnable(GL_DEPTH_TEST);
}

/* Called when the window is resized */
void handleResize(int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (double) w / (double) h, 1.0, 200.0);
    glMatrixMode(GL_MODELVIEW);
}

/* Called when a key is pressed */
void handleKeypress(unsigned char key, int x, int y) {
    if (key == 27) { /* Escape key */ 
        _destroyWindow();
    }
}
    
/* Draws the 3D scene */
void drawScene1() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	
    glMatrixMode(GL_MODELVIEW); /* Switch to the drawing perspective */
    glLoadIdentity(); /* Reset the drawing perspective */
    glRotatef(-cameraAngle, 0.0, 1.0, 0.0); /* Rotate the camera */
    glTranslatef(0.0, 0.0, -5.0); /* Move forward 5 units */
	
    glPushMatrix(); /* Save the transformations performed thus far */
    glTranslatef(0.0, -1.0, 0.0); /* Move to the center of the trapezoid */
    glRotatef(angle, 0.0, 0.0, 1.0); /* Rotate about the z-axis */
	
    glBegin(GL_QUADS);
	
    /* Trapezoid */
    glVertex3f(-0.7, -0.5, 0.0);
    glVertex3f(0.7, -0.5, 0.0);
    glVertex3f(0.4, 0.5, 0.0);
    glVertex3f(-0.4, 0.5, 0.0);
	
    glEnd();
	
    glPopMatrix(); /* Undo the move to the center of the trapezoid */
    glPushMatrix(); /* Save the current state of transformations */
    glTranslatef(1.0, 1.0, 0.0); /* Move to the center of the pentagon */
    glRotatef(angle, 0.0, 1.0, 0.0); /* Rotate about the y-axis */
    glScalef(0.7, 0.7, 0.7); /* Scale by 0.7 in the x, y, and z directions */
	
    glBegin(GL_TRIANGLES);
	
    /* Pentagon */
    glVertex3f(-0.5, -0.5, 0.0);
    glVertex3f(0.5, -0.5, 0.0);
    glVertex3f(-0.5, 0.0, 0.0);
	
    glVertex3f(-0.5, 0.0, 0.0);
    glVertex3f(0.5, -0.5, 0.0);
    glVertex3f(0.5, 0.0, 0.0);
	
    glVertex3f(-0.5, 0.0, 0.0);
    glVertex3f(0.5, 0.0, 0.0);
    glVertex3f(0.0, 0.5, 0.0);
	
    glEnd();
	
    glPopMatrix(); /* Undo the move to the center of the pentagon */
    glPushMatrix(); /* Save the current state of transformations */
    glTranslatef(-1.0, 1.0, 0.0); /* Move to the center of the triangle */
    glRotatef(angle, 1.0, 2.0, 3.0); /* Rotate about the the vector (1, 2, 3) */
	
    glBegin(GL_TRIANGLES);
	
    /* Triangle */
    glVertex3f(0.5, -0.5, 0.0);
    glVertex3f(0.0, 0.5, 0.0);
    glVertex3f(-0.5, -0.5, 0.0);
	
    glEnd();
	
    glPopMatrix(); /* Undo the move to the center of the triangle */
	
    glutSwapBuffers();
}

/* Draws the 3D scene */
void drawScene2() {
    glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
 
    gluLookAt(5.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
	
 
    /* Draw the cube, rotated and scaled. */
    glPushMatrix();
    glTranslatef(-1.0, 0.0, 0.0);
	
    glRotatef(angle, 0.0, 0.0, 1.0);
    glColor3f(0.8f, 0.0f, 0.8f);
    glutWireCube(2.0);
    glPopMatrix();
 
    /* Draw thre cone, rotated and scaled. */
    glPushMatrix();
    glTranslatef(1.0, 0.0, 0.0);
    glRotatef(90.0, 1.0, 0.0, 0.0);
    glRotatef(90.0, 0.0, 1.0, 0.0);

    glTranslatef(0.0, 0.0, -1.0);
    glColor3f(0.0f, 0.8f, 0.8f);
    glutWireCone(1.0, 3.0, 10, 10);
    glPopMatrix();
    glutSwapBuffers();
}

void update(int arg) {
    int id;

    angle += 2.0;
    if (angle > 360) 
        angle -= 360;
	
    WindowIDP curWindowIDP = windowIDsList;

    while(curWindowIDP != NULL) {
        glutSetWindow(curWindowIDP->id);    /* This is important */
        glutPostRedisplay(); /* Tell GLUT that the display has changed */
        curWindowIDP = curWindowIDP->next;
    }
    
    /* Tell GLUT to call update again in 25 milliseconds */
    glutTimerFunc(25, update, numOpenWindows);
}

void setWindowParameters(int id, char* title, int x, int y, int w, int h, int scn) {
    window.id = id;
    strcpy(window.title, title);
    window.x = x;
    window.y = y;
    window.w = w;
    window.h = h;
    window.initRendering = &initRendering;
    window.handleResize = &handleResize;
    window.handleKeypress = &handleKeypress;
    if (scn == 1)
        window.drawScene = &drawScene1;
    else 
        window.drawScene = &drawScene2; 
    window.update = &update;
}

void _createWindow() {
    glutInitWindowSize(window.w, window.h); 
    glutInitWindowPosition(window.x, window.y);

    WindowIDP windowIDP = (WindowIDP) malloc(sizeof(struct WindowID));
    windowIDP->id = glutCreateWindow(window.title);
    insertIntoWindowIDsList(windowIDP);
    
    initRendering();
            
    /* Set handler functions */
    glutDisplayFunc(window.drawScene);
    glutKeyboardFunc(window.handleKeypress);
    glutReshapeFunc(window.handleResize);
    glutCloseFunc(_close);
    if (numOpenWindows == 0)
        glutTimerFunc(25, update, 1); /* Add a timer */

    numOpenWindows += 1;
}

void _destroyWindow2(int id) {
    if (numOpenWindows > 0) {
        if (deleteFromWindowIDsList(id) == TRUE) {  
            numOpenWindows -= 1; 
            glutDestroyWindow(id); 
            if (numOpenWindows == 0) {
                windowIDsList = NULL;
                continueRunning = FALSE;
            }
        }
    }
}

void _destroyWindow() {
    if (numOpenWindows > 0) { 
        int id = glutGetWindow();
        _destroyWindow2(id);
    }
}

void _changeWindowSize(int id, int w, int h) {
    if (existsInWindowIDsList(id)) {
        glutSetWindow(id);
        glutReshapeWindow(w, h);
    }
}

void _close() {
    if (numOpenWindows > 0) { 
        int id = glutGetWindow();
        if (deleteFromWindowIDsList(id) == TRUE) {  
            numOpenWindows -= 1;  
            if (numOpenWindows == 0) {
                windowIDsList = NULL;
                continueRunning = FALSE;
            }
        }
    }
}



void *TaskCode(void *argument) {
    int i;

    _createWindow();    

    continueRunning = TRUE;

    while (continueRunning) {
        if (changeRequest == 1) {  
            if (_request == 1)
                _createWindow();
            else if (_request == 2)
                _destroyWindow2(window.id);  
            else if (_request == 3)
                _changeWindowSize(window.id, window.w, window.h); 
            _request = 0;
            changeRequest = 0;
        }

        glutMainLoopEvent();
    }

    for(i = 0; i < 1000; i++)
        glutMainLoopEvent();

    return NULL;
}

int getNumOpenWindows() {
    return numOpenWindows;
}

void incNumOpenWindows() {
    numOpenWindows += 1;
}

void decNumOpenWindows() {
    numOpenWindows -= 1;
    if (numOpenWindows < 0)
        numOpenWindows = 0;
}

int getChangeRequest() {
    return changeRequest; 
}

void setChangeRequest(int value) {
    changeRequest = value;
}

void setRequest(int value) {
    _request = value;
}

void createEventLoopThread() {
    int thread_args = 0;
    if (eventLoopThread > -1) {
        pthread_join(eventLoopThread, NULL);
        eventLoopThread = -1;
    } 
    pthread_create(&eventLoopThread, NULL, TaskCode, (void *) &thread_args);
}

void insertIntoWindowIDsList(WindowIDP windowIDP) {
    windowIDP->next = windowIDsList;
    windowIDsList = windowIDP;
}

int deleteFromWindowIDsList(int id) {
    int found = FALSE;

    WindowIDP curWindowIDP = windowIDsList;
    WindowIDP prevWindowIDP = windowIDsList;    

    while (curWindowIDP != NULL) {
        if (curWindowIDP->id == id) {
            if (curWindowIDP == windowIDsList)
                windowIDsList = curWindowIDP->next;
            else 
                prevWindowIDP->next = curWindowIDP->next;
           
            found = TRUE;

            free(curWindowIDP);
            break;
        }
        prevWindowIDP = curWindowIDP;
        curWindowIDP = curWindowIDP->next;
    }

    return found;
}

int existsInWindowIDsList(int id) {
    int found = FALSE;

    WindowIDP curWindowIDP = windowIDsList;
   
    while (curWindowIDP != NULL) {
        if (curWindowIDP->id == id) { 
            found = TRUE;
            break;
        }
        curWindowIDP = curWindowIDP->next;
    }

    return found;
}
