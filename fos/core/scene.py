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
import primitives


class Scene(object):

    
    def __init__(self):

        #Window settings
        self.disp_mode=glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH
        self.win_size=(1080,800)#width,height
        self.win_pos=(100,100)#px,py
        self.win_title='F.O.S.'
        

        #Init settings
        self.clear_color=(0.,0.,0.,0.) #rgba
        self.enab_depth=gl.GL_DEPTH_TEST
        self.shade_model=gl.GL_SMOOTH #or gl.GL_FLAT
        self.depth_range=(0.0,1.0) #default z mapping

        #Reshape settings
        self.viewport=(0,0,self.win_size[0],self.win_size[1])
        self.isperspect=1
        self.glu_perspect=(60.,self.win_size[0]/self.win_size[1],0.1,2000.)
        self.gl_orthog=(-300.,300.,-300.,300.,-1000,1000)       

        #Camera settings
        self.glu_lookat=(0.,0.,150., 0.,0.,0., 0.,1.,0.) 

        #Display settings
        self.clear_bit=gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT

        #Lights settings
        self.enab_light=gl.GL_LIGHTING #enable lighting
        self.enab_light0=gl.GL_LIGHT0 #enable first light

        self.light_model=gl.GL_LIGHT_MODEL_TWO_SIDE
        self.light_model_value=gl.GL_FALSE 
        self.light0_position=[1,1,1,0] # light position is at Inf,Inf,Inf 
        self.light0_ambient=[0.8,0.8,0.8,1.]
        self.light0_diffuse=[1.,1.,1.,1.]
        self.light0_specular=[1.,1.,1.,1.]
        
        #Interaction settings
        self.disp=self.display
        self.resh=self.reshape
        self.key=self.keystroke
        self.mouse_scale=(1.,1.) # translation & rotational scale
        self.mouse=None

        #Selection settings
        self.selection_buffer_size=100
        self.selection_buffer=self.selection_buffer_size*[0]
        self.selection_region=(1,1)#rectangle width, height

        #Timing settings
        self.timer1=self.video_timer
        self.timer1Dt=33 # duraction between consecutive runs in milliseconds
        self.autostart_timer1=False
        self.timer1on=False

        #Video settings
        self.frameno=0
        self.video_dir='/tmp/'

        #Extra Testing settings        

    
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
       
        
        gl.glEnable(self.enab_light)

        gl.glEnable(self.enab_light0)
        
        gl.glLightModeli(self.light_model,self.light_model_value)

        gl.glLightfv(self.enab_light0,gl.GL_POSITION, self.light0_position)

        gl.glLightfv(self.enab_light0,gl.GL_AMBIENT, self.light0_ambient)

        gl.glLightfv(self.enab_light0,gl.GL_DIFFUSE, self.light0_diffuse)

        gl.glLightfv(self.enab_light0,gl.GL_SPECULAR,self.light0_specular)

        #Load objects

        self.objects()
   

    def objects(self):

        #primitives.load_pot()

        #global cube        

        #cube=primitives.Collection()

        #cube.init()

        #global bsurf

        #bsurf=primitives.BrainSurface()

        #bsurf.init()

        #global im2d

        #im2d = primitives.Image2D()

        #im2d.init()

        global t3d

        t3d = primitives.Tracks3D()

        t3d.init()
        
        #global cube2

        #cube2=primitives.Collection()

        #cube2.init()
  

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

        key=args[0]

        x=args[1]

        y=args[2]

        if key == 's':

            self.save()

        if key == 'v':

            if self.autostart_timer1==False:

                if self.timer1on==False:

                    print('timer1 is on')

                    self.timer1on=True

                    glut.glutTimerFunc(self.timer1Dt, self.timer1,1)                    

                else:

                    print('timer1 is off')                    

                    self.timer1on=False

        if key == 'o':
            
            self.isperspect=int(not(self.isperspect))

            if self.isperspect:

                print('perspective projection on')
                
            else:
                
                print('orthogonal projection on')
           
            px,py,w,h=self.viewport
            
            self.reshape(w,h)
            
            glut.glutPostRedisplay()

        if args[0] == 'r':

            self.mouse.rotationMatrix.reset()
            
            self.mouse.translationMatrix.reset()
            
            glut.glutPostRedisplay()
            
        if key == 'j':

            cube.position[0]+=10.

            glut.glutPostRedisplay()

        if key == 'k':

            cube.position[0]-=10.

            glut.glutPostRedisplay()


        if key == 'p' or key == 'P': # picking       

            viewport=gl.glGetIntegerv(gl.GL_VIEWPORT)
 
            w=viewport[2]-viewport[0]

            h=viewport[3]-viewport[1]
                        
            #gl.glSelectBuffer(self.selection_buffer_size, self.selection_buffer) 

            gl.glSelectBuffer(self.selection_buffer_size)
            
            gl.glRenderMode(gl.GL_SELECT)

            gl.glInitNames()

            gl.glPushName(0)

            gl.glMatrixMode(gl.GL_PROJECTION)

            gl.glPushMatrix()

            gl.glLoadIdentity()

            selw,selh=self.selection_region

            glu.gluPickMatrix(x,viewport[3]-y,selw, selh, viewport)

            if self.isperspect:

                fovy,aspect,zNear,zFar=self.glu_perspect
        
                glu.gluPerspective(fovy,w/float(h),zNear,zFar)

            else:

                left,right,bottom,top,near,far=self.gl_orthog
            
                gl.glOrtho(left, right, bottom, top, near, far)

                    
            cube.display(gl.GL_SELECT)
            
            gl.glPopMatrix()
            
            gl.glFlush()

            buffer = gl.glRenderMode(gl.GL_RENDER)
            
            glut.glutPostRedisplay()
        
            for hit_record in buffer:

                min_depth, max_depth, names = hit_record

                print min_depth, max_depth, names#, self.selection_buffer
                
            
	if key == '\033':
            
            sys.exit()

    def video_timer(self,value):

        #print value

        if self.timer1on==True:

            self.save(filename=self.video_dir+'{0:010d}'.format(self.frameno)+'.png')
        
            self.frameno+=1
        
            glut.glutPostRedisplay()
        
            glut.glutTimerFunc( self.timer1Dt, self.video_timer, 1)

        


    def interaction(self):
        
        
        glut.glutDisplayFunc(self.disp)
        
        glut.glutReshapeFunc(self.resh)
        
        glut.glutKeyboardFunc(self.key)

        transl_scale,rotation_scale=self.mouse_scale
        
        self.mouse=mouse.MouseInteractor(transl_scale,rotation_scale)

        #registers both glutMouseFunc and glutMotionFunc
        self.mouse.registerCallbacks()
        
        #glut.glutTimerFunc(self.timer1Dt,self.timer1,1)       

        

    def display(self):

        gl.glClear(self.clear_bit)

        gl.glMatrixMode(gl.GL_MODELVIEW)       

        gl.glLoadIdentity()

        eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=self.glu_lookat

        

        glu.gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
        
        #gl.glTranslatef(0,0,-150)

        self.mouse.applyTransformation()

        #Add objects

        #cube.display()

        #bsurf.display()

        #im2d.display()

        #cube.display()
        #cube2.display()

        #primitives.render_pot()
        #primitives.render2_pot()

        t3d.display()

        '''
      
        gl.glDisable(self.enab_light)
        
        gl.glColor3f(1.,1.,0.3)        
        
        gl.glRasterPos3f(4.,4.,4.)
        
        for c in "hello :-)":

            glut.glutBitmapCharacter( glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c) )       
        
        gl.glEnable(self.enab_light)

        '''
        
        glut.glutSwapBuffers()        

    def reshape(self,w,h):        

        #px,py,w,h=self.viewport
        gl.glViewport (0,0,w,h)

        self.viewport=(0,0,w,h)
        
        gl.glMatrixMode (gl.GL_PROJECTION)
        
        gl.glLoadIdentity ()
                

        if self.isperspect:

            fovy,aspect,zNear,zFar=self.glu_perspect
        
            glu.gluPerspective(fovy,w/float(h),zNear,zFar)

        else:

            left,right,bottom,top,near,far=self.gl_orthog
            
            gl.glOrtho(left, right, bottom, top, near, far)

        gl.glMatrixMode (gl.GL_MODELVIEW) 

        gl.glLoadIdentity ()
        
        eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=self.glu_lookat

        glu.gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
        


    def run(self):

        self.window()
        
        self.init()
        
        self.interaction()

        glut.glutMainLoop()




if __name__ == "__main__":

    engine=Scene()
    engine.run()







        
        
        
    
