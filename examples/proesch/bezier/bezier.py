#!/usr/bin/python
# Surface deforming according to a damped oscillation consisting
# of bezier patches.
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import math
import sys
from time import sleep

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error: PyOpenGL is not installed properly !!'''
  sys.exit(  )

try:
	import psyco
	psyco.full()
except ImportError:
	print 'no psyco availiable'

animationAngle = 0.0
frameRate = 25
animationTime = 0

def animationStep( ):
	"""Update animated parameters.

	This Function is made active by glutSetIdleFunc"""
	global animationAngle
	global frameRate
	global animationTime
	animationAngle += 0.3
	animationTime += 0.1
	while animationAngle > 360:
		animationAngle -= 360
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

sigma = 0.5;
twoSigSq = 2. * sigma * sigma;

def dampedOscillation( u, v, t):
	"""Calculation of a R2 -> R1 function at position u,v at time t.

	A t-dependent cosine function is multiplied with a 2D gaussian.
	Both functions depend on the distance of (u,v) to the origin."""

	distSq = u * u + v * v;
	dist = math.pi * 4 * math.sqrt( distSq );
	global twoSigSq
	return 0.5 * math.exp(-distSq / twoSigSq) * math.cos(dist - t);

# number of patches in x and y direction
divisions = 7
nPts = divisions*3+1
xMin, xMax, yMin, yMax = -1.0, 1.0, -1.0, 1.0
xStep = (xMax-xMin)/(nPts-1)
yStep = (yMax-yMin)/(nPts-1)
divisionsGL = 20

# initialise a list representing a regular 2D grid of control points.
controlPoints = [ \
		[ [ yMin+y*yStep, xMin+x*xStep, 0.0 ]  for x in range ( nPts )]\
	for y in range( nPts ) ]

# The actual surface is divided into patches of 4 by 4
# control points
patch = [ [ [ ] for x in range( 4 )] for y in range( 4 ) ]

def updateControlPoints( t ):
	"""Calculate function values for all 2D grid points."""

	for row in controlPoints:
		for coord in row:
			coord[2] = dampedOscillation( coord[0], coord[1], t )

def display(  ):
	"""OpenGL display function."""
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity( )
	xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
	gluPerspective(60, float(xSize) / float(ySize), 0.1, 50)
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glTranslatef( 0, 0, -3 )
	glRotatef( -30, 1, .3, 0)
	glRotatef( animationAngle, 0, 0, 1 )
	global animationTime
	updateControlPoints( animationTime )
	global controlPoints, patch
	global nPts, divisionsGL
	# plot all surface patches
	# loop over all patches
	for y in range( 0, nPts-1, 3):
		for x in range( 0, nPts-1, 3 ):
			# display the current patch
			for i in range( 4 ):
				for k in range( 4 ):
					patch[i][k]=controlPoints[y+i][x+k]
			glMap2f( GL_MAP2_VERTEX_3, 0, 1, 0, 1, patch )
			glMapGrid2f( divisionsGL, 0.0, 1.0, divisionsGL, 0.0, 1.0 )
			glEvalMesh2( GL_FILL, 0, divisionsGL, 0, divisionsGL )
	glutSwapBuffers( )

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
	lD = 1.0; glLightfv( GL_LIGHT0, GL_DIFFUSE, [lD, lD, lD, 1] )
	lS = 1.0; glLightfv( GL_LIGHT0, GL_SPECULAR, [lS, lS, lS, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.7, 0.7, 0.7, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
	glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
	glEnable( GL_MAP2_VERTEX_3 )
	glEnable( GL_AUTO_NORMAL )

glutInit( sys.argv )
glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
glutInitWindowSize( 250, 250 )
glutInitWindowPosition( 100, 100 )
glutCreateWindow( sys.argv[0] )
init(  )
glutDisplayFunc( display )
glutIdleFunc( animationStep )
glutMainLoop(  )
