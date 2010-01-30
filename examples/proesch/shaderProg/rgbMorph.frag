// 
// Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
// transform rgb values with a matrix
// 
// This program is free software you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation either version 3
// of the License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with self program if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


// uniform variables 
uniform mat4 RGBTransformationMatrix;
uniform sampler2D TextureMapper;

// main function of the fragment shader
void main(){
  // get a color from the texture
  vec4 color = texture2D(TextureMapper, gl_TexCoord[0].st);
  // make a vector of 4 floating-point numbers by appending
  // an alpha of 1.0, and set this fragment's color
  gl_FragColor = RGBTransformationMatrix * color;
}
