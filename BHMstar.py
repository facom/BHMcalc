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

###################################################
#CLI ARGUMENTS
###################################################
Usage=\
"""
Usage:
   python %s <sysdir> <module>.conf <qoverride>

   <sysdir>: Directory where the system configuration files lie

   <module>.conf (file): Configuration file for the module.

   <qoverride> (int 0/1): Override any existent object with the same hash.
"""%argv[0]

sys_dir,star_conf,qover=\
    readArgs(argv,
             ["str","str","int"],
             ["sys/template","star1.conf","0"],
             Usage=Usage)

###################################################
#LOAD STAR PROPERTIES
###################################################
PRINTOUT("Loading object from '%s'"%(star_conf))
star,star_str,star_hash,star_dir=makeObject("star",
                                            sys_dir+"/"+star_conf,
                                            qover=qover)
PRINTOUT("Object directory '%s' created"%star_dir)
star_webdir=WEB_DIR+star_dir

#METALLICITY AND ISOCHRONE GRID
if star.Z==0:
     star.Z,dZ=ZfromFHe(star.FeH)
     PRINTOUT("Calculated metallicity:Z=%.4f"%(star.Z))
else:
     star.FeH=FeHfromZ(star.Z)
     PRINTOUT("Calculated metallicity:[Fe/H]=%.4f"%(star.FeH))

###################################################
#LOAD MODEL TRACK
###################################################
#FIND STELLAR EVOLUTION TRACK
model=star.str_model.replace("'","")
pfind,startrack=findTrack(model,star.Z,star.M,verbose=True)
trackfunc=trackFunctions(startrack)
trackarr=trackArrays(startrack)
modelwat="%s:Z=%.4f,M=%.2f"%(model,pfind[0],pfind[2])

def StellarGTRL(Z,M,t):
     try:
          g=trackfunc.g(t*GIGA)
          T=trackfunc.T(t*GIGA)
          R=trackfunc.R(t*GIGA)
          L=trackfunc.L(t*GIGA)
     except:
          g=T=R=L=-1
     return g,T,R,L

###################################################
#CALCULATE EVOLUTIONARY TRACK
###################################################
ts=trackarr.ts/1E9
tau_ini=ts[0]
tau_end=min(ts[-1],TAU_MAX)

#SAMPLING TIMES
#"""
exp_ts1=np.linspace(np.log10(max(TAU_MIN,tau_ini)),np.log10(tau_end/2),NTIMES/2)
exp_ts2=-np.linspace(-np.log10(min(TAU_MAX,tau_end)),-np.log10(tau_end/2),NTIMES/2)
ts=np.unique(np.concatenate((10**exp_ts1,(10**exp_ts2)[::-1])))
#"""

#EVOLUTIONARY MATRIX
PRINTOUT("Calculating Evolutionary Matrix...")
evodata=np.array([np.array([t]+list(StellarGTRL(star.Z,star.M,t))) for t in ts])
maxdata=evodata[:,1]>0
evodata=evodata[maxdata]
evodata_str=array2str(evodata)
star.evotrack=evodata

#MAXIMUM ALLOWABLE TIME
star.tau_min=evodata[0,0]
star.tau_max=evodata[-1,0]
PRINTOUT("Minimum age in model = %.3f"%star.tau_min)
PRINTOUT("Maximum age in model = %.3f"%star.tau_max)

#DETECTING THE END OF HYDROGEN BURNING
ts=evodata[:,0]
Rs=evodata[:,3]
if star.taums==0:
    tau_ms=disconSignal(ts,Rs,
                        tausys=star.tau_max/2,
                        iper=3,dimax=10)
else:tau_ms=star.taums
star.tau_ms=min(tau_ms,star.tau_max)
PRINTOUT("End of Hydrogen Burning Phase = %.3f"%star.tau_ms)

###################################################
#RADIUS AND MOMENT OF INERTIA EVOLUTION
###################################################
#GYRATION RADIUS
Nfine=500
star.MoI=np.sqrt(stellarMoI(star.M))
tsmoi=np.logspace(np.log10(TAU_MIN),np.log10(star.tau_ms),Nfine)

#========================================
#RADIUS EVOLUTION
#========================================
PRINTOUT("Calculating radius evolution...")
star.RMoI=stack(1)
for t in tsmoi:
     R=trackfunc.R(t*GIGA)
     star.RMoI+=[R]
star.RMoI=toStack(tsmoi)|star.RMoI
Rfunc=interp1d(star.RMoI[:,0],star.RMoI[:,1],kind='slinear')

PRINTOUT("Calculating derivative of radius...")
dRdt=[0]
for i in range(1,Nfine-1):
     dt=(tsmoi[i+1]-tsmoi[i-1])/4
     dRdt+=[(Rfunc(tsmoi[i]+dt)-Rfunc(tsmoi[i]-dt))/(2*dt)]
dRdt[0]=dRdt[1]
dRdt+=[dRdt[-1]]
star.RMoI=toStack(star.RMoI)|toStack(dRdt)

#========================================
#EVOLUTION OF MOMENT OF INERTIA
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
PRINTOUT("Calculating rotation evolution...")
evoInterpFunctions(star)

#CONVECTIVE TURNOVER AT 200 Myr
tauconv=convectiveTurnoverTime(star.Tfunc(0.2))

#INITIAL ROTATIONAL RATE
wini=2*PI/(star.Pini*DAY)

#SATURATION
if star.wsat==0:
     wsat_scaled=WSATSUN*TAUCSUN/tauconv
else:
     wsat_scaled=star.wsat

#INTEGRATION
rotpars=dict(\
     star=star,
     starf=None,binary=None,
     taudisk=star.taudisk,
     Kw=star.Kw,
     wsat=wsat_scaled
     )
star.rotevol=odeint(rotationalAcceleration,wini,tsmoi*GYR,args=(rotpars,))
star.rotevol=toStack(tsmoi)|toStack(star.rotevol)

###################################################
#EVOLUTION OF ACTIVITY
###################################################
#CRANMER & SAAR (2011)
PRINTOUT("Calculating evolution of activity...")

"""
Columns:
0:Time
1:Convective overturn time (Gyr)
2:filling factor (fstar)
3:Equipartition magnetic field (G)
4:Photospheric magnetic field (G)
5:Transition Region magnetic field (G)
6:Rossby number
7:Total mass-loss
8:Mass-loss due to a hot corona
9:Mass-loss due to wave pressure in chromosphee
10:Mach number at transition region
11:Ratio X-Ray luminosity to Bolometric Luminosity
12:X-Ray Luminosity
13:XUV (X+EUV) Luminosity
"""
star.activity=stack(13)
for i in range(0,Nfine):
     t=tsmoi[i]
     M=star.M
     R=star.Rfunc(t)
     L=star.Lfunc(t)
     Prot=2*PI/star.rotevol[i,1]/DAY

     #SURFICIAL MAGNETIC CONDITIONS
     tauc,fstar,Bequi,Bphoto,BTR,Rossby,Mdot,Mdot_hot,Mdot_cold,MATR=\
         pyBoreas(M,R,L,Prot,star.FeH)
     
     #X-RAY EMMISION
     RX=starRX(Rossby)
     LX=L*RX*LSUN
     LXUV=starLXEUV(LX)

     star.activity+=[tauc,fstar,Bequi,Bphoto,BTR,Rossby,
                     Mdot,Mdot_hot,Mdot_cold,MATR,
                     RX,LX,LXUV]
     
star.activity=toStack(tsmoi)|star.activity

###################################################
#CALCULATE DERIVATIVE INSTANTANEOUS PROPERTIES
###################################################
#BASIC PROPERTIES
g,Teff,R,L=StellarGTRL(star.Z,star.M,star.tau)

#HABITABLE ZONE LIMITS
PRINTOUT("Calculating HZ...")
lins=[]
for incrit in IN_CRITS:
    lin,lsun,lout=HZ(L,Teff,lin=incrit)
    lins+=[lin]
louts=[]
for outcrit in OUT_CRITS:
    lin,lsun,lout=HZ(L,Teff,lout=outcrit)
    louts+=[lout]

#DISSIPATION TIME
tdiss=dissipationTime(star.M,R,L)

PRINTOUT("Star ID: %s"%star.str_StarID)
star.str_StarID=star.str_StarID.replace("'","")
PRINTOUT("Star ID: %s"%star.str_StarID)
title=r"%s: $M_{\\rm star}/M_{\odot}$=%.2f, $Z$=%.4f, $[Fe/H]$=%.2f, $\\tau$=%.2f Gyr"%(star.str_StarID,star.M,star.Z,star.FeH,star.tau)

###################################################
#STORE STELLAR DATA
###################################################
PRINTOUT("Storing stellar data...")
f=open(star_dir+"star.data","w")
f.write("""\
from numpy import array
#MAXIMUM AGE
taumin=%.17e #Gyr
taumax=%.17e #Gyr
taums=%.17e #Gyr

#INSTANTANEOUS PROPERTIES
title="%s"

#INSTANTANEOUS PROPERTIES
gins=%.17e #m/s^2
Tins=%.17e #L
Rins=%.17e #Rsun
Lins=%.17e #Lsun
MoI=%.17e #Gyration radius (I/M R^2)
tauconv=%.17e #days, Convective turnover time
tdiss=%.17e #s

#ROTATION FIT
wsat_scaled=%e

#OTHER PROPERTIES
lins=%s #AU
lsun=%.17e #AU
louts=%s #AU

#EVOLUTIONARY TRACK
evotrack=%s

#MOMENT OF INERTIA EVOLUTION
RMoI=%s

#ROTATIONAL EVOLUTION
rotevol=%s

#MASS-LOSS EVOLUTION
activity=%s
"""%(star.tau_min,star.tau_max,star.tau_ms,title,
     g,Teff,R,L,star.MoI,tauconv,tdiss,
     wsat_scaled,
     array2str(lins),lsun,array2str(louts),
     evodata_str,
     array2str(star.RMoI),
     array2str(star.rotevol),
     array2str(star.activity)
     ))
f.close()

###################################################
#GENERATE PLOTS
###################################################
PRINTOUT("Creating plots...")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STELLAR PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"stellar-props",\
"""
from BHM.BHMstars import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
evodata=%s
ts=evodata[:,0]
ts=ts[ts<star.taums]
logrho_func,Teff_func,logR_func,logL_func=evoFunctions(evodata)

ax.plot(ts,10**logrho_func(np.log10(ts))/GRAVSUN/1E2,label=r"$g_{\\rm surf}$")
ax.plot(ts,Teff_func(np.log10(ts))/TSUN,label=r"$T_{\\rm eff}$")
ax.plot(ts,10**logR_func(np.log10(ts)),label=r"$R$")
ax.plot(ts,10**logL_func(np.log10(ts)),label=r"$L$")
ax.axvline(star.taums,color='k',linestyle='--',label='Turn Over')
ax.axvline(star.tau,color='k',linestyle='-',label='Stellar Age')

ax.set_xscale('log')
ax.set_yscale('log')

logTickLabels(ax,-2,1,(3,),axis='x',frm='%%.2f')
ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"Property in Solar Units")

ymin,ymax=ax.get_ylim()
ax.set_xlim((0,star.taumax))
ax.set_ylim((0.1,10.0))
ax.set_ylim((ymin,ymax))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes)

ax.legend(loc='best',prop=dict(size=12))
"""%(star_dir,star_dir,evodata_str,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#EVOLUTIONARY TRACK
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-track",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

evodata=%s
ts=evodata[:,0]
logrho_func,Teff_func,logR_func,logL_func=evoFunctions(evodata)

bbox=dict(fc='w',ec='none')

#TIMES
ts=ts[ts>=0.1]
ts=ts[ts<=star.taums]

#LINE
logts=np.log10(ts)
Teffs=Teff_func(logts)
Leffs=10**logL_func(logts)
ax.plot(Teffs,Leffs,"k-")
ax.plot(Teffs[0:1],Leffs[0:1],"ko",markersize=5)
ax.plot([Teffs[0]],[Leffs[0]],"go",markersize=10,markeredgecolor='none',label=r"$t_{\\rm ini}=$0.1 Gyr")
ax.plot([Teffs[-1]],[Leffs[-1]],"ro",markersize=10,markeredgecolor='none',label=r"$t_{\\rm end}=$%%.1f Gyr"%%star.taums)
ax.plot([star.Tins],[star.Lins],"bo",markersize=10,markeredgecolor='none',label=r"$t=$%%.1f Gyr"%%star.tau)

if star.R>0 and star.T>0:
   star.Terr=max(star.Terr,0.0)
   L=star.R**2*(star.T/5770)**4
   star.Rerr=max(star.Rerr,0.0)
   Lerr=L*(2*star.Rerr/star.R+4*star.Terr/star.T)
   ax.errorbar(star.T,L,xerr=star.Terr,yerr=Lerr,linewidth=2,color='b')
   ax.plot([star.T],[L],'o',markersize=5,markeredgecolor='none',color='b')

#MARKS
dt=round(star.taumax/20,1)
logts=np.log10(np.arange(0.1,star.taums,dt))
Teffs=Teff_func(logts)
Leffs=10**logL_func(logts)
ax.plot(Teffs,Leffs,"ko",label='Steps of %%.1f Gyr'%%dt,markersize=3)
ax.text(TSUN,1.0,r"$\odot$",fontsize=14)

ax.set_yscale('log')
ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$L/L_{\\rm Sun}$")

Tmin,Tmax=ax.get_xlim()
xmin,xmax=ax.get_xlim()
ax.set_xlim((xmax,xmin))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes)

ax.legend(loc='lower right')
"""%(star_dir,star_dir,
     evodata_str,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-radius",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

evodata=%s
ts=evodata[:,0]
logrho_func,Teff_func,logR_func,logL_func=evoFunctions(evodata)

bbox=dict(fc='w',ec='none')

#LINES
ts=ts[ts>=0.1]
ts=ts[ts<=star.taums]

logts=np.log10(ts)
Teffs=Teff_func(logts)
Rs=10**logR_func(logts)
ax.plot(Teffs,Rs,"k-")
ax.plot(Teffs[0:1],Rs[0:1],"ko",markersize=5)
ax.plot([Teffs[0]],[Rs[0]],"go",markersize=10,markeredgecolor='none',label=r"$t_{\\rm ini}=$0.1 Gyr")
ax.plot([Teffs[-1]],[Rs[-1]],"ro",markersize=10,markeredgecolor='none',label=r"$t_{\\rm end}=$%%.1f Gyr"%%star.taums)
ax.plot([star.Tins],[star.Rins],"bo",markersize=10,markeredgecolor='none',label=r"$t=$%%.1f Gyr"%%star.tau)

#EVOLUTIONARY TRACK
dt=round(star.taumax/20,1)
logts=np.log10(np.arange(0.1,star.taums,dt))
Teffs=Teff_func(logts)
Rs=10**logR_func(logts)
ax.plot(Teffs,Rs,"ko",label='Steps of %%.1f Gyr'%%dt,markersize=3)
ax.text(1.0,1.0,r"$\odot$",fontsize=14)

if star.R>0 and star.T>0:
   star.Terr=max(star.Terr,0.0)
   star.Rerr=max(star.Rerr,0.0)
   ax.errorbar(star.T,star.R,xerr=star.Terr,yerr=star.Rerr,linewidth=2,color='b')
   ax.plot([star.T],[star.R],'o',markersize=5,markeredgecolor='none',color='b')

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$R/R_{\\rm Sun}$")

Tmin,Tmax=ax.get_xlim()
ax.set_xlim((Tmax,Tmin))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes)

ax.legend(loc='best',prop=dict(size=10))
"""%(star_dir,star_dir,
     evodata_str,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-logg",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
evoInterpFunctions(star)
ts=star.evotrack[:,0]

bbox=dict(fc='w',ec='none')

#LINES
ts=ts[ts>=0.1]
ts=ts[ts<=star.taums]

Teffs=star.Tfunc(ts)
loggs=np.log10(star.gfunc(ts))
ax.plot(Teffs,loggs,"k-")
ax.plot(Teffs[0:1],loggs[0:1],"ko",markersize=5)
ax.plot([Teffs[0]],[loggs[0]],"go",markersize=10,markeredgecolor='none',label=r"$t_{\\rm ini}=$0.1 Gyr")
ax.plot([Teffs[-1]],[loggs[-1]],"ro",markersize=10,markeredgecolor='none',label=r"$t_{\\rm end}=$%%.1f Gyr"%%star.taums)
ax.plot([star.Tins],[np.log10(star.gins)],"bo",markersize=10,markeredgecolor='none',label=r"$t=$%%.1f Gyr"%%star.tau)

#EVOLUTIONARY TRACK
dt=round(star.taumax/20,1)
ts=np.arange(0.1,star.taums,dt)
Teffs=star.Tfunc(ts)
loggs=np.log10(star.gfunc(ts))
ax.plot(Teffs,loggs,"ko",label='Steps of %%.1f Gyr'%%dt,markersize=3)
ax.text(1.0,1.0,r"$\odot$",fontsize=14)

if star.logg>0 and star.T>0:
   star.Terr=max(star.Terr,0.0)
   star.loggerr=max(star.loggerr,0.0)
   ax.errorbar(star.T,star.logg,xerr=star.Terr,yerr=star.loggerr,linewidth=2,color='b')
   ax.plot([star.T],[star.logg],'o',markersize=5,markeredgecolor='none',color='b')

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$\log\ g$")

Tmin,Tmax=ax.get_xlim()
ax.set_xlim((Tmax,Tmin))
ymin,ymax=ax.get_ylim()
ax.set_ylim((ymax,ymin))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes)

ax.legend(loc='best',prop=dict(size=10))
"""%(star_dir,star_dir,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#MOMENT OF INERTIA EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-RMoI",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,8))
l=0.1;b=0.1;w=0.85;h=0.55;ho=0.01
ax_dI=fig.add_axes([l,b,w,h/2])
b+=h/2+ho
ax_I=fig.add_axes([l,b,w,h])

star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
evoInterpFunctions(star)

#MAIN PLOT
ts=star.RMoI[:,0]
I=star.RMoI[:,3]*MSUN*RSUN**2
Imin=min(I);Imax=max(I)
dIdt=star.RMoI[:,4]*MSUN*RSUN**2/GYR

ax_dI.plot(ts,np.abs(dIdt)/I,'-')
ax_I.plot(ts,I,'-')

#DECORATIONS
for ax in ax_I,ax_dI:
    ax.set_xscale('log')
    ax.set_yscale('log')

#I-TICKS
ax_I.set_ylim((Imin,Imax))
It=[];Il=[]
for I in np.linspace(Imin,Imax,10):
    It+=[I]
    Il+=["%%.2f"%%np.log10(I)]
ax_I.set_yticks(It)
ax_I.set_yticklabels(Il,fontsize=10)

ax_I.set_xticklabels([])
dIl=ax_dI.get_yticks()
ax_dI.set_yticks(dIl[:-1])

ax_I.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax_dI.set_xlabel(r"$\\tau$ (Gyr)")
ax_I.set_ylabel(r"$\log\,I$ (kg m$^2$)")
ax_dI.set_ylabel(r"$-|dI/dt|/I$ (s$^{-1}$)")

ax_I.set_xlim((TAU_MIN,star.taums))
ax_dI.set_xlim((TAU_MIN,star.taums))

ax_I.grid()
ax_dI.grid()

#MODEL WATERMARK
ax_I.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax_I.transAxes)

"""%(star_dir,star_dir,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS SCHEMATIC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"radius-schematic",\
"""
from BHM.BHMstars import *
fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.0,0.0,1.0,1.0])
bbox=dict(fc='w',ec='none')

star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

StarID='%s'
M=%.3f
Z=%.4f
tau=%.3f
R=%.3f
T=%.1f

color=cm.RdYlBu((T-2000)/7000)

starc=patches.Circle((0.0,0.0),R,fc=color,ec='none')
sun=patches.Circle((0.0,0.0),1.0,
                   linestyle='dashed',fc='none',zorder=10)
ax.add_patch(starc)
ax.add_patch(sun)
ax.text(0.0,1.0,'Sun',fontsize=12,transform=offSet(0,5),horizontalalignment='center',verticalalignment='bottom',color=cm.gray(0.5),bbox=bbox,zorder=10)
ax.text(0.0,-R,star.str_StarID.replace("'",""),fontsize=12,transform=offSet(0,-5),horizontalalignment='center',verticalalignment='top',color=cm.gray(0.5),bbox=bbox,zorder=10)

if star.R>0:
   starobs=patches.Circle((0.0,0.0),star.R,
                          linestyle='solid',fc='none',zorder=10,color='b')
   ax.add_patch(starobs)

ax.set_xticks([])
ax.set_yticks([])

if len(star.str_StarID)>0:startitle="%%s: "%%star.str_StarID
else:startitle=""
ax.set_title(r"%%s$M = %%.3f\,M_{\odot}$, $Z=$%%.4f, $\\tau=%%.3f$ Gyr, $R = %%.3f\,R_{\odot}$, $T_{\\rm eff} = %%.1f$ K"%%(startitle,M,Z,tau,R,T),
position=(0.5,0.05),fontsize=14)

rang=max(1.5*R,1.5)
ax.set_xlim((-rang,+rang))
ax.set_ylim((-rang,+rang))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes)

"""%(star_dir,star_dir,
     star.str_StarID,star.M,star.Z,star.tau,R,Teff,modelwat),watermarkpos="inner")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STELLAR ROTATION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"stellar-rotation",\
"""
from BHM.BHMstars import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

ts=star.rotevol[:,0]
w=star.rotevol[:,1]

ax.plot(ts,w/OMEGASUN)
ax.plot(ts,(ts/TAGE)**(-0.5),label='Skumanich Relationship')
ax.plot([],[],'r--',label='Saturation')

if star.Prot>0:
     Prot=star.Prot;
     Proterr=max(star.Proterr,0.0);
     wmax=PSUN/DAY/(Prot-Proterr);wmin=PSUN/DAY/(Prot+Proterr);
     ax.axhspan(wmin,wmax,color='b',alpha=0.3)

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)

bbox=dict(fc='w',ec='none')
ax.text(0.5,0.08,r"$\\tau_{\\rm disk}$=%%.3f Gyr, $\Omega_{\\rm sat}$ = %%.2f $\Omega_\odot$, $K_{\\rm W}$ = %%.2e"%%(star.taudisk,star.wsat_scaled,star.Kw),
transform=ax.transAxes,horizontalalignment='center',bbox=bbox)

ax.set_xlim((TAU_MIN,star.taums))
ax.set_xlim((TAU_MIN,12.0))

ax.text(1.07,0.5,r"$P$ (days)",rotation=90,verticalalignment='center',horizontalalignment='center',transform=ax.transAxes)
ax.axhline(star.wsat_scaled,linestyle='--',linewidth=2,color='r')

for star_name in ROTAGE_STARS.keys():
    staro=ROTAGE_STARS[star_name]
    tau=staro["tau"]
    Prot=staro["Prot"]
    ax.plot([tau],[2*PI/(Prot*DAY)/OMEGASUN],'o',markersize=10,markeredgecolor='none',color=cm.gray(0.5),zorder=-10)
    ax.text(tau,2*PI/(Prot*DAY)/OMEGASUN,star_name,fontsize=14,transform=offSet(-10,staro["up"]),horizontalalignment="right",color=cm.gray(0.5),zorder=-10)

#PERIODS
tmin,tmax=ax.get_xlim()
wmin,wmax=ax.get_ylim()
Pmin=2*PI/(wmax*OMEGASUN)/DAY
Pmax=2*PI/(wmin*OMEGASUN)/DAY

for P in np.logspace(np.log10(Pmin),np.log10(Pmax),10):
    #P=np.ceil(P)
    if P>Pmax:break
    w=2*PI/(P*DAY)/OMEGASUN
    ax.axhline(w,xmin=0.98,xmax=1.00,color='k')
    ax.text(tmax,w,"%%.1f"%%P,transform=offSet(5,0),verticalalignment='center',horizontalalignment='left',fontsize=10)

ax.set_ylabel("$\Omega/\Omega_\odot$")
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.grid(which='both')
ax.legend(loc='best')

"""%(star_dir,star_dir))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#MASS-LOSS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"stellar-massloss",\
"""
from BHM.BHMstars import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.15,0.1,0.8,0.8])

ts=star.activity[:,0]
Ml=star.activity[:,7]

ax.plot(ts,Ml)

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlim((TAU_MIN,star.taums))

ax.set_ylabel(r"$\dot M$ ($M_\odot$/yr)")
ax.set_xlabel(r"$\\tau$ (Gyr)")

ax.grid(which='both')
"""%(star_dir,star_dir))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#XUV LUMINOSITY
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"stellar-LXUV",\
"""
from BHM.BHMstars import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.15,0.1,0.8,0.8])

ts=star.activity[:,0]
LXUV=star.activity[:,13]

ax.plot(ts,LXUV/(LXSUN/1E7))

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlim((TAU_MIN,star.taums))

ax.set_ylabel(r"$L_{\\rm XUV}/L_{\\rm XUV,\odot,present}$")
ax.set_xlabel(r"$\\tau$ (Gyr)")

ax.grid(which='both')
"""%(star_dir,star_dir))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ACTIVITY 
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"stellar-activity",\
"""
from BHM.BHMstars import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

Ni=3
fig=plt.figure(figsize=(8,6*(Ni-1)))
l=0.1;b=0.05;dh=0.02;h=(1.0-2*b-(Ni-1)*dh)/Ni;w=1.0-1.5*l

ax_R=fig.add_axes([l,b,w,h])
b+=h+dh
ax_f=fig.add_axes([l,b,w,h])
b+=h+dh
ax_B=fig.add_axes([l,b,w,h])

ts=star.activity[:,0]
f=star.activity[:,2]
B=star.activity[:,4]
R=star.activity[:,6]
axs=[ax_R,ax_f,ax_B]

args=dict(color='k')
ax_R.plot(ts,R,**args)
ax_R.set_ylabel("Rossby Number")
ax_R.axhline(0.13,linestyle='--',linewidth=2,label='Saturation Level')

ax_f.plot(ts,f,**args)
ax_f.set_ylabel("Filling factor, $f_\star$")
ax_B.plot(ts,B,**args)
ax_B.set_ylabel("Photospheric field, $B_\star$")

for ax in axs:
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim((TAU_MIN,star.taums))
    ax.grid(which='both')
    ax.legend(loc='best',prop=dict(size=12))

axs[-1].set_title(star.title,position=(0.5,1.02),fontsize=12)
axs[0].set_xlabel(r"$\\tau$ (Gyr)")

for ax in axs[1:]:
    ax.set_xticklabels([])

"""%(star_dir,star_dir))

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(star_dir+"star.html","w")
fh.write("""\
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>
<h2>Stellar Properties</h2>
<center>
  <a href="%s/radius-schematic.png" target="_blank">
    <img width=60%% src="%s/radius-schematic.png">
  </a>
  <br/>
  <i>Schematic Representation</i>
  (
  <a href="%s/radius-schematic.png.txt" target="_blank">data</a>|
  <a href="%s/BHMreplot.php?dir=%s&plot=radius-schematic.py" target="_blank">replot</a>
  )
</center>
</table>
<h3>Input properties</h3>
<table>
  <tr><td>Mass (M<sub>sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>Z:</td><td>%.4f</td></tr>
  <tr><td>[Fe/H] (dex):</td><td>%.2f</td></tr>
  <tr><td>&tau; (Gyr):</td><td>%.2f</td></tr>
  <tr><td>&tau;<sub>max</sub> (Gyr):</td><td>%.2f</td></tr>
  <tr><td>&tau;<sub>MS</sub> (Gyr):</td><td>%.2f</td></tr>
  <tr><td>Hash:</td><td>%s</td></tr>
</table>

<h3>Rotational Evolution Properties</h3>
<table>
  <tr><td>P<sub>PMS</sub> (days):</td><td>%.3f</td></tr>
  <tr><td>&omega;<sub>sat</sub> (&omega;<sub>Sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>&tau;<sub>disk</sub> (Gyr):</td><td>%.3f</td></tr>
  <tr><td>Wind torque constant, K<sub>W</sub>:</td><td>%.3e</td></tr>
  <tr><td>Dynamo exponent, a:</td><td>%.1f</td></tr>
  <tr><td>Field geometry exponent, n:</td><td>%.1f</td></tr>
  <tr><td>&tau;<sub>conv</sub> (days):</td><td>%.3f</td></tr>
  <tr><td>Scaled &omega;<sub>sat</sub> (&omega;<sub>Sun</sub>):</td><td>%.3f</td></tr>
</table>

<h3>Instantaneous theoretical properties:</h3>
<table>
  <tr><td>g (m/s<sup>2</sup>):</td><td>%.2f</td></tr>
  <tr><td>T<sub>eff</sub> (K):</td><td>%.2f</td></tr>
  <tr><td>R/R<sub>sun</sub>:</td><td>%.3f</td></tr>
  <tr><td>L/L<sub>sun</sub>:</td><td>%.3f</td></tr>
  <tr><td>MoI=I/MR<sup>2</sup>:</td><td>%.3f</td></tr>
  <tr><td>t<sub>diss</sub> (yr):</td><td>%.3f</td></tr>
</table>
<h3>Circumstellar Habitable Zone:</h3>
<table>
  <tr><td>l<sub>in</sub> (AU):</td><td>(Recent Venus) %.2f, (Runaway Greenhouse) %.2f, (Moist Greenhous) %.2f</td></tr>
  <tr><td>l<sub>out</sub> (AU):</td><td>(Maximum Greenhouse) %.2f, (Early Mars) %.2f</td></tr>
</table>

<h3>Evolution of Stellar Properties:</h3>
<table>
  <tr><td>
      <a href="%s/stellar-props.png" target="_blank">
	<img width=100%% src="%s/stellar-props.png">
      </a>
      <br/>
      <i>Evolution of stellar properties</i>
	(
	<a href="%s/stellar-props.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=stellar-props.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/evol-track.png" target="_blank">
	<img width=100%% src="%s/evol-track.png">
      </a>
      <br/>
      <i>Evolutionary Track</i>
	(
	<a href="%s/evol-track.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=evol-track.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/evol-radius.png" target="_blank">
	<img width=100%% src="%s/evol-radius.png">
      </a>
      <br/>
      <i>Radius Evolution</i>
	(
	<a href="%s/evol-radius.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=evol-radius.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/evol-logg.png" target="_blank">
	<img width=100%% src="%s/evol-logg.png">
      </a>
      <br/>
      <i>Surface Gravity Evolution</i>
	(
	<a href="%s/evol-logg.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=evol-logg.py" target="_blank">replot</a>
	)
  </td></tr>
</table>
<h3>Evolution of stellar rotation and magnetic activity:</h3>
<table>
  <tr><td>
      <a href="%s/evol-RMoI.png" target="_blank">
	<img width=100%% src="%s/evol-RMoI.png">
      </a>
      <br/>
      <i>Moment of Inertia Evolution</i>
	(
	<a href="%s/evol-RMoI.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=evol-RMoI.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/stellar-rotation.png" target="_blank">
	<img width=100%% src="%s/stellar-rotation.png">
      </a>
      <br/>
      <i>Stellar Rotation Evolution</i>
	(
	<a href="%s/stellar-rotation.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=stellar-rotation.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/stellar-massloss.png" target="_blank">
	<img width=100%% src="%s/stellar-massloss.png">
      </a>
      <br/>
      <i>Stellar Mass-Loss</i>
	(
	<a href="%s/stellar-massloss.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=stellar-massloss.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/stellar-LXUV.png" target="_blank">
	<img width=100%% src="%s/stellar-LXUV.png">
      </a>
      <br/>
      <i>XUV Luminosity</i>
	(
	<a href="%s/stellar-LXUV.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=stellar-LXUV.py" target="_blank">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/stellar-activity.png" target="_blank">
	<img width=100%% src="%s/stellar-activity.png">
      </a>
      <br/>
      <i>Dynamo and magnetic field properties</i>
	(
	<a href="%s/stellar-activity.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=stellar-activity.py" target="_blank">replot</a>
	)
  </td></tr>
</table>
"""%(WEB_DIR,star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star.M,star.Z,star.FeH,star.tau,star.tau_max,star.tau_ms,star_hash,
star.Pini,star.wsat,star.taudisk,star.Kw,star.a,star.n,tauconv,WSATSUN*TAUCSUN/tauconv,
g,Teff,R,L,star.MoI,tdiss,
lins[0],lins[1],lins[2],
louts[0],louts[1],
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
closeObject(star_dir)
