""" Create an empty Fos world and attach a window to it """

from fos import World, FosWindow, DefaultCamera

# create the world
w = World("myworld")

# create the first window
wi = FosWindow(caption = "My Window 1", bgcolor = (1,1,1,1) )
wi.attach(w)

# add a new camera to the world
cam2 = DefaultCamera()
w.add(cam2)

# create the second window
wi2 = FosWindow(caption = "My Window 2", bgcolor = (0,0,0,1) )
wi2.attach(w)

# set the camera for the second window to the second camera
wi2.set_current_camera(cam2)
