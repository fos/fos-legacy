import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import Image


class Texture(object):


    def __init__(self,fname):

        self.fname = fname

        self.texture_index = None

        self.format = gl.GL_RGB # gl.GL_RGB, gl.GL_LUMINANCE

        self.components = 3 # 3 for RGB and 4 for RGBA

        self.size = None

    def init(self):

        image = Image.open(self.fname,'r')

        image = image.convert('RGB')

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

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, self.components, w, h, 0, self.format, gl.GL_UNSIGNED_BYTE, image) 



    def display(self):

        gl.glEnable(gl.GL_TEXTURE_2D)

        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_REPLACE)

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_index)

        gl.glBegin(gl.GL_QUADS)


        gl.glTexCoord2f(0.0, 0.0)

        gl.glVertex3f(0.0, 0.0, 0.0)


        gl.glTexCoord2f(0.0, 1.0)

        gl.glVertex3f(0.0, 100.0, 0.0)


        gl.glTexCoord2f(1.0, 1.0)

        gl.glVertex3f(100.0, 100.0, 0.0)


        gl.glTexCoord2f(1.0, 0.0)

        gl.glVertex3f(100.0, 0.0, 0.0)
        

        gl.glEnd()

        gl.glFlush()

        gl.glDisable(gl.GL_TEXTURE_2D)

        
