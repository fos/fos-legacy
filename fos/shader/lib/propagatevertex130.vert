#version 130
in vec3 aPosition;
in vec4 aColor; // This is the per-vertex color

out vec4 vColor;   // This is the output to the geometry shader
//out float vWidth;

//uniform sampler1D widthSampler;

void main()
{
/*
        // fetch texture value
        vec4 widthVec;
        widthVec = texelFetch(widthSampler, gl_VertexID, 0); // needs version 130
        float width;
        width = widthVec.x; // We have to fetch a vec4 from the texture, but we will
                            // use a format like GL_LUMINANCE32 which fetches to (L,L,L,1)
                            // so we can just read one component
        vWidth = width;
*/

        vColor = vec4(aColor.x , aColor.y , aColor.z, aColor.w); // Pass from VS -> GS
        gl_Position = gl_ModelViewProjectionMatrix * vec4(aPosition.x , aPosition.y, aPosition.z, 1.0);

}
