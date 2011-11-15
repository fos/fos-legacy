#from pyglet.gl import *
from pyglet.gl import glPushMatrix, glLoadIdentity, glPopMatrix, glMultMatrixf, \
    glRotatef, glTranslatef, gluLookAt
    
from fos.core.utils import get_model_matrix #,screen_to_model,get_viewport

class TransformCamera():
    
    def __init__(self, matrix=None):
        self.matrix=matrix
        self.reset()
       
    def reset(self):        
        glPushMatrix()
        glLoadIdentity()
        self.matrix=get_model_matrix() 
        glPopMatrix()

    def translate(self,dx,dy,dz):
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(dx,dy,dz)
        glMultMatrixf(self.matrix)
        self.matrix=get_model_matrix()
        glPopMatrix()

    def rotate(self,ang,rx,ry,rz):
        glPushMatrix()
        glLoadIdentity()
        glRotatef(ang,rx,ry,rz)
        glMultMatrixf(self.matrix)
        self.matrix=get_model_matrix()
        glPopMatrix()
  
class Camera():
    
    def __init__(self):
        pass
    
    def update(self):
        " This should update the camera "
        pass

    def draw(self):
        pass
    
    def info(self):
        pass
    
# for ideas: 
# http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/auto/mlab_camera.html
# http://www.opengl.org/resources/faq/technical/viewing.htm
  
class DefaultCamera(Camera):
    
    def __init__(self):
        self.lookat=[0,0,120,0,0,0,0,1,0]
        self.scroll_speed=10
        self.mouse_speed=0.1  
        self.cam_rot = TransformCamera()
        self.cam_trans = TransformCamera() 
        
    def draw(self):
        eyex,eyey,eyez,centx,centy,centz,upx,upy,upz=self.lookat
        gluLookAt(eyex,eyey,eyez,centx,centy,centz,upx,upy,upz)
        glMultMatrixf(self.cam_trans.matrix)
        glMultMatrixf(self.cam_rot.matrix)

    def reset(self):
        """ Resets the camera to the original position """
        self.lookat=[0,0,120,0,0,0,0,1,0]
        self.cam_rot.reset()
        self.cam_trans.reset()
        
        
    def set_position(self, x, y, z):
        """ Set the position of the camera """
        self.lookat[0], self.lookat[1], self.lookat[2] = x,y,z
        self.cam_rot.reset()
        self.cam_trans.reset()

    def set_lookatposition(self, x, y, z):
        """ Set the position the camera looks at """
        self.lookat[3], self.lookat[4], self.lookat[5] = x,y,z   
        
    def set_yupvector(self, xdir, ydir, zdir):
        """ Set the Y up vector of the camera """
        self.lookat[6], self.lookat[7], self.lookat[8] = xdir,ydir,zdir
        
    def move(self, forward = None, right = None, up = None):
        """ Translates the camera with the given relative distances.
        Changes the camera position and the focal point """
        if not forward is None:
            self.lookat[2] -= forward
            self.lookat[5] -= forward
        if not right is None:
            self.lookat[0] -= right
            self.lookat[3] -= right
        if not up is None:
            self.lookat[1] -= up
            self.lookat[4] -= up

        

