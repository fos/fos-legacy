#version 110
in vec3 aPosition;
in vec4 aColor; // This is the per-vertex color

// matrices
//in mat4 projMatrix;
//in mat4 modelviewMatrix;

out vec4 vColor;   // This is the output to the geometry shader

void main()
{

        vColor = vec4(aColor.x , aColor.y , aColor.z, aColor.w); // Pass from VS -> GS

        gl_Position = gl_ModelViewProjectionMatrix * vec4(aPosition.x , aPosition.y, aPosition.z, 1.0);;

}
