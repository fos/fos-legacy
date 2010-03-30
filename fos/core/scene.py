#!/usr/bin/python

import sys
import numpy as np

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
        self.disp_mode=glut.GLUT_DOUBLE | glut.GLUT_RGB
        self.win_size=(800,800)#width,height
        self.win_pos=(100,100)#px,py
        self.win_title='Tractography'
        

        #Init settings
        self.clear_color=(0.,0.,0.,0.) #rgba
        self.enab_depth=gl.GL_DEPTH_TEST
        self.shade_model=gl.GL_FLAT
        self.depth_range=(0.0,1.0) #default z mapping

        #Interaction settings
        self.disp=self.display
        self.resh=self.reshape
        self.mouse_scale=(0.01,0.02) # translation & rotational scale
        self.mouse=None        
        
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


    def interaction(self):
        
        transl_scale,rotation_scale=self.mouse_scale
        self.mouse=mouse.MouseInteractor(transl_scale,rotation_scale)
        self.mouse.registerCallbacks()

        glut.glutDisplayFunc(self.disp)
        glut.glutReshapeFunc(self.resh)
        
        #glut.glutKeyboardFunc(key)
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
        glu.gluPerspective(fovy,aspect,zNear,zFar)
                        
        #gl.glOrtho(0.0, 8.0, 0.0, 8.0, -0.5, 2.5)
        gl.glMatrixMode (gl.GL_MODELVIEW)    
        gl.glLoadIdentity ()
        
        eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=self.glu_lookat
        glu.gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
        


    def start(self):

        self.window()
        self.init()
        self.interaction()
        glut.glutMainLoop()



engine=Scene()
engine.start()




        
        
        
    
