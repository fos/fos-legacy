#!/usr/bin/env python
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.
#import OpenGL 
#OpenGL.FULL_LOGGING = True

import sys
import array
import Image
import random
from shaderProg import *

try:
	from OpenGL.GLUT import *
	from OpenGL.GL import *
	from OpenGL.GLU import *
	from OpenGL.GL.ARB.shader_objects import *
	from OpenGL.GL.ARB.fragment_shader import *
	from OpenGL.GL.ARB.vertex_shader import *
except:
	print ''' Error PyOpenGL not installed properly !!'''
	sys.exit(  )


class Texture( object ):
	def __init__( self ):
		self.xSize, self.ySize = 0, 0
		self.rawRefence = None

class RandomTexture( Texture ):
	def __init__( self, xSizeP, ySizeP ):
		self.xSize, self.ySize = xSizeP, ySizeP
		tmpList = [ random.randint(0, 255) \
			for i in range( 3 * self.xSize * self.ySize ) ]
		self.textureArray = array.array( 'B', tmpList )
		self.rawReference = self.textureArray.tostring( )

class FileTexture( Texture ):
	def __init__( self, fileName ):
		im = Image.open( fileName )
		self.xSize = im.size[0]
		self.ySize = im.size[1]
		self.rawReference = im.tostring("raw", "RGB", 0, -1)

frameRate = 30
from time import sleep
def animationStep( *args ):
	global frameRate
	global sP
	if not quadList:
		if len(sys.argv) > 1: 
			init( sys.argv[1] )
		else:
			init( None )
		assert quadList
	if sP.isEnabled():
		global rgbTransformMatrix
		row = random.randint( 0, 3 )
		column = random.randint( 0, 3 )
		rgbTransformMatrix[row*4+column] += random.normalvariate( 0, 0.05 )
		if rgbTransformMatrix[row*4+column] < 0:
			rgbTransformMatrix[row*4+column] = 0
		sum=0.
		for x in rgbTransformMatrix[ row*4:row*4+4 ]:
			sum+=x
		for i in range( row*4,row*4+4 ):
			rgbTransformMatrix[i] /= sum
		glUniformMatrix4fvARB(sP.indexOfUniformVariable("RGBTransformationMatrix"),\
			1, False, rgbTransformMatrix)
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

def display( *args ):
	if not quadList:
		if len(sys.argv) > 1: 
			init( sys.argv[1] )
		else:
			init( None )
		assert quadList
	glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
	glColor3f( 1, 1, 1 )
	glMatrixMode( GL_PROJECTION )
	glLoadIdentity( )
	xSize, ySize = glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT )
	f = float(ySize) / float(xSize)
	gluOrtho2D( -1.5, 1.5, -1.5*f, 1.5*f)
	glMatrixMode( GL_MODELVIEW )
	glLoadIdentity( )
	glPushMatrix( )
	glTranslatef( -0.6, 0, 0 )
	sP.disable( )
	glCallList( quadList )
	glPopMatrix( )
	glTranslatef( 0.6, 0, 0)
	sP.enable( )
	glCallList( quadList )
	glutSwapBuffers (  )

sP = None
def initShaders( ):
	global sP
	sP = ShaderProgram( )
	sP.addShader( GL_FRAGMENT_SHADER_ARB, "rgbMorph.frag" )
	sP.linkShaders( )
	sP.enable( )
	global rgbTransformMatrix
	glUniformMatrix4fvARB(sP.indexOfUniformVariable("RGBTransformationMatrix"), \
		1, False, rgbTransformMatrix)

quadList = None
rgbTransformMatrix = [ 0.0 for i in range( 16 ) ]
rgbTransformMatrix[0] = rgbTransformMatrix[5] = rgbTransformMatrix[10] \
	= rgbTransformMatrix[15] = 1.0
def init( fileName ):
	try:
		texture = FileTexture( fileName )
	except:
		print 'could not open ', fileName, '; using random texture'
		texture = RandomTexture( 256, 256 )
	glClearColor ( 0, 0, 0, 0 )
	glShadeModel( GL_SMOOTH )
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
	glTexImage2D( GL_TEXTURE_2D, 0, 3, texture.xSize, texture.ySize, 0,
				 GL_RGB, GL_UNSIGNED_BYTE, texture.rawReference )
	glEnable( GL_TEXTURE_2D )
	global quadList
	quadList = glGenLists( 1 )
	glNewList( quadList, GL_COMPILE )
	glBegin( GL_QUADS )
	glTexCoord2f( 0, 1 )
	glVertex3f( -0.5, 0.5, 0 )
	glTexCoord2f( 0, 0 )
	glVertex3f( -0.5, -0.5, 0 )
	glTexCoord2f( 1, 0 )
	glVertex3f( 0.5, -0.5, 0 )
	glTexCoord2f( 1, 1 )
	glVertex3f( 0.5, 0.5, 0 )
	glEnd(  )
	glEndList( )
	initShaders( )

def main():
	import logging
	logging.basicConfig()
	glutInit( sys.argv )
	glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
	glutInitWindowSize( 250, 250 )
	glutInitWindowPosition( 100, 100 )
	glutCreateWindow( sys.argv[0] )
	glutDisplayFunc( display )
	glutIdleFunc( animationStep )
	glutMainLoop(  )

if __name__ == "__main__":
	main()
	
