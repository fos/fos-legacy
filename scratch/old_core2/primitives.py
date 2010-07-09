from fos.core.actors import Actor
import numpy as np

class Empty(Actor):

    def __init__(self):

        pass

    def init(self):

        pass

    def display(self):

        print 'Near_pick', self.near_pick

        print 'Far_pick', self.far_pick

        

def map_colors(object, colors):
    ''' Map colors for specific objects

    Examples:
    ---------

    >>> from fos.core import primitives
    >>> primitives.map_colors([np.zeros((10,3)),np.ones((3,3))], (1,1,1,0))
    [array([[1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0]]),
    array([[1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 0]])]

    >>> primitives.map_colors([np.zeros((10,3)),np.ones((3,3))], np.array([[1,1,1],[0,1,0]]))
    [array([[1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]]),
    array([[0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]])]

    See Also:
    ---------

    fos.core.tracks

    '''

    if hasattr(object,'insert'): #object is a list

        if hasattr( object[0], 'shape') : #object is a list of arrays

            if hasattr(colors, 'shape') : # colors is a numpy array

                if colors.ndim == 1: # one color only for all objects

                    new_colors=[np.tile(colors,(len(arr),1)) for arr in object]

                    return new_colors

                if colors.ndim == 2: # one color for every element of the list object

                    if len(colors) == len(object): # absolutely
                                # necessary check

                        new_colors=[np.tile(colors[i],(len(arr),1)) for (i,arr) in enumerate(object)]

                        return new_colors


                    raise ValueError('object len needs to be the same \
                    with colors len')

            if isinstance(colors,list): # colors is a list object

                if len(colors)==3 or len(colors)==4:

                    colors = np.array(colors)
                    
                    new_colors=[np.tile(colors,(len(arr),1)) for arr in object]

                    return new_colors
                
                else:
                    
                    raise ValueError('colors can be one list of 3 or 4 \
                    values')

                

            if isinstance(colors,tuple):

                if len(colors)==3 or len(colors)==4:

                    colors = np.array(colors)
                    
                    new_colors=[np.tile(colors,(len(arr),1)) for arr in object]

                    return new_colors                   

                else:
                    
                    raise ValueError('colors can be one tuple of 3 or 4 \
                    values')
  

                

        else:

            raise ValueError('Unknown object type')


    if hasattr(object, 'shape'): # object is a numpy array

        if object.ndim == 2: # 2d numpy array

            pass

        if object.ndim == 1: # 1d numpy array

            return colors



    pass
