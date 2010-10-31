from threading import RLock

# it is sufficient to import "pyglet" here once
from fos.lib import import_thirdparty
pyglet = import_thirdparty("pyglet")

from fos.core.actor_graph import ActorGraph
from fos.core.camera_graph import CameraGraph
from fos.core.camera import Camera
from fos.core.actor import Actor

class World():

    def __init__(self, id):
        self.id = id
        self.ag = ActorGraph()
        self.cg = CameraGraph()
        
        self._render_lock = RLock()
        
    def add(self, obj):
        if isinstance(obj, Actor):
            print "added actor"
            self.ag.add(obj)
        elif isinstance(obj, Camera):
            print "added camera"
            self.cg.add(obj)
        else:
            print "Not valid actor or camera!"
        