#!/usr/bin/python2.4
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error PyOpenGL not installed properly!!'''
  sys.exit(  )

def setList( l, v ):
	"""Set all elements of a list to the same bvalue"""
	for i in range( len( l ) ):
		l[i] = v

class renderParam( object ):
	"""Class holding current parameters for rendering.

	Parameters are modified by user interaction"""
	def __init__( self ):
		self.initialColor = [1, 1, 1]
		self.drawColor = self.initialColor
		self.tVec = [0, 0, 0]
		self.mouseButton = None

	def reset( self ):
		self.drawColor = self.initialColor
		setList( self.tVec, 0 )
		self.mouseButton = None

rP = renderParam( )

oldMousePos = [ 0, 0 ]
def mouseButton( button, mode, x, y ):
	"""Callback function (mouse button pressed or released).

	The current and old mouse positions are stored in
	a	global renderParam and a global list respectively"""

	global rP, oldMousePos
	if mode == GLUT_DOWN:
		rP.mouseButton = button
	else:
		rP.mouseButton = None
	oldMousePos[0], oldMousePos[1] = x, y
	glutPostRedisplay( )

def mouseMotion( x, y ):
	"""Callback function (mouse moved while button is pressed).

	The current and old mouse positions are stored in
	a	global renderParam and a global list respectively.
	The global translation vector is updated according to
	the movement of the mouse pointer."""

	global rP, oldMousePos
	deltaX = x - oldMousePos[ 0 ]
	deltaY = y - oldMousePos[ 1 ]
	if rP.mouseButton == GLUT_LEFT_BUTTON:
		factor = 0.01
		rP.tVec[0] += deltaX * factor
		rP.tVec[1] -= deltaY * factor
		oldMousePos[0], oldMousePos[1] = x, y
	glutPostRedisplay( )

def keyPressed( key, x, y ):
	"""Callback function (ordinary key pressed)."""

	global rP
	if key in ('r', 'R'):
		rP.reset( )
	elif key in ('q', 'Q'):
		sys.exit( )
	glutPostRedisplay( )

def specialKeyPressed( key, x, y):
	"""Callback function (special key pressed).
	
	Arrow keys are used to shift the object displayed."""
	stepSize = 0.1
	global rP
	if key == GLUT_KEY_LEFT:
		rP.tVec[0] -= stepSize
	elif key == GLUT_KEY_RIGHT:
		rP.tVec[0] += stepSize
	elif key == GLUT_KEY_DOWN:
		rP.tVec[1] -= stepSize
	elif key == GLUT_KEY_UP:
		rP.tVec[1] += stepSize
	glutPostRedisplay( )

MENU_RED, MENU_GREEN, MENU_BLUE, MENU_QUIT = 0, 1, 2, 3
colors = [ [1, 0, 0], [0, 1, 0], [0, 0, 1] ]
def handleMenu( selection ):
	"""Callback function (menu).

	Glut menus are not supported in PyOpenGL-3.0.0a6"""

	global colors, rP
	if selection == MENU_QUIT:
		sys.exit()
	elif MENU_RED <= selection <= MENU_BLUE:
		rP.drawColor = colors[ selection ]
	else:
		print 'Warning: illegel Menu entry'
	glutPostRedisplay( )

def initMenus( ):
	global handleMenu
	colorMenu = glutCreateMenu( handleMenu )
	glutAddMenuEntry( "red", MENU_RED )
	glutAddMenuEntry( "green", MENU_GREEN )
	glutAddMenuEntry( "blue", MENU_BLUE )
	glutCreateMenu( handleMenu )
	glutAddSubMenu( "color", colorMenu)
	glutAddMenuEntry( "quit", MENU_QUIT )
	glutAttachMenu( GLUT_RIGHT_BUTTON )

def display(  ):
	"""OpenGL display function."""
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glColor3f( rP.drawColor[0], rP.drawColor[1], rP.drawColor[2] )
	glTranslatef( rP.tVec[0], rP.tVec[1], rP.tVec[2] )
	glBegin( GL_QUADS )
	glVertex3f( -0.25, 0.25, 0 )
	glVertex3f( -0.25, -0.25, 0 )
	glVertex3f( 0.25, -0.25, 0 )
	glVertex3f( 0.25, 0.25, 0 )
	glEnd(  )
	# m = glGetFloatv( GL_MODELVIEW_MATRIX ); print m; print
	glutSwapBuffers( )

def registerCallbacks( ):
	"""Initialise glut settings concerning functions"""
	glutMouseFunc( mouseButton )
	glutMotionFunc( mouseMotion )
	glutKeyboardFunc( keyPressed )
	glutSpecialFunc( specialKeyPressed )
	glutDisplayFunc( display )

def init(  ):
	# Glut menus are not supported in PyOpenGL-3.0.0a6
	# initMenus( )
	registerCallbacks( )
	glClearColor ( 0, 0, 0, 0 )
	glShadeModel( GL_SMOOTH )

glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
glutInitWindowSize( 250, 250 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( sys.argv[0] )
init( )
glutMainLoop(  )
