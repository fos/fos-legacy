#!/usr/bin/python2.4
# demo for interactive object motion
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
from mouseInteractor import MouseInteractor

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Fehler: PyOpenGL nicht intalliert !!'''
  sys.exit(  )


def display(  ):
	"""Glut display function."""
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity( )
	xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
	gluPerspective(60, float(xSize) / float(ySize), 0.1, 50)
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glTranslatef( 0, 0, -4 )
	global mouseInteractor
	mouseInteractor.applyTransformation( )
	glCallList( tkList )
	glDisable( GL_LIGHTING )
	glColor3f( 1, 1, 0.3 )
	glRasterPos3f( 1.8, .5, 0 )
	for c in "tip":
		glutBitmapCharacter( GLUT_BITMAP_TIMES_ROMAN_24, ord(c) )
	glEnable( GL_LIGHTING )
	glutSwapBuffers( )

def init(  ):
	"""Glut init function."""
	glClearColor ( 0, 0, 0, 0 )
	glEnable( GL_DEPTH_TEST )
	glShadeModel( GL_SMOOTH )
	glEnable( GL_LIGHTING )
	glEnable( GL_LIGHT0 )
	glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, 0 )
	glLightfv( GL_LIGHT0, GL_POSITION, [4, 4, 4, 1] )
	lA = 0.8
	glLightfv( GL_LIGHT0, GL_AMBIENT, [lA, lA, lA, 1] )
	lD = 1
	glLightfv( GL_LIGHT0, GL_DIFFUSE, [lD, lD, lD, 1] )
	lS = 1
	glLightfv( GL_LIGHT0, GL_SPECULAR, [lS, lS, lS, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.7, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
	glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
	global mouseInteractor
	mouseInteractor = MouseInteractor( .01, 1 )
	global tkList
	tkList = glGenLists( 1 )
	glNewList( tkList, GL_COMPILE )
	glutSolidTeapot( 1.0 )
	glEndList( )

glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
glutInitWindowSize( 250, 250 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( sys.argv[0] )
init(  )
mouseInteractor.registerCallbacks( )
glutDisplayFunc( display )
glutMainLoop(  )
