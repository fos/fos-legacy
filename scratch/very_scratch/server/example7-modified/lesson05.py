#!/usr/bin/env python
# pyglet version of NeHe's OpenGL lesson05
# based on the pygame+PyOpenGL conversion by Paul Furber 2001 - m@verick.co.za
# Philip Bober 2007 pdbober@gmail.com

from pyglet.gl import *
from pyglet import window
import pyglet.clock

rtri = rquad = 0.0

def resize(width, height):
	if height==0:
		height=1
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 1.0*width/height, 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

def init():
	glShadeModel(GL_SMOOTH)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
	glLoadIdentity();					
	glTranslatef(-1.5,0.0,-6.0)

	glRotatef(rtri,0.0,1.0,0.0)			

	glBegin(GL_TRIANGLES)				

	glColor3f(1.0,0.0,0.0)
	glVertex3f( 0.0, 1.0, 0.0)		
	glColor3f(0.0,1.0,0.0)
	glVertex3f(-1.0,-1.0, 1.0)
	glColor3f(0.0,0.0,1.0)	
	glVertex3f( 1.0,-1.0, 1.0)
	
	glColor3f(1.0,0.0,0.0)	
	glVertex3f( 0.0, 1.0, 0.0)
	glColor3f(0.0,0.0,1.0)	
	glVertex3f( 1.0,-1.0, 1.0)
	glColor3f(0.0,1.0,0.0)	
	glVertex3f( 1.0,-1.0, -1.0)

	glColor3f(1.0,0.0,0.0)	
	glVertex3f( 0.0, 1.0, 0.0)
	glColor3f(0.0,1.0,0.0)	
	glVertex3f( 1.0,-1.0, -1.0)
	glColor3f(0.0,0.0,1.0)	
	glVertex3f(-1.0,-1.0, -1.0)
		
		
	glColor3f(1.0,0.0,0.0)	
	glVertex3f( 0.0, 1.0, 0.0)
	glColor3f(0.0,0.0,1.0)	
	glVertex3f(-1.0,-1.0,-1.0)
	glColor3f(0.0,1.0,0.0)	
	glVertex3f(-1.0,-1.0, 1.0)
	glEnd()


	glLoadIdentity()
	glTranslatef(1.5,0.0,-7.0)
	glRotatef(rquad,1.0,1.0,1.0)
	glBegin(GL_QUADS)	


	glColor3f(0.0,1.0,0.0)
	glVertex3f( 1.0, 1.0,-1.0)
	glVertex3f(-1.0, 1.0,-1.0)		
	glVertex3f(-1.0, 1.0, 1.0)		
	glVertex3f( 1.0, 1.0, 1.0)		

	glColor3f(1.0,0.5,0.0)	
	glVertex3f( 1.0,-1.0, 1.0)
	glVertex3f(-1.0,-1.0, 1.0)		
	glVertex3f(-1.0,-1.0,-1.0)		
	glVertex3f( 1.0,-1.0,-1.0)		

	glColor3f(1.0,0.0,0.0)		
	glVertex3f( 1.0, 1.0, 1.0)
	glVertex3f(-1.0, 1.0, 1.0)		
	glVertex3f(-1.0,-1.0, 1.0)		
	glVertex3f( 1.0,-1.0, 1.0)		

	glColor3f(1.0,1.0,0.0)	
	glVertex3f( 1.0,-1.0,-1.0)
	glVertex3f(-1.0,-1.0,-1.0)
	glVertex3f(-1.0, 1.0,-1.0)		
	glVertex3f( 1.0, 1.0,-1.0)		

	glColor3f(0.0,0.0,1.0)	
	glVertex3f(-1.0, 1.0, 1.0)
	glVertex3f(-1.0, 1.0,-1.0)		
	glVertex3f(-1.0,-1.0,-1.0)		
	glVertex3f(-1.0,-1.0, 1.0)		

	glColor3f(1.0,0.0,1.0)	
	glVertex3f( 1.0, 1.0,-1.0)
	glVertex3f( 1.0, 1.0, 1.0)
	glVertex3f( 1.0,-1.0, 1.0)		
	glVertex3f( 1.0,-1.0,-1.0)		
	glEnd()	

def main():
	global rtri,rquad
	win = window.Window(width=640,height=480,visible=False)
	win.on_resize=resize

	init()

	win.set_visible()
	clock=pyglet.clock.Clock()

	while not win.has_exit:
		win.dispatch_events()
		
		draw()

		win.flip()

		dt=clock.tick()
		rtri += 40*dt
		rquad+= 40*dt
	
	print "fps:  %d" % clock.get_fps()

if __name__ == '__main__': main()
