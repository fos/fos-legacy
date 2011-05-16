#version 130
in vec3 aPosition;
in vec4 aColor; // This is the per-vertex color
out vec4 vColor;   // This is the output to the geometry shader

/*
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
*/
uniform sampler1D widthSampler;

void main()
{

        float modelview[16];
        glGetFloatv(GL_MODELVIEW_MATRIX, modelview);

        float projectionmatrix[16];
        glGetFloatv(GL_PROJECTION_MATRIX, projectionmatrix);

        
        gl_Position = projectionmatrix * modelview * vec4(aPosition.x, aPosition.y, aPosition.z, 1.0);

        vColor = aColor; // Pass from VS -> GS

        // fetch texture
        vec4 widthVec;
        float width;
        widthVec = texelFetch(widthSampler, gl_VertexID, 0); // needs version 130
        width = widthVec.x; // We have to fetch a vec4 from the texture, but we will
                            // use a format like GL_LUMINANCE32 which fetches to (L,L,L,1)
                            // so we can just read one component

}
