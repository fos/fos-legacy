def subdict(aabb, depth):
    if depth == 0:
        return {'leaf':True}
    
    # divide
    xcut = (aabb[0][0] + aabb[1][0]) / 2.
    ycut = (aabb[0][1] + aabb[1][1]) / 2.
    zcut = (aabb[0][2] + aabb[1][2]) / 2.
    print "cuts", xcut, ycut, zcut
    
    # generate oct-tree keys
    # x,y,z directions, right-handed system
    a = aaa = aabb[0]
    s = sss = (xcut, ycut, zcut)
    d = ddd = aabb[1]
    saa = (s[0],a[1],a[2])
    dss = (d[0],s[1],s[2])
    asa = (a[0],s[1],a[2])
    sds = (s[0],d[1],s[2])
    ssa = (s[0],s[1],a[2])
    dds = (d[0],d[1],s[2])
    aas = (a[0],a[1],s[2])
    ssd = (s[0],s[1],d[2])
    sas = (s[0],a[1],s[2])
    dsd = (d[0],s[1],d[2])
    ass = (a[0],s[1],s[2])
    sdd = (s[0],d[1],d[2])
    b0 = (aaa, sss)
    b1 = (saa, dss)
    b2 = (asa, sds)
    b3 = (ssa, dds)
    u0 = (aas, ssd)
    u1 = (sas, dsd)
    u2 = (ass, sdd)
    u3 = (sss, ddd)
    
    oct = [b0,b1,b2,b3,u0,u1,u2,u3]
    
    retdict = dict.fromkeys(oct)
    
    # for each item, call subdict
    for k,v in retdict.iteritems():
        retdict[k] = subdict(k, depth - 1)
    
    return retdict

def addvertex(ds, xyz, idx):
    # traverse until corresponding dictionary is found
    if ds.has_key('leaf'):
        if ds['leaf']:
            if ds.has_key('list'):
                ds['list'].append(idx)
            else:
                ds['list'] = [idx]
        print "vertex added", idx
    else:
        # traverse
        for k,boxdict in ds.iteritems():
            # check if vertex falls inside it
            if k[0][0] <= xyz[0] and xyz[0] <= k[1][0] and \
               k[0][1] <= xyz[1] and xyz[1] <= k[1][1] and \
               k[0][2] <= xyz[2] and xyz[2] <= k[1][2]:
                addvertex(boxdict, xyz, idx)
            
def generate(vert, depth):
    ds = {}
    # compute aabb
    aabb = (tuple(vert.min(axis=0)), 
            tuple(vert.max(axis=0)))
    print "aabb:", aabb
    
    ds = subdict(aabb, depth)

    # attach vertex indices to spatial ds
    for i in range(len(vert)):
        print "i...", i
        addvertex(ds, vert[i], i)
        
    return ds
        
def query(ds, xyz):
    if ds.has_key('leaf'):
        print "query: in leaf", ds
        if ds['leaf']:
            if ds.has_key('list'):
                return ds['list']
            else:
                print "found an empty leaf. not so good!"
                return []
    else:
        for k,boxdict in ds.iteritems():
            # check if vertex falls inside it
            if k[0][0] <= xyz[0] and xyz[0] <= k[1][0] and \
               k[0][1] <= xyz[1] and xyz[1] <= k[1][1] and \
               k[0][2] <= xyz[2] and xyz[2] <= k[1][2]:
                print "query along path...", k
                return query(boxdict, xyz)        
        return []
    
if __name__ == '__main__':
    import numpy as np
    vert=np.array([[.5,.5,.5],[1,1,1], [.6,.5,.6]])
    spds = generate(vert, depth=1)
    print query(spds, (.5,.5,.5))
    