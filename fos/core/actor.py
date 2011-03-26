import numpy as np

from fos.actor.primitives import AABBPrimitive
from fos.lib.pyglet.gl import GLfloat
from fos.lib.pyglet.gl import *

class Actor(object):
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
            
        aabb :  (corner1, corner2)
            the axis-aligned bounding box. axis-aligned means aligned
            with the world coordinate system axes

            corner1 : 3x1 array
                bottom-left-front point of the box when look into z direction
            corner2 : 3x1 array
                top-right-back point of the box
                
            If set to None, an axis aligned boundingbox is computed
            using the input vertices
                
        force_center_data : boolean
            if set to true, the mean of vertices location is subtracted from
            all the vertices. this is useful to compute a better bounding
            box and if the data has no meaningful affine
        
        obb : (center, orientation, halfwidths)
            
            center : 3x1 array
                the center point of the aabb
            orientation : 3x3 array
                orthogonal unit vectors
            halfwidths : 3x1 array
                box halfwidths along each axis
                
        """
        
        # data related information
        self.vertices = None
        self.living = False
        self.show_aabb = True
        
#        self.connectivity = None
#        self.field = None # scalar, vector, tensor
#        self.colormap = None
#        self.texture = None
        
        # movement related information. use the 
#        self.velocity = None
#        self.acceleration = None
        
        # event related information
#        self.event_queue = None
        # mouse or keyboard events on the actor
#        self.event_handlers = None
        # related: menu options for the actor

        
    def setup(self):
        """ Data preparation """
        # display lists, vbo
        # prepare different resolutions
        pass

    def update(self, dt):
        """ Update the actor 
        dt from the global timer """
        pass

    def draw_aabb(self):
        """ Draw the actor """
        
        if self.show_aabb:
            glPushMatrix()
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(1.0)
            glColor3f(1.0, 1.0, 0.0)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self.aabb.vertices_ptr)
            glDrawElements(self.aabb.mode,self.aabb.indices_nr,self.aabb.type,self.aabb.indices_ptr)
            glDisableClientState(GL_VERTEX_ARRAY)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopMatrix()
        
        
    def delete(self):
        """ Removing the geometry """
        pass
        
    def info(self):
        """ Show information about the actor """
        # debug mode
        print "this actor is at ", self
        print "number of vertices", len(self.vertices)
        print "is the actor living ?", self.living
        if not self.aabb is None:
            print "has boundary box", self.aabb
        
    
    def to_raytracer_file(self):
        """ Save the geometry to a file readable by a raytracer """
        pass

    def process_pickray(self, near, far):
        """ Process the pick ray like intersecting with the actor """
        pass
    
    # bounding box related
    ###
    
    def make_aabb(self, aabb = None, margin = 30):
        """ Make the axis aligned bounding box.
        
        Parameters
        ----------
        aabb : 2-tuple of numpy arrays of shape(3,)
            Defining the box by left-bottom-front and the top-right-back
            coordinate points. If None, a bounding box based on the
            vertices is computed.
        margin : float
            A margin to be added to the computed bounding box
        
        """
        # if no aabb is given, compute one
        if aabb == None:
            # compute an axis aligned bounding box
            # based on the vertices
            coord1 = np.array([self.vertices[:,0].min(),
                                self.vertices[:,1].min(),
                                self.vertices[:,2].min()], dtype = np.float32)
            coord2 = np.array([self.vertices[:,0].max(),
                               self.vertices[:,1].max(),
                               self.vertices[:,2].max()], dtype = np.float32)
            self.aabb = AABBPrimitive(blf = coord1, trb = coord2, margin = margin)
        else:
            assert len(aabb) == 2
            # otherwise set to given aabb
            self.aabb = AABBPrimitive(blf = aabb[0], trb = aabb[1], margin = margin)
    
    
    def make_obb(self):
        pass
        # just reuse the aabb points
#        leftbottom, righttop = self.aabb
#        
#        center = np.mean( np.vstack( (leftbottom, righttop) ), axis = 0)
#        halfwidths = (leftbottom - righttop) / 2.0
#        # in our default network, this obb is axis-aligned, thus the
#        # obb is the identity
#        orientation = np.eye( 3, 3 )
#         
#        self.obb = (center, halfwidths, orientation)
    
    def bounding_sphere(self):
        """ Compute the bounding sphere """
        pass
        # can use PCA?
    
    def bouding_ellipsoid(self):
        """ Compute the bounding elipsoid """
        pass
        # can use PCA?
        
    ## affine logic
    ###
    
    def set_affine(self, affine):
        # update the affine
        print "update affine", self.affine
        self.affine = affine
        self._update_glaffine()
    
    def scale(self, scale_factor):    
        """ Scales the actor by scale factor.
        Multiplies the diagonal of the affine for
        the first 3 elements """
        self.affine[0,0] *= scale_factor
        self.affine[1,1] *= scale_factor
        self.affine[2,2] *= scale_factor
        self._update_glaffine()
        
    def translate(self, dx, dy, dz):
        """ Translate the actor.
        Remember the OpenGL has right-handed 
        coordinate system """
        self.affine[0,3] += dx
        self.affine[1,3] += dy
        self.affine[2,3] += dz
        self._update_glaffine()
    
    def set_position(self, x, y, z):
        """ Position the actor.
        Remember the OpenGL has right-handed 
        coordinate system """
        self.affine[0,3] += x
        self.affine[1,3] += y
        self.affine[2,3] += z
        self._update_glaffine()

    def _update_glaffine(self):
        self.glaffine = (GLfloat * 16)(*tuple(self.affine.T.ravel()))

        
    # life processes
    ###
    
    def start(self, lifespan = 10, tickingtime = 2.0):
        print "the actor is alive"
        self.living = True
        self.internal_timestamp = 0.0
        # call self.update every tickingtime
        
    def stop(self):
        print "the actor stops living"
        self.living = False
        
    def cont(self):
        print "continue to live happily"
        self.living = True
        

