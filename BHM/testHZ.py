from isochrones import *
from plot import *
from BHM import *
from numpy import *
loadIsochroneSet(verbose=True,Zs=ZSVEC_siblings)

Ms=linspace(0.1,1.5,10)
Z=0.0152
tau=1.0
lins=[]
aHZs=[]
louts=[]
Ts=[]
Ss=[]
Sins=[]
Souts=[]
Sins2=[]
Souts2=[]
cin='recent venus'
cout='early mars'
for i in xrange(len(Ms)):
    g,T,R,L=StellarGTRL(Z,Ms[i],tau) 
    Sin,Sout=Seff2014(T,crits=[cin,cout])
    Sin2,Sout2=Seff2013(T,crits=[cin,cout])
    lin,aHZ,lout=HZ(L,T,Seff=Seff2014)
    Ts+=[T]
    Sins+=[Sin]
    Souts+=[Sout]
    Sins2+=[Sin2]
    Souts2+=[Sout2]
    lins+=[lin]
    louts+=[lout]
    aHZs+=[aHZ]

#plt.plot(lins,Ts)
plt.plot(Sins,Ts,'b-')
plt.plot(Souts,Ts,'r-')
plt.plot(Sins,Ts,'b--',linewidth=3)
plt.plot(Souts,Ts,'r--',linewidth=3)
xmin,xmax=plt.xlim()
plt.xlim(xmax,xmin)
plt.grid()
plt.savefig("tmp/HZ.png")

