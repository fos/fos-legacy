#from __future__ import print_function

import os, sys

#import subprocess

#wrapper = r"\documentclass{article}\usepackage{type1cm}\renewcommand{\rmdefault}{pnc}\usepackage{helvet}\usepackage{courier}\usepackage{textcomp}\usepackage[papersize={72in,72in}, body={70in,70in}, margin={1in,1in}]{geometry}\pagestyle{empty}\begin{document}thispagestyle{empty}\fontsize{16}{20}{%s}\end{document}"

wrapper = r'''
\documentclass{article} 
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\usepackage{bm}
\newcommand{\mx}[1]{\mathbf{\bm{#1}}} 
\newcommand{\vc}[1]{\mathbf{\bm{#1}}} 
\newcommand{\T}{\text{T}}             
\pagestyle{empty} 
\begin{document} 
'''

closing = r"\end{document}"

snippet = r"\sffamily Eleftherios rocks!!\\$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!"

document = wrapper + snippet + closing

label = "testfile"

latexfile = label+".tex"
dvifile = label+".dvi"

latexfilehandle = open(latexfile, "w")

latexfilehandle.write(document)

latexfilehandle.close()

# compile LaTeX document. A DVI file is created
os.system('latex -interaction=nonstopmode %s'  % latexfile)

pngpath = 'png/'

os.system('latex %s' % latexfile )

# Run dvipng on the generated DVI file. Use tight bounding box. 
# Magnification is set to 1200
cmd = "dvipng -T tight -x 1000 -z 9 -bg transparent " \
+ "-o %s%s.png %s" % (pngpath , label, label)
os.system(cmd) 

# Remove temporary files
os.remove(label+'.tex')
os.remove(label+'.log')
os.remove(label+'.aux')
os.remove(label+'.dvi')




