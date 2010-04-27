import sys
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

#import fos.core.primitives as prim
import fos.core.text as text
import fos.core.cortex as cortex
import fos.core.pyramid as pyramid

import mouse 

MS=1000


def center(x,y):

    return ((int(1024-x)/2),int((768-y)/2))



class Plot():


    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

        

    def init(self):

        global csurf

        csurfr ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/rh.pial.vtk'

        #csurf_fname ='/home/eg309/Desktop/rh.pial.vtk'
        
        csurfl ='/home/eg01/Data_Backup/Data/Adam/multiple_transp_volumes/freesurfer_trich/lh.pial.vtk'

        csurfr = cortex.CorticalSurface(csurfr)
        
        csurfl = cortex.CorticalSurface(csurfl)

        csurfr.init()

        csurfl.init()
       
        self.slots={0:{'actor':csurfr,'slot':( 0,   800*MS )},
                    1:{'actor':csurfl,'slot':( 0,   800*MS )}}                 

        
          
    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick




class PlotIan():


    def __init__(self):

        self.disp_mode=glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH
        self.win_size=(1024,768)#width,height
        self.win_pos=(100,100)#px,py
        self.win_title='F.O.S.'
        
        #Interaction settings
        self.disp=self.display
        self.resh=self.reshape
        self.key=self.keystroke
        self.mouse_scale=(1.,1.) # translation & rotational scale
        self.mouse=None

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None

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

        

    def init(self):

        global pyr

        pyr = pyramid.Pyramid()

        pyr.init()


       
        self.slots={0:{'actor':pyr,'slot':( 0,   800*MS )}}                 


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

            plot.update_pick_ray(near,far)
            
           
	if key == '\033':
            
            sys.exit()

    def display(self):

        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()



    def update_time(self,time):

        self.time=time


    def update_pick_ray(self,near_pick, far_pick):

        self.near_pick = near_pick

        self.far_pick = far_pick

    def run(self):

        self.window()

        self.init()

        self.interaction()

        glut.glutMainLoop()


    def window(self):

        glut.glutInit(sys.argv)
        
        glut.glutInitDisplayMode (self.disp_mode)
        
        w,h=self.win_size
        
        glut.glutInitWindowSize (w,h)
        
        px,py=self.win_pos
        
        glut.glutInitWindowPosition (px,py)

        glut.glutCreateWindow (self.win_title)
        




if __name__ == "__main__":

    engine=PlotIan()

    engine.run()

     
                 



        



        
