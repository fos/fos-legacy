#version 130

in vec4 vColor1;

void main()
{
    gl_FragColor = vec4(vColor1.x, vColor1.y, vColor1.z,  vColor1.w);
}
