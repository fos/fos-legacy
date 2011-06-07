#version 150
precision highp float;
in  vec4 vColor0;
void main(void) {
    gl_FragColor = vec4(vColor0);
}

