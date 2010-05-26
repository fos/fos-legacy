import numpy as np
import OpenGL.GL as gl

from fos.core.scene  import Scene
from fos.core.actors import Actor
from fos.core.plots  import Plot
from fos.core.primitives import Empty
from fos.core.tracks import Tracks


def show_tracks():

    line1=np.array([[0,0,0],[100,0,0],[100,100,0]],np.float32)
    
    line2=np.array([[0,0,0],[100,100,0],[100,100,300]],np.float32)

    data=[line1,line2]

    cols1=np.array([[0,0,0,1],[1,0,0,1],[1,1,0,1]],np.float32)

    cols2=np.array([[0,0,0,1],[1,1,0,1],[1,1,1,1]],np.float32)

    colors = [cols1,cols2]

    e=Empty()
   
    t=Tracks(data,colors)  
        
    slot={0:{'actor':e,'slot':(0, 10)},
          1:{'actor':t,'slot':(10, 800000)}}
            
    Scene(Plot(slot)).run()
   
            

if __name__ == "__main__":

    show_tracks()

