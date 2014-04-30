import numpy as np
from sys import exit,stderr,stdout,argv
from os import system,path
try:
    from scipy.optimize import minimize
except:
    from scipy.optimize import fmin
    def minimize(f,xo,**args):
        s=dict()
        s['x']=fmin(f,xo,disp=False)
        return dict2obj(s)

######################################################################
#MACROS
######################################################################
fileexists=path.isfile

######################################################################
#UTILITY ROUTINES
######################################################################
class dict2obj(object):
    """Object like dictionary
    
    Parameters:
    ----------
    dict:
       Dictionary with the attributes of object
    
    Examples:
    --------
    >>> c=dictobj({'a1':0,'a2':1})
    
    Addition:

    >>> c+=dictobj({'a3':2})

    """
    def __init__(self,dic={}):self.__dict__.update(dic)
    def __add__(self,other):
        for attr in other.__dict__.keys():
            exec("self.%s=other.%s"%(attr,attr))
        return self

def printerr(str):
    print >>stderr,str

######################################################################
#NUMERICAL ROUTINES
######################################################################
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

def scaleProp(m,alpha,beta):
    """
    Scaling function
    """
    return alpha*m**beta
