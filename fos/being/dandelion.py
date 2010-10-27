

class Dandelion(object):
    def __init__(self,signals,directions,batch,group=None):

        ''' Visualize the diffusion signal as a dandelion i.e. 
        multiply the signal for each corresponding gradient direction

        Red denotes the maximum signal
        Blue the minimum signal

        Examples
        --------
        >>> from .curve import SmoothLineGroup
        >>> signals=data[48,48,28]
        >>> slg=SmoothLineGroup()
        >>> actors.append(Dandelion(signals,gradients,batch=batch,group=slg))
        >>> Machine().run()
        
        '''
        directions=np.dot(np.diag(signals),directions)
        vertices=np.zeros((len(directions)*2,3))
        vertices[::2]=directions
        vertices[1:len(vertices):2]=-directions                
        verx=vertices.ravel().tolist()        
        colors=np.ones((len(vertices),4)) #np.random.rand(len(vertices),3)
        #colors[:len(vertices)/2,1]=np.interp(signals,[signals.min(),signals.max()],[0,1])
        #colors[len(vertices)/2:,1]=colors[:len(vertices)/2,1]
        #colors[:,0]=0
        #colors[:,2]=0
        mxs=np.argmax(signals)
        mns=np.argmin(signals)

        colors[mxs*2]=np.array([1,0,0,1])
        colors[mns*2]=np.array([0,0,1,1])
        
        cols=colors.ravel().tolist()                
        self.vertex_list = batch.add(len(vertices),GL_LINES,group,\
                                         ('v3d/static',verx),\
                                         ('c4d/static',cols))
    
    def update(self):
        pass
    
    def delete(self):
        self.vertex_list.delete()
