#!/usr/bin/env python

from math import pi, sin, cos, sqrt
from euclid import *

import pyglet
from pyglet.gl import *
from pyglet.window import key

from fos.actor.tree import Tree

import numpy as np

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config, vsync=False, width=1000, height=800) # "vsync=False" to check the framerate
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)


fps_display = pyglet.clock.ClockDisplay() # see programming guide pg 48

@window.event
def on_resize(width, height):
    if height==0: height=1
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50., width / float(height), .1, 8000)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update(dt):
    global autorotate
    global rot

    if autorotate:
        rot += Vector3(0.1, 12, 5) * dt
        rot.x %= 360
        rot.y %= 360
        rot.z %= 360
pyglet.clock.schedule(update)


# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glLoadIdentity()

    glTranslatef(0.0, 0.0, zoom)
    glRotatef(rot.x, 0, 0, 1)
    glRotatef(rot.y, 0, 1, 0)
    glRotatef(rot.z, 1, 0, 0)

#    cam.draw()

    act.draw()

    glLoadIdentity()
    glTranslatef(200, 280, -800)
    fps_display.draw()


@window.event
def on_key_press(symbol, modifiers):
    global autorotate
    global rot
    global zoom
    
    if symbol == key.R:
        print 'Reset'
        rot = Vector3(0, 90, 0)
        
    elif symbol == key.ESCAPE or symbol == key.Q:
        print 'Good Bye !'   # ESC would do it anyway, but not "Q"
        pyglet.app.exit()
        return pyglet.event.EVENT_HANDLED

    elif symbol == key.SPACE:
        print 'Toggle autorotate'
        autorotate = not autorotate

    elif symbol == key.A:
        print 'Stop left'
        if autorotate:
            autorotate = False
        else:
            rot.y += -rotstep
            rot.y %= 360


    elif symbol == key.Z:
        print 'Zoom out'
        zoom += 1

    elif symbol == key.U:
        print 'Zoom in'
        zoom -= 1

    elif symbol == key.S:
        print 'Stop down'
        if autorotate:
            autorotate = False
        else:
            rot.z += rotstep
            rot.z %= 360

    elif symbol == key.W:
        print 'Stop up'
        if autorotate:
            autorotate = False
        else:
            rot.z += -rotstep
            rot.z %= 360

    elif symbol == key.D:
        print 'Stop right'
        if autorotate:
            autorotate = False
        else:
            rot.y += rotstep
            rot.y %= 360
            
    else:
        print 'OTHER KEY'

def setup():

    glClearColor(0,0,0,1)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

rot          = Vector3(0, 0, 90)
autorotate   = True
rotstep      = 1
zoom = -0.4

setup()

# sample data
vert = np.array( [ [0,0,0],
                   [5,5,0],
                   [5,10,0],
                   [10,5,0]], dtype = np.float32 )

conn = np.array( [ 0, 1, 1, 2, 1, 3 ], dtype = np.uint32 )

cols = np.array( [ [0, 0, 1, 1],
                   [1, 0, 1, 1],
                   [0, 0, 1, 0.5] ] , dtype = np.float32 )

from fos.core.camera2 import DefaultCamera
cam = DefaultCamera()

act = Tree(vertices = vert, connectivity = conn, colors = cols)

pyglet.app.run()
