from util import *
from constants import *

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#OWN MODULES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from scipy.integrate import quad as integrate

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STELLAR PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def starLXUV(Ls,t):
    """
    Stellar XUV Luminosity
    Ls in LSUN and t in Gyrs
    """
    #==================================================
    #CRITICAL TIME: Scalo 2007, Khodachenko 2009 Fig.1
    #==================================================
    taui=2.03E15*(Ls*1.8)**(-0.65)/(1E9*YEAR)

    #==================================================
    #X-RAY LUMINOSITY --kilsykova et Lammer 2012
    #==================================================
    if t<=taui:
        LX=6.3E-4*(Ls*LSUN*1E7)
    else:
        LX=1.8928E28*t**(-1.34)

    #==================================================
    #EUV LUMINOSITY
    #==================================================
    LEUV=10**(4.8+0.86*np.log10(LX))
    LXUV=(LX+LEUV) #/(Ls*4E33)
    LXUV=LX #/(Ls*4E33)
    return LXUV

def maxPeriod(M,R):
    """
    Maximum period of rotation before disruption
    """
    Wmax=(GCONST*M*MSUN/(R*RSUN)**3)**0.5
    Pmax=2*PI/Wmax
    return Pmax/DAY

"""
Taken from Claret & Gimenez (1989, 1990)
ZAMS values
"""
STELLAR_MOI=np.array([
        [0.020,0.230**1],
        [0.600,0.378**2],
        [0.800,0.323**2],
        [1.000,0.277**2],
        [1.122,0.248**2],
        [1.259,0.224**2],
        ])

"""
type=Regression,Upper,Lower
"""
def stellarMoI(M,type="Regression"):
    #Regression Coefficients (calculated at May.7/2013)
    a=-1.577705e-01
    b=2.339366e-01
    
    #Lower limit
    MoIlow=0.076729 #Claret & Gimenez (1989)

    #Upper limit
    MoIup=0.25 #Leconte et al. (2011)
    
    #type="Upper"
    if type=="Regression":
        MoI=a*M+b
    elif type=="Upper":
        MoI=MoIup
    else:
        MoI=MoIlow
    return MoI

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STELLAR WIND
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def vn1AUeq(t):
    """
    Velocity and density 1 AU equivalent for main sequence stars.  G07.

    Parameter:
    t: secs

    Return:
    Velocity v at 1 AU: m/s
    Number density n at 1 AU: m^{-3}
    """
    vo=3971*KILO #m/s
    no=1.04E11 #m^{-3}
    tau=2.56E7*YEAR #secs
    betav=-0.43
    betan=-1.86

    ft=(1+t/tau)
    v=vo*ft**betav #Eq. 6
    n=no*ft**betan #Eq. 7
    return v,n

def EqTcorona(Tc,**pars):
    """
    Equation to compute corona temperature, G07
    
    """
    M=pars['M']
    t=pars['t']
    vref,nref=vn1AUeq(t*GIGA*YEAR)
    v=VParker(1.0,M,Tc)
    et=v-vref
    return et

def EqParker(vn,**pars):
    """
    Parker Equation.  G07.
    """
    dn=pars['dn']
    ep=np.log(vn**2.0)-vn**2.0+4*np.log(dn)+4/dn-3 #Eq.3
    return ep

def VParker(d,M,Tc):
    """
    Velocity of a Parker stellar wind. G07.
    
    Parameters:
    M: Stellar mass (solar masses)
    Tc: Corona temperature (K)
    d: Distance (AU)
    """
    M=M*MSUN
    d=d*AU
    m=MP
    
    vc=np.sqrt(KB*Tc/m) #Eq.4
    dc=m*GCONST*M/(4*KB*Tc) #Eq.5
    
    dn=d/dc
    
    if abs(dn-1)<1E-3:
        vn=1
    elif dn>1:
        vn=bisectFunction(EqParker,1.001,10,dn=dn)
    else:
        vn=bisectFunction(EqParker,0.0001,0.9998,dn=dn)
        
    return vn*vc

def Tcorona(t,M):
    """
    Temperature of Corona, G07
    """
    Tc=bisectFunction(EqTcorona,1E2,1E9,M=M,t=t)
    return Tc

def vnGreissmeier(d,t,M,R):
    """
    Velocity and number density computed from Greissmeier model at G07
    
    Parameters:
    d: distance in AU
    t: time in Gyrs
    M: Mass in Msun
    R: Radius in Rsun

    Return:
    v: Velocity in m/s
    n: Number density in m^{-3}
    """
    #STELLAR RADIUS
    R=R*RSUN #m

    #REFERENCE VELOCITY AND DENSITY
    vref,nref=vn1AUeq(t*GIGA*YEAR)

    #SOLAR MASS LOSS RATE AT t
    dMsun=4*PI*AU**2*nref*vref*MP #Eq. 10

    #SCALED STELLAR MASS LOSS RATE AT t
    dMstar=scaleProp(R,dMsun,2.0) # Eq.11

    #CORONAL TEMPERATURE AT t (ISOTHERMAL MODEL)
    Tc=Tcorona(t,M)

    #RADIAL VELOCITY
    vr=VParker(d,M,Tc)

    #NUMBER DENSITY
    n=dMstar/(4*PI*(d*AU)**2*vr*MP)

    #EFFECTIVE VELOCITY
    vkep=np.sqrt(GCONST*M*MSUN/(d*AU))
    v=np.sqrt(vr**2+vkep**2)

    return v,n

def binaryWind(a,tau1,M1,R1,tau2,M2,R2):
    v1,n1=vnGreissmeier(a,tau1,M1,R1)
    if tau2>0:
        v2,n2=vnGreissmeier(a,tau2,M2,R2)
    else:v2=n2=0
    Psw=n1*v1**2+n2*v2**2
    Fsw=n1*v1+n2*v2
    return Psw,Fsw

###################################################
#CALIBRATION PERIOD-RAM PRESSURE RELATIONSHIP
###################################################
VSUN,NSUN=vnGreissmeier(1.0,TAGE,1.0,1.0)
MDOTSUN=4*PI*(1*AU)**2*MP*NSUN*VSUN
#print "Solar mass loss: %e kg/s"%(MDOTSUN/MSUN*YEAR)
#Period-ram pressure relationship (Griessmeier, 2006):
#Mdot v = ko P^{-3.3}
KO=(MDOTSUN*VSUN)*(PSUN**3.3)

"""
Compare with:
MacGregor & Brenner, 1991
http://articles.adsabs.harvard.edu//full/1991ApJ...376..204M/0000211.000.html
"""
def Prot(t,**pars):
    """
    Stellar Rotational Period
    Consistent with stellar wind model
    """
    Ms=pars['Ms']
    Rs=pars['Rs']

    #Properties of the Solar Wind
    v,n=vnGreissmeier(1.0,t,Ms,Rs)

    #Mass Loss
    Mdot=4*PI*(1*AU)**2*MP*n*v

    #Period from the scaling law
    P=(Mdot*v/KO)**(-1/3.3)

    #print "Ms, t (Gyr), P (day)= ",Ms,t,P/DAY
    return P

def theoProt(t,x):
    a=x[0]
    b=x[1]
    c=x[2]
    y=a*t**b+c
    return y

def dtheoProt(t,x):
    a=x[0]
    b=x[1]
    c=x[2]
    y=a*b*t**(b-1)
    return y
    
def tfromProt(P,x):
    a=x[0]
    b=x[1]
    c=x[2]
    t=((P-c)/a)**(1./b)
    return t

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#HABITABILITY ZONE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def Seff2013(Teff,crits=['recent venus'],Tsun=TSUN):

    if Teff<2600:Teff=2600.0
    if Teff>7200:Teff=7200.0
    Tst=Teff-Tsun

    Seffs=[]
    for crit in crits:
        if crit=="runaway greenhouse":
            S=1.0385
            a=1.2456E-4;b=1.4612E-8;c=-7.6345E-12;d=-1.7511E-15
        elif crit=="moist greenhouse":
            S=1.0146
            a=8.1884E-5;b=1.9394E-9;c=-4.3618E-12;d=-6.8260E-16
        elif crit=="recent venus":
            S=1.7763
            a=1.4335E-4;b=3.3954E-9;c=-7.6364E-12;d=-1.1950E-15
        elif crit=="maximum greenhouse":
            S=0.3507
            a=5.9578E-5;b=1.6707E-9;c=-3.0058E-12;d=-5.1925E-16
        elif crit=="early mars":
            S=0.3207
            a=5.4471E-5;b=1.5275E-9;c=-2.1709E-12;d=-3.8282E-16
        else:
            S=a=b=c=d=Tst=-1
        Seffs+=[S+a*Tst+b*Tst**2+c*Tst**3+d*Tst**4]
        
    if len(Seffs)==1:return Seffs[0]
    else:return Seffs

def HZ2013(Ls,Teff,lin='recent venus',lout='early mars'):
    """
    Habitable Zone limits by Kopparapu et al. (2013)
    Ls: In solar Units
    Teff: In K
    """
    if Ls<0 or Teff<0:
        raise Exception("Negative value in stellar properties")
    Seffin,Seffout=Seff2013(Teff,crits=[lin,lout])
    Seffsun=1.0
    lin=(Ls/Seffin)**0.5
    lout=(Ls/Seffout)**0.5
    aHZ=(Ls/Seffsun)**0.5
    return lin,aHZ,lout

def Flux(q,Ls1=1.0,Ls2=1.0,rc1=0.1,rc2=0.1,D=1.0,qsgn=1):
    R1=np.sqrt(D**2+rc1**2+2*D*rc1*np.sin(q))
    R2=np.sqrt(D**2+rc2**2-2*D*rc2*np.sin(q))
    F=qsgn*(Ls1/R1**2+Ls2/R2**2)
    return F

def AverageFlux(d,**args):
    args['D']=d
    intFlux=lambda x:Flux(x,**args)
    #print args
    F=integrate(intFlux,0.0,2*PI)[0]/(2*PI)
    #print F
    #exit(0)
    return F

def HZbin4(q,Ls1,Ls2,Teffbin,abin,crits=['recent venus','early mars']):

    rc2=abin/(q+1)
    rc1=q*rc2
    args=dict(Ls1=Ls1,Ls2=Ls2,rc1=rc1,rc2=rc2)

    #EFFECTIVE TEMPERATURES
    Seffin,Seffout=Seff2013(Teffbin,crits=crits)

    #INNER LIMIT
    AF=lambda x:AverageFlux(x,**args)-Seffin
    lin=bisectFunction(AF,1E-4,20)

    #OUTER LIMIT
    AF=lambda x:AverageFlux(x,**args)-Seffout
    lout=bisectFunction(AF,1E-4,20)

    aHZ=(lin+lout)/2

    return lin,aHZ,lout

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ASTRODYNAMICS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def aKepler(P,M1,M2,UL=AU,UT=DAY,UM=MSUN):
    """
    P: in UT
    M1,M2: In UM
    
    Returns a in UL
    """
    a=(((P*UT)**2*GCONST*((M1+M2)*UM))/(4*PI**2))**(1./3.)/UL
    return a

def aCritical(mu,a,e):
    ac=(1.6+(5.1*e)-(2.22*e**2)+(4.12*mu)-(4.27*e*mu)-(5.09*mu**2)+(4.61*e**2*mu**2))*a
    return ac

def eCritical(mu,abin,a):
    ecrit=lambda x:aCritical(mu,abin,x)-a
    e=bisectFunction(ecrit,0.0,1.0)
    if e<0:e=1
    return e

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TIDAL INTERACTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def nSync(e):
    """
    Ratio Omega/n for a pseudosynchronised body (Hut, 1981)
    """
    nsync=(1+15./2*e**2+45./8*e**4+5./16*e**6)/\
        ((1+3*e**2+3./8*e**4)*(1-e**2)**1.5)
    return nsync

def tidalAcceleration(Mtarg,Rtarg,Ltarg,Mfield,abin,e,n,Omega,verbose=False):
    """
    Tidal acceleration on star Mtarg,Rtarg,Ltarg (in solar units) due
    to body Mfield when body is rotating with angular velocity Omega
    in an orbit with semimajor axis abin (AU), eccentricity e and mean
    angular velocity n (same units as Omega)
    
    Returns angular velocity 
    """
    if verbose:print "*"*50
    if verbose:print "HUT"
    if verbose:print "abin:",abin

    #Eccentricity function
    f2=1+(15./2.)*e**2+(45./8.)*e**4+(5./16.)*e**6
    f5=1+3*e**2+(3./8.)*e**4
    if verbose:print "f1,f5:",f2,f5

    #Maximum rotational rate
    Omega_min=n*f2/((1-e**2)**1.5*f5)

    #Zahn (2008) DISSIPATION TIME
    tdiss=3.48*((Mtarg*MSUN*(Rtarg*RSUN)**2)/(Ltarg*LSUN))**(1./3)
    kdiss=1/tdiss

    if verbose:print "tdiss:",tdiss
    if verbose:print "n,Omega:",n,Omega
    if verbose:print "e:",e

    #Radius of gyration
    rg2=stellarMoI(Mtarg)
    if verbose:print "Radius of Gyration:",rg2

    #Angular acceleration
    angacc=kdiss/rg2*(Mfield/Mtarg)**2*((Rtarg*RSUN)/(abin*AU))**6*(n/(1-e**2)**6)*(f2-(1-e**2)**1.5*f5*Omega/n)
    if verbose:print "Factors:",Omega/n,f2/((1-e**2)**1.5*f5)
    if verbose:print "Acc:",angacc

    return angacc

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#DERIVED CONSTANTS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#XUV Present Earth Level in erg cm^-2 s^-1
PEL=starLXUV(1.0,TAGE)/(4*PI*(1*AU*1E2)**2)
#XUV IN SI
PELSI=PEL*(1E-7/(1E-2))

