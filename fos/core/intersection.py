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


    