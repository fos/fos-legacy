#version 120 
#extension GL_EXT_geometry_shader4 : enable

void main(void)
{

    const vec3 trans = vec3(1, 0, 0);
    vec4 pos1 = gl_PositionIn[0];
    vec4 pos2 = gl_PositionIn[1];
    gl_Position = pos1;
    EmitVertex();

    gl_Position = pos2;
    EmitVertex();        
    
    float width = 0.5;
    
    vec3 perpen = normalize(gl_PositionIn[1] - gl_PositionIn[0]).xyz;
    // x --> x, y --> -y
    perpen = vec3(perpen.x, -perpen.y, perpen.z);
    
    // XXX: move one vertex
    //gl_Position = gl_PositionIn[1];
    //gl_Position.xyz = gl_PositionIn[1].xyz + width * perpen;    
    
    //gl_Position = pos1;
    //gl_Position.xyz += trans;
    //gl_Position = gl_ProjectionMatrix  * gl_Position;

    gl_Position = gl_PositionIn[0];
    gl_Position.xyz += width * perpen;
    
    EmitVertex();
    
    EndPrimitive();

    //gl_Position = pos2; //vec4(-100,0,0, 1.0);
    //gl_Position.xyz += trans;
    //gl_Position = gl_ProjectionMatrix  * gl_Position;
    //EmitVertex();

    gl_Position = gl_PositionIn[0];
    gl_Position.xyz += width * perpen;
    EmitVertex();

    gl_Position = gl_PositionIn[1];
    EmitVertex();
    
    gl_Position = gl_PositionIn[1];
    gl_Position.xyz += width * perpen;
    EmitVertex();
    EndPrimitive();

    
}
