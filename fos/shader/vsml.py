# A port of VSML
# http://www.lighthouse3d.com/very-simple-libs/vsml/vsml-in-action/
# to support matrix operations

# Singleton class from
# http://code.activestate.com/recipes/52558/

class VSML:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """

        def spam(self):
            """ Test method, return singleton id """
            return id(self)

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if VSML.__instance is None:
            # Create and remember instance
            VSML.__instance = VSML.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_VSML__instance'] = VSML.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)


# Test it
s1 = VSML()
print id(s1), s1.spam()

s2 = VSML()
print id(s2), s2.spam()

# Sample output, the second (inner) id is constant:
# 8172684 8176268
# 8168588 8176268
