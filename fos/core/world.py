from fos.lib import pyglet
from fos.core.actor_graph import ActorGraph
from fos.core.camera_graph import CameraGraph
from fos.core.camera import Camera
from fos.core.actor import Actor

class World():

    def __init__(self, id):
        self.id = id
        self.ag = ActorGraph()
        self.cg = CameraGraph()
        
    def add(self, obj):
        if isinstance(obj, Actor):
            print "added actor"
            self.ag.add(obj)
        elif isinstance(obj, Camera):
            print "added camera"
            self.cg.add(obj)
        else:
            print "Not valid actor or camera!"
        