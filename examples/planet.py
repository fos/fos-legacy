#!/usr/bin/python

import sys

try:
    
    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    import OpenGL.GLU as glu
    
except ImportError:
    
    ImportError('PyOpenGL is not installed')

year=0.
day=0.
zdist=-10.

def display():
    
    global day,year,zdist
    gl.glClear (gl.GL_COLOR_BUFFER_BIT)          
    gl.glPushMatrix()
    gl.glColor3f (1.0, 1.0, 0.0) 
    
    gl.glLoadIdentity ()   
    gl.glRotatef(year, 0.0, 1.0, 0.0)
    gl.glTranslatef(0.,0.,zdist)
    
    glut.glutWireSphere(1.0, 20, 16) #sun
    
    gl.glRotatef(day, 0.0, 0.0, 1.0)    
    gl.glTranslatef(2.0, 0.0,0.0)            
    gl.glColor3f (1.0, 0.0, 0.0)
    glut.glutWireSphere(0.2, 10, 8) #planet 1
    
    gl.glLoadIdentity ()   
    gl.glRotatef(year, 0.0, 1.0, 0.0)
    gl.glTranslatef(0.,0.,zdist)
    
    gl.glRotatef(day, 0.0, 1.0, 0.0)    
    gl.glTranslatef(2.0, 0.0,0.0)            
    gl.glColor3f (1.0, 0.0, 1.0)
    glut.glutSolidSphere(0.2, 10, 8) #planet 2
    
    gl.glRotatef(day, 0.0, 1.0, 0.0)    
    gl.glTranslatef(0.5, 0.0,0.0)            
    gl.glColor3f (0.7, 0.2, 1.0)
    glut.glutSolidSphere(0.1, 10, 8) #moon of planet 2
    
    gl.glPopMatrix()
    
    glut.glutSwapBuffers()    
   
def reshape (w, h):
    
    gl.glViewport (0, 0, w, h)
    gl.glMatrixMode (gl.GL_PROJECTION)
    
    gl.glLoadIdentity ()
    glu.gluPerspective(60.0, w/ h , 1.0, 20.0)    
    
    gl.glMatrixMode (gl.GL_MODELVIEW)    
    gl.glLoadIdentity ()
    glu.gluLookAt(0.0,0.0,5.0,0.0,0.0,0.0,0.0,1.0,0.0)
   

def keyboard(key, x, y):
    global day,year,zdist

    if key == chr(27):          
        sys.exit(0)
      
    if key == 'd':
        day = (day+10) % 360
        glut.glutPostRedisplay()
        
    if key == 'D':
        day = (day-10) % 360
        glut.glutPostRedisplay()
        
    if key == 'y':
        year = (year+5) % 360
        glut.glutPostRedisplay()
        
    if key == 'Y':
        year = (year-5) % 360
        glut.glutPostRedisplay()
        
    if key == 'u': 
        zdist = zdist - 0.5
        glut.glutPostRedisplay()
        
    if key == 'U':
        zdist = zdist + 0.5
        glut.glutPostRedisplay()
        

def mouse(button, state, x, y):    
    global day,year
    
    if button == glut.GLUT_LEFT_BUTTON:
        if(state == glut.GLUT_DOWN):
            #glutIdleFunc(spinDisplay)
            year = (year+15) % 360
            glut.glutPostRedisplay()
          
    if button == glut.GLUT_RIGHT_BUTTON:
        if(state == glut.GLUT_DOWN):
            #glutIdleFunc(None)
            year = (year-15) % 360
            glut.glutPostRedisplay()
          



def window(w=500,h=500,title='Fos',px=100,py=100,color=(0.,0.,0.)):

    #glut init
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode (glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize (w, h)
    glut.glutInitWindowPosition (px, py)
    glut.glutCreateWindow (title)

    #gl init
    gl.glClearColor (color[0], color[1], color[2], 0.0)
    gl.glShadeModel (gl.GL_FLAT)

def interaction(dispf=display,reshf=reshape, keyf=keyboard,mousf=mouse):
    
    glut.glutDisplayFunc(dispf)
    glut.glutReshapeFunc(reshf)
    glut.glutKeyboardFunc(keyf)
    glut.glutMouseFunc(mousf)

def start():
    
    glut.glutMainLoop()

window()
interaction()
start()
