#!/usr/bin/python2.4
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
from time import sleep
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error: PyOpenGL not installed properly !!'''
  sys.exit(  )

animationAngle = 0.0
frameRate = 25

def doAnimationStep( ):
	"""Update animated parameters.

	This Function is made active by glutSetIdleFunc"""
	global animationAngle
	global frameRate
	animationAngle += 1
	while animationAngle > 360:
		animationAngle -= 360
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

def display(  ):
	"OpenGL display function"""
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glColor3f( 1, 1, 1 )
	glRotatef( animationAngle, 0, 0, 1 )
	glBegin( GL_QUADS )
	glVertex3f( -0.5, 0.5, 0 )
	glVertex3f( -0.5, -0.5, 0 )
	glVertex3f( 0.5, -0.5, 0 )
	glVertex3f( 0.5, 0.5, 0 )
	glEnd(  )
	glutSwapBuffers( )

def init(  ):
	glClearColor ( 0, 0, 0, 0 )
	glShadeModel( GL_SMOOTH )

glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
glutInitWindowSize( 250, 250 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( sys.argv[0] )
init( )
glutDisplayFunc( display )
glutIdleFunc( doAnimationStep )
glutMainLoop(  )
