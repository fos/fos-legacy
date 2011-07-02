from threading import RLock

from fos.core.actor_graph import ActorGraph
from fos.core.camera_list import CameraList
from fos.core.camera import Camera
from fos.core.actor import Actor
from fos.core.camera import DefaultCamera
from fos.core.intersection import test_segment_aabb

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

#            if update_camera:
#                print "TODO: update the camera view"
            
            #print "added actor", obj
            self.ag.add(obj)
        elif isinstance(obj, Camera):
            #print "added camera", obj
            self.cl.add(obj)
        else:
            print "Not valid actor or camera!"
            
    def propagate_pickray(self, near, far):
        # propagate the pickray to all the actors
        # XXX: implement intersection with the bounding boxes first
        
        for a in self.ag.actors:
            # aabb intersection
            if not a.aabb is None:
                if test_segment_aabb(near, far, a.aabb.coord[0], a.aabb.coord[1]):
                    print "found aabb"
                    try:
                        a.process_pickray(near,far)
                    except:
                        pass
                else:
                    print "no aabb"

                    
    def find_selected_actor(self, near, far):
        """ Finds the first actor """
        for a in self.ag.actors:
            # aabb intersection
            if not a.aabb is None:
                if test_segment_aabb(near, far, a.aabb.coord[0], a.aabb.coord[1]):
                    print "found aabb"
                    return a
                else:
                    print "no aabb"
                    return None
            
    def update_cameraview(self):
        pass
        # loop over all windows and update the camera    
    
    def remove(self, obj):
        if obj in self.ag.actors:
            print "remove actors"
            del self.ag.actors[self.ag.actors.index(obj)]
            
    def get_cameras(self):
        """ Returns the cameras existing in this world """
        return self.cl.cameras
    

            