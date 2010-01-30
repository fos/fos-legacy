#!/usr/bin/env python
# Plot nurbs surface corresponding to a 2D damped oscillation.
# The surface has two holes. A Teapot below the surface is
# visible through these holes.
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
import math
from time import sleep
import traceback

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except ImportError, err:
  traceback.print_exc()
  print ''' Error: PyOpenGL not installed properly!!'''
  sys.exit(  )

# globals
animationAngle = 0.0
frameRate = 25
curr_time=0.0
nurbsID=0

def animationStep( ):
	"""Update animated parameters"""
	global animationAngle
	global frameRate
	animationAngle += 1
	while animationAngle > 360:
		animationAngle -= 360
	global curr_time
	curr_time+=0.05
	global nurbsID
	glDeleteLists( nurbsID, 1 )
	nurbsID = glGenLists( 1 )
	glNewList( nurbsID, GL_COMPILE )
	plotSurface( curr_time )
	glEndList( )
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

sigma = 0.5;
twoSigSq = 2. * sigma * sigma;

def dampedOscillation( u, v, t):
	"""Calculation of a R2 -> R1 function at position u,v at curr_time t.

	A t-dependent cosine function is multiplied with a 2D gaussian.
	Both functions depend on the distance of (u,v) to the origin."""

	distSq = u * u + v * v;
	dist = math.pi * 4 * math.sqrt( distSq );
	global twoSigSq
	return  0.5 * math.exp(-distSq / twoSigSq) * math.cos(dist - t);

nPts = 15
degree = 4
samplingTolerance=2.0
xMin, xMax, yMin, yMax = -1.0, 1.0, -1.0, 1.0
xStep = (xMax-xMin)/(nPts-1)
yStep = (yMax-yMin)/(nPts-1)

# initialise a list representing a regular 2D grid of control points.
controlPoints = [ \
		[ [ yMin+y*yStep, xMin+x*xStep, 0.0 ]  for x in range ( nPts )]\
	for y in range( nPts ) ]

# initialise knots ...
knots = [ 0.0 for i in range( degree/2 ) ] +\
				[ float(i)/(nPts-1) for i in range( nPts )] +\
				[ 1.0 for i in range( (degree+1)/2 ) ]

# initialise enclosing
enclosing=[ [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0] ]

# first trim curve is a circle
angleNum = 16
angles = [ -2*math.pi*float(i)/angleNum for i in range( angleNum ) ]
radius=0.05
offset=(0.4, 0.6)
circleDegree=degree
circlePoints = [ \
	[ offset[0]+radius*math.cos(theta), offset[1]+radius*math.sin(theta) ]\
	for theta in angles ]
for i in range( circleDegree-1 ):
	circlePoints = circlePoints + [ circlePoints[i] ]
knotNum = len( circlePoints ) + circleDegree 
circleKnots =  [ float(i)/(knotNum-1) for i in range( knotNum ) ]

# second trim curve is a square
squareHolePoints=[ [0.4, 0.4], [0.4, 0.45], [0.45, 0.45],\
	[0.45, 0.4], [0.4, 0.4] ]

def updateControlPoints( t ):
	"""Calculate function values for all 2D grid points."""
	for row in controlPoints:
		for coord in row:
			coord[2] = dampedOscillation( coord[0], coord[1], t )

def plotSurface( t ):
	# display surface 
	updateControlPoints( t )
	global controlPoints, knots
	global nurb

	gluBeginSurface( nurb )
	gluNurbsSurface	(	nurb, knots, knots, controlPoints, GL_MAP2_VERTEX_3 )

	# trim curve enclosing
	gluBeginTrim( nurb )
	global enclosing
	gluPwlCurve( nurb, enclosing, GLU_MAP1_TRIM_2 )
	gluEndTrim( nurb )

	# trim using square
	gluBeginTrim( nurb )
	global squareHolePoints
	gluPwlCurve( nurb, squareHolePoints, GLU_MAP1_TRIM_2 )
	gluEndTrim( nurb )
	
	# trim using circle
	gluBeginTrim( nurb )
	global circlePoints, circleKnots
	gluNurbsCurve	(	nurb, circleKnots, circlePoints, GLU_MAP1_TRIM_2 )
	gluEndTrim( nurb )

	gluEndSurface( nurb )
	

def display(  ):
	"""Glut display function."""
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity( )
	xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
	gluPerspective(60, float(xSize) / float(ySize), 0.1, 50)
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glPushMatrix( )
	glTranslatef( 0, 0, -3 )
	glRotatef( -30, 1, .3, 0)
	glRotatef( animationAngle, 0, 0, 1 )

	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.7, 0.7, 0.7, 1] )
	glCallList( nurbsID )

	glPopMatrix( )
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.7, 1] )
	glTranslatef( 0.0, 0.0, -12.0 )
	glCallList( teapotID )
	glutSwapBuffers( )

teapotID=0
nurb=None
def init(  ):
	"""Glut init function."""
	glClearColor ( 0, 0, 0, 0 )
	glEnable( GL_DEPTH_TEST )
	glShadeModel( GL_SMOOTH )
	glEnable( GL_LIGHTING )
	glEnable( GL_LIGHT0 )
	glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, 0 )
	glLightfv( GL_LIGHT0, GL_POSITION, [2, 0, 10, 1] )
	lA = 0.8; glLightfv( GL_LIGHT0, GL_AMBIENT, [lA, lA, lA, 1] )
	lD = 1; glLightfv( GL_LIGHT0, GL_DIFFUSE, [lD, lD, lD, 1] )
	lS = 1; glLightfv( GL_LIGHT0, GL_SPECULAR, [lS, lS, lS, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
	glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
	glEnable( GL_AUTO_NORMAL )
	global nurb
	nurb = gluNewNurbsRenderer()
	global samplingTolerance
	gluNurbsProperty(nurb, GLU_SAMPLING_TOLERANCE, samplingTolerance)
	gluNurbsProperty(nurb, GLU_DISPLAY_MODE, GLU_FILL)
	global teapotID
	teapotID = glGenLists( 1 )
	glNewList( teapotID, GL_COMPILE )
	glutSolidTeapot( 1.0 )
	glEndList( )
	global nurbsID
	nurbsID = glGenLists( 1 )
	glNewList( nurbsID, GL_COMPILE )
	global curr_time
	plotSurface( curr_time )
	glEndList( )

glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
glutInitWindowSize( 250, 250 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( sys.argv[0] )
init(  )
glutDisplayFunc( display )
glutIdleFunc( animationStep )
glutMainLoop(  )
