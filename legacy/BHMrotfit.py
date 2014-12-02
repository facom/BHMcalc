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
# Stellar Evolution 
###################################################
from BHM import *
from BHM.BHMplot import *
from BHM.BHMstars import *

sys_dir="tests"
star_conf="star1.conf"
qover=1

###################################################
#LOAD STAR PROPERTIES
###################################################
PRINTOUT("Loading object from '%s'"%(star_conf))
star,star_str,star_hash,star_dir=makeObject("star",
                                            sys_dir+"/"+star_conf,
                                            qover=qover)

###################################################
#LOAD ISOCHRONES
###################################################
zsvec=chooseZsvec(star.Z)
PRINTOUT("Loading isochrone set: %s"%(zsvec))
try:
    zsvec=chooseZsvec(star.Z)
    exec("num=loadIsochroneSet(verbose=False,Zs=%s)"%zsvec)
except:
    PRINTERR("Error loading isochrones.")
    errorCode("FILE_ERROR")

###################################################
#CALCULATE EVOLUTIONARY TRACK
###################################################
#DETERMINING APPROXIMATELY THE MAXIMUM AGE
PRINTOUT("Estimating maximum age...")
tau_max=TAU_MAX
ts=np.linspace(TAU_MIN,TAU_MAX,NTIMES)
for t in ts:
    data=StellarGTRL(star.Z,star.M,t)
    if data[1]<0:
        tau_max=t
        break

#SAMPLING TIMES
exp_ts1=np.linspace(np.log10(TAU_MIN),np.log10(tau_max/2),NTIMES/2)
exp_ts2=-np.linspace(-np.log10(min(TAU_MAX,1.5*tau_max)),-np.log10(tau_max/2),NTIMES/2)
ts=np.unique(np.concatenate((10**exp_ts1,(10**exp_ts2)[::-1])))

#EVOLUTIONARY MATRIX
PRINTOUT("Calculating Evolutionary Matrix...")
evodata=np.array([np.array([t]+list(StellarGTRL(star.Z,star.M,t))) for t in ts])
maxdata=evodata[:,1]>0
evodata=evodata[maxdata]
evodata_str=array2str(evodata)
star.evotrack=evodata

#MAXIMUM ALLOWABLE TIME
tau_max=evodata[-1,0]
PRINTOUT("Maximum age = %.3f"%tau_max)

#DETECTING THE END OF HYDROGEN BURNING
ts=evodata[:,0]
Rs=evodata[:,3]
if star.taums==0:
    tau_ms=disconSignal(ts,Rs,
                        tausys=tau_max/2,
                        iper=3,dimax=10)
else:tau_ms=star.taums
star.taums=tau_ms

###################################################
#RADIUS AND MOMENT OF INERTIA EVOLUTION
###################################################
#GIRATION RADIUS
Nfine=500
star.MoI=np.sqrt(stellarMoI(star.M))
tsmoi=np.logspace(np.log10(TAU_MIN),np.log10(tau_ms),Nfine)

#========================================
#RADIUS EVOLUTION
#========================================
PRINTOUT("Calculating radius evolution...")
star.RMoI=stack(1)
for t in tsmoi:
     logg=StellarProperty('logGravitation',star.Z,star.M,t)
     g=10**logg/100
     R=StellarRadius(star.M,g)
     star.RMoI+=[R]
star.RMoI=toStack(tsmoi)|star.RMoI
Rfunc=interp1d(star.RMoI[:,0],star.RMoI[:,1],kind='slinear')

dRdt=[0]
for i in range(1,Nfine-1):
     dt=(tsmoi[i+1]-tsmoi[i-1])/4
     dRdt+=[(Rfunc(tsmoi[i]+dt)-Rfunc(tsmoi[i]-dt))/(2*dt)]
dRdt[0]=dRdt[1]
dRdt+=[dRdt[-1]]
star.RMoI=toStack(star.RMoI)|toStack(dRdt)

#========================================
#MOMENT OF INERTIA EVOLUTION
#========================================
Ievo=stack(2)
for i in range(Nfine):
     R=star.RMoI[i,1]
     dRdt=star.RMoI[i,2]
     facI=star.MoI*star.M
     I=facI*R**2
     dIdt=2**facI*R*dRdt
     Ievo+=[I,dIdt]
star.RMoI=toStack(star.RMoI)|Ievo

###################################################
#ROTATION EVOLUTION
###################################################
evoInterpFunctions(star)
from lmfit import minimize,Parameters,Parameter,report_fit
from scipy.optimize import fmin

tsmoi=np.logspace(np.log10(0.01),np.log10(4.56),30)
def residualRotation(params,plot=False):
     Pini=params["Pini"].value
     Kw=params["Kw"].value*1E40
     wsat=params["wsat"].value
     taudisk=params["taudisk"].value*0.01
     """
     Pini=params[0]
     #Pini=10.0
     Kw=10**params[1]
     #Kw=7E40
     wsat=params[2]
     #wsat=10.0
     taudisk=params[3]*1E-2
     #taudisk=0.01
     """
     print "Pini,Kw,wsat,taudisk = ",Pini,Kw,wsat,taudisk

     wini=2*PI/(Pini*DAY)
     rotpars=dict(\
          star=star,
          starf=None,binary=None,
          taudisk=taudisk,
          Kw=Kw,
          wsat=wsat
          )
     rotevol=odeint(rotationalAcceleration,wini,tsmoi*GYR,args=(rotpars,))

     if plot:
          fig=plt.figure()
          ax=fig.add_axes([0.1,0.1,0.8,0.8])
          ax.plot(tsmoi,rotevol[:,0]/OMEGASUN)
          ax.plot([4.56],[1.0],'ro',markersize=10)
          ax.set_xscale("log")
          ax.set_yscale("log")
          fig.savefig("tests/rot-evol.png")
          
     #residual=np.abs(PSUN/DAY-2*PI/rotevol[-1,0]/DAY)
     residual=abs(PSUN/DAY-2*PI/rotevol[-1,0]/DAY)
     print "Residual = ",residual
     return [residual]*6
     
"""
params=[5.0,40.0,10,1.0]
#params=[20.0]
#params=[41.0]
params=fmin(residualRotation,params)
print params
"""
params=Parameters()
params.add("Pini",value=5.0,
           min=1.0,
           max=10.0,
           vary=0)
params.add("Kw",value=5,
           min=0.1,
           max=10.0,
           vary=0)
params.add("wsat",value=10.0,
           min=1.0,
           max=50.0,
           vary=0)
params.add("taudisk",value=1.0,
           min=1.0,
           max=50.0,
           vary=0)

residualRotation(params,plot=True)
exit(0)
result=minimize(residualRotation,params)
residualRotation(params,plot=True)
report_fit(params)
