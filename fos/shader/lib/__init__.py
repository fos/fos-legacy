import os.path as op

def get_shader_code(name):
    """ Returns the shader as a string """
    fname = op.join( op.dirname(__file__), name )
    if op.exists( fname ):
        with open(fname) as f:
            return f.read()
