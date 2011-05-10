#version 110
varying vec3 vColor0; // Input from GS
void main()
{
        gl_FragColor = vec4(vColor0, 1.0);
}