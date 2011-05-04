// Authors
// Dan Ginsburg & Stephan Gerhard

//
//  clipCoord - incoming clipCoord, output from vertex shader
//  viewport - arguments to glViewport(x,y,width,height)
//  winCoord - [output] Window coordinates
//
void projectCoord(vec4 clipCoord, ivec4 viewport, out vec3 winCoord)
{
    // The clipCoord is already multiplied by the MVP, so we can just do
    // the second half of gluProject()
    vec3 inCoord = clipCoord.xyz / clipCoord.w;
    inCoord = inCoord.xyz * 0.5 + 0.5;

    // Map x/y to viewport
    // The viewport is just the four arguments to glViewport()
    inCoord.x = inCoord.x * viewport.z + viewport.x;
    inCoord.y = inCoord.y * viewport.w + viewport.y;

    winCoord = inCoord;
}

//
//  winCoord - incoming winCoord, unproject back to clip-space
//  w - this should be (incomingClipCoord.w)
//  viewport - arguments to glViewport(x,y,width,height)
//  clipCoord - [output] Clip coordinates
//
void unProjectCoord(vec3 winCoord, float w, ivec4 viewport, out vec4 clipCoord)
{
    vec4 inCoord = vec4(winCoord.xyz, 1.0);

    // Map x and y from window coordinates
    inCoord.x = (inCoord.x - viewport.x) / viewport.z;
    inCoord.y = (inCoord.y - viewport.y) / viewport.w;

    // Map to range -1 to 1
    inCoord.xyz = inCoord.xyz * 2.0 - 1.0;

    // Multiply by w to undo perspective division
    inCoord.xyz = inCoord.xyz * w;

    clipCoord = vec4(inCoord.xyz, w);
}

void main()
{
    // ...
    // Now in pseudocode the GS does something like this
    vec3 winCoord0;
    vec3 winCoord1;

    // viewport should be a uniform ivec4 that you set
    projectCord(gl_PositionIn[0], viewport, winCoord0);
    projectCord(gl_PositionIn[1], viewport, winCoord1);

    // Now do the quad extrusion in screen-coordinates, don't have time to work this out now, if you need help with it let me know...

    // Unproject the window-coordinates BACK to clip-space
    unprojectCoord(computedWinCoord0, gl_PositionIn[0].w, viewport, clipCoord0);
    // ..

    // (you'll do one of the above for each computed coordinate
    // Now you can pass those along as clip-space coords for the frag shader
    gl_Position=clipCoord0;
    // ... And the rest... Emitting vertices as you go
}