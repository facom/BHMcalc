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
from scipy.integrate import quad as integrate
from scipy.linalg import norm
from scipy.optimize import newton 
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

def interpArray(t,r,kind='slinear'):
    x=interp1d(t,r[:,0],kind=kind)
    y=interp1d(t,r[:,1],kind=kind)
    rfunc=lambda t:array([x(t),y(t)])
    return rfunc

def statsArray(array):
    mean=array.mean()
    minn=array.min()
    maxx=array.max()
    rang=maxx-minn
    stdv=array.std()
    return mean,minn,maxx,rang,stdv
