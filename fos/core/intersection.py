import numpy as np

def intersect_ray_sphere(p, d, sphereR, sphereC):
    """ Intersects ray r = p + td, |d| = 1, with sphere s
    
    Parameters
    ----------
    p : (3,1)
        starting point of ray
    d : (3,1)
        normalized direction vector of ray
    sphereR : float
        sphere radius
    sphereC : (3,1)
        sphere center coordinates
    
    Returns
    -------
    If intersects
    t : float
        value of intersection
    q : (3,1)
        intersection point
    If not intersect, returns (None, None)
    """
    m = p - sphereC
    b = np.dot(m, d)
    c = np.dot(m, m) - sphereR * sphereR
    # exit if sphreR's origin outside of s (c > 0)
    # and sphereR pionting away from s (b<0)
    if c > 0.0 and b > 0.0:
        return (None, None)
    discr = b * b - c
    # A negative discriminant corresponds to ray missing sphere
    if (discr < 0.0):
        return (None, None)
    # ray now found to intersect sphere, compute smallest t value of intersection
    t = -b - np.sqrt(discr)
    # if t is negative, ray started inside sphere, so clamp t to zero
    if t < 0.0:
            t = 0.0
    q = p + t * d
    return (t, q)

def point_inside_volume(p, ab1, ab2, eps = 0.01):
    """
    Check if point p is inside the aabb volume
    """
    ab1 = ab1.copy() - eps
    ab2 = ab2.copy() + eps
    if ab1[0] <= p[0] <= ab2[0] and \
        ab1[1] <= p[1] <= ab2[1] and \
        ab1[2] <= p[2] <= ab2[2]:
        return True
    else:
        return False


def ray_aabb_intersection(p0, p1, ab1, ab2):
    # http://www.cs.princeton.edu/courses/archive/fall00/cs426/lectures/raycast/sld017.htm
    # faces are interpreted as planes, need
    # first test segment intersection to confine to bounding box volume

    v = (p1-p0) / np.linalg.norm( (p1-p0) )
    # ray: p = p0 + t * v
    # plane: p * n + d = 0

    # create the face planes
    # because they are axis aligned, to define n is easy
    xn = -np.array( [1,0,0], dtype = np.float32 )
    yn = -np.array( [0,1,0], dtype = np.float32 )
    zn = -np.array( [0,0,1], dtype = np.float32 )
    norm_vect = (xn, yn, zn)
    ret = []
    for n in norm_vect:
        for d in (ab1, ab2):

            di = np.dot(v,n)
            if di == 0.0:
                continue
                
            t = -( np.dot(p0, n) + d ) / di
            pout = p0 + t * v

            if point_inside_volume(pout, ab1, ab2):
                ret.append(pout)

    return ret


def ray_triangle_intersection(p, d, v0, v1, v2):
    """ Implemented from http://www.lighthouse3d.com/tutorials/maths/ray-triangle-intersection/
    """
    e1 = v1 - v0
    e2 = v2 - v0
    h = np.cross(d, e2)
    a = np.dot(e1, h)
    if a > -0.00001 and a < 0.00001:
		return False

    f = 1 / a
    s = p - v0
    u = f * np.dot(s, h)

    if u < 0.0 or u > 1.0:
        return False

    q = np.cross(s, e1)
    v = f * np.dot(d, q)

    if v < 0.0 or u + v > 1.0:
        return False

    # at this stage we can compute t to find out where
    # the intersection point is on the lin
    t = f * np.dot(e2, q)

    if t > 0.00001: # ray intersection
        # return (t, u, v)
        return p + t * d
    else: # this means that there is a line intersection
        return False # but not a ray intersection


def test_segment_aabb(p0, p1, aabb_c1, aabb_c2):
    """ Test if segement specified by points p0 and p1
    intersects aabb """
    aabbc1 = np.array(aabb_c1)
    aabbc2 = np.array(aabb_c2)
    p0 = np.array(p0)
    p1 = np.array(p1)
    c = (aabbc1 + aabbc2) * 0.5 # box center-point
    e = aabbc2 - c # box halflength extents
    m = (p0 + p1) * 0.5 # segment midpoint
    d = p1 - m # segment halflength
    m = m -c # translate box and segment to origin
    # try world coordinate axes as separating axes
    adx = np.abs(d[0])
    if np.abs(m[0]) > e[0] + adx:
        return False
    ady = np.abs(d[1])
    if np.abs(m[1]) > e[1] + ady:
        return False
    adz = np.abs(d[2])
    if np.abs(m[2]) > e[2] + adz:
        return False
    
    # add in an epsilon term to counteract arithmetic errors when segment
    # is (near) parallel to a coordinate axis
    eps = 0.001
    adx += eps; ady += eps; adz += eps

    # try cross products of segment direction vector with coordinate axes
    if np.abs(m[1] * d[2] - m[2] * d[1]) > e[1] * adz + e[2] * ady:
        return False
    if np.abs(m[2] * d[0] - m[0] * d[2]) > e[0] * adz + e[2] * adx:
        return False
    if np.abs(m[0] * d[1] - m[1] * d[0]) > e[0] * ady + e[2] * adx:
        return False
    
    # no separating axis found: segment must be overlapping aabb
    return True


if __name__ == '__main__':
    p0 = np.array([2,2,4])
    p1 = np.array([2,2,-2])
    ab1 = np.array([0,0,2])
    ab2 = np.array([5,5,-1])
    ray_aabb_intersection(p0, p1, ab1, ab2)