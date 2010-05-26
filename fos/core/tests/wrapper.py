import os, sys

import subprocess

opening = r'''
\documentclass{article}
\usepackage{type1cm}
\renewcommand{\rmdefault}{pnc}
\usepackage{helvet}
\usepackage{courier}
\usepackage{textcomp}
\usepackage {graphicx}
\pagestyle{empty}
\usepackage[none]{hyphenat}
\begin{document}
\raggedright
\thispagestyle{empty}
\fontsize{48}{54}
  \begin{minipage}{190mm}
    \sffamily
    \raggedright
'''

closing = r'''
\end{minipage}
\end{document}
'''

def label_wrapper(snippet, label, background_colour):

    document = opening + snippet + closing

    latexfile = label+".tex"

    dvifile = label+".dvi"

    pngfile = "png/"+label+".png"

    os.chdir(os.getcwd()+'/data')

    latexfilehandle = open(latexfile, "w")

    latexfilehandle.write(document)

    latexfilehandle.close()

    # compile LaTeX document. A DVI file is created

    latex_process = subprocess.Popen(['latex -interaction=nonstopmode ' + \
                    latexfile], shell=True, stdout=open('/dev/null'))

    latex_process.wait()

    # Run dvipng on the generated DVI file. Use tight bounding box.
    # Magnification is set to x 2

    print background_colour
    
    dvipng_cmd = ["dvipng --depth --height -q -T tight  -x 2000 -z 1 " + \
                      '-bg '+ background_colour  + ' -o ' + pngfile + ' ' + label]

    dvipng_process = subprocess.Popen(dvipng_cmd, shell=True, stdout = subprocess.PIPE)

    dvipng_process.wait()

    output = dvipng_process.communicate()[0]
    dimensions = [s.split('=') for s in output.split()]
    depth  = dimensions[-2][1]
    height = dimensions[-1][1]

    print 'Depth', depth, 'Height', height

    eog_process = subprocess.Popen(['eog ' + pngfile], shell=True, stdout=open('/dev/null'))

    eog_process.wait()

    # Remove temporary files
    os.remove(label+'.tex')
    #os.remove(label+'.log')
    os.remove(label+'.aux')
    os.remove(label+'.dvi')
    os.remove('png/'+label+'.png')
    
snippet = r'''
\begin{itemize}
  \item spino-cortical tract or some such structure
  \item 100,000+ or so
  \item provisional till \textsc{LARCH} gets to work
\end{itemize}
'''

label = "testfile"

background_colour = "'rgb 0.8  0.8  1.0'" # pale blue

label_wrapper(snippet, label, background_colour)
