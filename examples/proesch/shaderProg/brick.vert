// Motion of vertices for torus added by
// Peter.Roesch@fh-augsburg.de
//
// Vertex shader for procedural bricks
//
// Authors: Dave Baldwin, Steve Koren, Randi Rost
//          based on a shader by Darwyn Peachey
//
// Copyright (c) 2002-2004 3Dlabs Inc. Ltd. 
//
// See 3Dlabs-License.txt for license information
//


uniform float Time;
uniform float Amplitude;
uniform vec3 LightPosition;

const float SpecularContribution = 0.3;
const float DiffuseContribution  = 1.0 - SpecularContribution;
const float M_PI=3.14159265358979323846;

varying float LightIntensity;
varying vec2  MCposition;

void main(void)
{ 
	// calculate offset vector in model space
	float angle=0.0;
	// nvidia linux driver has problems with atan(0) ...
	if (abs(gl_Vertex.y) > 1e-7){
		angle=atan(gl_Vertex.y/gl_Vertex.x);
		if (gl_Vertex.x<0.0)
			angle+=M_PI;
	}
	vec3 offsetVector = gl_Normal*sin(2.0*angle+Time)*Amplitude;
	// shift vertex along the normal
    vec3 ecPosition = vec3 (gl_ModelViewMatrix * (gl_Vertex+vec4(offsetVector,0)));
    vec3 tnorm      = normalize(gl_NormalMatrix * gl_Normal);
    vec3 lightVec   = normalize(LightPosition - ecPosition);
    vec3 reflectVec = reflect(-lightVec, tnorm);
    vec3 viewVec    = normalize(-ecPosition);
    float diffuse   = max(dot(lightVec, tnorm), 0.0);
    float spec      = 0.0;

    if (diffuse > 0.0)
    {
        spec = max(dot(reflectVec, viewVec), 0.0);
        spec = pow(spec, 16.0);
    }

    LightIntensity  = DiffuseContribution * diffuse +
                      SpecularContribution * spec;

    MCposition      = gl_Vertex.xy;
    // MCposition      = gl_Vertex.xy+offsetVector.xy;
    gl_Position     = gl_ProjectionMatrix*vec4(ecPosition,1);
}
