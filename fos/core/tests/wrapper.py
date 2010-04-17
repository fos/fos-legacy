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
\fontsize{24}{30}
\sffamily
\resizebox{120mm}{!}{%
  \begin{minipage}{90mm}
    \raggedright
    \begin{itemize}
      \item[\texttt{bundle}] spino-cortical tract or some such structure
      \item[\texttt{\#tracks}] 100,000+ or so
      \item[\texttt{status}] provisional till \textsc{LARCH} gets to work
    \end{itemize}
  \end{minipage}
}% end of resizebox
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

latex_process = subprocess.Popen(['latex -interaction=nonstopmode '
                                  + latexfile], shell=True, stdout=open('/dev/null'))

latex_process.wait()

# Run dvipng on the generated DVI file. Use tight bounding box. 
# Magnification is set to 1200

cmd_original = ["dvipng -o " + pngfile + ' ' + label]

cmd_new = ["dvipng -q -T tight -x 1000 -z 1 -bg 'rgb 1 0.6 0.6' -o" + pngfile + ' ' + label]

dvipng_process = subprocess.Popen(cmd_new, shell=True, stdout=open('/dev/null'))

dvipng_process.wait()

eog_process = subprocess.Popen(['eog ' + pngfile], shell=True, stdout=open('/dev/null'))

eog_process.wait()

# Remove temporary files
os.remove(label+'.tex')
#os.remove(label+'.log')
os.remove(label+'.aux')
os.remove(label+'.dvi')
#os.remove('png/'+label+'.png')

# but don't do it too soon!



