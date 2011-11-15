#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------


        

'''
# glumpy in pyglet?
import pyglet
import numpy, glumpy

Z = numpy.random.random((32,32)).astype(numpy.float32)
I = glumpy.Image(Z)
#ball = pyglet.sprite.Sprite(I, x=50, y=50)

class GlumpyImageWrapper(glumpy.Image):
    
    def __init__(self):
        self.textcoords
    
    def get_texture(self):
        return self._texture
    
    
Ii = GlumpyImageWrapper(Z)
ball = pyglet.sprite.Sprite(Ii, x=50, y=50)

# glumpy
#####



import numpy, glumpy

window = glumpy.Window(512,512)
Z = numpy.random.random((32,32)).astype(numpy.float32)
I = glumpy.Image(Z)

@window.event
def on_draw():
    I.blit(0,0,window.width,window.height)
window.mainloop()


# pyglet
#######
import pyglet
ball_image = pyglet.image.load('/home/stephan/Dev/PyWorkspace/pyglet/examples/pyglet.png')
ball = pyglet.sprite.Sprite(ball_image, x=50, y=50)

window = pyglet.window.Window()

@window.event
def on_draw():
    ball.draw()

pyglet.app.run()
'''


# custom
#####
from  arrayimage import ArrayInterfaceImage
import pyglet
from pyglet.gl import *
import numpy as np

window = pyglet.window.Window(400,400)

arr2 = np.random.random((32,32)).astype(np.float32)
arr2 = np.interp( arr2, [arr2.min(), arr2.max()], [0, 255] )
arr2 = arr2.astype(np.uint8)

aii = ArrayInterfaceImage(arr2)
img = aii.texture
        
# Enable alpha blending, required for image.blit.
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

#aii.view_new_array(arr2)
#window.dispatch_events()
#glPushMatrix()
#glScalef(10, 10., 0)  # assuming a 2d projection
#img.blit(0, 0, 0)
#glPopMatrix()
#window.flip()

@window.event
def on_draw():

    
    window.clear()
    #'''
    glPushMatrix()
    glScalef(3, 1., 0)
    ball.draw()
    glPopMatrix()
    #'''
    glPushMatrix()
    glScalef(1, 1., 0)
    glTranslatef(150,0,2)    
    ball.draw()
    glPopMatrix()
    
ball = pyglet.sprite.Sprite(img, x=10, y=100)


pyglet.app.run()

