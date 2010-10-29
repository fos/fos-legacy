
class Actor():
    """ Define a visualization object in Fos """
    
    def __init__(self):
        
        # data related information
        self.vertices = None
        self.connectivity = None
        self.field = None # scalar, vector, tensor
        self.colormap = None
        self.texture = None
        
        # time related information
        self.lifespan = None
        # connectivity across time steps
        
        # movement related information 
        self.position = None
        self.velocity = None
        self.acceleration = None
        self.center = None # center of mass / center of bounding box
        self.orientation = None # of the bounding volume, orientation on the local coordinate system
        self.local_coord_system = None # from the global opengl coordinate system
        
        # event related information
        self.event_queue = None
        # mouse or keyboard events on the actor
        self.event_handlers = None
        # related: menu options for the actor
        
        # is the object in a group?
        # 
        
    def setup(self):
        """ Data preparation """
        # display lists, vbo
        # prepare different resolutions
        pass

    def update(self, dt):
        """ Update the actor 
        dt from the global timer """
        pass

    def draw(self):
        """ Draw the actor """
        pass
        
    def delete(self):
        """ Removing the geometry """
        pass
        
    # should we use repr or __repr__ or __str__ ?
    # we would need to inherit from object
    def info(self):
        """ Show information about the actor """
        # 'gl'
        # 'conf'
        # 'actor'
        # debug mode
        pass
    
    def to_raytracer_file(self):
        """ Save the geometry to a file readable by a raytracer """
        pass

    def process_pickray(self, near, far):
        """ Process the pick ray like intersecting with the actor """
        pass
    
    def bounding_box(self):
        """ Compute the bounding box """
        pass
    
    def bounding_sphere(self):
        """ Compute the bounding sphere """
        pass
        # can use PCA?
    
    def bouding_ellipsoid(self):
        """ Compute the bounding elipsoid """
        pass
        # can use PCA?
        
        

