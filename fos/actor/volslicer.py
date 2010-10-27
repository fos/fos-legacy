
from fos.lib import pyglet
from fos.lib.pyglet.gl import *

#sprite = pyglet.sprite.Sprite(img, x=0, y=0)
#sprite.position = (-sprite.width/2, - sprite.height/2)
#actors.append(sprite)

class ConnectedSlices():

    def __init__(self,affine,data):

        self.shape=data.shape
        self.data=data
        self.affine=affine
        #volume center coordinates
        self.vxi,self.vxj,self.vxk=self.shape[0]/2,self.shape[1]/2,self.shape[2]/2
        self.update_vox_coords(self.vxi,self.vxj,self.vxk)

    def update_vox_coords(self,vxi,vxj,vxk):

        self.vxi,self.vxj,self.vxk=vxi,vxj,vxk
        #current slices for the 3 axes
        self.sli=self.data[self.vxi,:,:]
        self.slj=self.data[:,self.vxj,:]
        self.slk=self.data[:,:,self.vxk]

        #interpolate for textures
        sli=np.interp(self.sli,[self.sli.min(),self.sli.max()],[0,255]).astype(np.uint8)        
        slj=np.interp(self.slj,[self.slj.min(),self.slj.max()],[0,255]).astype(np.uint8)        
        slk=np.interp(self.slk,[self.slk.min(),self.slk.max()],[0,255]).astype(np.uint8)        
        
        texi = ArrayInterfaceImage(sli).texture
        texj = ArrayInterfaceImage(slj).texture
        texk = ArrayInterfaceImage(slk).texture

        #how far in Z axis is texture projection plane in gl space
        self.z=-1
        #three points are needed to define the projection plane
        self.p0=(0,0,self.z)
        self.p1=(1,0,self.z)
        self.p2=(0,1,self.z)
                       
        spri=pyglet.sprite.Sprite(texi, x=0, y=0)                       
        spri.position=(-spri.width/2, - spri.height/2)
        
        sprj=pyglet.sprite.Sprite(texj, x=0, y=0)                       
        sprj.position=(-sprj.width/2, - sprj.height/2)

        sprk=pyglet.sprite.Sprite(texk, x=0, y=0)                       
        sprk.position=(-sprk.width/2, - sprk.height/2)    

        self.spri=spri
        self.sprj=sprj
        self.sprk=sprk

    def draw(self):
        #print('draw')

  
        glPushMatrix()
        glTranslatef(-self.spri.width/2-self.sprj.width/2,0,self.z)
        glScalef(1, 1., 0)
        self.spri.draw()
        glPopMatrix()         
 
        glPushMatrix()
        glTranslatef(0,0,self.z)
        glScalef(1, 1., 0)
        self.sprj.draw()
        glPopMatrix() 
    
        glPushMatrix()
        glTranslatef(self.sprj.width/2+self.sprk.width/2,0,self.z)
        #glTranslatef(0,0,self.z)
        glScalef(1, 1., 0)
        self.sprk.draw()
        glPopMatrix()        

    def process_pickray(self,near,far):
        #collision with plane
 
        success,t,p= cll.intersect_segment_plane(near,far,self.p0,self.p1,self.p2)

        print success
        print p

        o0_low_left=(-self.spri.width-self.sprj.width/2.,-self.spri.height/2)
        o0_up_right= (-self.sprj.width/2.,self.spri.height/2)       
        if tell_me_if(p,o0_low_left,o0_up_right):
            print 'Object 0'
            pix0=np.round(p[0]-o0_low_left[0]).astype(int)
            pix1=np.round(p[1]-o0_low_left[1]).astype(int)            
            self.update_vox_coords(self.vxi,pix1,pix0)            
            print 'Changed', self.vxi,pix0,pix1            
 
        o1_low_left=(-self.sprj.width/2.,-self.sprj.height/2)
        o1_up_right= (self.sprj.width/2.,self.sprj.height/2)               
        if tell_me_if(p,o1_low_left,o1_up_right):
            print 'Object 1'
            pix0=np.round(p[0]-o1_low_left[0]).astype(int)
            pix1=np.round(p[1]-o1_low_left[1]).astype(int)
            self.update_vox_coords(pix1,self.vxj,pix0)            
            

        o2_low_left=(self.sprj.width/2.,-self.sprk.height/2)
        o2_up_right= (self.sprj.width/2+self.sprk.width,self.spri.height/2)       
        if tell_me_if(p,o2_low_left,o2_up_right):
            print 'Object 2'
            pix0=np.round(p[0]-o2_low_left[0]).astype(int)
            pix1=np.round(p[1]-o2_low_left[1]).astype(int)
            self.update_vox_coords(pix1,pix0,self.vxk)
         
        print np.round(p)

        #self.update_vox_coords()

    def update(self):
        pass
    
def tell_me_if(p,low_left,up_right):
            if low_left[0]  <= p[0] and p[0]<=up_right[0]:
                if low_left[1]  <= p[1] and p[1]<=up_right[1]:
                    return True
            return False

'''
import scipy.ndimage as nd

f1='/home/eg309/Data/regtest/fiac0/meanafunctional_01.nii'
img=ni.load(f1)

data =img.get_data()
affine=img.get_affine()

cds =ConnectedSlices(affine,data)
actors.append(cds)
'''
