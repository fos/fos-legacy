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
        self.position=(0,0,0)
        self.orbit=None
        self.orbit_index=0
    def init_texture(self):
        image = Image.open(self.fname,'r')
        print self.fname
        image = image.convert('RGB')
        image = image.convert('RGBA')
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
        gl.glVertex3f(-10.0, -10.0, 0.0)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex3f(-10.0, 10.0, 0.0)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex3f(10.0, 10.0, 0.0)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex3f(10.0, -10.0, 0.0)
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
        if self.orbit == None:
            x,y,z=self.position
        else:
            #print'Next'
            x,y,z=self.orbit[self.orbit_index]
            if self.orbit_index < len(self.orbit)-1:
                self.orbit_index+=1
            else:
                self.orbit_index=0
        gl.glPushMatrix()
        gl.glTranslatef(x,y,z)               
        gl.glRotatef(self.rotation_angle,0,0,1)
        #gl.glColor4f(1,0,0,0.5)
        gl.glCallList(self.list_index)
        gl.glPopMatrix()
        #gl.glTranslatef(100,0.,0.)               
        gl.glPushMatrix()
        gl.glTranslatef(x,y,z)               
        #gl.glColor4f(1,1,0,0.4)
        gl.glRotatef(2*self.rotation_angle,0,0,1)
        gl.glCallList(self.list_index)
        gl.glPopMatrix()
        


class Texture_Demo(object):


    def __init__(self,fname,red=True,green=True,blue=True):
        self.fname = fname
        self.texture_index = None
        self.format = gl.GL_RGBA # gl.GL_RGB, gl.GL_LUMINANCE
        self.components = 4 # 3 for RGB and 4 for RGBA
        self.size = None
        self.rotation_angle = 0.
        self.rotation_angle_speed = 2.
        self.position=(0,0,0)
        self.orbit=None
        self.orbit_index=0
        self.lists=[]
        self.orbits=[]
        self.orbits_index=None
        self.red = red
        self.green = green
        self.blue = blue

    def init_texture(self,image):
        w,h = self.size
        self.list_index = gl.glGenLists(1)
        self.lists.append(self.list_index)
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
        gl.glVertex3f(-10.0, -10.0, 0.0)
        gl.glTexCoord2f(0.0, 1.0)
        gl.glVertex3f(-10.0, 10.0, 0.0)
        gl.glTexCoord2f(1.0, 1.0)
        gl.glVertex3f(10.0, 10.0, 0.0)
        gl.glTexCoord2f(1.0, 0.0)
        gl.glVertex3f(10.0, -10.0, 0.0)
        gl.glEnd()
        gl.glFlush()
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEndList()

    def init(self):
        image = Image.open(self.fname,'r')
        print self.fname
        image = image.convert('RGB')
        image = image.convert('RGBA')
        #image.putalpha(50)
        self.size = image.size
        col = [self.red,self.green, self.blue]
        for x,y in np.ndindex(self.size[0],self.size[1]):
            r,g,b,a=image.getpixel((x,y))
            #print x,y,r,g,b,a
            if self.red:
                ra=1
            else:
                ra=0
            if self.green:
                ga=1
            else:
                ga=0
            if self.blue:
                ba=1
            else:
                ba=0
            image.putpixel((x,y),(r*ra,g*ga,b*ba,a))
            #image.putpixel((x,y),(r,g,b,a))
        image=image.tostring("raw",image.mode, 0, -1)
        self.texture_index = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_index)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT,1)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        for o in self.orbits:
            self.init_texture(image)
    def display(self):
        self.rotation_angle += self.rotation_angle_speed
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        #gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        for (i,o) in enumerate(self.orbits):
            self.display_textures(i)

    def display_textures(self,i):
        #print i, len(self.orbits), len(self.orbits_index)
        x,y,z=self.orbits[i][self.orbits_index[i]]
        if self.orbits_index[i] < len(self.orbits[i])-1:
            self.orbits_index[i]+=1
        else:
            self.orbits_index[i]=0
        gl.glPushMatrix()
        gl.glTranslatef(x,y,z)               
        gl.glRotatef(self.rotation_angle,0,0,1)
        #gl.glColor4f(1,0,0,0.5)
        gl.glCallList(self.lists[i])
        gl.glPopMatrix()
        #gl.glTranslatef(100,0.,0.)               
        gl.glPushMatrix()
        gl.glTranslatef(x,y,z)               
        #gl.glColor4f(1,1,0,0.4)
        gl.glRotatef(2*self.rotation_angle,0,0,1)
        gl.glCallList(self.lists[i])
        gl.glPopMatrix()
        

        




        
        
