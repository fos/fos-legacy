#version 130
#extension GL_EXT_gpu_shader4 : enable    //Include support for this extension, which defines usampler2D

varying vec4 vColor0; // Input from GS
uniform sampler1D Texture0;

smooth in vec4 TexCoord0;


void main()
{
    //vec4 texel = texture1D(Texture0, TexCoord0);
    //float texel = texture1D(Texture0, gl_TexCoord[0].s);
    gl_FragColor = vec4(vColor0.x, vColor0.y, vColor.z,  vColor.w);
    
}
