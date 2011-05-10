#version 110
varying vec4 vColor0; // Input from GS
void main()
{
        gl_FragColor = vec4(vColor0);
}