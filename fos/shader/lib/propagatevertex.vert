// #version 150
// in_Position was bound to attribute index 0 and in_Color was bound to attribute index 1
<<<<<<< HEAD
in vec2 in_Position;
//in vec3 in_Color;
=======
in vec2 aPosition;
//in  vec3 in_Color;
>>>>>>> f9dbf6df61d6aff1fdc908a28ea3406aee07beb0
 
// We output the ex_Color variable to the next shader in the chain
//out vec3 ex_Color;

void main(void) {
    // Since we are using flat lines, our input only had two points: x and y.
    // Set the Z coordinate to 0 and W coordinate to 1
 
    //gl_Position = vec4(in_Position.x, in_Position.y, 0.0, 1.0);
 
    // GLSL allows shorthand use of vectors too, the following is also valid:
    // gl_Position = in_Position; //vec4(in_Position, 1.0);
    
<<<<<<< HEAD
    // gl_Position = vec4(in_Position.x, in_Position.y, in_Position.z , 1.0);
    gl_Position = vec4(in_Position, 1.0);
    
    // We're simply passing the color through unmodified
 
    //ex_Color = in_Color;
=======
    // gl_Position = vec4(aPosition, 1.0);
    gl_Position = vec4(aPosition.x, aPosition.y, 0.0, 1.0);

    // We're simply passing the color through unmodified
 
  //  ex_Color = in_Color;
   // gl_Position = ftransform();
   //gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
>>>>>>> f9dbf6df61d6aff1fdc908a28ea3406aee07beb0
}
/*
void main()
{   
    gl_Position = ftransform();
}
*/