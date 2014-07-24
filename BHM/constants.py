from util import *
import scipy.constants as const
######################################################################
#CONSTANTS
######################################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#EARTH PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Rp_E=6.371E6 #m
Rc_E=3.480E6 #m,**RG00**
Ric_E=1.2215E6 #m, **RG00**
Chi_E=Ric_E/Rc_E 
rhoc_E=1.1E4 #kg/m3, **OC06**
gc_E=10.68 #**RG00**
Rosl_E=0.09/(1+Chi_E) #**OC06+ALP09**
Tc_E=5000

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#PHYSICAL CONSTANTS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#GRAVITATIONAL CONSTANTS
GCONST=6.67E-11
#MAGNETIC PERMEABILITY
MU0=const.mu_0
#BOLTZMAN CONSTANT
KB=const.k
#BOLTZMAN CONSTANT
HP=const.h
#SPEED OF LIGHT
CSPEED=const.c
#PROTON MASS
MP=const.m_p
#STEFAN-BOLTZMAN CONSTANT
SIGMAC=3E-15*1E-4 #cm^2
#ATOMIC MASS UNIT
UMA=1.66054E-27 # kg

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ATOMIC CONSTANTS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#MOLECULAR MASSES
MCARBON=12.0107*UMA
MOXYGEN=15.9994*UMA
MNITROGEN=14.0067*UMA
MH2O=18.01528*UMA
MCO2=43.98983*UMA

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ASTRONOMICAL CONSTANTS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ASTRONOMICAL UNIT
AU=1.496E11 #m
#SECONDS IN AN HOUR
HOUR=3600.0
#SECONDS IN A DAY
DAY=86400.0
#YEAR
YEAR=365.0*DAY
GYR=1E9*YEAR
#SOLAR MASS
MSUN=1.99E30 #kg
#SOLAR TEMPERATURE
TSUN=5780.0 #K
#SOLAR RADIUS
RSUN=6.955E8 #m
#SOLAR LUMINOSITY
LSUN=3.842E26
#SOLAR AVERAGE ROTATION PERIOD
PSUN=25.05*DAY
#SOLAR METALLICITY
ZSUN=0.0152
#SOLAR LXUV
LXSUN=10**27.35 # Mamajek 2011
LEUVSUN=26.7*1E-3*1E7/1E4/5.3*4*np.pi*(AU*1E2)**2 #Tian2008, Pag. 14
LXUVSUN=LXSUN+LEUVSUN
#RATE OF MASS LOSS FOR THE SUN
MSTSUN=2.5E-14*MSUN/YEAR #kg/s.  Source: Wood et al. (2002)
#SOLAR CONSTANT
SOLAR_CONSTANT=1367.9046529 #W m^-2

#EARTH MASS
MEARTH=5.9722E24 #kg
#EARTH COMPOSITIONS (*CITATION*)
MOCEANS=1.39E24 #g
MATMOSPHERE=5.15E18 #kg
NOCEANS=4.64E46
NCO2=2.5E46

#PRESSURE-COLUMN DENSITY EQUIVALENT (*CITATION*)
BAR=1E5 #PA
M1BAR=1.14E3 #g cm^-2 

#AVERAGE EARTH MAGNETIC FIELD (*CITATION*)
MDIPE=7.768E22 #A m^2
BDIPE=42.48 #micro T

#AGE OF SOLAR SYSTEM
TAGE=4.56

#PRIMORDIAL ROTATION OF THE EARTH (*CITATION*)
PPRIM=17.0*HOUR

#JUPITER
MJUP=1.899E27 #kg
RJUP=7.1492E7 #m

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#MULTIPLES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GIGA=1.0E9
KILO=1.0E3
MICRO=1.0E-6
NANO=1E-9

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#NUMERIC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PI=np.pi
