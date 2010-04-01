#!/usr/bin/python

import sys
import time
import numpy as np
import Image # PIL


try:
    
    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    import OpenGL.GLU as glu
    
except ImportError:
    
    ImportError('PyOpenGL is not installed')

import mouse
#import primitives


class Scene(object):

    
    def __init__(self):

        #Window settings
        self.disp_mode=glut.GLUT_DOUBLE | glut.GLUT_RGBA
        self.win_size=(1080,800)#width,height
        self.win_pos=(100,100)#px,py
        self.win_title='FOS means light in Greek'
        

        #Init settings
        self.clear_color=(0.,0.,0.,0.) #rgba
        self.enab_depth=gl.GL_DEPTH_TEST
        self.shade_model=gl.GL_FLAT
        self.depth_range=(0.0,1.0) #default z mapping

        #Interaction settings
        self.disp=self.display
        self.resh=self.reshape
        self.key=self.keystroke
        self.mouse_scale=(0.01,0.02) # translation & rotational scale
        self.mouse=None        

        #Timing settings
        self.timer1=self.video_timer
        self.timer1Dt=33 # in milliseconds

        #Video settings
        self.frameno=0
        self.video_dir='/tmp/'
        
        #Reshape settings
        self.viewport=(0,0,self.win_size[0],self.win_size[1])        
        self.glu_perspect=(30.,self.win_size[0]/self.win_size[1],0.,200.)
        self.glu_lookat=(0.,0.,150., 0.,0.,0., 0.,1.,0.) 

        #Display settings
        self.clear_bit=gl.GL_COLOR_BUFFER_BIT

    
    def window(self):

        glut.glutInit(sys.argv)
        
        glut.glutInitDisplayMode (self.disp_mode)
        
        w,h=self.win_size
        glut.glutInitWindowSize (w,h)
        
        px,py=self.win_pos
        glut.glutInitWindowPosition (px,py)

        glut.glutCreateWindow (self.win_title)

    def init(self):
        
        r,g,b,a=self.clear_color
        gl.glClearColor (r,g,b,a)
        
        gl.glEnable(self.enab_depth)
        
        gl.glShadeModel (self.shade_model)
        
        near,far=self.depth_range
        
        gl.glDepthRange(near,far) #default z mapping

    def save(self, filename="test.png", format="PNG" ):
	"""Save current buffer to filename in format

        try also test.jpg with format="JPEG"

        """
	
	x,y,width,height = gl.glGetDoublev(gl.GL_VIEWPORT)
        
	width,height = int(width),int(height)
        
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        
	data = gl.glReadPixels(x, y, width, height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)        
	image = Image.fromstring( "RGB", (width, height), data )
        
	image = image.transpose( Image.FLIP_TOP_BOTTOM)
        
	image.save( filename, format )
	#print 'Saved image to %s'% (os.path.abspath( filename))
	#return image

    def keystroke(self,*args):
	# If escape is pressed, kill everything.

        if args[0] == 's':

            self.save()            
            
	if args[0] == '\033':
            sys.exit()

    def video_timer(self,value):
        
        self.save(filename=self.video_dir+'{0:010d}'.format(self.frameno)+'.png')
        
        self.frameno+=1
        
        glut.glutPostRedisplay()
        
        glut.glutTimerFunc( self.timer1Dt, self.video_timer, 1)       


    def interaction(self):
        
        transl_scale,rotation_scale=self.mouse_scale
        
        self.mouse=mouse.MouseInteractor(transl_scale,rotation_scale)
        
        self.mouse.registerCallbacks()

        glut.glutDisplayFunc(self.disp)
        
        glut.glutReshapeFunc(self.resh)
        
        glut.glutKeyboardFunc(self.key)
        
        glut.glutTimerFunc(self.timer1Dt,self.timer1,1)
        
        #glut.glutMouseFunc(mous)
        

    def display(self):

        gl.glClear(self.clear_bit)
        #load primitives
        #glut.glutSolidTeapot(5.0)
        glut.glutWireCube(50.)
        
        self.mouse.applyTransformation()
        
        glut.glutSwapBuffers()

    def reshape(self,w,h):
        

        #px,py,w,h=self.viewport
        gl.glViewport (0,0,w,h)
        
        gl.glMatrixMode (gl.GL_PROJECTION)
        
        gl.glLoadIdentity ()
        
        fovy,aspect,zNear,zFar=self.glu_perspect
        
        glu.gluPerspective(fovy,w/float(h),zNear,zFar)
                        
        #gl.glOrtho(0.0, 8.0, 0.0, 8.0, -0.5, 2.5)

        gl.glMatrixMode (gl.GL_MODELVIEW)    

        gl.glLoadIdentity ()
        
        eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=self.glu_lookat

        glu.gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
        


    def run(self):

        self.window()
        
        self.init()
        
        self.interaction()

        glut.glutMainLoop()



#engine=Scene()
#engine.run()







        
        
        
    
