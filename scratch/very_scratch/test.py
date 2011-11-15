#import fos
#print fos.__file__


from sympy import symbols, Plot
x,y,z = symbols('xyz')
Plot(x*y**3-y*x**3)
