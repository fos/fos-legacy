import os, sys

import subprocess

wrapper_original = r'''
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

#wrapper_new = r'''
#\documentclass{article} 
#\usepackage{amsmath}
#\usepackage{amsthm}
#\usepackage{amssymb}
#\usepackage{bm}
#%\makeatletter
#%\usepackage{fancybox}
#\newcommand{\mx}[1]{\mathbf{\bm{#1}}} 
#\newcommand{\vc}[1]{\mathbf{\bm{#1}}} 
#\newcommand{\T}{\text{T}}             
#\pagestyle{empty} 
#\begin{document} 
#'''

closing = r'''
\end{document}
'''

#snippet = r'''
#\sffamily \TeX rocks!!\\
#\mbox{$\alpha\beta\gamma$}\\
#$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!
#'''

snippet = r'''
\fontsize{48}{54}
\sffamily
  \begin{minipage}{190mm}
    \raggedright
    \begin{itemize}
      \item[\texttt{bundle}] spino-cortical tract or some such structure
      \item[\texttt{\#tracks}] 100,000+ or so
      \item[\texttt{status}] provisional till \textsc{LARCH} gets to work
    \end{itemize}
  \end{minipage}
'''

document = wrapper_original + snippet + closing

label = "testfile"

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

backgroundcolour = "'rgb 0.8  0.8  1.0'"

dvipng_cmd = ["dvipng --depth --height -q -T tight  -x 2000 -z 1 " + \
                  '-bg '+ backgroundcolour  + " -o " + pngfile + ' ' + label]

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

# but don't do it too soon!



