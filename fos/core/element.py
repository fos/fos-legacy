
class Element():
    """ An element is a sub-part of an actor
    used to simplify and actor and expose functions to
    generate the primitives/buffers to be used by OpenGL
    """
    
    def __init__(self):
        # 4x4 affine transformation matrix from the local
        # coordinate system of the actor to the elements position
        # includes a rotational and translational part 
    
        # rigid transformation including a linear component
        # and a translational component represented as a 4x4 matrix
    
        # a rigid transformations preserves angles as well as distances
        
        # a rigid transofrmation is linear when the inverse of the linear
        # component A is regular (not singular)
        
        pass
    
    
    def get_num_glvertices(self):
        pass
    
    def get_glvertices(self):
        pass
    
    