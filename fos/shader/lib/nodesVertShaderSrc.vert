attribute vec3 aVertexPosition;
attribute vec3 aNormal;
        
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform mat4 uNMatrix;
        
varying vec3 vNormal;

void main(void) {

    vec3 pos = aVertexPosition.xyz;       
    vNormal = vec3(uNMatrix * vec4(aNormal, 1.0));

    vec4 position = uMVMatrix * vec4(pos, 1.0);
    gl_Position = uPMatrix * position;
}
