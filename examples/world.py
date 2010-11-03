""" Create an empty Fos world and attach a window to it """

from fos import FosWindow, DefaultCamera

# create the first window
wi = FosWindow(caption = "My Window 1", bgcolor = (1,1,1,1) )

# return the default empty world of this window
w = wi.get_world()

# add a new camera to this world
cam2 = DefaultCamera()
w.add(cam2)

# create the second window
wi2 = FosWindow(caption = "My Window 2", bgcolor = (0,0,0,1) )

# we want to look at the same world as window 1, thus drop
# the default world and attach the window to our world with the second camera
wi2.attach(w)

# set the camera for the second window to the second camera
wi2.set_current_camera(cam2)
