import numpy as np

class Actor():
    """ Define a visualization object in Fos """
    
    def __init__(self,
                 affine = None,
                 aabb = None,
                 force_center_data = False,
                 **kwargs):
        """ Create an actor
        
        Parameters
        ----------
        
        affine : 4x4 array
            the affine is expected to be normal, i.e. it has only
            rotational and translational components, but no shears
            the affine is applied to the input vertices data to position
            the actor in the world space. If set to none, an affine is
            generated to positions the actor optimally for the camera view
            
        aabb : (center, orientation, halfwidths) or (corner1, corner2)
            the axis-aligned bounding box. axis-aligned means aligned
            with the world coordinate system axes
            
            center : 3x1 array
                the center point of the aabb
            orientation : 3x3 array
                orthogonal unit vectors
            halfwidths : 3x1 array
                box halfwidths along each axis
                
            alternatively, you can define the axis aligned bounding-box
            using two opposite corner points of the cube
            corner1 : 3x1 array
                lower-bottom-left point of the box when look into z direction
            corner2 : 3x1 array
                upper-top-right point of the box
                
            if set to None, an axis aligned boundingbox is computed
            from the input vertices
                
        force_center_data : boolean
            if set to true, the mean of vertices location is subtracted from
            all the vertices. this is useful to compute a better bounding
            box and if the data has no meaningful affine
        
        
        """
        
        # data related information
        self.vertices = None
        self.connectivity = None
        self.field = None # scalar, vector, tensor
        self.colormap = None
        self.texture = None
        
        # time related information
        self.lifespan = None
        # connectivity across time steps
        
        # movement related information. use the 
        self.velocity = None
        self.acceleration = None
        
        # event related information
        self.event_queue = None
        # mouse or keyboard events on the actor
        self.event_handlers = None
        # related: menu options for the actor
        
        
        # if no aabb is given, compute one
        if aabb == None:
            # compute an axis aligned bounding box
            self.aabb = self.update_aabb()
        else:
            # otherwise set to given aabb
            if len(aabb) == 3:
                # store directly
                self.aabb = aabb
                
            elif len(aabb) == 2:
                # two points given. convert to 3-tuple
                # center = computemean
                # half_x = abs(point2[0] - point1[0]) / 2.
                # half_y = abs(point2[1] - point1[1]) / 2.
                # half_z = abs(point2[2] - point1[3]) / 2.
                # orientation are the default vectors [1,0,0], [0,1,0], [0,0,1]
                self.aabb = aabb
        
        
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
    
    def update_aabb(self):
        """ Updates the axis aligned bounding box. Either on object
        creation without a bounding box given, or after a dynamic change
        of the internal structure, e.g. changes in position of vertices """
        pass
        # if self.aabb = None
        #     self.aabb = self.bounding_box()
    
    def update_aabb(self):
        """ Compute the bounding box using the internal structure
        of the actor, e.g. position of vertices """
        pass
    
    def bounding_sphere(self):
        """ Compute the bounding sphere """
        pass
        # can use PCA?
    
    def bouding_ellipsoid(self):
        """ Compute the bounding elipsoid """
        pass
        # can use PCA?
        
        

