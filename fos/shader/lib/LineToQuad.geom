#version 120 
#extension GL_EXT_geometry_shader4 : enable

void main(void)
{

    gl_Position = gl_PositionIn[0];
    EmitVertex();

    gl_Position = gl_PositionIn[1];
    EmitVertex();        
    
    float width = 50.0;
    
    vec3 perpen = normalize(gl_PositionIn[1] - gl_PositionIn[0]).yxz;
    
    // XXX: move one vertex
    gl_Position = gl_PositionIn[0];
    gl_Position.xyz += width * perpen;    
    gl_Position = gl_ProjectionMatrix  * gl_Position;

    
    EmitVertex();
    
    EndPrimitive();	
    
}
