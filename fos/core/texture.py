import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import Image

#==============================
def display_just_one_track(track,color4=np.array([1,1,0,1],dtype=np.float32),linewidth=np.float32(1.)):

    gl.glPushMatrix()

    gl.glDisable(gl.GL_LIGHTING)

    gl.glEnable(gl.GL_LINE_SMOOTH)

    gl.glDisable(gl.GL_DEPTH_TEST)

    #gl.glDepthFunc(gl.GL_NEVER)

    gl.glEnable(gl.GL_BLEND)

    gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

    gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

    gl.glLineWidth(linewidth)

    gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

    gl.glColor4fv(color4)

    d=track.astype(np.float32)

    gl.glVertexPointerf(d)

    gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))        

    gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

    gl.glEnable(gl.GL_LIGHTING)

    gl.glEnable(gl.GL_DEPTH_TEST)

    gl.glPopMatrix()

#=============================


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

        self.init_texture()

   


    def display(self):

        self.rotation_angle += self.rotation_angle_speed

        gl.glEnable(gl.GL_DEPTH_TEST)

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

        self.reveal_count = None

        self.reveal = False

        self.track_colors = None

        
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

        from dipy.viz.colormaps import boys2rgb

        from dipy.core.track_metrics import mean_orientation, length, downsample

        self.reveal = True
        
        image = Image.open(self.fname,'r')

        print self.fname

        image = image.convert('RGB')

        image = image.convert('RGBA')

        #image.putalpha(50)

        self.light_up = 0

        self.size = image.size

        col = [self.red, self.green, self.blue]

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

            #image.putpixel((x,y),(0,0,255,255))

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


        self.count = np.zeros(len(self.orbits),dtype=np.int)

        self.reveal_count = 10

        self.track_colors = []

        for (i,d) in enumerate(self.orbits):
        
            ds=downsample(d,6)

            mo=ds[3]-ds[2]

            mo=mo/np.sqrt(np.sum(mo**2))

            mo.shape=(1,3)
            
            color=boys2rgb(mo)

            self.track_colors.append(np.array([color[0][0],color[0][1],color[0][2],0.6],np.float32))
                    
        for o in self.orbits:

            self.init_texture(image)

   


        

    def display(self):

        self.rotation_angle += self.rotation_angle_speed

        gl.glEnable(gl.GL_DEPTH_TEST)

        #gl.glDepthFunc(gl.GL_NEVER)

        gl.glEnable(gl.GL_BLEND)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)


        for (i,o) in enumerate(self.orbits):

            '''
            if self.reveal:

                if i < self.light_up:

                    #self.count[i] += 1

                    #print self.count

                    self.display_textures_count(i,False)

                elif i == self.light_up:

                    #self.count[i] += 1

                    self.display_textures_count(i,True)

                    #print self.count

                else:
                
                    self.display_textures(i)

            else:

                self.display_textures(i)
            '''

            self.display_textures_count(i,True)

        #self.light_up = sum(self.count > self.reveal_count)

        #print self.light_up    

        

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
        
        

        
    def display_textures_count(self,i, with_sprite=False):

        #print i, len(self.orbits), len(self.orbits_index)

        x,y,z=self.orbits[i][self.orbits_index[i]]

        if with_sprite:


        #if self.count[i] > self.reveal_count:

            #print i,self.count[i]

            display_just_one_track(self.orbits[i],color4=self.track_colors[i],linewidth=4.)
            #pass

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

            gl.glColor4f(1,1,0,0.4)

            gl.glRotatef(2*self.rotation_angle,0,0,1)


            gl.glCallList(self.lists[i])

            gl.glPopMatrix()
        

        self.count[i] += 1

        
        




        
        
