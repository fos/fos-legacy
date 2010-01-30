# helper class for stereo visualisation using OpenGL
# The underlying equations and their implementation are by courtesy of 
# Paul Bourke, http://local.wasp.uwa.edu.au/~pbourke/projection/stereorender/
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.

import sys
import math

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error: PyOpenGL not installed properly !!'''
  sys.exit(  )

class StereoCamera( object ):
	"""Helper class for stereo frustum calculation.

	Frustum settings for left and right camera are
	calculated according to parameters e.g. eye
	separtion"""
	DEG2RAD = math.pi / 180.0

	def __init__( self ):
		self.centerPosition = [ 0, 0, 10 ]
		self.viewingDirection = [ 0, 0, -1 ]
		self.upVector = [ 0, 1, 0 ]
		self.near, self.far, self.focalLength = 0.1, 100.0, 10.0
		self.whRatio = 4.0/3.0
		self.aperture = 60.0
		self.eyeSeparation = self.focalLength / 20.0
		self.eyePositionLeft, self.eyePositionRight = [ ], [ ]
		self.frustumLeft = ( )
		self.frustumRight = ( )
		self.lookAtRight = ( )
		self.lookAtLeft = ( )

	def difference( self, a, b):
		"""Calculate difference vector."""
		if not (len( a ) == len ( b )):
			print ''' Error: different vector length in sub'''
			sys.exit(  )
		c=[ 0 for i in range( len( a ) ) ]
		for i in range( len( a )):
			c[i] = a[i]-b[i]
		return c

	def sum( self, a, b ):
		"""Calculate sum vector."""
		if not (len( a ) == len ( b )):
			print ''' Error: different vector length in add'''
			sys.exit(  )
		c=[ 0 for i in range( len( a ) ) ]
		for i in range( len( a ) ):
			c[i] = a[i]+b[i]
		return c

	def scale( self, a, f ):
		"""Scale a vector."""
		for i in range( len( a ) ):
			a[i] = a[i]*f

	def crossProduct( self, a, b ):
		"""Cross product of two 3D vectors."""
		if len( a ) != 3 or len( b ) != 3:
			print ''' Error: cross product needs 3D vectors as input'''
			sys.exit(  )
		c=[ 0, 0, 0 ]
		c[0] = a[1]*b[2]-a[2]*b[1]
		c[1] = a[2]*b[0]-a[0]*b[2]
		c[2] = a[0]*b[1]-a[1]*b[0]
		return c

	def update( self ):
		"""Calculate left and right frustum."""
		betweenTheEyes = self.crossProduct( self.viewingDirection, self.upVector )
		self.scale( betweenTheEyes, self.eyeSeparation/2.0 )
		self.eyePositionLeft = self.difference( self.centerPosition,
			betweenTheEyes )
		self.eyePositionRight = self.sum( self.centerPosition, betweenTheEyes )
		self.lookAtLeft = ( 
			self.eyePositionLeft[0],
			self.eyePositionLeft[1],
			self.eyePositionLeft[2],
			self.eyePositionLeft[0]+self.viewingDirection[0],
			self.eyePositionLeft[1]+self.viewingDirection[1],
			self.eyePositionLeft[2]+self.viewingDirection[2],
			self.upVector[0], self.upVector[1], self.upVector[2] )
		self.lookAtRight = ( 
			self.eyePositionRight[0],
			self.eyePositionRight[1],
			self.eyePositionRight[2],
			self.eyePositionRight[0]+self.viewingDirection[0],
			self.eyePositionRight[1]+self.viewingDirection[1],
			self.eyePositionRight[2]+self.viewingDirection[2],
			self.upVector[0], self.upVector[1], self.upVector[2] )
		perpDelta = self.near * math.tan( self.aperture*StereoCamera.DEG2RAD/2.0 )
		parallaxCorrection = self.near/self.focalLength;
		self.frustumLeft = (
			-self.whRatio*perpDelta+self.eyeSeparation/2.0*parallaxCorrection,
			self.whRatio*perpDelta+self.eyeSeparation/2.0*parallaxCorrection,
			-perpDelta, perpDelta, self.near, self.far )
		self.frustumRight = (
			-self.whRatio*perpDelta-self.eyeSeparation/2.0*parallaxCorrection,
			self.whRatio*perpDelta-self.eyeSeparation/2.0*parallaxCorrection,
			-perpDelta, perpDelta, self.near, self.far )

# test program
if __name__ == '__main__' :
	sC = StereoCamera( )
	a=[1,0,0]
	b=[0,0,1]
	print sC.crossProduct( a, b )
	sC.update( )
	print sC.lookAtLeft
	print sC.frustumLeft
	print sC.lookAtRight
	print sC.frustumRight
