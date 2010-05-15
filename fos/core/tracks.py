import os
import time
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import Image
import PIL.ImageOps as iops
from fos.core.utils import list_indices as lind
from os.path import join as pjoin
import fos.core.pyramid as pyramid

from dipy.core import track_metrics as tm

import fos.core.collision as cll

#import fos.core.plots as plots

global angle_table

global anglex

global angley

global anglez

global angle_table_index


MS=1000

def make_angle_table(lists):

    #angle_table = make_angle_table([[[0,0,0],[90,0,0],30],[[90,0,0],[90,90,0],30]])

    table = []
    for list in lists:
        start,finish,n = list
        sx,sy,sz = start
        fx,fy,fz = finish
        cx = np.linspace(sx,fx,n)
        cy = np.linspace(sy,fy,n)
        cz = np.linspace(sz,fz,n)
        if table == []:
            table = np.column_stack((cx,cy,cz))
        else:
            table = np.vstack((table,np.column_stack((cx,cy,cz))))
    print 'angle table has length %d' % table.shape[0]
    return table

'''
angle_table = make_angle_table([
                [[0,0,90],[90,0,90],200],
                [[90,0,90],[90,90,90],200],
                [[90,90,90],[90,90,360],200]
                ])
'''

angle_table = make_angle_table([

        #[[0,0,0],[0,0,0],50],
        

        [[0,0,0],[-90,0,1800],900],

        [[-90,0,1800],[-90,0,36000],17100]

        ])

                
'''
angle_table = make_angle_table([[[0,0,0],[-90,0,0],200],
                                        [[-90,0,0],[-90,-90,0],200],
                                        [[-90,-90,0],[-90,-90,90],200],
                                        [[-90,-90,90],[0,-90,-90],400]])
'''

angle_table_index = 0

anglex = 0.

angley = 0.

anglez = 0.








data_path = pjoin(os.path.dirname(__file__), 'data')

class Ghost(object):

    def __init__(self):

        pass

    def init(self):

        pass

    def display(self):

        global angle_table_index

        global angle_table

        angle_table_index += 1

        if angle_table_index >= angle_table.shape[0]:
                
            angle_table_index = angle_table.shape[0] - 1



class Empty(object):

    def __init__(self):

        self.slots = None

        self.time = 0

        self.near_pick = None

        self.far_pick = None
        

    def init(self):

        pass

    def display(self):

        pass
    
        '''
        now = self.time

        for s in self.slots:

            if now >= self.slots[s]['slot'][0] and now <=self.slots[s]['slot'][1]:

                self.slots[s]['actor'].near_pick = self.near_pick

                self.slots[s]['actor'].far_pick = self.far_pick               
                
                self.slots[s]['actor'].display()

        '''
        
#=======================================================

class Tracks(object):

    def __init__(self,fname,ang_table=None,colormap=None, line_width=3., shrink=None,subset=None,data_ext=None):

        self.position = (0,0,0)

        self.fname = fname
        
        self.manycolors = True
        
        self.bbox = None

        self.list_index = None

        self.affine = None

        self.data = None

        self.list_index = None

        self.rot_angle = 0

        self.colormap = None
                
        self.min = None
         
        self.max = None

        self.mean = None

        self.material_color = False

        self.fadeout = False

        self.fadein = False

        self.fadeout_speed = 0.

        self.fadein_speed = 0.

        self.min_length = 20.

        self.data_ext = data_ext

        self.angle = 0.

        self.angular_speed = .5

        self.line_width = line_width

        self.opacity = 1.

        self.near_pick = None

        self.far_pick = None

        self.near_pick_prev = None

        self.far_pick_prev = None

        self.picked_track = None

        self.pick_color = [1,1,0]

        self.brain_color = [1,1,1]

        self.yellow_indices = None

        self.dummy_data = False

        if subset != None:

            self.data_subset = subset #[0,20000]#None

        else:

            self.data_subset = None

        self.orbit_demo = False          

        self.orbit_anglez = 0.

        self.orbit_anglez_rate = 0.
        

        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 0.


        self.orbit_angley = 0.

        self.orbit_angley_rate = 0.


        self.angle_table = ang_table

        
        self.angle_table_index = 0



        

        self.shrink = shrink

        self.picking_example = False

        if self.data_ext!=None:

            self.data=self.data_ext

        else:

            import dipy.io.trackvis as tv

            lines,hdr = tv.read(self.fname)

            ras = tv.aff_from_hdr(hdr)

            self.affine=ras

            tracks = [l[0] for l in lines]

            if self.yellow_indices != None :

                tracks = [t for t in tracks if tm.length(t) > 20]

            print 'tracks loaded'

            #self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]#tracks[:20000]

            if self.dummy_data:

                self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]

            if self.data_subset!=None:

                self.data = tracks[self.data_subset[0]:self.data_subset[1]]

            else:

                self.data = tracks



            data_stats = np.concatenate(tracks)

            self.min=np.min(data_stats,axis=0)

            self.max=np.max(data_stats,axis=0)

            self.mean=np.mean(data_stats,axis=0)

            if self.shrink != None:

                self.data = [ self.shrink*t  for t in self.data]

            del data_stats

            del lines
        
        

    def init(self):

        if self.material_color:

            self.material_colors()

        else:

            self.multiple_colors()



               
 

    def display(self):


        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)                
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
      

                
        
    
        x,y,z=self.position

        if self.orbit_demo and self.angle_table == None:

            #print('Yo%f',self.position[0])

            gl.glPushMatrix()

            gl.glTranslatef(x,y,z)

            gl.glPushMatrix()

            #gl.glTranslatef(x,y,z)

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)
            
            #'''
            gl.glPushMatrix()

            self.orbit_angley+=self.orbit_angley_rate
            
            gl.glRotatef(self.orbit_angley,0,1,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            #x,y,z=self.position
            

            gl.glRotatef(self.orbit_anglez,0,0,1)

            #gl.glTranslatef(x,y,z)

            #'''


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            


        elif self.orbit_demo == True and self.angle_table != None:

            
            
            gl.glPushMatrix()

            #print angle_table

            #print table_ind

            global angle_table_index

            global angle_table

            table_ind=angle_table_index

            #print 'ti',table_ind

            anglex=angle_table[table_ind,0]

            #print anglex

            gl.glRotatef(anglex,1,0,0)
            
            
            gl.glPushMatrix()

            angley=angle_table[table_ind,1]

            gl.glRotatef(angley,0,1,0)
            

            gl.glPushMatrix()

            anglez=angle_table[table_ind,2]

            gl.glRotatef(anglez,0,0,1)


            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            '''

            angle_table_index += 1

            if angle_table_index >= angle_table.shape[0]:
                
                angle_table_index = angle_table.shape[0] - 1

            '''
            

            '''

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,0],1,0,0)

            #x,y,z = self.position
            
            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,1],0,1,0)

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,2],0,0,1)

            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            self.angle_table_index += 1

            if self.angle_table_index >= self.angle_table.shape[0]:
                
                self.angle_table_index = self.angle_table.shape[0] - 1

            '''
            
        else:

            gl.glCallList(self.list_index)




            if self.picked_track != None:

                self.display_one_track(self.picked_track)



            if self.yellow_indices != None:

                for i in self.yellow_indices:


                    self.display_one_track(i)


        

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print 'min index',self.picked_track

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        A = np.array(min_dist_info)

        dist=10**(-3)

        iA=np.where(A[:,0]<dist)

        minA=A[iA]

        print 'minA ', minA

        miniA=minA[:,1].argmin()

        print 'final min index ',iA[0][miniA]

        self.picked_track=iA[0][miniA]

   
        

        
        


    def display_one_track(self,track_index,color4=np.array([1,1,0,1],dtype=np.float32)):

        x,y,z = self.position

        if self.orbit_demo and self.angle_table == None:

            #print('Yo%f',self.position[0])

            gl.glPushMatrix()

            gl.glTranslatef(x,y,z)

            gl.glPushMatrix()

            #gl.glTranslatef(x,y,z)

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)
            
            #'''
            gl.glPushMatrix()

            self.orbit_angley+=self.orbit_angley_rate
            
            gl.glRotatef(self.orbit_angley,0,1,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            #x,y,z=self.position
            

            gl.glRotatef(self.orbit_anglez,0,0,1)

            #gl.glTranslatef(x,y,z)

            #'''


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)


            #gl.glPushMatrix()

            gl.glDisable(gl.GL_LIGHTING)

            gl.glEnable(gl.GL_LINE_SMOOTH)

            gl.glDisable(gl.GL_DEPTH_TEST)

            #gl.glDepthFunc(gl.GL_NEVER)


            gl.glEnable(gl.GL_BLEND)

            gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

            gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

            gl.glLineWidth(3.)

            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

            gl.glColor4fv(color4)


            d=self.data[track_index].astype(np.float32)

            gl.glVertexPointerf(d)

            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))        

            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

            gl.glEnable(gl.GL_LIGHTING)

            gl.glEnable(gl.GL_DEPTH_TEST)

            #gl.glPopMatrix()

            

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()




    def multiple_colors(self):

        from dipy.viz.colormaps import boys2rgb

        from dipy.core.track_metrics import mean_orientation, length, downsample

        colors=np.random.rand(1,3).astype(np.float32)

        print colors

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        #gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)
        
        #!!!gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glDisable(gl.GL_DEPTH_TEST)

        #gl.glDepthFunc(gl.GL_NEVER)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE,gl.GL_ONE_MINUS_SRC_ALPHA)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        #!!!gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        #gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_NICEST)

        gl.glLineWidth(self.line_width)

        #gl.glDepthMask(gl.GL_FALSE)


        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        for d in self.data:

            if length(d)> self.min_length:
            
                #mo=mean_orientation(d)

                if self.manycolors:
                
                    ds=downsample(d,6)

                    mo=ds[3]-ds[2]

                    mo=mo/np.sqrt(np.sum(mo**2))

                    mo.shape=(1,3)
            
                    color=boys2rgb(mo)

                    color4=np.array([color[0][0],color[0][1],color[0][2],self.opacity],np.float32)
                    

                else:

                    color4=np.array([self.brain_color[0],self.brain_color[1],\
                                         self.brain_color[2],self.opacity],np.float32)


                if self.fadein == True:

                    color4[3] += self.fadein_speed

                if self.fadeout == True:

                    color4[3] -= self.fadeout_speed

                gl.glColor4fv(color4)                

                gl.glVertexPointerf(d)
                               
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        #gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_DEPTH_TEST)
        
        #gl.glPopMatrix()

        gl.glEndList()
 
    

   


    def material_colors(self):
        

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [1,1,1,.1] )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, [1,1,1,.1] )
        
        
        #gl.glMaterialf( gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 50. )

        #gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_EMISSION, [1,1,1,1.])


        gl.glEnable(gl.GL_LINE_SMOOTH)
               
        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)


        #gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        #gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        #gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()


class TracksModified(object):

    def __init__(self,fname,ang_table=None,colormap=None, line_width=3., shrink=None,subset=None,tracks=None,text=None,text_color=np.array([1,0,0])):

        self.position = (0,0,0)

        self.fname = fname
        
        self.manycolors = True
        
        self.bbox = None

        self.list_index = None

        self.affine = None

        self.data = None

        self.list_index = None

        self.rot_angle = 0

        self.colormap = None

        self.text = text
        
        self.min = None
         
        self.max = None

        self.mean = None

        self.material_color = False

        self.fadeout = False

        self.fadein = False

        self.fadeout_speed = 0.

        self.fadein_speed = 0.

        self.min_length = 20.

        self.angle = 0.

        self.angular_speed = .5

        self.line_width = line_width

        self.opacity = 1.

        self.near_pick = None

        self.far_pick = None

        self.near_pick_prev = None

        self.far_pick_prev = None

        self.picked_track = None

        self.pick_color = [1,1,0]

        self.brain_color = [1,1,1]

        self.yellow_indices = None

        self.dummy_data = False

        self.tracks = tracks

        if subset != None:

            self.data_subset = subset #[0,20000]#None

        else:

            self.data_subset = None

        self.orbit_demo = False          

        self.orbit_anglez = 0.

        self.orbit_anglez_rate = 10.
        

        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 2.


        self.angle_table = ang_table

        
        self.angle_table_index = 0



        

        self.shrink = shrink

        self.picking_example = False


        self.partial_colors = False
        

        import dipy.io.trackvis as tv


        if self.tracks == None:

            lines,hdr = tv.read(self.fname)

            ras = tv.aff_from_hdr(hdr)

            self.affine=ras

            tracks = [l[0] for l in lines]

            del lines
        


        else:

            tracks = self.tracks


        if self.yellow_indices != None :

            tracks = [t for t in tracks if tm.length(t) > 20]

        print '%d tracks loaded' % len(tracks)

        #self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]#tracks[:20000]

        if self.dummy_data:

            self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]

        if self.data_subset!=None:

            self.data = tracks[self.data_subset[0]:self.data_subset[1]]

        else:

            self.data = tracks


        

        if self.shrink != None:

            self.data = [ self.shrink*t  for t in self.data]
            

            
        data_stats = np.concatenate(tracks)

        self.min=np.min(data_stats,axis=0)
         
        self.max=np.max(data_stats,axis=0)

        self.mean=np.mean(data_stats,axis=0)

        del data_stats
        
        

    def init(self):

        if self.material_color:

            self.material_colors()

        else:

            self.multiple_colors()



               
 

    def display(self):


        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)             
              
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
      

                
        
    
        x,y,z=self.position

        if self.orbit_demo and self.angle_table == None:

            gl.glPushMatrix()

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            x,y,z=self.position

           

            gl.glRotatef(self.orbit_anglez,0,0,1)

            gl.glTranslatef(x,y,z) 


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()


        elif self.orbit_demo == True and self.angle_table != None:

            
            
            gl.glPushMatrix()

            #print angle_table

            #print table_ind

            global angle_table_index

            table_ind=angle_table_index

            anglex=angle_table[table_ind,0]

            #print anglex

            gl.glRotatef(anglex,1,0,0)
            
            
            gl.glPushMatrix()

            angley=angle_table[table_ind,1]

            gl.glRotatef(angley,0,1,0)
            

            gl.glPushMatrix()

            anglez=angle_table[table_ind,2]

            gl.glRotatef(anglez,0,0,1)


            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            angle_table_index += 1

            if angle_table_index >= angle_table.shape[0]:
                
                angle_table_index = angle_table.shape[0] - 1

            

            '''

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,0],1,0,0)

            #x,y,z = self.position
            
            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,1],0,1,0)

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,2],0,0,1)

            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            self.angle_table_index += 1

            if self.angle_table_index >= self.angle_table.shape[0]:
                
                self.angle_table_index = self.angle_table.shape[0] - 1

            '''
            
        else:

            gl.glCallList(self.list_index)




            if self.picked_track != None:

                self.display_one_track(self.picked_track)



            if self.yellow_indices != None:

                for i in self.yellow_indices:


                    self.display_one_track(i)


        if self.text != None:

            gl.glDisable(gl.GL_LIGHTING)
            
            gl.glColor3f(1.,0.,0.)

            for (i,t) in enumerate(self.data):

                #gl.glRasterPos3f(t[0][0],t[0][1],t[0][2])
            
                label = str(i)

                if i == 22: #cortico spinal track

                    gl.glRasterPos3f(t[0][0],t[0][1],t[0][2])


                    label='spine'

                    for c in label:

                        glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

                    gl.glRasterPos3f(t[-1][0],t[-1][1],t[-1][2])


                    label='motor'

                    for c in label:

                        glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

                    

                    label='corticospinal highway'

                    t2=tm.downsample(t,len(label)+3)

                    for (ci,c) in enumerate(label[::-1]):
                        
                        gl.glRasterPos3f(t2[ci+2][0],t2[ci+2][1],t2[ci+2][2])

                        glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

                else:

                    pass


                '''

                    gl.glRasterPos3f(t[0][0],t[0][1],t[0][2])

                    for c in label:

                        glut.glutBitmapCharacter(glut.GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

                '''
                
            gl.glEnable(gl.GL_LIGHTING)

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print 'min index',self.picked_track

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        A = np.array(min_dist_info)

        dist=10**(-3)

        iA=np.where(A[:,0]<dist)

        minA=A[iA]

        print 'minA ', minA

        miniA=minA[:,1].argmin()

        print 'final min index ',iA[0][miniA]

        self.picked_track=iA[0][miniA]

   
        

        
        


    def display_one_track(self,track_index,color4=np.array([1,1,0,1],dtype=np.float32)):
        

        gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glDisable(gl.GL_DEPTH_TEST)

        #gl.glDepthFunc(gl.GL_NEVER)


        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        gl.glLineWidth(7.)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        gl.glColor4fv(color4)


        d=self.data[track_index].astype(np.float32)

        gl.glVertexPointerf(d)
                               
        gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_DEPTH_TEST)
        
        gl.glPopMatrix()



    def multiple_colors(self):

        from dipy.viz.colormaps import boys2rgb

        from dipy.core.track_metrics import mean_orientation, length, downsample

        colors=np.random.rand(1,3).astype(np.float32)

        print colors

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        #gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)
        
        #!!!gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glDisable(gl.GL_DEPTH_TEST)

        #gl.glDepthFunc(gl.GL_NEVER)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE,gl.GL_ONE_MINUS_SRC_ALPHA)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        #!!!gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        #gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_NICEST)

        gl.glLineWidth(self.line_width)

        #gl.glDepthMask(gl.GL_FALSE)


        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        for d in self.data:

            if length(d)> self.min_length:
            
                #mo=mean_orientation(d)

                if self.manycolors:
                
                    ds=downsample(d,6)

                    mo=ds[3]-ds[2]

                    mo=mo/np.sqrt(np.sum(mo**2))

                    mo.shape=(1,3)
            
                    color=boys2rgb(mo)

                    color4=np.array([color[0][0],color[0][1],color[0][2],self.opacity],np.float32)
                    

                else:

                    color4=np.array([self.brain_color[0],self.brain_color[1],\
                                         self.brain_color[2],self.opacity],np.float32)


                if self.fadein == True:

                    color4[3] += self.fadein_speed

                if self.fadeout == True:

                    color4[3] -= self.fadeout_speed

                gl.glColor4fv(color4)                

                gl.glVertexPointerf(d)
                               
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        #gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_DEPTH_TEST)
        
        #gl.glPopMatrix()

        gl.glEndList()
 
    

   


    def material_colors(self):
        

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [1,1,1,.1] )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, [1,1,1,.1] )
        
        
        #gl.glMaterialf( gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 50. )

        #gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_EMISSION, [1,1,1,1.])


        gl.glEnable(gl.GL_LINE_SMOOTH)
               
        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)


        #gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        #gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        #gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()



class ChromoTracks(object):

    def __init__(self,fname,colormap=None, line_width=1., shrink=None, thinning = 0,
                 angle_table = None, manycolors = False, brain_color=[1,1,1]):

        self.position = (0,0,0)

        self.fname = fname
        
        self.manycolors = manycolors

        #self.color = monocolor
        
        self.bbox = None

        self.list_index = None

        self.affine = None

        self.data = None

        self.list_index = None

        self.rot_angle = 0

        self.colormap = None
                
        self.min = None
         
        self.max = None

        self.mean = None

        self.material_color = False

        self.fadeout = False

        self.fadein = False

        self.fadeout_speed = 0.

        self.fadein_speed = 0.

        self.min_length = 20.

        self.angle = 0.

        self.angular_speed = .5

        self.line_width = line_width

        self.opacity = 1.

        self.opacity_rate = 0.

        self.near_pick = None

        self.far_pick = None

        self.near_pick_prev = None

        self.far_pick_prev = None

        self.picked_track = None

        self.pick_color = [1,1,0]

        #self.brain_color = [1,1,1] # white
        #self.brain_color = [.941,.862,.510] # buff
        self.brain_color = brain_color
        
        self.yellow_indices = None

        self.dummy_data = False

        self.data_subset = [0,20000]#None


        self.orbit_demo = False          

        self.orbit_anglez =0.

        self.orbit_anglez_rate = 10.
        

        self.orbit_anglex = 0.

        self.orbit_anglex_rate = 2.


        self.angle_table = angle_table

        if angle_table != None:
            print 'Tracks angle_table shape %s' % str(self.angle_table.shape)

        self.angle_table_index = 0

        #print 'angle_table_index %d' % self.angle_table_index

        self.shrink = shrink

        self.picking_example = False

        import dipy.io.trackvis as tv

        lines,hdr = tv.read(self.fname)

        ras = tv.aff_from_hdr(hdr
)
        self.affine=ras

        tracks = [l[0] for l in lines]

        print 'tracks %d loaded' % len(tracks)

        self.thinning = thinning

        if self.yellow_indices != None :

            tracks = [t for t in tracks if tm.length(t) > 20]

        if self.thinning != 0:

            tracks = [tracks[k] for k in range(0,len(tracks),self.thinning)]

        print '%d tracks active' % len(tracks)

        #self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]#tracks[:20000]

        if self.dummy_data:

            self.data = [100*np.array([[0,0,0],[1,0,0],[2,0,0]]).astype(np.float32) ,100*np.array([[0,1,0],[0,2,0],[0,3,0]]).astype(np.float32)]

        if self.data_subset!=None:

            self.data = tracks[self.data_subset[0]:self.data_subset[1]]

        else:

            self.data = tracks

        if self.shrink != None:

            self.data = [ self.shrink*t  for t in self.data]
            

        data_stats = np.concatenate(tracks)

        self.min=np.min(data_stats,axis=0)
         
        self.max=np.max(data_stats,axis=0)

        self.mean=np.mean(data_stats,axis=0)

        del data_stats
        
        del lines
        
        

    def init(self):

        if self.material_color:

            self.material_colors()

        else:

            self.multiple_colors()



               
 

    def display(self):


        if self.near_pick!= None:

            #print self.near_pick

            if np.sum(np.equal(self.near_pick, self.near_pick_prev))< 3:        

                self.process_picking(self.near_pick, self.far_pick)             
              
                self.near_pick_prev = self.near_pick

                self.far_pick_prev = self.far_pick
      

                
        
    
        x,y,z=self.position

        if self.orbit_demo and self.angle_table == None:

            gl.glPushMatrix()

            self.orbit_anglex+=self.orbit_anglex_rate
            
            gl.glRotatef(self.orbit_anglex,1,0,0)

            gl.glPushMatrix()

            self.orbit_anglez+=self.orbit_anglez_rate

            #x,y,z=self.position


            gl.glRotatef(self.orbit_anglez,0,0,1)

            gl.glTranslatef(x,y,z) 


            #gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)

            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

        elif self.orbit_demo == True and self.angle_table != None:

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,0],1,0,0)

            #x,y,z = self.position
            
            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,1],0,1,0)

            gl.glPushMatrix()

            gl.glRotatef(self.angle_table[self.angle_table_index,2],0,0,1)

            gl.glTranslate(x,y,z)
            
            gl.glCallList(self.list_index)

            gl.glFinish()

            gl.glPopMatrix()

            gl.glPopMatrix()

            gl.glPopMatrix()

            self.angle_table_index += 1

            if self.angle_table_index >= self.angle_table.shape[0]:
                self.angle_table_index = self.angle_table.shape[0] - 1

            #print 'self.angle_table_index = %d' % self.angle_table_index

        elif self.fade_demo:

            #gl.glPushMatrix()

            self.opacity += self.opacity_rate

            if self.opacity <= 0.0:
                self.opacity = 0.0
                self.opacity_rate = -self.opacity_rate
            elif self.opacity >= 1.0:
                self.opacity = 1.0
                self.opacity_rate = -self.opacity_rate
            
            #print self.opacity

            gl.glCallList(self.list_index)

            gl.glFinish()

            #gl.glPopMatrix()

            
        else:

            gl.glCallList(self.list_index)




            if self.picked_track != None:

                self.display_one_track(self.picked_track)



            if self.yellow_indices != None:

                for i in self.yellow_indices:


                    self.display_one_track(i)

        gl.glFinish()        


    def process_picking(self,near,far):

        print('process picking')

        min_dist=[cll.mindistance_segment2track(near,far,xyz) for xyz in self.data]

        min_dist=np.array(min_dist)

        #print min_dist

        self.picked_track=min_dist.argmin()

        print 'min index',self.picked_track

        min_dist_info=[cll.mindistance_segment2track_info(near,far,xyz) for xyz in self.data]

        A = np.array(min_dist_info)

        dist=10**(-3)

        iA=np.where(A[:,0]<dist)

        minA=A[iA]

        print 'minA ', minA

        miniA=minA[:,1].argmin()

        print 'final min index ',iA[0][miniA]

        self.picked_track=iA[0][miniA]

   
        

        
        


    def display_one_track(self,track_index,color4=np.array([1,1,0,1],dtype=np.float32)):
        

        gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)

        gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        gl.glLineWidth(7.)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        gl.glColor4fv(color4)


        d=self.data[track_index].astype(np.float32)

        gl.glVertexPointerf(d)
                               
        gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEnable(gl.GL_LIGHTING)
        
        gl.glPopMatrix()



    def multiple_colors(self):

        from dipy.viz.colormaps import boys2rgb

        from dipy.core.track_metrics import mean_orientation, length, downsample

        colors=np.random.rand(1,3).astype(np.float32)

        print colors

        self.list_index = gl.glGenLists(1)

        if self.fade_demo:

            #gl.glPushMatrix()

            self.opacity += self.opacity_rate

            if self.opacity <= 0.0:
                self.opacity = 0.0
                self.opacity_rate = -self.opacity_rate
            elif self.opacity >= 1.0:
                self.opacity = 1.0
                self.opacity_rate = -self.opacity_rate
            
            #print self.opacity

            gl.glCallList(self.list_index)

            gl.glFinish()

            #gl.glPopMatrix()

            
        gl.glNewList( self.list_index,gl.GL_COMPILE_AND_EXECUTE)

        #gl.glPushMatrix()

        gl.glDisable(gl.GL_LIGHTING)
        
        #!!!gl.glEnable(gl.GL_LINE_SMOOTH)

        gl.glDisable(gl.GL_DEPTH_TEST)

        gl.glDepthFunc(gl.GL_NEVER)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA_SATURATE,gl.GL_ONE_MINUS_SRC_ALPHA)
        
        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE)

        #!!!gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_DONT_CARE)

        #gl.glHint(gl.GL_LINE_SMOOTH_HINT,gl.GL_NICEST)

        gl.glLineWidth(self.line_width)

        #gl.glDepthMask(gl.GL_FALSE)


        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)        

        for d in self.data:

            if length(d)> self.min_length:
            
                #mo=mean_orientation(d)

                if self.manycolors:
                
                    ds=downsample(d,6)

                    mo=ds[3]-ds[2]

                    mo=mo/np.sqrt(np.sum(mo**2))

                    mo.shape=(1,3)
            
                    color=boys2rgb(mo)

                    color4=np.array([color[0][0],color[0][1],color[0][2],self.opacity],np.float32)
                    

                else:

                    color4=np.array([self.brain_color[0],self.brain_color[1],\
                                         self.brain_color[2],self.opacity],np.float32)


                if self.fadein == True:

                    color4[3] += self.fadein_speed

                if self.fadeout == True:

                    color4[3] -= self.fadeout_speed

                gl.glColor4fv(color4)                

                gl.glVertexPointerf(d)
                               
                gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        #gl.glDisable(gl.GL_BLEND)
        
        gl.glEnable(gl.GL_LIGHTING)
        
        #gl.glPopMatrix()

        gl.glEndList()
 
    

   


    def material_colors(self):
        

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT, [1,1,1,.1] )

        gl.glMaterialfv( gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, [1,1,1,.1] )
        
        
        #gl.glMaterialf( gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 50. )

        #gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_EMISSION, [1,1,1,1.])


        gl.glEnable(gl.GL_LINE_SMOOTH)
               
        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)


        #gl.glMaterialfv( gl.GL_FRONT, gl.GL_SPECULAR, self.specular )

        #gl.glMaterialf( gl.GL_FRONT, gl.GL_SHININESS, self.shininess )

        #gl.glMaterialfv(gl.GL_FRONT, gl.GL_EMISSION, self.emission)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        for d in self.data:            

            gl.glVertexPointerd(d)
        
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, len(d))

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)

        gl.glEndList()

