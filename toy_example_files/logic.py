from __future__ import division
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

x, y = symbols('x,y')
zz=parse_expr('(x | y) & (x | ~y) & (~x | y)')
print(zz)
print(satisfiable((x | y) & (x | ~y) & (~x | y)))