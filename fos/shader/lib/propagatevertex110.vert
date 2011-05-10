#version 110
in vec3 aPosition;
attribute vec3 aColor; // This is the per-vertex color
varying vec3 vColor;   // This is the output to the geometry shader

void main()
{

        gl_Position = gl_ModelViewProjectionMatrix * vec4(aPosition.x, aPosition.y, aPosition.z, 1.0);

        vColor = aColor; // Pass from VS -> GS
}
