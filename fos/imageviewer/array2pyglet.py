from pyglet.gl import *
from pyglet import window
from pyglet import image
from arrayimage import ArrayInterfaceImage
import pyglet
from pyglet.gl import *

#window = pyglet.window.Window(visible=False, resizable=True)


#@window.event
#def on_draw():
#    background.blit_tiled(0, 0, 0, window.width, window.height)
#    img.blit(window.width // 2, window.height // 2, 0)


import numpy
import numpy as np
import nibabel as ni
from pylab import imshow

if __name__ == '__main__':
    
    w = window.Window(visible=False, resizable=True)
    
    # test constructor from numpy array
    #width, height= 640,480
    depth=1 # 1, 3, or 4
    #arr = numpy.arange( width*height*depth, dtype=numpy.uint8)
    #arr2 = numpy.random.random( ( width, height, depth) )
    #arr2 = numpy.random.randn( width, height, depth )
    
#    fname='/home/eg309/Data/PROC_MR10032/subj_02/MPRAGE/1312211075232351192010091419535287463311204CBUMPRAGEs002a1001.nii.gz'
    
    # get the brain
    #arr2img = ni.load(fname).get_data()
    arr2img = np.random.random( ( 200,200,200))
    arr2img[:50,:,:] = 10
    arr2img = numpy.ascontiguousarray(arr2img)
    last_slice = arr2img.shape[0]
    
    arr2 = arr2img[100,:,:]
    arr2 = np.interp( arr2, [arr2.min(), arr2.max()], [0, 255] )
    arr2 = arr2.astype(np.uint8)
    
    aii = ArrayInterfaceImage(arr2)
    img = aii.texture

#    img.anchor_x = img.width // 2
#    img.anchor_y = img.height // 2

    # background
    checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
    #background = pyglet.image.TileableTexture.create_for_image(checks)
        
    # Enable alpha blending, required for image.blit.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    w.width = 800#img.width
    w.height = 800#img.height
    w.set_visible()
    
    #pyglet.app.run()
    
    i=100
    while not w.has_exit:
        w.dispatch_events()
        
        #background.blit_tiled(0, 0, 0, w.width, w.height)
        glPushMatrix()
        glScalef(1, 1., 0)  # assuming a 2d projection
        img.blit(0, 0, 0)
        glPopMatrix()
        w.flip()

        # arr.fill(i)
        arr2 = arr2img[i,:,:]
        arr2 = np.interp( arr2, [arr2.min(), arr2.max()], [0, 255] )
        arr2 = arr2.astype(np.uint8)

        #aii.arr = arr2
        #aii.dirty()
        aii.view_new_array(arr2)
        #aii.dirty() # dirty the ArrayInterfaceImage because the data changed
        #
        i=(i+1)%last_slice

#        if i == 1 and 0:
#            arr = numpy.ones_like( arr ) # create a new array
#            aii.view_new_array(arr) # switch ArrayInterfaceImage to view the new array

    
