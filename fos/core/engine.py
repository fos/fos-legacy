#!/usr/bin/python

import sys
import numpy as np

try:
    
    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    import OpenGL.GLU as glu
    
except ImportError:
    
    ImportError('PyOpenGL is not installed')

import mouse


# objects

SELECT_BUFFER_SIZE=100


def drawRects(mode):

   if mode == gl.GL_SELECT:
      gl.glLoadName(1)

   gl.glBegin(gl.GL_QUADS)
   gl.glColor3f(1.0, .0, 0.0)
   gl.glVertex3i(2, 0, 0)
   gl.glVertex3i(2, 6, 0)
   gl.glVertex3i(6, 6, 0)
   gl.glVertex3i(6, 0, 0)
   gl.glEnd()

   if mode == gl.GL_SELECT:
      gl.glLoadName(2)

   gl.glBegin(gl.GL_QUADS)
   gl.glColor3f(0.0, 1.0, .0)
   gl.glVertex3i(3, 2, -1)
   gl.glVertex3i(3, 8, -1)
   gl.glVertex3i(8, 8, -1)
   gl.glVertex3i(8, 2, -1)
   gl.glEnd()

   if mode == gl.GL_SELECT:
      gl.glLoadName(3)

   gl.glBegin(gl.GL_QUADS)
   gl.glColor3f(.0, 0.0, 1.0)
   gl.glVertex3i(0, 2, -2)
   gl.glVertex3i(0, 7, -2)
   gl.glVertex3i(5, 7, -2)
   gl.glVertex3i(5, 2, -2)
   gl.glEnd()



def reshape (w, h):
    
    gl.glViewport (0, 0, w, h)
    gl.glMatrixMode (gl.GL_PROJECTION)    
    gl.glLoadIdentity ()
    glu.gluPerspective(60.0, w/ h , 1.0, 20.0)    
    #gl.glOrtho(0.0, 8.0, 0.0, 8.0, -0.5, 2.5);

    gl.glMatrixMode (gl.GL_MODELVIEW)    
    gl.glLoadIdentity ()
    glu.gluLookAt(0.0,0.0,15.0, 0.0,0.0,0.0, 0.0,1.0,0.0)


def display():
    
    gl.glClear (gl.GL_COLOR_BUFFER_BIT)          
    
    #gl.glRotatef(day, 0.0, 1.0, 0.0) 
    #gl.glTranslatef(0.0, 0.0, zdist)            
    #gl.glCallList(1)
    #glut.glutWireSphere(1.0, 20, 16) #sun
    drawRects(gl.GL_RENDER)
    global mi
    mi.applyTransformation( )
    glut.glutSwapBuffers()



def window(w=500,h=500,title='light',px=100,py=100):

    #glut init
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode (glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize (w, h)
    glut.glutInitWindowPosition (px, py)
    glut.glutCreateWindow (title)


def init(color=(0.,0.,0.)):    

    #add objects
    #origin()

    gl.glClearColor (color[0], color[1], color[2], 0.0)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glShadeModel (gl.GL_FLAT)
    gl.glDepthRange(0.0,1.0) #default z mapping


def keyboard(key, x, y):
    #global day,year,zdist

    if key == chr(27):          
        sys.exit(0)
        
    if key == 'a':
        glut.glutIdleFunc(spin)
    

    if key == 'p' or key == 'P': # picking
       

        viewport=gl.glGetIntegerv(gl.GL_VIEWPORT)
        #print viewport
        w=viewport[2]-viewport[0]
        h=viewport[3]-viewport[1]

        #print 'SBS',SELECT_BUFFER_SIZE
        gl.glSelectBuffer(SELECT_BUFFER_SIZE) 
        gl.glRenderMode(gl.GL_SELECT)

        gl.glInitNames()
        gl.glPushName(0)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        glu.gluPickMatrix(x,viewport[3]-y,.1, .1, viewport)
        glu.gluPerspective(60.0, w/ h , 1.0, 20.0)
        #gl.glOrtho(0.0, 8.0, 0.0, 8.0, -0.5, 2.5);

        
        drawRects(gl.GL_SELECT)
        gl.glPopMatrix()
        gl.glFlush()

        buffer = gl.glRenderMode(gl.GL_RENDER)
        glut.glutPostRedisplay()
        #print buffer
        for hit_record in buffer:
            min_depth, max_depth, names = hit_record
            print min_depth, max_depth, names
    

'''
def mouse(button, state, x, y):    
    #global day,year
    
    if button == glut.GLUT_LEFT_BUTTON:
        if state == glut.GLUT_DOWN:
            #glutIdleFunc(spinDisplay)
            glut.glutPostRedisplay()
          
    if button == glut.GLUT_RIGHT_BUTTON:
        if state == glut.GLUT_DOWN:
            #glutIdleFunc(None)
            glut.glutPostRedisplay()

    if button == glut.GLUT_MIDDLE_BUTTON:
        if state == glut.GLUT_DOWN:
            glut.glutPostRedisplay()
        
'''

#def interaction(disp=display,resh=reshape, key=keyboard, mous=mouse):
def interaction(disp=display,resh=reshape, key=keyboard):    

    global mi
    mi=mouse.MouseInteractor(.01, 1)
    mi.registerCallbacks( )

    glut.glutDisplayFunc(disp)
    glut.glutReshapeFunc(resh)
    glut.glutKeyboardFunc(key)
    #glut.glutMouseFunc(mous)

def start():

    window()
    init()
    interaction() 
    glut.glutMainLoop()
          
start()



