from __future__ import division
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
#
# x, y = symbols('x,y')
# zz=parse_expr('(x | y) & (x | ~y) & (~x | y)')
# print(zz)
# print('x=true,y=false')
# print(zz.subs({x:True,y:False}))
# print('x=true,y=true')
# print(zz.subs({'x':True,'y':False}))
# print(satisfiable((x | y) & (x | ~y) & (~x | y)))
#

f="('object_at', ('$can', '$armadillo', '$dummy'))"
s="('object_at', ('$door', '$armadillo', '$dummy'))"
ff='a'+str(abs(hash(f)))+'a'
ss='a'+str(abs(hash(s)))+'a'
sys,syf = symbols(ss+','+ff)
sexp="('object_at', ('$can', '$armadillo', '$dummy')) & ('object_at', ('$door', '$armadillo', '$dummy'))"
nsexp = sexp.replace(f,ff).replace(s,ss)
ex = parse_expr(nsexp)
print('first=true,second=false')
print(ex.subs({sys:True,syf:False}))
print('first=true,second=true')
print(ex.subs({sys:True,syf:True}))
print('')
print('with string dictionary')
print('first=true,second=false')
print(ex.subs({sys:True,syf:False}))
print('first=true,second=true')
print(ex.subs({ss:True,ff:True}))
