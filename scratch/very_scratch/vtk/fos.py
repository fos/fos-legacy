''' Fos module implements simple visualization functions using VTK. Fos means light in Greek.    
   
    The main idea is the following:
    A window can have one or more renderers. A renderer can have none, one or more actors. Examples of actors are a sphere, line, point etc.
    You basically add actors in a renderer and in that way you can visualize the forementioned objects e.g. sphere, line ...
    
    fos Example:
    ----------------
    >>> from dipy.viz import fos
    >>> r=fos.ren()    
    >>> a=fos.axes()        
    >>> fos.add(r,a)
    >>> fos.show(r)
    
    The future version will be as simple as 
    Foz Example:
    ----------------
    >>> from dipy.viz import fos
    >>> foz=fos.Foz()
    >>> foz.axes()
    
    but Foz is still ongoing and needs more testing...
    
'''

try:
    import vtk       
except ImportError:
    raise ImportError('VTK is not installed.')
    
try:
    import numpy as np
except ImportError:
    raise ImportError('Numpy is not installed.')


import types    

'''
For more color names see
http://www.colourlovers.com/blog/2007/07/24/32-common-color-names-for-easy-reference/
'''
#Some common colors
red=np.array([1,0,0])
green=np.array([0,1,0])
blue=np.array([0,0,1])
yellow=np.array([1,1,0])
cyan=np.array([0,1,1])
azure=np.array([0,0.49,1])
golden=np.array([1,0.84,0])
white=np.array([1,1,1])
black=np.array([0,0,0])
           	
aquamarine=np.array([0.498,1.,0.83])
indigo=np.array([ 0.29411765,  0.,  0.50980392])
lime=np.array([ 0.74901961,  1.,  0.])
hot_pink=np.array([ 0.98823529,  0.05882353,  0.75294118])

gray=np.array([0.5,0.5,0.5])
dark_red=np.array([0.5,0,0])
dark_green=np.array([0,0.5,0])
dark_blue=np.array([0,0,0.5])

tan=np.array([ 0.82352941,  0.70588235,  0.54901961])
chartreuse=np.array([ 0.49803922,  1.        ,  0.        ])
coral=np.array([ 1.        ,  0.49803922,  0.31372549])

#a track buffer used only with picking tracks
track_buffer=[]
#indices buffer for the tracks
ind_buffer=[]
#tempory renderer used only with picking tracks
tmp_ren=None

# Create a text mapper and actor to display the results of picking.
textMapper = vtk.vtkTextMapper()
tprop = textMapper.GetTextProperty()
tprop.SetFontFamilyToArial()
tprop.SetFontSize(10)
#tprop.BoldOn()
#tprop.ShadowOn()
tprop.SetColor(1, 0, 0)
textActor = vtk.vtkActor2D()
textActor.VisibilityOff()
textActor.SetMapper(textMapper)
# Create a cell picker.
picker = vtk.vtkCellPicker()

class Foz(object):
    ''' An object for fast accessing the fos utilities.
    '''
    def __init__(self):
        
        self.canvas={}
        self.cren=0
        self.canvas[0]=ren()
        self.canvas[1]=ren()
        self.canvas[2]=ren()
        self.canvas[3]=ren()
        self.on=True
        self.clear()
        
        '''
        Note :
        ------
        add actors below their renderers
        '''
        
        
    def __len__(self):
        pass

    def __iter__(self):
        pass            

    def length(self):
        pass

    def volume(self,vol,voxsz=(1.0,1.0,1.0),affine=None,center_origin=1,info=1,maptype=0,trilinear=1,iso=0,iso_thr=100,opacitymap=None,colormap=None):    
        
        v=volume(vol,voxsz,affine,center_origin,info,maptype,trilinear,iso,iso_thr,opacitymap,colormap)   
        add(self.canvas[self.cren],v)
        if self.on:
            show(self.canvas[self.cren])
        
        return v
        
    def origin(self,scale=(1,1,1),colorx=(1,0,0),colory=(0,1,0),colorz=(0,0,1),opacity=1):
                
        ax=axes(scale,colorx,colory,colorz,opacity)
        add(self.canvas[self.cren],ax)
        if self.on:
            show(self.canvas[self.cren])
        
        return ax
    
    def line(self,lines,colors,opacity=1,linewidth=1):
        
        l=line(lines,colors,opacity,linewidth)
        add(self.canvas[self.cren],l)
        if self.on:
            show(self.canvas[self.cren])
        
        return l
    
    def point(self,points,colors,opacity=1):
        
        p=point(points,colors,opacity)
        add(self.canvas[self.cren],p)
        if self.on:
            show(self.canvas[self.cren])
    
    def dots(self,points,color=(1,0,0),opacity=1):
        
        d=dots(points,color,opacity)
        add(self.canvas[self.cren],d)
        if self.on:
            show(self.canvas[self.cren])
        
        return d    
    
    def label(self,ren,text='Origin',pos=(0,0,0),scale=(0.2,0.2,0.2),color=(1,1,1)):
        
        la=label(ren=self.cren,text=text,pos=pos,scale=scale,color=color)        
        if self.on:
            show(self.canvas[self.cren])
        
        return la
    
    def sphere(self,position=(0,0,0),radius=0.5,thetares=8,phires=8,color=(0,0,1),opacity=1,tessel=0):

        s=sphere(position,radius,thetares,phires,color,opacity,tessel)
        add(self.canvas[self.cren],s)
        if self.on:
            show(self.canvas[self.cren])
        return s
    
    def show(self,title='Fos',size=(300,300)):
        
        show(self.canvas[self.cren],title='Foz ',size=(300,300))
        self.on=False
        
    def clear(self,actor=None):
        if actor == None:
            clear(self.canvas[self.cren])
        else:
            rm(self.canvas[self.cren],actor)
            
        
    @property
    def new(self):
        pass
                


def ren():
    ''' Create a renderer
    
    Returns
    --------
    a vtkRenderer() object    
    
    Examples
    ---------
    >>> from dipy.viz import fos
    >>> import numpy as np
    >>> r=ren()    
    >>> lines=[np.random.rand(10,3)]        
    >>> c=line(lines)    
    >>> add(r,c)
    >>> show(r)    
    '''
    return vtk.vtkRenderer()


def add(ren,a):
    ''' Add a specific actor    
    '''
    if isinstance(a,vtk.vtkVolume):
        ren.AddVolume(a)
    else:    
        ren.AddActor(a)

def rm(ren,a):
    ''' Remove a specific actor    
    '''    
    ren.RemoveActor(a)

def clear(ren):
    ''' Remove all actors from the renderer 
    '''
    ren.RemoveAllViewProps()

def rm_all(ren):
    ''' Remove all actors from the renderer 
    '''
    clear(ren)

def _arrow(pos=(0,0,0),color=(1,0,0),scale=(1,1,1),opacity=1):
    ''' Internal function for generating arrow actors.    
    '''
    arrow = vtk.vtkArrowSource()
    #arrow.SetTipLength(length)
    
    arrowm = vtk.vtkPolyDataMapper()
    arrowm.SetInput(arrow.GetOutput())
    
    arrowa= vtk.vtkActor()
    arrowa.SetMapper(arrowm)
    
    arrowa.GetProperty().SetColor(color)
    arrowa.GetProperty().SetOpacity(opacity)
    arrowa.SetScale(scale)
    
    return arrowa
    
def axes(scale=(1,1,1),colorx=(1,0,0),colory=(0,1,0),colorz=(0,0,1),opacity=1):
    ''' Create an actor with the coordinate system axes where  red = x, green = y, blue =z.
    '''
    
    arrowx=_arrow(color=colorx,scale=scale,opacity=opacity)
    arrowy=_arrow(color=colory,scale=scale,opacity=opacity)
    arrowz=_arrow(color=colorz,scale=scale,opacity=opacity)
    
    arrowy.RotateZ(90)
    arrowz.RotateY(-90)

    ass=vtk.vtkAssembly()
    ass.AddPart(arrowx)
    ass.AddPart(arrowy)
    ass.AddPart(arrowz)
           
    return ass

def _lookup(colors):
    ''' Internal function
    Creates a lookup table with given colors.
    
    Parameters
    ------------
    colors : array, shape (N,3)
            Colormap where every triplet is encoding red, green and blue e.g. 
            r1,g1,b1
            r2,g2,b2
            ...
            rN,gN,bN        
            
            where
            0=<r<=1,
            0=<g<=1,
            0=<b<=1,
    
    Returns
    ----------
    vtkLookupTable
    
    '''
        
    colors=np.asarray(colors,dtype=np.float32)
    
    if colors.ndim>2:
        raise ValueError('Incorrect shape of array in colors')
    
    if colors.ndim==1:
        N=1
        
    if colors.ndim==2:
        
        N=colors.shape[0]    
    
    
    lut=vtk.vtkLookupTable()
    lut.SetNumberOfColors(N)
    lut.Build()
    
    if colors.ndim==2:
        scalar=0
        for (r,g,b) in colors:
            
            lut.SetTableValue(scalar,r,g,b,1.0)
            scalar+=1
    if colors.ndim==1:
        
        lut.SetTableValue(0,colors[0],colors[1],colors[2],1.0)
            
    return lut

def line(lines,colors,opacity=1,linewidth=1):
    ''' Create an actor for one or more lines.    
    
    Parameters
    ----------
    lines :  list of arrays representing lines as 3d points  for example            
            lines=[np.random.rand(10,3),np.random.rand(20,3)]   
            represents 2 lines the first with 10 points and the second with 20 points in x,y,z coordinates.
    colors : array, shape (N,3)
            Colormap where every triplet is encoding red, green and blue e.g. 
            r1,g1,b1
            r2,g2,b2
            ...
            rN,gN,bN        
            
            where
            0=<r<=1,
            0=<g<=1,
            0=<b<=1
            
    opacity : float, default 1
                    0<=transparency <=1
    linewidth : float, default is 1
                    line thickness
                    
    
    Returns
    ----------
    vtkActor object
    
    Examples
    --------    
    >>> from dipy.viz import fos
    >>> r=fos.ren()    
    >>> lines=[np.random.rand(10,3),np.random.rand(20,3)]    
    >>> colors=np.random.rand(2,3)
    >>> c=fos.line(lines,colors)    
    >>> fos.add(r,c)
    >>> fos.show(r)
    '''    
    if not isinstance(lines,types.ListType):
        lines=[lines]    
        
    points= vtk.vtkPoints()
    lines_=vtk.vtkCellArray()
    linescalars=vtk.vtkFloatArray()
   
    #lookuptable=vtk.vtkLookupTable()
    lookuptable=_lookup(colors)

    scalarmin=0
    if colors.ndim==2:            
        scalarmax=colors.shape[0]-1
    if colors.ndim==1:        
        scalarmax=0
   
    curPointID=0
          
    m=(0.0,0.0,0.0)
    n=(1.0,0.0,0.0)
    
    scalar=0
    #many colors
    if colors.ndim==2:
        for Line in lines:
            
            inw=True
            mit=iter(Line)
            nit=iter(Line)
            nit.next()        
            
            while(inw):
                
                try:
                    m=mit.next() 
                    n=nit.next()
                    
                    #scalar=sp.rand(1)
                    
                    linescalars.SetNumberOfComponents(1)
                    points.InsertNextPoint(m)
                    linescalars.InsertNextTuple1(scalar)
                
                    points.InsertNextPoint(n)
                    linescalars.InsertNextTuple1(scalar)
                    
                    lines_.InsertNextCell(2)
                    lines_.InsertCellPoint(curPointID)
                    lines_.InsertCellPoint(curPointID+1)
                    
                    curPointID+=2
                except StopIteration:
                    break
             
            scalar+=1
    #one color only
    if colors.ndim==1:
        for Line in lines:
            
            inw=True
            mit=iter(Line)
            nit=iter(Line)
            nit.next()        
            
            while(inw):
                
                try:
                    m=mit.next() 
                    n=nit.next()
                    
                    #scalar=sp.rand(1)
                    
                    linescalars.SetNumberOfComponents(1)
                    points.InsertNextPoint(m)
                    linescalars.InsertNextTuple1(scalar)
                
                    points.InsertNextPoint(n)
                    linescalars.InsertNextTuple1(scalar)
                    
                    lines_.InsertNextCell(2)
                    lines_.InsertCellPoint(curPointID)
                    lines_.InsertCellPoint(curPointID+1)
                    
                    curPointID+=2
                except StopIteration:
                    break
             



    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines_)
    polydata.GetPointData().SetScalars(linescalars)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInput(polydata)
    mapper.SetLookupTable(lookuptable)
    
    mapper.SetColorModeToMapScalars()
    mapper.SetScalarRange(scalarmin,scalarmax)
    mapper.SetScalarModeToUsePointData()
    
    actor=vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetLineWidth(linewidth)
    actor.GetProperty().SetOpacity(opacity)
    
    return actor


def dots(points,color=(1,0,0),opacity=1):
    '''
    Create one or more 3d dots(points) returns one actor handling all the points
    '''

    if points.ndim==2:
        points_no=points.shape[0]
    else:
        points_no=1

    polyVertexPoints = vtk.vtkPoints()
    polyVertexPoints.SetNumberOfPoints(points_no)
    aPolyVertex = vtk.vtkPolyVertex()
    aPolyVertex.GetPointIds().SetNumberOfIds(points_no)

    cnt=0
    if points.ndim>1:
        for point in points:
            polyVertexPoints.InsertPoint(cnt, point[0], point[1], point[2])
            aPolyVertex.GetPointIds().SetId(cnt, cnt)
            cnt+=1
    else:
        polyVertexPoints.InsertPoint(cnt, points[0], points[1], points[2])
        aPolyVertex.GetPointIds().SetId(cnt, cnt)
        cnt+=1


    aPolyVertexGrid = vtk.vtkUnstructuredGrid()
    aPolyVertexGrid.Allocate(1, 1)
    aPolyVertexGrid.InsertNextCell(aPolyVertex.GetCellType(), aPolyVertex.GetPointIds())

    aPolyVertexGrid.SetPoints(polyVertexPoints)
    aPolyVertexMapper = vtk.vtkDataSetMapper()
    aPolyVertexMapper.SetInput(aPolyVertexGrid)
    aPolyVertexActor = vtk.vtkActor()
    aPolyVertexActor.SetMapper(aPolyVertexMapper)

    aPolyVertexActor.GetProperty().SetColor(color)
    aPolyVertexActor.GetProperty().SetOpacity(opacity)
    return aPolyVertexActor

def point_deprecated(points,colors,opacity=1):
    ''' Create 3d points and generate only one actor for all points. Similar with dots but here you can 
    color every point or class of points with a different color.
    '''
    #return dots(points,color=(1,0,0),opacity=1)
    
    if np.array(colors).ndim==1:
        return dots(points,colors,opacity)
    
    points_=vtk.vtkCellArray()
    pointscalars=vtk.vtkFloatArray()
   
    #lookuptable=vtk.vtkLookupTable()
    lookuptable=_lookup(colors)

    scalarmin=0
    if colors.ndim==2:            
        scalarmax=colors.shape[0]-1
    if colors.ndim==1:        
        scalarmax=0    


    if points.ndim==2:
        points_no=points.shape[0]
    else:
        points_no=1

    polyVertexPoints = vtk.vtkPoints()
    polyVertexPoints.SetNumberOfPoints(points_no)
    aPolyVertex = vtk.vtkPolyVertex()
    aPolyVertex.GetPointIds().SetNumberOfIds(points_no)

    cnt=0
    
    if points.ndim>1:
        for point in points:
            
            pointscalars.SetNumberOfComponents(1)                        
            polyVertexPoints.InsertPoint(cnt, point[0], point[1], point[2])
            pointscalars.InsertNextTuple1(cnt)
            aPolyVertex.GetPointIds().SetId(cnt, cnt)
            cnt+=1
            
    else:
        polyVertexPoints.InsertPoint(cnt, points[0], points[1], points[2])
        aPolyVertex.GetPointIds().SetId(cnt, cnt)
        cnt+=1
        

    aPolyVertexGrid = vtk.vtkUnstructuredGrid()
    aPolyVertexGrid.Allocate(1, 1)
    aPolyVertexGrid.InsertNextCell(aPolyVertex.GetCellType(), aPolyVertex.GetPointIds())
    

    aPolyVertexGrid.SetPoints(polyVertexPoints)
    aPolyVertexGrid.GetPointData().SetScalars(pointscalars)
    
    aPolyVertexMapper = vtk.vtkDataSetMapper()
    aPolyVertexMapper.SetInput(aPolyVertexGrid)
    aPolyVertexMapper.SetLookupTable(lookuptable)
    
    
    aPolyVertexMapper.SetColorModeToMapScalars()
    aPolyVertexMapper.SetScalarRange(scalarmin,scalarmax)
    aPolyVertexMapper.SetScalarModeToUsePointData()
    
    aPolyVertexActor = vtk.vtkActor()
    aPolyVertexActor.SetMapper(aPolyVertexMapper)

    #aPolyVertexActor.GetProperty().SetColor(color)
    aPolyVertexActor.GetProperty().SetOpacity(opacity)

    return aPolyVertexActor

def point(points,colors,opacity=1,point_radius=0.001):
    
    if np.array(colors).ndim==1:
        return dots(points,colors,opacity)
    
       
    scalars=vtk.vtkUnsignedCharArray()
    scalars.SetNumberOfComponents(3)
    
    pts=vtk.vtkPoints()
    cnt_colors=0
    
    for p in points:
        
        pts.InsertNextPoint(p[0],p[1],p[2])
        scalars.InsertNextTuple3(round(255*colors[cnt_colors][0]),round(255*colors[cnt_colors][1]),round(255*colors[cnt_colors][2]))
        #scalars.InsertNextTuple3(255,255,255)
        cnt_colors+=1
     
    '''   
    src = vtk.vtkDiskSource()
    src.SetRadialResolution(1)
    src.SetCircumferentialResolution(10)
    src.SetInnerRadius(0.0)
    src.SetOuterRadius(0.001)
    '''
    #src = vtk.vtkPointSource()
    src = vtk.vtkSphereSource()
    src.SetRadius(point_radius)
    src.SetThetaResolution(3)
    src.SetPhiResolution(3)
    
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(pts)
    polyData.GetPointData().SetScalars(scalars)

    glyph = vtk.vtkGlyph3D()
    glyph.SetSourceConnection(src.GetOutputPort())
    glyph.SetInput(polyData)
    glyph.SetColorModeToColorByScalar()
    glyph.SetScaleModeToDataScalingOff() 

    mapper=vtk.vtkPolyDataMapper()
    mapper.SetInput(glyph.GetOutput())    
    
    actor=vtk.vtkActor()
    actor.SetMapper(mapper)
            
    return actor
    

def sphere(position=(0,0,0),radius=0.5,thetares=8,phires=8,color=(0,0,1),opacity=1,tessel=0):
    ''' Create a sphere actor
    '''
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetLatLongTessellation(tessel)
   
    sphere.SetThetaResolution(thetares)
    sphere.SetPhiResolution(phires)
    
    spherem = vtk.vtkPolyDataMapper()
    spherem.SetInput(sphere.GetOutput())
    spherea = vtk.vtkActor()
    spherea.SetMapper(spherem)
    spherea.SetPosition(position)
    spherea.GetProperty().SetColor(color)
    spherea.GetProperty().SetOpacity(opacity)
        
    return spherea



def ellipsoid(R=np.array([[2, 0, 0],[0, 1, 0],[0, 0, 1] ]),position=(0,0,0),thetares=20,phires=20,color=(0,0,1),opacity=1,tessel=0):

    ''' Create a ellipsoid actor.    
    Stretch a unit sphere to make it an ellipsoid under a 3x3 translation matrix R 
    
    R=sp.array([[2, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1] ])
    '''
    
    Mat=sp.identity(4)
    Mat[0:3,0:3]=R
       
    '''
    Mat=sp.array([[2, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0,  1]  ])
    '''
    mat=vtk.vtkMatrix4x4()
    
    for i in sp.ndindex(4,4):
        
        mat.SetElement(i[0],i[1],Mat[i])
    
    radius=1
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetLatLongTessellation(tessel)
   
    sphere.SetThetaResolution(thetares)
    sphere.SetPhiResolution(phires)
    
    trans=vtk.vtkTransform()
    
    trans.Identity()
    #trans.Scale(0.3,0.9,0.2)
    trans.SetMatrix(mat)
    trans.Update()
    
    transf=vtk.vtkTransformPolyDataFilter()
    transf.SetTransform(trans)
    transf.SetInput(sphere.GetOutput())
    transf.Update()
    
    spherem = vtk.vtkPolyDataMapper()
    spherem.SetInput(transf.GetOutput())
    
    spherea = vtk.vtkActor()
    spherea.SetMapper(spherem)
    spherea.SetPosition(position)
    spherea.GetProperty().SetColor(color)
    spherea.GetProperty().SetOpacity(opacity)
    #spherea.GetProperty().SetRepresentationToWireframe()
    
    return spherea

    
def label(ren,text='Origin',pos=(0,0,0),scale=(0.2,0.2,0.2),color=(1,1,1)):
    
    ''' Create a label actor 
    This actor will always face the camera
    
    Parameters
    ----------
    ren : vtkRenderer() object as returned from ren()
    text : a text for the label
    pos : left down position of the label
    scale : change the size of the label 
    color : (r,g,b) and RGB tuple
    
    Returns
    ----------
    vtkActor object
    
    Examples
    --------  
    >>> from dipy.viz import fos  
    >>> r=fos.ren()    
    >>> l=fos.label(r)
    >>> fos.add(r,l)
    >>> fos.show(r)
    '''
    atext=vtk.vtkVectorText()
    atext.SetText(text)
    
    textm=vtk.vtkPolyDataMapper()
    textm.SetInput(atext.GetOutput())
    
    texta=vtk.vtkFollower()
    texta.SetMapper(textm)
    texta.SetScale(scale)    

    texta.GetProperty().SetColor(color)
    texta.SetPosition(pos)
    
    ren.AddActor(texta)
    texta.SetCamera(ren.GetActiveCamera())
        
    return texta

def volume(vol,voxsz=(1.0,1.0,1.0),affine=None,center_origin=1,info=1,maptype=0,trilinear=1,iso=0,iso_thr=100,opacitymap=None,colormap=None):    
    ''' Create a volume and return a volumetric actor using volumetric rendering. 
    This function has many different interesting capabilities. The maptype, opacitymap and colormap are the most crucial parameters here.
    
    Parameters:
    ----------------
    vol : array, shape (N, M, K), dtype uint8
         an array representing the volumetric dataset that we want to visualize using volumetric rendering            
        
    voxsz : sequence of 3 floats
            default (1., 1., 1.)
            
    affine : array, shape (4,4), default None
            as given by volumeimages             
            
    center_origin : int {0,1}, default 1
             it considers that the center of the volume is the 
            point (-vol.shape[0]/2.0+0.5,-vol.shape[1]/2.0+0.5,-vol.shape[2]/2.0+0.5)
            
    info : int {0,1}, default 1
            if 1 it prints out some info about the volume, the method and the dataset.
            
    trilinear: int {0,1}, default 1
            Use trilinear interpolation, default 1, gives smoother rendering. If you want faster interpolation use 0 (Nearest).
            
    maptype : int {0,1}, default 0,        
            The maptype is a very important parameter which affects the raycasting algorithm in use for the rendering. 
            The options are:
            If 0 then vtkVolumeTextureMapper2D is used.
            If 1 then vtkVolumeRayCastFunction is used.
            
    iso : int {0,1} default 0,
            If iso is 1 and maptype is 1 then  we use vtkVolumeRayCastIsosurfaceFunction which generates an isosurface at 
            the predefined iso_thr value. If iso is 0 and maptype is 1 vtkVolumeRayCastCompositeFunction is used.
            
    iso_thr : int, default 100,
            if iso is 1 then then this threshold in the volume defines the value which will be used to create the isosurface.
            
    opacitymap : array, shape (N,2), default None.
            The opacity map assigns a transparency coefficient to every point in the volume.
            The default value uses the histogram of the volume to calculate the opacitymap.
    colormap : array, shape (N,4), default None.
            The color map assigns a color value to every point in the volume.
            When None from the histogram it uses a red-blue colormap.
                
    Returns:
    ----------
    vtkVolume    
    
    Notes:
    --------
    What is the difference between TextureMapper2D and RayCastFunction? 
    Coming soon... See VTK user's guide [book] & The Visualization Toolkit [book] and VTK's online documentation & online docs.
    
    What is the difference between RayCastIsosurfaceFunction and RayCastCompositeFunction?
    Coming soon... See VTK user's guide [book] & The Visualization Toolkit [book] and VTK's online documentation & online docs.
    
    What about trilinear interpolation?
    Coming soon... well when time permits really ... :-)
    
    Examples:
    ------------
    First example random points    
    
    >>> from dipy.viz import fos
    >>> import numpy as np
    >>> vol=100*np.random.rand(100,100,100)
    >>> vol=vol.astype('uint8')
    >>> print vol.min(), vol.max()
    >>> r = fos.ren()
    >>> v = fos.volume(vol)
    >>> fos.add(r,v)
    >>> fos.show(r)
    
    Second example with a more complicated function
        
    >>> from dipy.viz import fos
    >>> import numpy as np
    >>> x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    >>> s = np.sin(x*y*z)/(x*y*z)
    >>> r = fos.ren()
    >>> v = fos.volume(s)
    >>> fos.add(r,v)
    >>> fos.show(r)
    
    If you find this function too complicated you can always use mayavi. 
    Please do not forget to use the -wthread switch in ipython if you are running mayavi.
    
    >>> from enthought.mayavi import mlab       
    >>> import numpy as np
    >>> x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
    >>> s = np.sin(x*y*z)/(x*y*z)
    >>> mlab.pipeline.volume(mlab.pipeline.scalar_field(s))
    >>> mlab.show()
    
    More mayavi demos are available here:
    
    http://code.enthought.com/projects/mayavi/docs/development/html/mayavi/mlab.html
    
    '''
    if vol.ndim!=3:    
        raise ValueError('3d numpy arrays only please')
    
    if info :
        print('Datatype',vol.dtype,'converted to uint8' )
    
    vol=np.interp(vol,[vol.min(),vol.max()],[0,255])
    vol=vol.astype('uint8')

    if opacitymap==None:
        
        bin,res=np.histogram(vol.ravel())
        res2=np.interp(res,[vol.min(),vol.max()],[0,1])
        opacitymap=np.vstack((res,res2)).T
        opacitymap=opacitymap.astype('float32')
                
        '''
        opacitymap=np.array([[ 0.0, 0.0],
                          [50.0, 0.9]])
        ''' 

    if info:
        print 'opacitymap', opacitymap
        
    if colormap==None:

        bin,res=np.histogram(vol.ravel())
        res2=np.interp(res,[vol.min(),vol.max()],[0,1])
        zer=np.zeros(res2.shape)
        colormap=np.vstack((res,res2,zer,res2[::-1])).T
        colormap=colormap.astype('float32')

        '''
        colormap=np.array([[0.0, 0.5, 0.0, 0.0],
                                        [64.0, 1.0, 0.5, 0.5],
                                        [128.0, 0.9, 0.2, 0.3],
                                        [196.0, 0.81, 0.27, 0.1],
                                        [255.0, 0.5, 0.5, 0.5]])
        '''

    if info:
        print 'colormap', colormap                        
    
    im = vtk.vtkImageData()
    im.SetScalarTypeToUnsignedChar()
    im.SetDimensions(vol.shape[0],vol.shape[1],vol.shape[2])
    #im.SetOrigin(0,0,0)
    #im.SetSpacing(voxsz[2],voxsz[0],voxsz[1])
    im.AllocateScalars()        
    
    for i in range(vol.shape[0]):
        for j in range(vol.shape[1]):
            for k in range(vol.shape[2]):
                
                im.SetScalarComponentFromFloat(i,j,k,0,vol[i,j,k])
    
    if affine != None:

        aff = vtk.vtkMatrix4x4()
        aff.DeepCopy((affine[0,0],affine[0,1],affine[0,2],affine[0,3],affine[1,0],affine[1,1],affine[1,2],affine[1,3],affine[2,0],affine[2,1],affine[2,2],affine[2,3],affine[3,0],affine[3,1],affine[3,2],affine[3,3]))
        #aff.DeepCopy((affine[0,0],affine[0,1],affine[0,2],0,affine[1,0],affine[1,1],affine[1,2],0,affine[2,0],affine[2,1],affine[2,2],0,affine[3,0],affine[3,1],affine[3,2],1))
        #aff.DeepCopy((affine[0,0],affine[0,1],affine[0,2],127.5,affine[1,0],affine[1,1],affine[1,2],-127.5,affine[2,0],affine[2,1],affine[2,2],-127.5,affine[3,0],affine[3,1],affine[3,2],1))
        
        reslice = vtk.vtkImageReslice()
        reslice.SetInput(im)
        #reslice.SetOutputDimensionality(2)
        #reslice.SetOutputOrigin(127,-145,147)    
        
        reslice.SetResliceAxes(aff)
        #reslice.SetOutputOrigin(-127,-127,-127)    
        #reslice.SetOutputExtent(-127,128,-127,128,-127,128)
        #reslice.SetResliceAxesOrigin(0,0,0)
        #print 'Get Reslice Axes Origin ', reslice.GetResliceAxesOrigin()
        #reslice.SetOutputSpacing(1.0,1.0,1.0)
        
        reslice.SetInterpolationModeToLinear()    
        #reslice.UpdateWholeExtent()
        
        #print 'reslice GetOutputOrigin', reslice.GetOutputOrigin()
        #print 'reslice GetOutputExtent',reslice.GetOutputExtent()
        #print 'reslice GetOutputSpacing',reslice.GetOutputSpacing()
    
        changeFilter=vtk.vtkImageChangeInformation() 
        changeFilter.SetInput(reslice.GetOutput())
        #changeFilter.SetInput(im)
        if center_origin:
            changeFilter.SetOutputOrigin(-vol.shape[0]/2.0+0.5,-vol.shape[1]/2.0+0.5,-vol.shape[2]/2.0+0.5)
            print 'ChangeFilter ', changeFilter.GetOutputOrigin()
        
    opacity = vtk.vtkPiecewiseFunction()
    for i in range(opacitymap.shape[0]):
        opacity.AddPoint(opacitymap[i,0],opacitymap[i,1])

    color = vtk.vtkColorTransferFunction()
    for i in range(colormap.shape[0]):
        color.AddRGBPoint(colormap[i,0],colormap[i,1],colormap[i,2],colormap[i,3])
        
    if(maptype==0): 
    
        property = vtk.vtkVolumeProperty()
        property.SetColor(color)
        property.SetScalarOpacity(opacity)
        
        if trilinear:
            property.SetInterpolationTypeToLinear()
        else:
            prop.SetInterpolationTypeToNearest()
            
        if info:
            print('mapper VolumeTextureMapper2D')
        mapper = vtk.vtkVolumeTextureMapper2D()
        if affine == None:
            mapper.SetInput(im)
        else:
            #mapper.SetInput(reslice.GetOutput())
            mapper.SetInput(changeFilter.GetOutput())
        
    
    if (maptype==1):

        property = vtk.vtkVolumeProperty()
        property.SetColor(color)
        property.SetScalarOpacity(opacity)
        property.ShadeOn()
        if trilinear:
            property.SetInterpolationTypeToLinear()
        else:
            prop.SetInterpolationTypeToNearest()

        if iso:
            isofunc=vtk.vtkVolumeRayCastIsosurfaceFunction()
            isofunc.SetIsoValue(iso_thr)
        else:
            compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
        
        if info:
            print('mapper VolumeRayCastMapper')
            
        mapper = vtk.vtkVolumeRayCastMapper()
        if iso:
            mapper.SetVolumeRayCastFunction(isofunc)
            if info:
                print('Isosurface')
        else:
            mapper.SetVolumeRayCastFunction(compositeFunction)   
            
            #mapper.SetMinimumImageSampleDistance(0.2)
            if info:
                print('Composite')
             
        if affine == None:
            mapper.SetInput(im)
        else:
            #mapper.SetInput(reslice.GetOutput())    
            mapper.SetInput(changeFilter.GetOutput())
            #Return mid position in world space    
            #im2=reslice.GetOutput()
            #index=im2.FindPoint(vol.shape[0]/2.0,vol.shape[1]/2.0,vol.shape[2]/2.0)
            #print 'Image Getpoint ' , im2.GetPoint(index)
           
        
    volum = vtk.vtkVolume()
    volum.SetMapper(mapper)
    volum.SetProperty(property)

    if info :  
         
        print 'Origin',   volum.GetOrigin()
        print 'Orientation',   volum.GetOrientation()
        print 'OrientationW',    volum.GetOrientationWXYZ()
        print 'Position',    volum.GetPosition()
        print 'Center',    volum.GetCenter()  
        print 'Get XRange', volum.GetXRange()
        print 'Get YRange', volum.GetYRange()
        print 'Get ZRange', volum.GetZRange()  
        print 'Volume data type', vol.dtype
        
    return volum

def contour(vol,voxsz=(1.0,1.0,1.0),affine=None,levels=[50],colors=[np.array([1.0,0.0,0.0])],opacities=[0.5]):
    ''' Take a volume and draw surface contours for any any number of thresholds (levels) where every contour has its own
    color and opacity
    
    Parameters:
    ----------------
    vol : array, shape (N, M, K)
        an array representing the volumetric dataset for which we will draw some beautiful contours .         
    
    voxsz : sequence of 3 floats
        default (1., 1., 1.)
        
    affine : not used here
    
    levels : sequence of thresholds for the contours taken from image values
                needs to be same datatype as vol    
    colors : array, shape (N,3) with the rgb values in where r,g,b belong to [0,1]
    
    opacities : sequence of floats [0,1]
            
        
    Returns:
    -----------
    ass: assembly of actors
            representing the contour surfaces
            
    Examples:
    -------------
    >>> import numpy as np
    >>> from dipy.viz import fos
    >>> A=np.zeros((10,10,10))
    >>> A[3:-3,3:-3,3:-3]=1
    >>> r=fos.ren()
    >>> fos.add(r,fos.contour(A,levels=[1]))
    >>> fos.show(r)
    
    '''
    
    im = vtk.vtkImageData()
    im.SetScalarTypeToUnsignedChar()
    im.SetDimensions(vol.shape[0],vol.shape[1],vol.shape[2])
    #im.SetOrigin(0,0,0)
    #im.SetSpacing(voxsz[2],voxsz[0],voxsz[1])
    im.AllocateScalars()        
    
    for i in range(vol.shape[0]):
        for j in range(vol.shape[1]):
            for k in range(vol.shape[2]):
                
                im.SetScalarComponentFromFloat(i,j,k,0,vol[i,j,k])
    
    ass=vtk.vtkAssembly()
    #ass=[]
    
    for (i,l) in enumerate(levels):
        
        #print levels
        skinExtractor = vtk.vtkContourFilter()        
        skinExtractor.SetInput(im)
        skinExtractor.SetValue(0, l)
        
        skinNormals = vtk.vtkPolyDataNormals()
        skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
        skinNormals.SetFeatureAngle(60.0)
        
        skinMapper = vtk.vtkPolyDataMapper()
        skinMapper.SetInputConnection(skinNormals.GetOutputPort())
        skinMapper.ScalarVisibilityOff()
        
        skin = vtk.vtkActor()
        
        skin.SetMapper(skinMapper)
        skin.GetProperty().SetOpacity(opacities[i])
        
        print colors[i]
        skin.GetProperty().SetColor(colors[i][0],colors[i][1],colors[i][2])
        #skin.Update()
        
        ass.AddPart(skin)    
        
        del skin
        del skinMapper
        del skinExtractor
        #ass=ass+[skin]
    
    return ass

    

def _cm2colors(colormap='Blues'):
    '''
    Colormaps from matplotlib 
    ['Spectral', 'summer', 'RdBu', 'gist_earth', 'Set1', 'Set2', 'Set3', 'Dark2', 
    'hot', 'PuOr_r', 'PuBuGn_r', 'RdPu', 'gist_ncar_r', 'gist_yarg_r', 'Dark2_r', 
    'YlGnBu', 'RdYlBu', 'hot_r', 'gist_rainbow_r', 'gist_stern', 'cool_r', 'cool', 
    'gray', 'copper_r', 'Greens_r', 'GnBu', 'gist_ncar', 'spring_r', 'gist_rainbow', 
    'RdYlBu_r', 'gist_heat_r', 'OrRd_r', 'bone', 'gist_stern_r', 'RdYlGn', 'Pastel2_r', 
    'spring', 'Accent', 'YlOrRd_r', 'Set2_r', 'PuBu', 'RdGy_r', 'spectral', 'flag_r', 'jet_r', 
    'RdPu_r', 'gist_yarg', 'BuGn', 'Paired_r', 'hsv_r', 'YlOrRd', 'Greens', 'PRGn', 
    'gist_heat', 'spectral_r', 'Paired', 'hsv', 'Oranges_r', 'prism_r', 'Pastel2', 'Pastel1_r',
     'Pastel1', 'gray_r', 'PuRd_r', 'Spectral_r', 'BuGn_r', 'YlGnBu_r', 'copper', 
    'gist_earth_r', 'Set3_r', 'OrRd', 'PuBu_r', 'winter_r', 'jet', 'bone_r', 'BuPu', 
    'Oranges', 'RdYlGn_r', 'PiYG', 'YlGn', 'binary_r', 'gist_gray_r', 'BuPu_r', 
    'gist_gray', 'flag', 'RdBu_r', 'BrBG', 'Reds', 'summer_r', 'GnBu_r', 'BrBG_r', 
    'Reds_r', 'RdGy', 'PuRd', 'Accent_r', 'Blues', 'Greys', 'autumn', 'PRGn_r', 'Greys_r', 
    'pink', 'binary', 'winter', 'pink_r', 'prism', 'YlOrBr', 'Purples_r', 'PiYG_r', 'YlGn_r', 
    'Blues_r', 'YlOrBr_r', 'Purples', 'autumn_r', 'Set1_r', 'PuOr', 'PuBuGn']
    
    '''
    try:
        from pylab import cm
    except ImportError:
        ImportError('pylab is not installed')
    
    blue=cm.datad[colormap]['blue']
    blue1=[b[0] for b in blue]
    blue2=[b[1] for b in blue]
    
    red=cm.datad[colormap]['red']
    red1=[b[0] for b in red]
    red2=[b[1] for b in red]
        
    green=cm.datad[colormap]['green']
    green1=[b[0] for b in green]
    green2=[b[1] for b in green]
            
    return red1,red2,green1,green2,blue1,blue2
    
def colors(v,colormap):

    ''' Create colors from a specific colormap and return it 
    as an array of shape (N,3) where every row gives the corresponding
    r,g,b value. The colormaps we use are similar with that of pylab.
    
    Notes :
    -------
    If you want to add more colormaps here is what you could do. Go to
    this website http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps
    see which colormap you need and then get in pylab using the cm.datad 
    dictionary.

    e.g. cm.datad['jet']

          {'blue': ((0.0, 0.5, 0.5),
                    (0.11, 1, 1),
                    (0.34000000000000002, 1, 1),
                    (0.65000000000000002, 0, 0),
                    (1, 0, 0)),
           'green': ((0.0, 0, 0),
                    (0.125, 0, 0),
                    (0.375, 1, 1),
                    (0.64000000000000001, 1, 1),
                    (0.91000000000000003, 0, 0),
                    (1, 0, 0)),
           'red': ((0.0, 0, 0),
                   (0.34999999999999998, 0, 0),
                   (0.66000000000000003, 1, 1),
                   (0.89000000000000001, 1, 1),
                   (1, 0.5, 0.5))}

    '''
    if v.ndim>1:
        ValueError('This function works only with 1d arrays. Use ravel()')

    v=np.interp(v,[v.min(),v.max()],[0,1])
    

    if colormap=='jet':
        print 'jet'
        
        red=np.interp(v,[0,0.35,0.66,0.89,1],[0,0,1,1,0.5])
        green=np.interp(v,[0,0.125,0.375,0.64,0.91,1],[0,0,1,1,0,0])
        blue=np.interp(v,[0,0.11,0.34,0.65,1],[0.5,1,1,0,0])
    
    if colormap=='blues':
        #cm.datad['Blues']
        print 'blues'

        red=np.interp(v,[0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0],[0.96862745285,0.870588243008,0.776470601559,0.61960786581,0.419607847929,0.258823543787,0.129411771894,0.0313725508749,0.0313725508749])
        green=np.interp(v,[0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0],[0.984313726425,0.921568632126,0.858823537827,0.792156875134,0.68235296011,0.572549045086,0.443137258291,0.317647069693,0.188235297799])
        blue=np.interp(v,[0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0] , [1.0,0.96862745285,0.937254905701,0.882352948189,0.839215695858,0.776470601559,0.709803938866,0.611764729023,0.419607847929])   
        
    if colormap=='blue_red':
        print 'blue_red'
        #red=np.interp(v,[],[])
        
        red=np.interp(v,[0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0],[0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0])        
        green=np.zeros(red.shape)
        blue=np.interp(v,[0.0,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1.0],[1.0,0.875,0.75,0.625,0.5,0.375,0.25,0.125,0.0])
        
        blue=green

    if colormap=='accent':
        print 'accent'
        red=np.interp(v,[0.0,  0.14285714285714285,  0.2857142857142857,  0.42857142857142855,  0.5714285714285714,  0.7142857142857143,  0.8571428571428571,1.0],
            [0.49803921580314636, 0.7450980544090271, 0.99215686321258545, 1.0, 0.21960784494876862, 0.94117647409439087, 0.74901962280273438, 0.40000000596046448])
        green=np.interp(v,[0.0,  0.14285714285714285,  0.2857142857142857,  0.42857142857142855,  0.5714285714285714,  0.7142857142857143,  0.8571428571428571,  1.0],
            [0.78823530673980713, 0.68235296010971069, 0.75294119119644165,1.0, 0.42352941632270813, 0.0078431377187371254, 0.35686275362968445, 0.40000000596046448]) 
        blue=np.interp(v,[0.0, 0.14285714285714285,  0.2857142857142857, 0.42857142857142855, 0.5714285714285714, 0.7142857142857143, 0.8571428571428571,  1.0],
            [0.49803921580314636,  0.83137255907058716,  0.52549022436141968,  0.60000002384185791,  0.69019609689712524,  0.49803921580314636,  0.090196080505847931,  0.40000000596046448])
            
        
        
    return np.vstack((red,green,blue)).T

def _closest_track(p,tracks):
    ''' Return the index of the closest track from tracks to point p
    '''

    d=[]
    #enumt= enumerate(tracks)
    
    for (ind,t) in enumerate(tracks):
        for i in range(len(t[:-1])):
            
            d.append((ind, np.sqrt(np.sum(np.cross((p-t[i]),(p-t[i+1]))**2))/np.sqrt(np.sum((t[i+1]-t[i])**2))))
        
    d=np.array(d)
    
    imin=d[:,1].argmin()
    
    return int(d[imin,0])
    

def annotatePick(object, event):
    ''' Create a Python function to create the text for the 
    text mapper used to display the results of picking.
    '''
    global picker, textActor, textMapper,track_buffer
    
    if picker.GetCellId() < 0:
        textActor.VisibilityOff()
    else:
        if len(track_buffer)!=0:
            
            selPt = picker.GetSelectionPoint()
            pickPos = picker.GetPickPosition()
            
            closest=_closest_track(np.array([pickPos[0],pickPos[1],pickPos[2]]),track_buffer)
            
            textMapper.SetInput("(%.6f, %.6f, %.6f)"%pickPos)
            textActor.SetPosition(selPt[:2])
            textActor.VisibilityOn()            
            
            label(tmp_ren,text=str(ind_buffer[closest]),pos=(track_buffer[closest][0][0],track_buffer[closest][0][1],track_buffer[closest][0][2]))
            
            tmp_ren.AddActor(line(track_buffer[closest],golden,opacity=1))

def show(ren,title='Fos',size=(300,300),track_bf=None,ind_bf=None,color_bf=None):
    ''' Show window 
    
    Parameters
    ----------
    ren : vtkRenderer() object 
            as returned from function ren()
    title : string 
            a string for the window title bar
    size : (int, int) 
            (width,height) of the window
    track_bf : sequence (default None)
                tracklist 
    color_bf : array, shape (N,3) where N =len(track_bf), default None
                a color for every track
    
    Examples
    --------    
    >>> from dipy.viz import fos
    >>> r=fos.ren()    
    >>> lines=[np.random.rand(10,3),np.random.rand(20,3)]    
    >>> colors=[0.2,0.8]
    >>> c=fos.line(lines,colors)    
    >>> fos.add(r,c)
    >>> l=fos.label(r)
    >>> fos.add(r,l)
    >>> fos.show(r)
    '''
    global track_buffer,tmp_ren,ind_buffer
    
    #if a list of tracks is available for picking show the tracks with red
    if track_bf!=None:
        track_buffer=track_bf
        ind_buffer=ind_bf
        
        if color_bf==None:
            ren.AddActor(line(track_buffer,red,opacity=1))
        else:
            ren.AddActor(line(track_buffer,color_bf,opacity=1))
        tmp_ren=ren

    picker.AddObserver("EndPickEvent", annotatePick)
    
    ren.AddActor2D(textActor)
    
    ren.ResetCamera()        
    window = vtk.vtkRenderWindow()
    window.AddRenderer(ren)
    window.SetWindowName(title) 
    window.SetSize(size)
    style=vtk.vtkInteractorStyleTrackballCamera()        
    iren = vtk.vtkRenderWindowInteractor()    
    iren.SetRenderWindow(window)
    iren.SetPicker(picker)
    

    
    iren.SetInteractorStyle(style)
    iren.Initialize()
    picker.Pick(85, 126, 0, ren)    
    window.Render()
    iren.Start()
    
    
if __name__ == "__main__":
    
    pass
    