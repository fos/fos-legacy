#version 130
in vec3 aPosition;
in vec4 aColor; // This is the per-vertex color

in vec4 InTexCoord0;

out vec4 vColor;   // This is the output to the geometry shader

uniform sampler1D widthSampler;

smooth out vec4 TexCoord0;


void main()
{

	   // gl_TexCoord[0] =  gl_MultiTexCoord0;


        // vColor = vec4(aColor.x , aColor.y , aColor.z, aColor.w); // Pass from VS -> GS

        int a = gl_VertexID;
        
        // fetch texture
        vec4 widthVec;
        //widthVec = texelFetch(widthSampler, gl_VertexID, 0); // needs version 130
        widthVec = texelFetch(widthSampler, gl_VertexID, 0); // needs version 130
        float width;
        width = widthVec.x; // We have to fetch a vec4 from the texture, but we will
                            // use a format like GL_LUMINANCE32 which fetches to (L,L,L,1)
                            // so we can just read one component

        // vColor = vec4(aColor.x  , aColor.y , aColor.z, aColor.w); // Pass from VS -> GS
        vColor = vec4(aColor.x , aColor.y , aColor.z, aColor.w); // Pass from VS -> GS
        gl_Position = gl_ModelViewProjectionMatrix * vec4(aPosition.x , aPosition.y, aPosition.z, 1.0);


}
