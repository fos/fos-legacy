// #version 150
// in_Position was bound to attribute index 0
in vec3 aPosition;

void main(void) {
    
    gl_Position = gl_ModelViewProjectionMatrix * vec4(aPosition.x, aPosition.y, aPosition.z, 1.0);

}