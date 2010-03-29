import sys
import math

try:

    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    import OpenGL.GLU as glu

except ImportError:
    
    ImportError('PyOpenGL is not installed')

class InteractionMatrix ( object ):
	"""Class holding a matrix representing a rigid transformation.

	The current OpenGL is read into an internal variable and
	updated using rotations and translations given by
	user interaction."""

	def __init__( self ):
		self.__currentMatrix = None
		self.reset( )

	def reset( self ):
		"""Initialise internal matrix with identity"""
		gl.glPushMatrix( )
		gl.glLoadIdentity( )
		self.__currentMatrix = gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX )
		gl.glPopMatrix( )

	def addTranslation( self, tx, ty, tz ):
		"""Concatenate the internal matrix with a translation matrix"""
		gl.glPushMatrix( )
		gl.glLoadIdentity( )
		gl.glTranslatef(tx, ty, tz)
		gl.glMultMatrixf( self.__currentMatrix )
		self.__currentMatrix = gl.glGetFloatv( gl.GL_MODELVIEW_MATRIX )
		gl.glPopMatrix( )

	def addRotation( self, ang, rx, ry, rz ):
		"""Concatenate the internal matrix with a translation matrix"""
		gl.glPushMatrix( )
		gl.glLoadIdentity( )
		gl.glRotatef(ang, rx, ry, rz)
		gl.glMultMatrixf( self.__currentMatrix )
		self.__currentMatrix = gl.glGetFloatv( gl.GL_MODELVIEW_MATRIX )
		gl.glPopMatrix( )

	def getCurrentMatrix( self ):
		return self.__currentMatrix


class MouseInteractor (object):
	"""Connection between mouse motion and transformation matrix"""
	def __init__( self, translationScale=0.1, rotationScale=.2):
		self.scalingFactorRotation = rotationScale
		self.scalingFactorTranslation = translationScale
		self.rotationMatrix = InteractionMatrix( )
		self.translationMatrix = InteractionMatrix( )
		self.mouseButtonPressed = None
		self.oldMousePos = [ 0, 0 ]

	def mouseButton( self, button, mode, x, y ):
		"""Callback function for mouse button."""
		if mode == glut.GLUT_DOWN:
			self.mouseButtonPressed = button
		else:
			self.mouseButtonPressed = None
		self.oldMousePos[0], self.oldMousePos[1] = x, y
		glut.glutPostRedisplay( )

	def mouseMotion( self, x, y ):
		"""Callback function for mouse motion.

		Depending on the button pressed, the displacement of the
		mouse pointer is either converted into a translation vector
		or a rotation matrix."""

		deltaX = x - self.oldMousePos[ 0 ]
		deltaY = y - self.oldMousePos[ 1 ]
		if self.mouseButtonPressed == glut.GLUT_RIGHT_BUTTON:
			tX = deltaX * self.scalingFactorTranslation
			tY = deltaY * self.scalingFactorTranslation
			self.translationMatrix.addTranslation(tX, -tY, 0)

		elif self.mouseButtonPressed == glut.GLUT_LEFT_BUTTON:
			rY = deltaX * self.scalingFactorRotation
			self.rotationMatrix.addRotation(rY, 0, 1, 0)
			rX = deltaY * self.scalingFactorRotation
			self.rotationMatrix.addRotation(rX, 1, 0, 0)

		elif self.mouseButtonPressed == glut.GLUT_MIDDLE_BUTTON:
			tZ = deltaY * self.scalingFactorTranslation
			self.translationMatrix.addTranslation(0, 0, tZ)

		self.oldMousePos[0], self.oldMousePos[1] = x, y
		glut.glutPostRedisplay()

	def applyTransformation( self ):
		"""Concatenation of the current translation and rotation
		matrices with the current OpenGL transformation matrix"""

		gl.glMultMatrixf( self.translationMatrix.getCurrentMatrix() )
		gl.glMultMatrixf( self.rotationMatrix.getCurrentMatrix() )

	def registerCallbacks( self ):
		"""Initialise glut callback functions."""
		glut.glutMouseFunc( self.mouseButton )
		glut.glutMotionFunc( self.mouseMotion )
