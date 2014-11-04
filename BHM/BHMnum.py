###################################################
#  ____  _    _ __  __           _      
# |  _ \| |  | |  \/  |         | |     
# | |_) | |__| | \  / | ___ __ _| | ___ 
# |  _ <|  __  | |\/| |/ __/ _` | |/ __|
# | |_) | |  | | |  | | (_| (_| | | (__ 
# |____/|_|  |_|_|  |_|\___\__,_|_|\___|
# v2.0
###################################################
# 2014 [)] Jorge I. Zuluaga, Viva la BHM!
###################################################
# Numerical routines
###################################################
from BHM import *

###################################################
#PACKAGES
###################################################
from scipy.interpolate import interp1d
try:
    from scipy.optimize import minimize
except:
    from scipy.optimize import fmin
    def minimize(f,xo,**args):
        s=dict()
        s['x']=fmin(f,xo,disp=False)
        return dict2obj(s)

###################################################
#ROUTINES
###################################################
def scaleProp(m,alpha,beta):
    """
    Scaling function
    """
    return alpha*m**beta

def bisectFunction(fsw,a,b,maxiter=20,tol=1E-3,**pars):
    """
    Bisection algorithm
    """
    eps=1.0;
    i=0
    f1=fsw(b,**pars)
    f2=fsw(a,**pars)
    if f1*f2>0:
        #print "Bisection failed. f1 = %e, f2 = %e No zero in the interval (%e,%e)"%(f1,f2,a,b)
        return -1

    while eps>tol and i<maxiter:
        m=a+(b-a)/2.
        f1=fsw(a,**pars)
        fm=fsw(m,**pars)
        f2=fsw(b,**pars)
        if f1*fm<0:b=m
        else:a=m
        eps=abs(b-a)/abs(a+b)
        i=i+1

    return m
