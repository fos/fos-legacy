#!/usr/bin/python2.4
# OpenGL stereo demo using stereoCamera class
#
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

from sys import argv, exit
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Fehler: PyOpenGL not installed properly !!'''
  sys.exit(  )

from stereoCamera import StereoCamera
sC = StereoCamera( )

animationAngle = 0.0
frameRate = 20
stereoMode = "NONE"
lightColors = {
	"white":(1.0, 1.0, 1.0, 1.0),
	"red":(1.0, 0.0, 0.0, 1.0),
	"green":(0.0, 1.0, 0.0, 1.0),
	"blue":(0.0, 0.0, 1.0, 1.0)
}

lightPosition = (5.0, 5.0, 20.0, 1.0)

from time import sleep
def animationStep( ):
	"""Update animated parameters."""
	global animationAngle
	global frameRate
	animationAngle += 2
	while animationAngle > 360:
		animationAngle -= 360
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

def setLightColor( s ):
	"""Set light color to 'white', 'red', 'green' or 'blue'."""
	if lightColors.has_key( s ):
		c = lightColors[ s ]
		glLightfv( GL_LIGHT0, GL_AMBIENT, c )
		glLightfv( GL_LIGHT0, GL_DIFFUSE, c )
		glLightfv( GL_LIGHT0, GL_SPECULAR, c )

def render( side ):
	"""Render scene in either GLU_BACK_LEFT or GLU_BACK_RIGHT buffer"""
	glViewport( 0, 0,
		glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT ))
	if side == GL_BACK_LEFT:
		f = sC.frustumLeft
		l = sC.lookAtLeft
	else:
		f = sC.frustumRight
		l = sC.lookAtRight
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glFrustum( f[0], f[1], f[2], f[3], f[4], f[5] )
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt( l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8] )
	glRotatef( animationAngle, 0.2, 0.7, 0.3 )	
	glCallList( teapotList )

def display(  ):
	"""Glut display function."""
	if stereoMode != "SHUTTER":
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	if stereoMode == "SHUTTER":
		setLightColor( "white" )
		glDrawBuffer( GL_BACK_LEFT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		render( GL_BACK_LEFT )
		glDrawBuffer( GL_BACK_RIGHT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		render( GL_BACK_RIGHT )
	elif stereoMode == "ANAGLYPH": 
		glDrawBuffer( GL_BACK_LEFT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		setLightColor( "red" )
		render( GL_BACK_LEFT )
		glClear( GL_DEPTH_BUFFER_BIT )
		glColorMask( False, True, False, False )
		setLightColor( "green" )
		render( GL_BACK_RIGHT )
		glColorMask( True, True, True, True )
	else: 
		glDrawBuffer(GL_BACK_LEFT)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		setLightColor( "white" )
		render(GL_BACK_LEFT)
	glutSwapBuffers( )

teapotList = 0
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
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.7, 0.7, 0.7, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
	glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
	global teapotList
	teapotList = glGenLists( 1 )
	glNewList( teapotList, GL_COMPILE )
	glutSolidTeapot( 1.0 )
	glEndList( )
	sC.aperture = 40.0
	sC.focalLength = 10.0
	sC.centerPosition[0], sC.centerPosition[1], sC.centerPosition[2] = \
		0.0, 0.0, 5.0
	sC.viewingDirection[0], sC.viewingDirection[1], sC.viewingDirection[2] = \
		0.0, 0.0, -1.0
	sC.near = sC.focalLength / 500.0
	sC.far = 1000
	sC.eyeSeparation = sC.focalLength / 200.0
	sC.whRatio = \
	 float( glutGet( GLUT_WINDOW_WIDTH ) ) /  glutGet( GLUT_WINDOW_HEIGHT )
	sC.update( )

def reshape( width, height ):
	"""Glut reshape function."""
	sC.whRatio = float(width)/float(height)
	sC.update( )

if len( argv ) != 2:
	print "Usage:"
	print "python stereDemo.py SHUTTER | ANAGLYPH | NONE \n"
else:
	glutInit( sys.argv )
	stereoMode = sys.argv[1].upper( )
	if stereoMode == "SHUTTER":
		glutInitDisplayMode( GLUT_STEREO | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
	else:
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
	glutInitWindowSize( 250, 250 )
	glutInitWindowPosition( 100, 100 )
	glutCreateWindow( sys.argv[0] )
	init(  )
	glutDisplayFunc( display )
	glutReshapeFunc( reshape )
	glutIdleFunc( animationStep )
	glutMainLoop(  )
