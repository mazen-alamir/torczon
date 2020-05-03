from torczon import solve
import numpy as np

# This is the test file for the torczon module. 
# it contains three constrained optimization examples.

# Example 1
#=============
# Assume a cost function that need some class instance to be defined 
class Data():
        def __init__(self):
            self.a = 10
            self.b = -1
            self.c = 1.0  # assign to 0 to put solution at (a,b)
p = Data()

# The cost function  
def f1dex(x, p):
    return (x[0]-p.a)**2 +p.c*(x[1]*x[0])**4+(x[1]-p.b)**2

Nguess = 5
Niter = 30
R = solve(f1dex, p, [0.0,0.0], [-10,-10], [10, 10], Nguess, Niter)
print("Example 1")
print("----------")
print(f"Best found Solution = {R.x}")
print(f"Best Value found = {R.f}")
print("------------------------------")
#----------------

# Example 2
#============
# from http://www-optima.amp.i.kyoto-u.ac.jp/member/student/hedar/Hedar_files/TestGO_files/Page3389.htm

def f2dex(x, constraint_penalty):
    c1 = (np.sin(2*np.pi*x[0]))**3
    c2 = np.sin(2*np.pi*x[1])
    c3 = (x[1]**3)*(x[0]+x[1])
    try:
        cost = c1*c2/c3
    except:
        cost = 1e19
    g1 = x[0]**2-x[1]+1
    g2 = 1-x[0]+(x[1]-4)**2
    constraint = np.max(np.array([0,np.array([g1,g2]).max()]))

    return cost + constraint_penalty*constraint

Nguess = 10
Niter = 50
rho = 1e6
x0 = [0.1,0.1]
dx = 1.0

R = solve(f2dex, rho, x0, [0.001,0.001], [10, 10], Nguess, Niter, initial_box_width=dx)

print("Example 2")
print("----------")
print(f"Best found Solution = {R.x}")
print(f"Best Value found = {R.f}")
print("------------------------------")

# Example 3
#============
# from http://www-optima.amp.i.kyoto-u.ac.jp/member/student/hedar/Hedar_files/TestGO_files/Page2031.htm


def f3dex(x, constraint_penalty):

    c1 = (x[0]-10)**2+5*(x[1]-12)**2
    c2 = x[2]**4+3*(x[3]-11)**2+10*x[4]**6
    c3 = 7*x[5]**2+x[6]**4-4*x[5]*x[6]-10*x[5]-8*x[6]
    cost = c1+c2+c3

    v1 = 2*x[0]**2
    v2 = x[1]**2
    g = np.zeros(4)
    g[0] = v1+3*v2**2+x[2]+4*x[3]**2+5*x[4]-127
    g[1] = 7*x[0]+3*x[1]+10*x[2]**2+x[3]-x[4]-282
    g[2] = 23*x[0]+v2+6*x[5]**2-8*x[6]-196
    g[3] = 2*v1+v2-3*x[0]*x[1]+2*x[2]**2+5*x[5]-11*x[6]

    constraint = np.max(np.array([0, g.max()]))

    return cost + constraint_penalty*constraint


Nguess = 5
Niter = 60
rho = 1e6
x0 = np.zeros(7)

xmin = np.asarray([-10]*7)
xmax = np.asarray([+10]*7)

R = solve(f3dex, rho, x0, xmin, xmax, Nguess, Niter)

print("Example 3")
print("----------")
print(f"Best found Solution = {R.x}")
print(f"Best Value found = {R.f}")
print("------------------------------")
