from threading import RLock

from fos.core.actor_graph import ActorGraph
from fos.core.camera_list import CameraList
from fos.core.camera import Camera
from fos.core.actor import Actor
from fos.core.camera import DefaultCamera

class World():

    def __init__(self, name = None):
        self.name = name
        self.ag = ActorGraph()
        self.cl = CameraList()
        
        # attached window
        self.wins = []
        
        # create a simple camera
        simple_camera = DefaultCamera()
        self.cl.cameras.append(simple_camera)
        
        self._render_lock = RLock()
        
    def add(self, obj, update_camera = True):
        if isinstance(obj, Actor):

            if update_camera:
                print "update the camera view"
            
            print "added actor", obj
            self.ag.add(obj)
        elif isinstance(obj, Camera):
            print "added camera", obj
            self.cl.add(obj)
        else:
            print "Not valid actor or camera!"
            
    def delete(self, obj):
        if obj in self.ag.actors:
            print "delete actors"
            del self.ag.actors[self.ag.actors.index(obj)]
            
    def get_cameras(self):
        """ Returns the cameras existing in this world """
        return self.cl.cameras
    

            