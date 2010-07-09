
def list_indices(L, value, start=0):
    
    ''' find the `indices` with specific `value` in list L

    This is implemented as a generator function


    Example:
    --------

    >>> from fos.core.utils import list_indices as lind
    >>> test=[True, False, True, False, False]
    >>> for i in lind(test,False): print i
    1
    3
    4

    '''
    
    try:

        while start<len(L):

            i = L.index(value, start)

            start=i+1

            yield i

    except ValueError:

        pass

        
