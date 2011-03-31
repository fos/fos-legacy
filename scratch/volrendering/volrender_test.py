'''
A quick and dirty skeleton for prototyping GLSL shaders.  It consists of a 
self contained slice-based volume renderer.
'''

import numpy, sys, wx

from OpenGL.GL import *
from OpenGL.GLU import *

from numpy import array
from transfer_function import TransferFunctionWidget
from wx.glcanvas import GLCanvas

# The skeleton
def box_side(w=1.0, z=0.0):
    return [[0.0, 0.0, z], [w, 0.0, z], [w, 0.0, z], [w, w, z],
            [w, w, z], [0.0, w, z], [0.0, w, z], [0.0, 0.0, z]]

def gen_plane(t, p=0.0, w=1.0):
    ''' Creates front facing planes '''
    try:
        return { 'yz': [(p, 0, 0), (p, w, 0), (p, w, w), (p, 0, w)],
                 'xz': [(0, p, w), (w, p, w), (w, p, 0), (0, p, 0)],
                 'xy': [(0, 0, p), (w, 0, p), (w, w, p), (0, w, p)]}[t]
    except KeyError:
        raise Exception, 'What kind of planes do you want?'
    
box = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0],
       [1.0, 0.0, 0.0], [1.0, 0.0, 1.0],
       [1.0, 1.0, 0.0], [1.0, 1.0, 1.0],
       [0.0, 1.0, 0.0], [0.0, 1.0, 1.0]]
box.extend(box_side())
box.extend(box_side(z=1.0))

plane_count = 1000

def compile_program(vertex_src, fragment_src):
    '''
    Compile a Shader program given the vertex
    and fragment sources
    '''
    
    program = glCreateProgram()
 
    shaders = []
 
    for shader_type, src in ((GL_VERTEX_SHADER, vertex_src), 
                             (GL_FRAGMENT_SHADER, fragment_src)):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, src)
        glCompileShader(shader)

        shaders.append(shader)
            
        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    
        if not status:
            if glGetShaderiv(shader, GL_INFO_LOG_LENGTH) > 0:
                log = glGetShaderInfoLog(shader)
                print >> sys.stderr, log.value
            glDeleteShader(shader)
            raise ValueError, 'Shader compilation failed'

        glAttachShader(program, shader)
 
    glLinkProgram(program)

    for shader in shaders:
        glDeleteShader(shader)
 
    return program

class TransferGraph(wx.Dialog):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):

        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        self.mainPanel = wx.Panel(self, -1)

        # Create some CustomCheckBoxes
        self.t_function = TransferFunctionWidget(self.mainPanel, -1, "", size=wx.Size(300, 150))
       
        # Layout the items with sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.mainPanel, 1, wx.EXPAND)
        
        self.SetSizer(mainSizer)
        mainSizer.Layout()

class VolumeRenderSkeleton(GLCanvas):
    def __init__(self, parent):
        GLCanvas.__init__(self, parent, -1, attribList=[wx.glcanvas.WX_GL_DOUBLEBUFFER])

        self.t_graph = TransferGraph(self)
       
        wx.EVT_PAINT(self, self.OnDraw)
        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_MOTION(self, self.OnMouseMotion)
        wx.EVT_LEFT_DOWN(self, self.OnMouseLeftDown)
        wx.EVT_LEFT_UP(self, self.OnMouseLeftUp)
        wx.EVT_ERASE_BACKGROUND(self, lambda e: None)
        wx.EVT_CLOSE(self, self.OnClose)
        wx.EVT_CHAR(self, self.OnKeyDown)
        
        self.SetFocus()
        
        # So we know when new values are added / changed on the tgraph
        self.t_graph.Connect(-1, -1, wx.wxEVT_COMMAND_SLIDER_UPDATED, self.OnTGraphUpdate)
       
        self.init = False
        self.rotation_y = 0.0
        self.rotation_x = 0.0
        self.prev_y = 0
        self.prev_x = 0
        self.mouse_down = False
        
        self.width = 400
        self.height = 400
        
        self.fragment_shader_src = '''
        uniform sampler1D TransferFunction;
        uniform sampler3D VolumeData;       
        void main(void)
        {            
            gl_FragColor = vec4(1.0, 0.0, 0.0, 0.0);
        }
        '''

        self.vertex_shader_src = '''
        void main(void)
        {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
        '''        
        self.fragment_src_file = 'earth.f.c'
        self.vertex_src_file = 'earth.v.c'
        self.lighting = False
        self.light_count = 1
        
        # List of textures that need to be freed
        self.texture_list = []
        # List of VBOs that need to be freed
        self.buffers_list = []
        # This is the transfer graph
        self.t_graph.Show()

    def OnTGraphUpdate(self, event):
        self.UpdateTransferFunction()
        self.Refresh()

    def OnDraw(self, event):
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = True

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslate(0.0, 0.0, -2.0)
        glRotate(self.rotation_y, 0.0, 1.0, 0.0)
        glRotate(self.rotation_x, 1.0, 0.0, 0.0)
        glTranslate(-0.5, -0.5, -0.5)

        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)


        # Draw the box
        glUseProgram(0)
        glColor(0.0, 1.0, 0.0)
        glDisable(GL_LIGHTING)
        glVertexPointerf(box)
        glDrawArrays(GL_LINES, 0, len(box))

        # Draw the slice planes
        glUseProgram(self.program)
        
        self.SetupUniforms()

        # Choose the correct set of planes
        if self.rotation_y < 45.0 or self.rotation_y >= 315.0:
            vertex_vbo = self.planes_vbo['xy'][0]
        elif self.rotation_y >= 45.0 and self.rotation_y < 135.0:
            vertex_vbo = self.planes_vbo['yz'][1]
        elif self.rotation_y >= 135.0 and self.rotation_y < 225.0:
            vertex_vbo = self.planes_vbo['xy'][1]
        elif self.rotation_y >= 225.0 and self.rotation_y < 315.0:
            vertex_vbo = self.planes_vbo['yz'][0]
                    
        # Render the planes using VBOs
        glBindBuffer(GL_ARRAY_BUFFER, vertex_vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        glDrawArrays(GL_QUADS, 0, 4*plane_count)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.SwapBuffers()
        return

    def InitGL(self):
        
        # Load the Shader sources from the files
        self.LoadShaderSources()
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glEnableClientState(GL_VERTEX_ARRAY)
        
        glDepthFunc(GL_LESS)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glShadeModel(GL_SMOOTH)
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, self.width/float(self.height), 0.1, 1000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.SetupLighting()
        self.LoadVolumeData()
        self.LoadTransferFunction((self.t_graph.t_function.get_map() / array([255.0, 255.0, 255.0, 1.0])).flatten())
        self.program = compile_program(self.vertex_shader_src, self.fragment_shader_src)
        self.BuildGeometry()

    def SetupLighting(self):
        '''
        Initialize default lighting
        '''
        
        glLight(GL_LIGHT0, GL_AMBIENT, (1.0, 1.0, 1.0))
        glLight(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0))
        glLight(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0))
        glLight(GL_LIGHT0, GL_POSITION, (-1.0, -1.0, -1.0))
        glEnable(GL_LIGHT0)
        
    def SetupUniforms(self):
       
        # Init the texture units
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_1D, self.transfer_function)
        glUniform1i(glGetUniformLocation(self.program, "TransferFunction"), 0)
        glUniform1i(glGetUniformLocation(self.program, "EnableLighting"), 
                    self.lighting)
        glUniform1i(glGetUniformLocation(self.program, "NumberOfLights"), 
                    self.light_count)

    def BuildGeometry(self):
        self.planes_vbo = { 'xy':None, 'xz':None, 'yz':None }
        
        increment  = 1.0 / (plane_count)
                
        for k in self.planes_vbo.keys():
            fwd = [gen_plane(p=(i*increment), t=k) for i in range(plane_count + 1)]
        
            rev = []
            rev.extend(fwd)
            rev.reverse()
            
            data = (array(fwd, dtype=numpy.float32).flatten(), 
                    array(rev, dtype=numpy.float32).flatten())

            self.planes_vbo[k] = []

            for i in range(2):
                self.planes_vbo[k].append(glGenBuffers(1))
                glBindBuffer(GL_ARRAY_BUFFER, self.planes_vbo[k][i])
                glBufferData(GL_ARRAY_BUFFER, data[i], GL_STATIC_DRAW_ARB)

    def LoadTransferFunction(self, data):
        # Create Texture
        self.transfer_function = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_1D, self.transfer_function)
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA, 256, 0, GL_RGBA, GL_FLOAT, data)
        return

    def UpdateTransferFunction(self):
        data = (self.t_graph.t_function.get_map() / array([255.0, 255.0, 255.0, 1.0])).flatten()
        glBindTexture(GL_TEXTURE_1D, self.transfer_function)
        glTexSubImage1D(GL_TEXTURE_1D, 0, 0, 256, GL_RGBA, GL_FLOAT, data)

    def LoadVolumeData(self):
        pass
    
    def LoadShaderSources(self):
        try:
            self.fragment_shader_src = open(self.fragment_src_file).read()
        except IOError, e:
            print 'Fragment source not found, using default'

        try:
            self.vertex_shader_src = open(self.vertex_src_file).read()
        except IOError, e:
            print 'Vertex source not found, using default'


    def OnSize(self, event):
        try:
            self.width, self.height = event.GetSize()
        except:
            self.width = event.GetSize().width
            self.height = event.GetSize().height
        
        self.Refresh()
        self.Update()

    def OnMouseMotion(self, event):
        
        x = event.GetX()
        y = event.GetY()

        if self.mouse_down:
            self.rotation_y += (x - self.prev_x)/2.0
            self.rotation_y %= 360.0
#            self.rotation_x -= ((y - self.prev_y)/2.0
#            self.rotation_x %= 360.0
            self.prev_x = x
            self.prev_y = y
            self.Refresh()
            self.Update()

    def OnMouseLeftDown(self, event):
        self.mouse_down = True
        self.prev_x = event.GetX()
        self.prev_y = event.GetY()
        
    def OnMouseLeftUp(self, event):
        self.mouse_down = False
    
    def OnKeyDown(self, event):
        
        if event.GetKeyCode() == ord('r'):
            try:
                print 'Compiling shaders...',
                self.LoadShaderSources()
                program = compile_program(self.vertex_shader_src, 
                                          self.fragment_shader_src)
                self.program = program
                self.Refresh()
            except Exception, e:
                print 'FAILED'
                print e
            print 'Done'
        elif event.GetKeyCode() == ord('l'):
            self.lighting = not self.lighting
            print 'Lighting', self.lighting 
            self.Refresh()
            
    def OnClose(self):
        
        for t in self.texture_list:
            glDeleteTextures(t)
        
        for b in self.buffers_list:
            glDeleteBuffers(1, b)

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, -1, 'Volume Rendering Skeleton', wx.DefaultPosition, wx.Size(600, 600))
    canvas = VolumeRenderSkeleton(frame)

    frame.Show()
    app.MainLoop()
