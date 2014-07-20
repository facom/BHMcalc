from isochrones import *
from plot import *
from BHM import *
import numpy as np

T=5000
lambs=np.linspace(1.0*NANO,1E3*NANO)
plt.close('all')
plt.figure()
planckDistrib(lambs,T)
plt.plot(lambs/NANO,1E-9*planckDistrib(lambs,T)/1E3,'r--')
saveFig("tmp/planck.png")

Asun=(4*np.pi*RSUN**2)
Adist=(4*np.pi*AU**2)
R=planckPower(1.0*NANO,1E5*NANO,TSUN)*Asun
f=R/Adist
print R,f

#PPFD
N=planckPhotons(400.0*NANO,1400*NANO,TSUN)*Asun
n=N/Adist
print N,n

#PPFD
N=planckPhotons(400.0*NANO,1100*NANO,TSUN)*Asun
n=N/Adist
print N,n

N=planckPhotons(400.0*NANO,700*NANO,TSUN)*Asun
n=N/Adist
print N,n

#PFD
N=planckPhotons(1.0*NANO,1E6*NANO,TSUN)*Asun
n=N/Adist
print N,n
