import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import Image


class Texture(object):


    def __init__(self,fname):

        self.fname = fname

        self.texture_index = None

        self.format = gl.GL_RGBA # gl.GL_RGB, gl.GL_LUMINANCE

        self.components = 4 # 3 for RGB and 4 for RGBA

        self.size = None

        self.rotation_angle = 0.

        self.rotation_angle_speed = 2.


    def init_texture(self):

        image = Image.open(self.fname,'r')

        print self.fname

        image = image.convert('RGB')

        image = image.convert('RGBA')

        #image.putalpha(50)

        self.size = image.size

        image=image.tostring("raw",image.mode, 0, -1)

        self.texture_index = gl.glGenTextures(1)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_index)

        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)

        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT,1)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)


        w,h = self.size

        


        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        #gl.glColor4f(0,0,0,0)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, self.components, w, h, 0, self.format, gl.GL_UNSIGNED_BYTE, image) 
        
        gl.glEnable(gl.GL_TEXTURE_2D)

        #gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE,gl.GL_REPLACE)

        #gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_BLEND)

        #gl.glEnable(gl.GL_BLEND)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)



        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_index)


        #self.rotation_angle+=self.rotation_angle_speed
        
        #gl.glRotatef(self.rotation_angle,0,0,1)


        

        gl.glBegin(gl.GL_QUADS)

        #gl.glColor4f(1,0,0,1)


        gl.glTexCoord2f(0.0, 0.0)

        gl.glVertex3f(-100.0, -100.0, 0.0)


        gl.glTexCoord2f(0.0, 1.0)

        gl.glVertex3f(-100.0, 100.0, 0.0)


        gl.glTexCoord2f(1.0, 1.0)

        gl.glVertex3f(100.0, 100.0, 0.0)


        gl.glTexCoord2f(1.0, 0.0)

        gl.glVertex3f(100.0, -100.0, 0.0)
        

        gl.glEnd()


        gl.glFlush()

        gl.glDisable(gl.GL_TEXTURE_2D)


        gl.glEndList()

        

    def init(self):

        self.init_texture()

   


    def display(self):

        self.rotation_angle += self.rotation_angle_speed

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glEnable(gl.GL_BLEND)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)



        
        gl.glPushMatrix()

        gl.glTranslatef(0,0.,0.)               


        gl.glRotatef(self.rotation_angle,0,0,1)
        
        #gl.glColor4f(1,0,0,0.5)
        
        gl.glCallList(self.list_index)

        gl.glPopMatrix()


        #gl.glTranslatef(100,0.,0.)               


        gl.glPushMatrix()


        gl.glTranslatef(0,0.,0.)               

        #gl.glColor4f(1,1,0,0.4)

        gl.glRotatef(2*self.rotation_angle,0,0,1)
        

        gl.glCallList(self.list_index)

        gl.glPopMatrix()
        

        

        
