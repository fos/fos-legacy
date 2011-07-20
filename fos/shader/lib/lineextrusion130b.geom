#version 120
#extension GL_EXT_geometry_shader4 : enable

in vec4 vColor0[2];
in float vWidth[2];

out vec4 vColor1;

void main()
{
    gl_Position = vec4(0,0,0,1); EmitVertex();
    gl_Position = vec4(10,0,0,1); EmitVertex();
    gl_Position = vec4(0,10,0,1); EmitVertex();
    EndPrimitive();
}