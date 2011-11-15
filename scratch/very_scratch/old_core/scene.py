#!/usr/bin/python

import sys
import time
import numpy as np
import Image # PIL
from fos.core import collision as cll
from fos.core import plots

try:
    
    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    import OpenGL.GLU as glu
    
except ImportError:
    
    ImportError('PyOpenGL is not installed')

import mouse


class Scene(object):

    
    def __init__(self,plot=plots.Plot()):

        #Window settings
        self.disp_mode=glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH
        self.win_size=(1280,1024)#width,height
        self.win_pos=(100,100)#px,py
        self.win_title='F.O.S.'
        

        #Init settings
        self.clear_color=(0.,0.,0.,1.) #rgba
        self.enab_depth=gl.GL_DEPTH_TEST
        self.shade_model=gl.GL_SMOOTH #or gl.GL_FLAT
        self.depth_range=(0.0,1.0) #default z mapping

        #Reshape settings
        self.viewport=(0,0,self.win_size[0],self.win_size[1])
        self.isperspect=1
        self.glu_perspect=[60.,self.win_size[0]/self.win_size[1],0.1,2000.]
        self.gl_orthog=(-300.,300.,-300.,300.,-1000,1000)       

        #Camera settings
        self.glu_lookat=(0.,0.,170., 0.,0.,0., 0.,1.,0.) 

        #Display settings
        self.clear_bit=gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT

        #Lights settings
        self.enab_light=gl.GL_LIGHTING #enable lighting
        self.enab_light0=gl.GL_LIGHT0 #enable first light

        #self.light_model=gl.GL_LIGHT_MODEL_AMBIENT
        #self.light_model_value=[0.5,0.5,0.5,1.]
        self.light_model=gl.GL_LIGHT_MODEL_TWO_SIDE
        self.light_model_value=gl.GL_FALSE

        self.light0_position=[1,1,1,0] # light position is at Inf,Inf,Inf       
        self.light0_ambient=[0.2,0.2,0.2,1.]
        self.light0_diffuse=[.2,.2,.2,1.]
        self.light0_specular=[.2,.2,.2,1.]

        
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

        #Animation timing settings
        self.timer1=self.animation_timer
        self.timer1Dt=33 # duration between consecutive runs in milliseconds
        self.autostart_timer1=True
        self.timer1on=True
        self.recordingon=False        

        #World timing settings
        self.timer2=self.world_timer
        self.timer2Dt=1000
        self.autostart_timer2=True
        self.timer2on=True
        self.time2now=0 #holds current time in milliseconds

        #Video settings
        self.frameno=0
        self.video_dir='/tmp/'

        #Extra Testing settings

        self.plot=plot

    
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
        
        #gl.glLightModeli(self.light_model,self.light_model_value)
        
        #gl.glLightModelfv(self.light_model,self.light_model_value)

        gl.glLightfv(self.enab_light0,gl.GL_POSITION, self.light0_position)

        gl.glLightfv(self.enab_light0,gl.GL_AMBIENT, self.light0_ambient)

        gl.glLightfv(self.enab_light0,gl.GL_DIFFUSE, self.light0_diffuse)

        gl.glLightfv(self.enab_light0,gl.GL_SPECULAR,self.light0_specular)

        #Load objects

        #self.objects()

        #!global plot

        #!plot=plots.Plot()

        self.plot.init()
  

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

            if self.recordingon==False:

                self.recordingon=True

                print('Recording is on')

            else:

                self.recordingon=False

                print('Recording is off')
                

        if key == '9': #zoom out

            
            self.glu_perspect[0]+=10.#self.glu_perspect[0]

            glut.glutPostRedisplay()

        if key == '0': #zoom in

            self.glu_perspect[0]-=10. #0.5*self.glu_perspect[0]

            glut.glutPostRedisplay()
                

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

            self.glu_perspect[0]=60.

            self.mouse.rotationMatrix.reset()
            
            self.mouse.translationMatrix.reset()
            
            glut.glutPostRedisplay()
            
        if key == 'j':

            cube.position[0]+=10.

            glut.glutPostRedisplay()

        if key == 'k':

            cube.position[0]-=10.

            glut.glutPostRedisplay()


        if key == 'p':

            viewport=gl.glGetDoublev(gl.GL_VIEWPORT)

            #print 'Viewport'
            #print viewport

            #print float(x), viewport[3]-float(y)
    
            xn,yn,zn=glu.gluUnProject(np.double(x),viewport[3]-np.double(y),0.)

            #print 'World Coordinates Near'
            #print xn,yn,zn

            xf,yf,zf=glu.gluUnProject(np.double(x),viewport[3]-np.double(y),1.)
            
            near=np.array([xn,yn,zn])
            far =np.array([xf,yf,zf])

            self.plot.update_pick_ray(near,far)
            
           
	if key == '\033':
            
            sys.exit()

    def animation_timer(self,value):

        #print value

        if self.timer1on:

            if self.recordingon:

                self.save(filename=self.video_dir+'{0:010d}'.format(self.frameno)+'.png')
        
                self.frameno+=1
        
            glut.glutPostRedisplay()
        
            glut.glutTimerFunc( self.timer1Dt, self.animation_timer, 1)


    def world_timer(self,value):

        if self.timer2on:

            self.time2now+=self.timer2Dt

            self.plot.update_time(self.time2now)

            glut.glutTimerFunc( self.timer2Dt, self.world_timer, 1)


    def interaction(self):
        
        
        glut.glutDisplayFunc(self.disp)
        
        glut.glutReshapeFunc(self.resh)
        
        glut.glutKeyboardFunc(self.key)

        transl_scale,rotation_scale=self.mouse_scale
        
        self.mouse=mouse.MouseInteractor(transl_scale,rotation_scale)

        #registers both glutMouseFunc and glutMotionFunc
        self.mouse.registerCallbacks()

        if self.autostart_timer1:

            glut.glutTimerFunc(self.timer1Dt,self.timer1,1) 

        if self.autostart_timer2:

            glut.glutTimerFunc(self.timer2Dt,self.timer2,1) 
            
        

    def display(self):

        gl.glClear(self.clear_bit)        

        x,y,w,h=self.viewport
        
        gl.glMatrixMode (gl.GL_PROJECTION)
        
        gl.glLoadIdentity()
                

        if self.isperspect:

            fovy,aspect,zNear,zFar=self.glu_perspect

            #print fovy
        
            glu.gluPerspective(fovy,w/float(h),zNear,zFar)

        else:

            left,right,bottom,top,near,far=self.gl_orthog
            
            gl.glOrtho(left, right, bottom, top, near, far)
        

        

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

        #t3d.display()

        #dp.display()

        '''
      
        gl.glDisable(self.enab_light)
        
        gl.glColor3f(1.,1.,0.3)        
        
        gl.glRasterPos3f(4.,4.,4.)
        
        for c in "hello :-)":

            glut.glutBitmapCharacter( glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c) )               
        gl.glEnable(self.enab_light)

        '''

        self.plot.display()

        gl.glFlush()
        
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

class SceneStuff(object):

    
    def __init__(self,plot=plots.Plot()):

        #Window settings
        self.disp_mode=glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH
        self.win_size=(1280,1024)#width,height
        self.win_pos=(100,100)#px,py
        self.win_title='F.O.S.'
        

        #Init settings
        self.clear_color=(0.,0.,0.,1.) #rgba
        self.enab_depth=gl.GL_DEPTH_TEST
        self.shade_model=gl.GL_SMOOTH #or gl.GL_FLAT
        self.depth_range=(0.0,1.0) #default z mapping

        #Reshape settings
        self.viewport=(0,0,self.win_size[0],self.win_size[1])
        self.isperspect=1
        self.glu_perspect=[60.,self.win_size[0]/self.win_size[1],0.1,2000.]
        self.gl_orthog=(-300.,300.,-300.,300.,-1000,1000)       

        #Camera settings
        self.glu_lookat=(0.,0.,150., 0.,0.,0., 0.,1.,0.) 

        #Display settings
        self.clear_bit=gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT

        #Lights settings
        self.enab_light=gl.GL_LIGHTING #enable lighting
        self.enab_light0=gl.GL_LIGHT0 #enable first light

        #self.light_model=gl.GL_LIGHT_MODEL_AMBIENT
        #self.light_model_value=[0.5,0.5,0.5,1.]
        self.light_model=gl.GL_LIGHT_MODEL_TWO_SIDE
        self.light_model_value=gl.GL_FALSE

        self.light0_position=[1,1,1,0] # light position is at Inf,Inf,Inf       
        self.light0_ambient=[0.2,0.2,0.2,1.]
        self.light0_diffuse=[.2,.2,.2,1.]
        self.light0_specular=[.2,.2,.2,1.]

        
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

        #Animation timing settings
        self.timer1=self.animation_timer
        self.timer1Dt=33 # duration between consecutive runs in milliseconds
        self.autostart_timer1=True
        self.timer1on=True
        self.recordingon=False        

        #World timing settings
        self.timer2=self.world_timer
        self.timer2Dt=1000
        self.autostart_timer2=True
        self.timer2on=True
        self.time2now=0 #holds current time in milliseconds

        #Video settings
        self.frameno=0
        self.video_dir='/tmp/'

        #Extra Testing settings

        self.plot=plot

    
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
        
        #gl.glLightModeli(self.light_model,self.light_model_value)
        
        #gl.glLightModelfv(self.light_model,self.light_model_value)

        gl.glLightfv(self.enab_light0,gl.GL_POSITION, self.light0_position)

        gl.glLightfv(self.enab_light0,gl.GL_AMBIENT, self.light0_ambient)

        gl.glLightfv(self.enab_light0,gl.GL_DIFFUSE, self.light0_diffuse)

        gl.glLightfv(self.enab_light0,gl.GL_SPECULAR,self.light0_specular)

        #Load objects

        #self.objects()

        #!global plot

        #!plot=plots.Plot()

        self.plot.init()
  

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

            if self.recordingon==False:

                self.recordingon=True

                print('Recording is on')

            else:

                self.recordingon=False

                print('Recording is off')
                

        if key == '9': #zoom out

            
            self.glu_perspect[0]+=10.#self.glu_perspect[0]

            glut.glutPostRedisplay()

        if key == '0': #zoom in

            self.glu_perspect[0]-=10. #0.5*self.glu_perspect[0]

            glut.glutPostRedisplay()
                

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

            self.glu_perspect[0]=60.

            self.mouse.rotationMatrix.reset()
            
            self.mouse.translationMatrix.reset()
            
            glut.glutPostRedisplay()
            
        if key == 'j':

            cube.position[0]+=10.

            glut.glutPostRedisplay()

        if key == 'k':

            cube.position[0]-=10.

            glut.glutPostRedisplay()


        if key == 'p':

            viewport=gl.glGetDoublev(gl.GL_VIEWPORT)

            #print 'Viewport'
            #print viewport

            #print float(x), viewport[3]-float(y)
    
            xn,yn,zn=glu.gluUnProject(np.double(x),viewport[3]-np.double(y),0.)

            #print 'World Coordinates Near'
            #print xn,yn,zn

            xf,yf,zf=glu.gluUnProject(np.double(x),viewport[3]-np.double(y),1.)
            
            near=np.array([xn,yn,zn])
            far =np.array([xf,yf,zf])

            self.plot.update_pick_ray(near,far)
            
           
	if key == '\033':
            
            sys.exit()

    def animation_timer(self,value):

        #print value

        if self.timer1on:

            if self.recordingon:

                self.save(filename=self.video_dir+'{0:010d}'.format(self.frameno)+'.png')
        
                self.frameno+=1
        
            glut.glutPostRedisplay()
        
            glut.glutTimerFunc( self.timer1Dt, self.animation_timer, 1)


    def world_timer(self,value):

        if self.timer2on:

            self.time2now+=self.timer2Dt

            self.plot.update_time(self.time2now)

            glut.glutTimerFunc( self.timer2Dt, self.world_timer, 1)


    def interaction(self):
        
        
        glut.glutDisplayFunc(self.disp)
        
        glut.glutReshapeFunc(self.resh)
        
        glut.glutKeyboardFunc(self.key)

        transl_scale,rotation_scale=self.mouse_scale
        
        self.mouse=mouse.MouseInteractor(transl_scale,rotation_scale)

        #registers both glutMouseFunc and glutMotionFunc
        self.mouse.registerCallbacks()

        if self.autostart_timer1:

            glut.glutTimerFunc(self.timer1Dt,self.timer1,1) 

        if self.autostart_timer2:

            glut.glutTimerFunc(self.timer2Dt,self.timer2,1) 
            
        

    def display(self):

        gl.glClear(self.clear_bit)        

        x,y,w,h=self.viewport
        
        gl.glMatrixMode (gl.GL_PROJECTION)
        
        gl.glLoadIdentity()
                

        if self.isperspect:

            fovy,aspect,zNear,zFar=self.glu_perspect

            #print fovy
        
            glu.gluPerspective(fovy,w/float(h),zNear,zFar)

        else:

            left,right,bottom,top,near,far=self.gl_orthog
            
            gl.glOrtho(left, right, bottom, top, near, far)
        

        

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

        #t3d.display()

        #dp.display()

        '''
      
        gl.glDisable(self.enab_light)
        
        gl.glColor3f(1.,1.,0.3)        
        
        gl.glRasterPos3f(4.,4.,4.)
        
        for c in "hello :-)":

            glut.glutBitmapCharacter( glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c) )               
        gl.glEnable(self.enab_light)

        '''

        self.plot.display()

        gl.glFlush()
        
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


    engine = Scene()
    
    engine.run()







        
        
        
    
