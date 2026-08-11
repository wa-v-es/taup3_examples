# script by Philip Crotwell to check fluid to solid coefficients ##
##
from math import *
from sympy import *
from sympy import init_printing
init_printing(use_unicode=True)
from IPython.display import display
##

# Create symbols for sympy
a1 = symbols('alpha_1') # p,s velocity
a2 = symbols('alpha_2')
b2 = symbols('beta_2')
r1 = symbols('rho_1') # density
r2 = symbols('rho_2')
p = symbols('p') # ray param (flat earth)
na1 = symbols(r'eta_{\alpha_1}') # eta, vertical slowness (flat earth)
na2 = symbols(r'eta_{\alpha_2}')
nb2 = symbols(r'eta_{\beta_2}')
e1 = symbols(r'e')
e2 = symbols(r'e^{t}')
f2 = symbols(r'f^{t}')

# Create substitutions from the trig style to slowness style

cos2f2subs = [(cos(2*f2), 1-2*b2**2*p**2)]
trigsubs = [ (cos(e1), a1*na1), (cos(e2), a2*na2), (sin(f2), b2*p),
            (sin(2*e2), 2*na2*a2*a2*p), (sin(2*f2), 2*nb2*b2*b2*p)
           ]
##
#M matrix from Seismic Waves and Sources
MM = Matrix( [ [ cos(e1), cos(e2), -sin(f2)],
              [ 0, sin(2*e2), a2/b2*cos(2*f2)],
              [ -1, r2*a2/(r1*a1)*cos(2*f2), -r2*b2/(r1*a1)*sin(2*f2)] ])

# display(MM)

#Now substitute slowness for trig functions. We delay the cos(2f) term as sympy simplify makes things uglier if we let it use this term.
M = MM.subs(trigsubs)
print('matrix in slowness:\n')
display(M)
print("=======================================================================================\n")
#Show the determiniate, using the cos(2f) term.
S=simplify(M.det()).subs(cos2f2subs)
print('determiniate of matrix :\n')
display(S)
print("=======================================================================================\n")

##
# Here is the corresponding determinate (more or less I think) from FMGS:
d_fmgs = a1*r1*na2 + a1*r2*na1*(4*b2**4*p**2*na2*nb2 + (1-2*b2**2*p**2)**2)
print('determiniate from FMGS for comparison :\n')
display(d_fmgs)
print("=======================================================================================\n")
#
s_fmgs=simplify(M.subs(cos2f2subs).det()-d_fmgs)

#Calculate the coefficiets, we factor out the determinate as that makes coding the individual terms easier. So each term will need to be divided by M.det().
N = Matrix( [  a1*na1,  0, 1])
coef = (( M**-1 ) * N)
SS=simplify(coef  * M.det()).subs(cos2f2subs)
print('[Rpp, Tpp, Tps] :\n')
display(SS)
print("=======================================================================================\n")
##
R = ( M**-1 ).subs(cos2f2subs) * N
Rpp = R[0]
Tpp = R[1]
Tps = R[2]
outenergy = r1*a1*a1*na1*Rpp*Rpp + r2*a2*a2*na2*Tpp*Tpp + r2*b2*b2*nb2*Tps*Tps
inenergy = r1*a1*a1*na1
energy = outenergy-inenergy
###
