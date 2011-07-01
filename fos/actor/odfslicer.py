import numpy as np

class ODF_Slice(object):

    def __init__(self,odfs,vertices,faces,noiso,batch,group=None):

        J=0

        self.odfs_no=J
        self.vertex_list=(odfs.shape[0]*odfs.shape[1])*[None]
        
        for index in np.ndindex(odfs.shape[:2]):

            values=odfs[index]
            if noiso:
                values=np.interp(values,[values.min(),values.max()],[0,.5])
                
            inds=faces.ravel().tolist()
            shift=index+(0,)

            print J,odfs.shape[0]*odfs.shape[1]            
            points=np.dot(np.diag(values),vertices)
            
            points=points+np.array(shift)            
            verx=points.ravel().tolist()

            normals=np.zeros((len(vertices),3))        
            ones_=np.ones(len(values))
            colors=np.vstack((values,ones_,ones_)).T
            colors=colors.ravel().tolist()
        
            p=vertices
            l=faces
            
            trinormals=np.cross(p[l[:,0]]-p[l[:,1]],\
                                p[l[:,1]]-p[l[:,2]],\
                                axisa=1,axisb=1)
        
            for (i,lp) in enumerate(faces):
                normals[lp]+=trinormals[i]
                div=np.sqrt(np.sum(normals**2,axis=1))     
                div=div.reshape(len(div),1)
                normals=(normals/div)
                norms=np.array(normals).ravel().tolist()
        
            self.vertex_list[i] = batch.add_indexed(len(vertices),\
                                                 GL_TRIANGLES,\
                                                 group,\
                                                 inds,\
                                                 ('v3d/static',verx),\
                                                 ('n3d/static',norms),\
                                                 ('c3d/static',colors))

            J+=1
            
    def update(self):
        pass
    
    def delete(self):
        for i in range(self.odfs_no):
            self.vertex_list.delete()
