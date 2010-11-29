import networkx as nx
from time import time
import numpy as np

def mesh2graph(faces):
    """ Converts a triangular mesh to a graph only taking
    the connectivity into account """
    g = nx.Graph()
    for i in range(len(faces)):
        g.add_edge(faces[i,0], faces[i,1])
        g.add_edge(faces[i,1], faces[i,2])
    return g

def graphlaplacian(g):
    
    import scipy.sparse as sp
    # scipy.sparse.linalg.eigen
    n = g.order()
    D = sp.identity(n)
    A = nx.to_scipy_sparse_matrix(g)
    di = A.sum(axis=1).T.tolist()[0]
    
    D.setdiag(di)
    L = D - A
    return L

def grapheigendecomposition(graphlaplacian, k = 3):
    """ k is the number of eigenvalues desired
    
    See http://docs.scipy.org/doc/scipy/reference/sparse.linalg.html
    """
    from scipy.sparse.linalg.eigen import lobpcg
    guess = np.random.rand(graphlaplacian.shape[0],k) * 100
    return lobpcg(graphlaplacian, guess)

if __name__ == '__main__':
    
    
    faces = np.array([ [0,1,2],
                       [1,2,3]], dtype = np.uint)
    
    start = time()
    import nibabel.gifti as gi
    a=gi.read('/home/stephan/Dev/PyWorkspace/connectomeviewer/cviewer/resources/atlases/template_atlas_homo_sapiens_01/Gifti/fsaverage.gii')
    faces = a.darrays[1].data[:100,:]
    print "Loading took ", time()-start
    
    g = mesh2graph(faces)
    print "Making graph ", time()-start

    gl = graphlaplacian(g)
    print "Getting laplacian ", time()-start

    w,v = grapheigendecomposition(gl, k = 3)
    # Ev, Evect = eig(gl)
    print w
    print "Getting eigendecomposition ", time()-start
    from scipy.linalg import eig, eigh
    Ev, Evect = eigh(gl.todense())
    print Ev
    #print np.real(Ev)
    
