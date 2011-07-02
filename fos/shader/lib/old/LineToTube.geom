#version 120 
#extension GL_EXT_geometry_shader4 : enable

void main(void)
{

    const int resolution = 5; // five points
    const float radius = 30.0; // generic radius, later uniform
    int i;

    vec4 startp[resolution];
    vec4 endp[resolution];

    // normalize vector, "z-direction"
    vec3 dir = normalize(gl_PositionIn[1] - gl_PositionIn[0]).xyz;
    
    // find perpendicular vector (to x-axis and direction)
    vec3 axis = vec3(1.0, 0, 0);

    vec3 cross; // "x-direction"
    cross.x = dir.y*axis.z - dir.z*axis.y;
    cross.y = dir.z*axis.x - dir.x*axis.z;
    cross.z = dir.x*axis.y - dir.y*axis.x;

    vec3 cross2; // "y-direction"
    cross2.x = dir.y*cross.z - dir.z*cross.y;
    cross2.y = dir.z*cross.x - dir.x*cross.z;
    cross2.z = dir.x*cross.y - dir.y*cross.x;


    // new vertex positions using resolution and radius
    const float angle = (2*3.141592)/resolution;
    float startangle = 0.0;

    vec4 pos1 = gl_PositionIn[0];
    vec4 pos2 = gl_PositionIn[1];

    float cosa;
    float sina;

    for(i = 0; i < resolution; i++) {
        cosa = cos(startangle);
        sina = sin(startangle);

        startp[i] = vec4( pos1.x + cosa * radius * cross.x,
                          pos1.y + sina * radius * cross.y,
                          pos1.z,
                          pos1.w);

        endp[i] = vec4(   pos2.x + cosa * radius * cross.x,
                          pos2.y + sina * radius * cross.y,
                          pos2.z,
                          pos2.w);

        startangle += angle;

    }

    // emit vertices with GL_TRIANGLE_STRIP
    for(i = 0; i < 4; i++ ) {
        gl_Position = endp[i+0];
        EmitVertex();
        gl_Position = startp[i+0];
        EmitVertex();
        gl_Position = startp[i+1];
        EmitVertex();

        EndPrimitive();

        gl_Position = endp[i+0];
        EmitVertex();
        gl_Position = startp[i+1];
        EmitVertex();
        gl_Position = endp[i+1];
        EmitVertex();

        EndPrimitive();
    }

}
