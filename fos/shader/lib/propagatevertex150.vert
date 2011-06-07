// #version 150
in vec3 aPosition;
in vec4 aColor;

out vec4 vColor0;   // This is the output to the geometry shader

void main(void) {
    gl_Position = gl_ModelViewProjectionMatrix * vec4(aPosition.x, aPosition.y, aPosition.z, 1.0);
    vColor0 = vec4(aColor.x , aColor.y , aColor.z, aColor.w); // Pass from VS -> GS
}