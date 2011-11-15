
import os, sys
import subprocess
import numpy as np
import OpenGL.GL as gl
import Image
import PIL.ImageOps as iops

class TeX(object):

    def __init__(self,label,snippet):

        self.label=label        
        
        self.viewport = (0,0, 1080,800)

        self.bgcolor = (1., 1., 1.)

        self.position = [0,0,0]

        self.near_pick = None

        self.far_pick = None
        

        self.begin_document= r'''
\documentclass{article}
\usepackage{type1cm}
\renewcommand{\rmdefault}{pnc}
\usepackage{helvet}
\usepackage{courier}
\usepackage{textcomp}
%\usepackage[papersize={210mm,297mm},body={190mm,277in},margin={10mm,10mm}]{geometry}
\usepackage {graphicx}
\pagestyle{empty}
\usepackage[none]{hyphenat}
\begin{document}
\raggedright
\thispagestyle{empty}
'''

        self.end_document= r'''
\end{document}
        '''

        self.snippet_start = r'''
\fontsize{48}{54}
\sffamily
\begin{minipage}{190mm}
\raggedright
'''

        self.snippet_end = r'''
\end{minipage}
        '''

        self.snippet = snippet

        self.size = None

        self.win_size = None

        self.data = None

        self.alpha = 255 # 0 - 255

        self.rm_blackish = True

        self.list_index = None

        self.magnification = 400

        self.compression = 1


    def init(self):

        document = self.begin_document + self.snippet_start + self.snippet + self.snippet_end + self.end_document

        #print document

        latexfile = self.label+'.tex'

        dvifile = self.label + '.dvi'

        pngfile = self.label + '.png'

        bgcolor = str(self.bgcolor[0]) + ' ' + str(self.bgcolor[1]) + ' ' + str(self.bgcolor[1]) 

        f = open(latexfile, 'w')

        f.write(document)

        f.close()

        #compile LaTeX document.  A DVI file is created.

        latex_process = subprocess.Popen(['latex -interaction=nonstopmode ' + latexfile], shell=True, stdout=open('/dev/null'))

        latex_process.wait()

        # Run dvipng on the generated DVI file. Use tight bounding box.
        # Magnification is set to 1200

        #cmd_new = ["dvipng "+self.label+".dvi"]

        #cmd_original = ["dvipng -o " + pngfile + ' ' + self.label]

        cmd_new = ["dvipng -q -T tight  -x "+str(self.magnification) \
                       +" -z "+str(self.compression) \
                       +" -bg 'rgb " + bgcolor+ "' -o" + pngfile + ' ' + self.label]

        #cmd_new = ["dvipng -q -T -x 500 -z 1 -o " + pngfile + ' ' + self.label]

        dvipng_process = subprocess.Popen(cmd_new, shell=True, stdout=open('/dev/null'))

        dvipng_process.wait()

        #eog_process = subprocess.Popen(['eog ' + pngfile], shell=True, stdout=open('/dev/null'))

        #eog_process.wait()

        #Remove temporary files

        os.remove(self.label+'.tex')

        #os.remove(label+'.log')

        os.remove(self.label+'.aux')

        os.remove(self.label+'.dvi')

        self.load_image()



    def load_image(self):

        #gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        img = Image.open(self.label+'.png')

        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        self.size = img.size

        rgbi=iops.invert(img.convert('RGB'))

        rgbai=rgbi.convert('RGBA')

        if self.alpha != None:

            rgbai.putalpha(self.alpha)
        
        if self.rm_blackish:


            for x,y in np.ndindex(self.size[0],self.size[1]):

                r,g,b,a=rgbai.getpixel((x,y))

                #print x,y,r,g,b,a

                if r < 10 and g < 10 and b < 10:

                    #print x,y,r,g,b,a

                    rgbai.putpixel((x,y),(0,0,0,0))
    
        #for x,y in

        #rgbai.save('test2.png')
        
        self.data=rgbai.tostring()

        x,y,width,height = gl.glGetIntegerv(gl.GL_VIEWPORT)
        
	width,height = width,height

        self.win_size=(width,height)

        '''

        w,h = self.size

        self.list_index = gl.glGenLists(1)

        gl.glNewList(self.list_index, gl.GL_COMPILE)

        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        #gl.glAlphaFunc(gl.GL_GEQUAL, 0.5);

        #gl.glDisable(gl.GL_ALPHA_TEST);

        #gl.glEnable(gl.GL_DITHER);

        
        gl.glWindowPos3iv(self.position)

        #gl.glDisable(gl.GL_ALPHA_TEST)

        gl.glEnable(gl.GL_BLEND)

        gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glDrawPixels(w, h,gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.data)

        gl.glDisable(gl.GL_BLEND)

        gl.glEndList()

        #os.remove(self.label+'.png')

        #print self.win_size

        '''

    def display(self):

        #gl.glCallList(self.list_index)

        #gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)

        #gl.glAlphaFunc(gl.GL_GEQUAL, 0.5);

        #gl.glDisable(gl.GL_ALPHA_TEST);

        #gl.glEnable(gl.GL_DITHER);

        w,h = self.size

        gl.glEnable(gl.GL_ALPHA_TEST)
        
        gl.glAlphaFunc(gl.GL_GREATER,0)
        
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        
        gl.glWindowPos3iv(self.position)

        #gl.glEnable(gl.GL_BLEND)

        #gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glDrawPixels(w, h,gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.data)

        gl.glDisable(gl.GL_BLEND)

        



class PNG(object):

    def __init__(self,fname):

        self.fname = fname        
        
        self.viewport = (0,0, 1080,800)

        self.bgcolor = (1., 1., 1.)

        self.position = [0,0,0]

        self.near_pick = None

        self.far_pick = None
        
        self.size = None

        self.win_size = None

        self.data = None

        self.alpha = 255 # 0 - 255

        self.rm_blackish = True

        self.list_index = None

        self.magnification = 400

        self.compression = 1

        self.invert = True


        img = Image.open(self.fname)

        img = img.transpose(Image.FLIP_TOP_BOTTOM)

        self.size = img.size

        self.img = img


    def init(self):

        
        self.load_image()



    def load_image(self):


        img=self.img


        if self.invert == True:

            rgbi=iops.invert(img.convert('RGB'))

        else:

            rgbi=img.convert('RGB')

        rgbai=rgbi.convert('RGBA')

        if self.alpha != None:

            rgbai.putalpha(self.alpha)
        
        if self.rm_blackish:


            for x,y in np.ndindex(self.size[0],self.size[1]):

                r,g,b,a=rgbai.getpixel((x,y))

                #print x,y,r,g,b,a

                if r < 10 and g < 10 and b < 10:

                    #print x,y,r,g,b,a

                    rgbai.putpixel((x,y),(0,0,0,0))
    
        #for x,y in        
        
        self.data=rgbai.tostring()

        x,y,width,height = gl.glGetIntegerv(gl.GL_VIEWPORT)
        
	width,height = width,height

        self.win_size=(width,height)

        self.list_index = gl.glGenLists(1)

        gl.glNewList( self.list_index,gl.GL_COMPILE)

        w,h = self.size

        gl.glEnable(gl.GL_ALPHA_TEST)
        
        gl.glAlphaFunc(gl.GL_GREATER,0)
        
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        
        gl.glWindowPos3iv(self.position)

        gl.glDrawPixels(w, h,gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, self.data)

        gl.glDisable(gl.GL_BLEND)

        gl.glEndList()


    def display(self):

        gl.glCallList(self.list_index)



        

       


if __name__ == "__main__":


    snippet = r'''
\begin{itemize}
  \item[\texttt{bundle}] spino-cortical tract or some such structure
  \item[\texttt{\#tracks}] 100,000+ or so
  \item[\texttt{status}] provisional till \textsc{LARCH} gets to work
\end{itemize}
'''

    t=TeX('test',snippet)

    t.init()
    



        

    
