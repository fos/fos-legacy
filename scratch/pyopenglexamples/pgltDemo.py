# http://people.cs.uchicago.edu/~glk/pglt/
#
# See "LOOK HERE" below for the code that's currently broken
# See "LOOK HERE" below for the code that's currently broken
# See "LOOK HERE" below for the code that's currently broken
#
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from pgltGeom import *
import sys, math, traceback

def affine(i,v,I,o,O):
  return (1.0*O-o)*(1.0*v-i)/(1.0*I-i) + 1.0*o

def init():
    zero = (0,0,0,0)
    one = (1,1,1,1)
    lpos = (0,0,1,0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, zero)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, one)
    glLightfv(GL_LIGHT0, GL_SPECULAR, one)
    glLightfv(GL_LIGHT0, GL_POSITION, lpos)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(7, 1.0, 20, 30)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(-20, 10, 12,
               0, 0, 0,
               0, 0, 1)

glpt = [
    0,                 # 0: limnPrimitiveUnknown
    GL_POINTS,         # 1: limnPrimitiveNoop 
    GL_TRIANGLES,      # 2: limnPrimitiveTriangles 
    GL_TRIANGLE_STRIP, # 3: limnPrimitiveTriangleStrip 
    GL_TRIANGLE_FAN,   # 4: limnPrimitiveTriangleFan 
    GL_QUADS,          # 5: limnPrimitiveQuads 
    GL_LINE_STRIP,     # 6: limnPrimitiveLineStrip 
    GL_LINES
]

def pgltDraw(_lpld, useVertexArrays):
    lpld = _lpld.contents
    vertIdx = 0
    if useVertexArrays:
        # LOOK HERE
        # LOOK HERE
        # LOOK HERE
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(4, GL_FLOAT, 0, lpld.xyzw)
        if lpld.norm:
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, lpld.norm)
        if lpld.rgba:
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(4, GL_UNSIGNED_BYTE, 0, lpld.rgba)
        for primIdx in range(lpld.primNum):
            vertCnt = lpld.icnt[primIdx]
            if limnPrimitiveNoop != lpld.type[primIdx]:
                # get a segfault if last arg is simply "lpld.indx"
                glDrawElements(glpt[lpld.type[primIdx]], vertCnt,
                               GL_UNSIGNED_INT, lpld.indx + vertIdx)
            vertIdx += vertCnt
        glDisableClientState(GL_VERTEX_ARRAY)
        if lpld.norm:
            glDisableClientState(GL_NORMAL_ARRAY)
        if lpld.rgba:
            glDisableClientState(GL_COLOR_ARRAY)
    else:
        for primIdx in range(lpld.primNum):
            if limnPrimitiveNoop == lpld.type[primIdx]:
                continue
            vertCnt = lpld.icnt[primIdx]
            glWhat = glpt[lpld.type[primIdx]]
            glBegin(glWhat)
            for vii in range(vertCnt):
                ii = lpld.indx[vii + vertIdx]
                if lpld.norm:
                    glNormal3f(lpld.norm[0 + 3*ii],
                               lpld.norm[1 + 3*ii],
                               lpld.norm[2 + 3*ii])
                if lpld.rgba:
                    glColor4ub(lpld.rgba[0 + 4*ii],
                               lpld.rgba[1 + 4*ii],
                               lpld.rgba[2 + 4*ii],
                               lpld.rgba[3 + 4*ii])
                glVertex4f(lpld.xyzw[0 + 4*ii],
                           lpld.xyzw[1 + 4*ii],
                           lpld.xyzw[2 + 4*ii],
                           lpld.xyzw[3 + 4*ii])
            glEnd()
            vertIdx += vertCnt

uva = 0
def display():
    # this is called repeatedly, alternating between drawing the geometry
    # *without* vertex arrays on a yellow background, and 
    # *with* vertex arrays on a white background
    global pgltObject
    global uva
    glClearColor(1, 1, uva, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    try:
        pgltDraw(pgltObject, uva)
    except:
        print "problems drawing: -------------"
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        traceback.print_exception(exceptionType, exceptionValue,
                                  exceptionTraceback,
                                  limit=2, file=sys.stdout)
        print "-------------------------------"
        sys.exit(1)
    glutSwapBuffers()
    uva = 1-uva

stepNum = 30
tubeNum = 8
_line = limnPolyDataNew()
line = _line.contents
limnPolyDataAlloc(_line, 1 << limnPolyDataInfoRGBA,
                  stepNum*tubeNum, stepNum*tubeNum, tubeNum)
running = 0
for ti in range(tubeNum):
    th0 = affine(0, ti, tubeNum, -3.14159, 3.14159)
    for si in range(stepNum):
        theta = th0 + affine(0, si, stepNum,
                             -3.14159/tubeNum, 3.14159/tubeNum)
        line.xyzw[0 + 4*running] = math.cos(theta)
        line.xyzw[1 + 4*running] = math.sin(theta)
        line.xyzw[2 + 4*running] = affine(0,si,stepNum,-0.8,0.8)
        line.xyzw[4 + 4*running] = 1
        line.rgba[0 + 4*running] = (128 + si*ti) % 256
        line.rgba[1 + 4*running] = (128 + 2*si*ti) % 256
        line.rgba[2 + 4*running] = (128 + 4*si*ti) % 256
        line.rgba[3 + 4*running] = 255
        line.indx[running] = running
        running += 1
    line.type[ti] = limnPrimitiveLineStrip
    line.icnt[ti] = stepNum

pgltObject = limnPolyDataNew()
if limnPolyDataSpiralTubeWrap(pgltObject, _line,
                              limnPolyDataInfoBitFlag(_line),
                              10, 5, 0.15):
    print "error!"
    sys.exit(1);

limnPolyDataNix(_line)
  
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH | GLUT_ALPHA)
glutInitWindowSize(300, 300)
glutCreateWindow("pgltDemo")
glutDisplayFunc(display)
glutIdleFunc(display)
init()
glutMainLoop()
