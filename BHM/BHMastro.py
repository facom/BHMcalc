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
# General Astrophysics Routines
###################################################
from BHM import *
from BHM.BHMnum import *

###################################################
#PACKAGES
###################################################

###################################################
#CONFIGURATION
###################################################

###################################################
#MACROS
###################################################
sin=np.sin
cos=np.cos
tan=np.tan

###################################################
#GLOBALS
###################################################

###################################################
#ROUTINES
###################################################
def aKepler(P,M1,M2,UL=AU,UT=DAY,UM=MSUN):
    """
    P: in UT
    M1,M2: In UM
    
    Returns a in UL
    """
    a=(((P*UT)**2*GCONST*((M1+M2)*UM))/(4*PI**2))**(1./3.)/UL
    return a

def PKepler(a,M1,M2,UL=AU,UT=DAY,UM=MSUN):
    """
    P: in UT
    M1,M2: In UM
    
    Returns a in UL
    """
    P=np.sqrt((a*UL)**3/(GCONST*((M1+M2)*UM)/(4*PI**2)))/UT;
    return P

def aCritical(mu,a,e):
    ac=(1.6+(5.1*e)-(2.22*e**2)+(4.12*mu)-(4.27*e*mu)-(5.09*mu**2)+(4.61*e**2*mu**2))*a
    return ac

def eCritical(mu,abin,a):
    ecrit=lambda x:aCritical(mu,abin,x)-a
    e=bisectFunction(ecrit,0.0,1.0)
    if e<0:e=1
    return e

def nSync(e):
    """
    Ratio Omega/n for a pseudosynchronised body (Hut, 1981)
    """
    nsync=(1+15./2*e**2+45./8*e**4+5./16*e**6)/\
        ((1+3*e**2+3./8*e**4)*(1-e**2)**1.5)
    return nsync

def eccentricAnomaly(e,M):
    """
    Mikkola, 1991
    Code at: http://smallsats.org/2013/04/20/keplers-equation-iterative-and-non-iterative-solver-comparison/
    """
    if e==0:return M
    a=(1-e)*3/(4*e+0.5);
    b=-M/(4*e+0.5);
    y=(b*b/4 +a*a*a/27)**0.5;
    x=(-0.5*b+y)**(1./3)-(0.5*b+y)**(1./3);
    w=x-0.078*x**5/(1 + e);
    E=M+e*(3*w-4*x**3);

    #NEWTON CORRECTION 1
    sE=sin(E)
    cE=cos(E)

    f=(E-e*sE-M);
    fd=1-e*cE;
    f2d=e*sE;
    f3d=-e*cE;
    f4d=e*sE;
    E=E-f/fd*(1+\
                  f*f2d/(2*fd*fd)+\
                  f*f*(3*f2d*f2d-fd*f3d)/(6*fd**4)+\
                  (10*fd*f2d*f3d-15*f2d**3-fd**2*f4d)*\
                  f**3/(24*fd**6))

    #NEWTON CORRECTION 2
    f=(E-e*sE-M);
    fd=1-e*cE;
    f2d=e*sE;
    f3d=-e*cE;
    f4d=e*sE;
    E=E-f/fd*(1+\
                  f*f2d/(2*fd*fd)+\
                  f*f*(3*f2d*f2d-fd*f3d)/(6*fd**4)+\
                  (10*fd*f2d*f3d-15*f2d**3-fd**2*f4d)*\
                  f**3/(24*fd**6))
    return E

def orbitalPosition(n,a,e,t,w=0):
    M=n*t
    E=eccentricAnomaly(e,M)
    x=a*cos(E)-a*e
    y=a*(1-e**2)**0.5*sin(E)
    cw=cos(w)
    sw=sin(w)
    return np.array([x*cw-y*sw,x*sw+y*cw])

def planckDistrib(lamb,T):
    B=2*HP*CSPEED**2/(lamb**5)/(np.exp(HP*CSPEED/(KB*T*lamb))-1)
    I=np.pi*B
    return I

def planckPhotonDistrib(lamb,T):
    B=2*HP*CSPEED**2/(lamb**5)/(np.exp(HP*CSPEED/(KB*T*lamb))-1)
    J=np.pi*B/(HP*CSPEED/lamb)
    return J

def planckPower(lamb1,lamb2,T):
    R,dR=integrate(planckDistrib,lamb1,lamb2,args=(T,))
    return R

def planckPhotons(lamb1,lamb2,T):
    N,dN=integrate(planckPhotonDistrib,lamb1,lamb2,args=(T,))
    return N
