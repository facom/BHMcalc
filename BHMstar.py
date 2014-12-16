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

#*PROPERTY*#
star.hash=star_hash
star.Ycal=star.Y
star.Zcal=star.Z
star.FeHcal=star.FeH

###################################################
#LOAD MODEL TRACK
###################################################
PRINTOUT("Finding the closest evolutionary track...")
#FIND STELLAR EVOLUTION TRACK
model=star.str_model.replace("'","")
pfind,startrack=findTrack(model,star.Z,star.M,verbose=True)
trackfunc=trackFunctions(startrack)
trackarr=trackArrays(startrack)
modelwat="%s:Z=%.4f,M=%.2f"%(model,pfind[0],pfind[2])

#*PROPERTY*#
star.Yuse=star.Ycal
star.Zuse=pfind[0]
star.Muse=pfind[2]

###################################################
#STELLAR EVOLUTION PROPERTIES INTERPOLATION
###################################################
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

#========================================
#SAMPLING TIMES
#========================================
exp_ts1=np.linspace(np.log10(max(TAU_MIN,tau_ini)),np.log10(tau_end/2),NTIMES/2)
exp_ts2=-np.linspace(-np.log10(min(TAU_MAX,tau_end)),-np.log10(tau_end/2),NTIMES/2)
ts=np.unique(np.concatenate((10**exp_ts1,(10**exp_ts2)[::-1])))

#========================================
#EVOLUTIONARY MATRIX
#========================================
PRINTOUT("Calculating Evolutionary Matrix...")
evodata=np.array([np.array([t]+list(StellarGTRL(star.Z,star.M,t))) for t in ts])
maxdata=evodata[:,1]>0
evodata=evodata[maxdata]

#*PROPERTY*#
star.evotrack=evodata

#========================================
#MAXIMUM ALLOWABLE TIME
#========================================
#*PROPERTY*#
star.tau_min=evodata[0,0]
star.tau_max=evodata[-1,0]

PRINTOUT("Minimum age in model = %.3f"%star.tau_min)
PRINTOUT("Maximum age in model = %.3f"%star.tau_max)

#========================================
#DETECTING END OF HYDROGEN BURNING PHASE
#========================================
ts=evodata[:,0]
Rs=evodata[:,3]
if star.taums==0:
     PRINTOUT("Detecting the end of Hydrogen Burning Phase...")
     tau_ms=disconSignal(ts,Rs,
                         tausys=star.tau_max/2,
                         iper=3,dimax=10)
else:tau_ms=star.taums

#*PROPERTY*#
star.tau_ms=min(tau_ms,star.tau_max)

PRINTOUT("End of Hydrogen Burning Phase = %.3f"%star.tau_ms)

if star.tau>star.tau_ms:
     PRINTERR("We cannot simulate the star beyond the Hydrogen Burning phase (provided age %.2f Gyr)"%star.tau)
     errorCode("INPUT_ERROR")

###################################################
#RADIUS AND MOMENT OF INERTIA EVOLUTION
###################################################
#========================================
#LOAD MOI DATA
#========================================
PRINTOUT("Loading MoI model...")
MoIdata=interpolMoI(star.M,verbose=True)
logtmoi,MoIfunc=interpMatrix(MoIdata)

#========================================
#EVOLUTION OF MOMENT OF INERTIA
#========================================
Ievot=stack(7)
logIrad=0
logtrad=logtmoi[0]
for logt in logtmoi[::-1]:
     t=10**logt

     #BULK MOI
     logMR2=np.log10((star.M*MSUN*1E3)*(trackfunc.R(t)*RSUN*1E2)**2)

     #TOTAL K2 AND MOI
     k2=MoIfunc[8](logt)
     logk2=np.log10(k2)
     logItot=logk2+logMR2

     #CONVECTIVE K2 AND MOI
     kconv2=MoIfunc[9](logt)
     logkconv2=np.log10(kconv2)
     logIconv=logkconv2+logMR2

     #RADIATIVE K2 AND MOI
     krad2=MoIfunc[10](logt)
     if krad2>0:
          Irad=krad2*10**logMR2
     elif logtrad==logtmoi[0]:
          logtrad=logt
          Irad=0

     #RADIUS AND MASS OF RADIUS 
     Rrad=MoIfunc[14](logt)
     Mrad=MoIfunc[15](logt)

     #APSIDAL MOTION CONSTANT
     ka2=apsidalMotionConstant(k2)

     #DERIVATIVE OF INERTIA MOMENT
     Ievot+=[logt,logIconv-7.0,Irad/1E7,logItot-7.0,Rrad*RSUN,Mrad*MSUN,ka2]

PRINTOUT("Time of formation of the radiative core: %.2f"%logtrad)
Ievot=Ievot.array[::-1]
logtmoi,Ievot_funcs=interpMatrix(Ievot)

#========================================
#CONTRACTION TORQUES
#========================================
logtini=logtmoi[0]
logtend=logtmoi[-1]
dlogt=(logtend-logtini)/300

"""
Ievo:
0:t
1:log(Iconv)
2:log(Irad)
3:log(Itot)
4:Rrad
5:Mrad
6:d(log Iconv)/dt
7:d(log Irad)/dt
8:d(log Itot)/dt
9:Rrad^2/Itot dMrad/dt
10:dMrad/dt
11:k_2, apsidal motion constant
"""
Ievo=stack(12)
for logt in np.arange(logtini+dlogt,logtend-dlogt,dlogt):

     #TIME
     t=10**logt

     #BASIC QUANTITIES
     logIconv=Ievot_funcs[1](logt)
     Irad=Ievot_funcs[2](logt)
     logItot=Ievot_funcs[3](logt)
     Rrad=Ievot_funcs[4](logt)
     Mrad=Ievot_funcs[5](logt)
     ka2=Ievot_funcs[6](logt)

     #DERIVATIVES
     
     #CONVECTIVE ENVELOPE
     dlogIcondlogt=derivative(Ievot_funcs[1],logt,dlogt)
     dlogIcondt=dlogIcondlogt/(t*YEAR)

     #RADIATIVE ENVELOPE
     dIraddlogt=derivative(Ievot_funcs[2],logt,dlogt)
     dIraddt=dIraddlogt/(t*YEAR)
     if Irad>0:dlogIraddt=dIraddt/Irad
     else:dlogIraddt=0.0

     #TOTAL
     dlogItotdlogt=derivative(Ievot_funcs[3],logt,dlogt)
     dlogItotdt=dlogItotdlogt/(t*YEAR)

     #MASS TRANSFER
     dMdlogt=derivative(Ievot_funcs[5],logt,dlogt)
     dMdt=dMdlogt/(t*YEAR)

     #TORQUE DUE TO MASS TRANSFER
     dlogIcomdt=2./3*Rrad**2*dMdt/10**logIconv
     if Irad>0:dlogIramdt=2./3*Rrad**2*dMdt/Irad
     else:dlogIramdt=0.0

     """
     print "Time: t = %e, logt = %.2f"%(t,logt)
     print "Inertia moments:"
     print "\tItot = %e"%10**logItot
     print "\tIcon = %e"%10**logIconv
     print "\tIrad = %e"%Irad
     print "\tRrad = %e"%Rrad
     print "\tMrad = %e"%Mrad
     
     print "Full logarithmic derivatives:"
     print "\td(log Itot)/d(log t) = %e"%dlogItotdlogt
     print "\td(log Iconv)/d(log t) = %e"%dlogIcondlogt
     print "\tdIrad/d(log t) = %e"%dIraddlogt
     print "\tdM/dt = %e Msun/year"%(dMdt*YEAR/MSUN)

     print "Logarithmic derivatives:"
     print "\td(log Itot)/dt = %e"%dlogItotdt
     print "\td(log Iconv)/dt) = %e"%dlogIcondt
     print "\td(log Irad)/dt = %e"%dlogIraddt
     print "\td(log Iconv,mass)/dt = %e"%dlogIcomdt
     print "\td(log Irad,mass)/dt = %e"%dlogIramdt
     if logt>logtrad:raw_input()
     #"""

     Ievo+=[logt,logIconv,Irad,logItot,Rrad,Mrad*MSUN,
            dlogIcondt,dlogIcomdt,dlogIraddt,dlogIramdt,dMdt,ka2]

Ievo=Ievo.array
logtmoi=Ievo[:,0]
tsmoi=10**Ievo[:,0]/GIGA
Nsmoi=len(tsmoi)
cond=Ievo[:,0]>logtrad

fig=plt.figure()
axdI=fig.add_axes([0.1,0.1,0.8,0.2])
axI=fig.add_axes([0.1,0.33,0.8,0.6])

axI.plot(Ievo[:,0],Ievo[:,1],label='Convective',color='b')
axI.plot(Ievo[cond,0],np.log10(Ievo[cond,2]),label='Radiative',color='r')
axI.plot(Ievo[:,0],Ievo[:,3],label='Total',color='g')

axdI.plot(Ievo[:,0],Ievo[:,6],color='b')
axdI.plot(Ievo[:,0],Ievo[:,8],color='r')
axdI.plot(Ievo[:,0],Ievo[:,7],color='b')
axdI.plot(Ievo[:,0],Ievo[:,9],color='r')

#axI.set_ylim((51,56))
axI.set_xticklabels([])
axI.legend(loc="best")
#axdI.set_ylim((-1E-12,1E-12))
for ax in axI,axdI:
     ax.set_xlim((logtmoi[0],logtmoi[-1]))
     ax.grid(which="both")
     ax.set_xlim((6,6.5))
fig.savefig("tests/moi.png")

#*PROPERTY*#
star.Ievo=Ievo
star.tmoi_min=tsmoi[0]
star.tmoi_max=tsmoi[-1]
PRINTOUT("Limits for rotational evolution simulation: [%.2f,%.2f]"%(star.tmoi_min,
                                                                    star.tmoi_max))

if star.tau>star.tmoi_max:
     PRINTERR("We cannot simulate rotation beyond model maximum (provided age %.2f Gyr)"%star.tau)
     errorCode("INPUT_ERROR")

###################################################
#ROTATION EVOLUTION
###################################################
PRINTOUT("Calculating rotation evolution...")
evoInterpFunctions(star)

#CONVECTIVE TURNOVER AT 200 Myr
tauconv=convectiveTurnoverTime(star.Tfunc(0.2))

#*PROPERTY*#
star.tauconv=tauconv

#INITIAL ROTATIONAL RATE
wini=2*PI/(star.Pini*DAY)

#SATURATION
if star.wsat==0:
     wsat_scaled=WSATSUN*TAUCSUN/tauconv
else:
     wsat_scaled=star.wsat

#*PROPERTY*#
star.wsat_scaled=wsat_scaled

#INTEGRATION
rotpars=dict(\
     star=star,
     starf=None,binary=None,
     model=star.str_rotmodel.replace("'",""),
     taucont=TAU_CONT,
     fdiss=1.0
     )
Omega_ini=np.array([wini,wini])
rotevol=odeint(rotationalTorques,Omega_ini,tsmoi*GYR,args=(rotpars,))

#*PROPERTY*#
"""
rotevol:
0:t
1:Omega_conv
2:Omega_rad
"""
star.rotevol=toStack(tsmoi)|toStack(rotevol)
trots,rotevol_funcs=interpMatrix(star.rotevol)

#print 2*PI/rotevol_funcs[1](TAGE)/DAY;exit(0)

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
for i in range(0,Nsmoi):
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
     
#*PROPERTY*#
star.activity=toStack(tsmoi)|star.activity
tacts,activity_funcs=interpMatrix(star.activity)

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

#MOMENT OF INERTIA
#*PROPERTY*#

#INSTANTANEOUS PROPERTIES
star.gins=g
star.Tins=Teff
star.Rins=R
star.Lins=L
star.tdiss=tdiss
star.lins=lins
star.lsun=lsun
star.louts=louts

#MOMENT OF INERTIA
star.logIconv=star.logIconfunc(np.log10(star.tau*GIGA))
star.Irad=star.Iradfunc(np.log10(star.tau*GIGA))
if star.Irad>0:star.logIrad=np.log10(star.Irad)
star.logItot=star.logItotfunc(np.log10(star.tau*GIGA))
star.omegaconv=rotevol_funcs[1](star.tau)
star.Pconv=2*PI/star.omegaconv/DAY
star.omegarad=rotevol_funcs[2](star.tau)
star.Prad=2*PI/star.omegarad/DAY
star.vsurf=2*PI*star.Rins*RSUN/1E3*star.omegaconv

#ACTIVITY
star.fstar=activity_funcs[2](star.tau)
star.Bstar=star.fstar*activity_funcs[4](star.tau)
star.Ro=activity_funcs[6](star.tau)
star.Mdot=activity_funcs[7](star.tau)
star.RX=activity_funcs[11](star.tau)
star.LX=activity_funcs[12](star.tau)
star.LXUV=activity_funcs[13](star.tau)

#TITLE
PRINTOUT("Star ID: %s"%star.str_StarID)
star.str_StarID=star.str_StarID.replace("'","")
PRINTOUT("Star ID: %s"%star.str_StarID)
title=r"%s: $M_{\\rm star}/M_{\odot}$=%.2f, $Z$=%.4f, $[Fe/H]$=%.2f, $\\tau$=%.2f Gyr"%(star.str_StarID,star.M,star.Z,star.FeH,star.tau)

#*PROPERTY*#
star.title=title

###################################################
#STORE STELLAR DATA
###################################################
PRINTOUT("Storing stellar data...")
f=open(star_dir+"star.data","w")
f.write("""\
from numpy import array
#OBJECT HASH
hash="%s"

#COMPOSITION
Ycal=%.17e
Zcal=%.17e
FeHcal=%.17e

#USED EVOLUTIONARY TRACK
Yuse=%.17e
Zuse=%.17e
Muse=%.17e

#EVOLUTIONARY TRACK
evotrack=%s

#EXTREME AGES
tau_min=%.17e #Gyr
tau_max=%.17e #Gyr
tau_ms=%.17e #Gyr

#EVOLUTIONARY MoI
Ievo=%s
tmoi_min=%.17e
tmoi_max=%.17e

#CONVECTIVE TURNOVER TIME AT 200 MYR
tauconv=%.17e #Myrs

#ROTATIONAL EVOLUTION
wsat_scaled=%.17e #W_Sun
rotevol=%s

#ACTIVITY
activity=%s

#INSTANTANEOUS PROPERTIES
title="%s"

#INSTANTANEOUS PROPERTIES
gins=%.17e #m/s^2
Tins=%.17e #L
Rins=%.17e #Rsun
Lins=%.17e #Lsun
tdiss=%.17e #s

#ROTATION AND INERTIA MOMENT
logIconv=%.17e #log(I_conv[g cm^2])
logIrad=%.17e #log(I_rot[g cm^2])
logItot=%.17e #log(I_tot[g cm^2])
omegaconv=%.17e #s^-1
omegarad=%.17e #s^-1
Pconv=%.17e #days
Prad=%.17e #days
vsurf=%.17e #km/s

#ACTIVITY INDICATORS
fstar=%.17e 
Bstar=%.17e #Gauss
Ro=%.17e
Mdot=%.17e #Msun yr^-1
RX=%.17e 
LX=%.17e #W
LXUV=%.17e #W

#HABITABLE ZONE
lins=%s #AU
lsun=%.17e #AU
louts=%s #AU
"""%(star.hash,
     star.Ycal,star.Zcal,star.FeHcal,
     star.Yuse,star.Zuse,star.Muse,
     array2str(star.evotrack),
     star.tau_min,star.tau_max,star.tau_ms,
     array2str(star.Ievo),
     star.tmoi_min,star.tmoi_max,
     star.tauconv,star.wsat_scaled,
     array2str(star.rotevol),
     array2str(star.activity),
     star.title,
     star.gins,star.Tins,star.Rins,star.Lins,
     star.tdiss,
     star.logIconv,star.logIrad,star.logItot,
     star.omegaconv,star.omegarad,
     star.Pconv,star.Prad,star.vsurf,
     star.fstar,star.Bstar,star.Ro,star.Mdot,
     star.RX,star.LX,star.LXUV,
     array2str(star.lins),
     star.lsun,
     array2str(star.louts),
     ))
f.close()

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(star_dir+"star.html","w")
fh.write("""\
<html>
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>
<body>
<h2>Properties of Star %s</h2>
<h3>Plots</h3>
<h4>Schematic Representation</h4>
<table>
<tr><td>
    <a href="%s/radius-schematic.png" target="_blank">
      <img width=100%% src="%s/radius-schematic.png">
    </a>
    <br/>
    <div class="caption">
    <i>Schematic Representation</i>
    (
    <a href="%s/radius-schematic.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=radius-schematic.py" target="_blank">replot</a>
    )
    </div>
</td></tr>
</table>

<h4>Stellar Evolution</h4>

<table>
<tr><td>
    <a href="%s/stellar-props.png" target="_blank">
      <img width=100%% src="%s/stellar-props.png">
    </a>
    <br/>
    <div class="caption">
    <i>Properties Evolution</i>
    (
    <a href="%s/stellar-props.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=stellar-props.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

<tr><td>
    <a href="%s/evol-radius.png" target="_blank">
      <img width=100%% src="%s/evol-radius.png">
    </a>
    <br/>
    <div class="caption">
    <i>Radius Track</i>
    (
    <a href="%s/evol-radius.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=evol-radius.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

<tr><td>
    <a href="%s/evol-logg.png" target="_blank">
      <img width=100%% src="%s/evol-logg.png">
    </a>
    <br/>
    <div class="caption">
    <i>Gravitation Track</i>
    (
    <a href="%s/evol-logg.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=evol-logg.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

<tr><td>
    <a href="%s/evol-moi.png" target="_blank">
      <img width=100%% src="%s/evol-moi.png">
    </a>
    <br/>
    <div class="caption">
    <i>Moment of Inertia</i>
    (
    <a href="%s/evol-moi.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=evol-moi.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

</table>

<h4>Rotation and Activity</h4>
<table>

<tr><td>
    <a href="%s/stellar-rotation.png" target="_blank">
      <img width=100%% src="%s/stellar-rotation.png">
    </a>
    <br/>
    <div class="caption">
    <i>Rotation Evolution</i>
    (
    <a href="%s/stellar-rotation.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=stellar-rotation.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

<tr><td>
    <a href="%s/stellar-massloss.png" target="_blank">
      <img width=100%% src="%s/stellar-massloss.png">
    </a>
    <br/>
    <div class="caption">
    <i>Mass-loss</i>
    (
    <a href="%s/stellar-massloss.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=stellar-massloss.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

<tr><td>
    <a href="%s/stellar-LXUV.png" target="_blank">
      <img width=100%% src="%s/stellar-LXUV.png">
    </a>
    <br/>
    <div class="caption">
    <i>XUV Luminosity</i>
    (
    <a href="%s/stellar-LXUV.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=stellar-LXUV.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

<tr><td>
    <a href="%s/stellar-activity.png" target="_blank">
      <img width=100%% src="%s/stellar-activity.png">
    </a>
    <br/>
    <div class="caption">
    <i>Activity Indicators</i>
    (
    <a href="%s/stellar-activity.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=stellar-activity.py" target="_blank">replot</a>
    )
    </div>
</td></tr>

</table>

<h3>Numerical Properties</h3>

<h4>Basic Input Properties</h4>
<table>
  <tr><td>M (M<sub>sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>Y:</td><td>%.4f</td></tr>
  <tr><td>Z:</td><td>%.4f</td></tr>
  <tr><td>A:</td><td>%.4f</td></tr>
  <tr><td>[Fe/H] (dex):</td><td>%.2f</td></tr>
  <tr><td>&tau; (Gyr):</td><td>%.2f</td></tr>
  <tr><td>Object ash:</td><td>%s</td></tr>
</table>

<h4>Observed Properties</h4>
<table>
  <tr><td>R (R<sub>sun</sub>):</td><td>%s &pm; %s</td></tr>
  <tr><td>T (K):</td><td>%s &pm; %s</td></tr>
  <tr><td>log g (cm/s<sup>2</sup>):</td><td>%s &pm; %s</td></tr>
  <tr><td>P<sub>rot</sub> (days):</td><td>%s &pm; %s</td></tr>
  <tr><td>v sin i (km/s):</td><td>%s &pm; %s</td></tr>
  <tr><td>P<sub>rot,v</sub> (days):</td><td>%s</td></tr>
  <tr><td>Spectral Type:</td><td>%s</td></tr>
</table>

<h4>Stellar Evoluion</h4>
<table>
  <tr><td>Model:</td><td>%s</td></tr>
  <tr><td>&tau;<sub>min</sub> (Gyr):</td><td>%.4f</td></tr>
  <tr><td>&tau;<sub>max</sub> (Gyr):</td><td>%.4f</td></tr>
  <tr><td>&tau;<sub>MS</sub> (Gyr):</td><td>%.4f</td></tr>
  <tr><td>&tau;<sub>rot,min</sub> (Gyr):</td><td>%.4f</td></tr>
  <tr><td>&tau;<sub>rot,max</sub> (Gyr):</td><td>%.4f</td></tr>
</table>

<h4>Rotational Evoluion Model</h4>
<table>
  <tr><td>Rotational Evolution Model:</td><td>%s</td></tr>
  <tr><td>&tau;<sub>disk</sub> (Gyr):</td><td>%.4f</td></tr>
  <tr><td>&omega; (&Omega;<sub>Sun</sub>):</td><td>%.4f</td></tr>
  <tr><td>P<sub>ini</sub> (days):</td><td>%.4f</td></tr>
  <tr><td>K<sub>W</sub>:</td><td>%.3e</td></tr>
  <tr><td>K<sub>1</sub>:</td><td>%.3e</td></tr>
  <tr><td>a:</td><td>%.3f</td></tr>
  <tr><td>n:</td><td>%.3f</td></tr>
</table>

<h4>Instantaneous Properties</h4>
<table>
  <tr><td>g (m/s<sup>2</sup>):</td><td>%.4f</td></tr>
  <tr><td>L (L<sub>Sun</sub>):</td><td>%.4f</td></tr>
  <tr><td>R (R<sub>Sun</sub>):</td><td>%.4f</td></tr>
  <tr><td>T (K):</td><td>%.4f</td></tr>
  <tr><td>log I<sub>conv</sub> (g cm<sup>2</sup>):</td><td>%.2f</td></tr>
  <tr><td>log I<sub>rad</sub> (g cm<sup>2</sup>):</td><td>%.2f</td></tr>
  <tr><td>log I<sub>tot</sub> (g cm<sup>2</sup>):</td><td>%.2f</td></tr>
  <tr><td>P<sub>conv</sub> (days):</td><td>%.2f</td></tr>
  <tr><td>P<sub>rad</sub> (days):</td><td>%.2f</td></tr>
  <tr><td>v<sub>surf</sub> (km/s):</td><td>%.2f</td></tr>
  <tr><td>f<sub>*</sub>:</td><td>%.2e</td></tr>
  <tr><td>B<sub>*</sub> (Gauss):</td><td>%.2f</td></tr>
  <tr><td>Ro:</td><td>%.2f</td></tr>
  <tr><td>dM/dt (M<sub>Sun</sub>/year):</td><td>%.2e</td></tr>
  <tr><td>R<sub>X</sub>:</td><td>%.2e</td></tr>
  <tr><td>L<sub>X</sub> (W):</td><td>%.3e</td></tr>
  <tr><td>L<sub>XUV</sub> (W):</td><td>%.3e</td></tr>
</table>

<h4>Habitable Zone</h4>

<table>
  <tr><td>l<sub>in</sub> (AU):</td><td>(Recent Venus) %.2f, (Runaway Greenhouse) %.2f, (Moist Greenhous) %.2f</td></tr>
  <tr><td>l<sub>out</sub> (AU):</td><td>(Maximum Greenhouse) %.2f, (Early Mars) %.2f</td></tr>
</table>

</body>
</html>
"""%(WEB_DIR,
     star.str_StarID,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star_webdir,star_webdir,star_webdir,WEB_DIR,star_webdir,
     star.M,star.Yuse,star.Zuse,star.A,star.FeH,
     star.tau,
     star.hash,
     tableValue(star.R,"%.4f",">0","-"),tableValue(star.Rerr,"%.1e",">0","-"),
     tableValue(star.T,"%.4f",">0","-"),tableValue(star.Terr,"%.1e",">0","-"),
     tableValue(star.logg,"%.2f",">0","-"),tableValue(star.loggerr,"%.1e",">0","-"),
     tableValue(star.Prot,"%.2f",">0","-"),tableValue(star.Proterr,"%.1e",">0","-"),
     tableValue(star.vsini,"%.2f",">0","-"),tableValue(star.vsinierr,"%.1e",">0","-"),
     tableValue(star.Protv,"%.2f",">0","-"),
     star.str_Stype,
     star.str_model,
     star.tau_min,star.tau_max,star.tau_ms,star.tmoi_min,star.tmoi_max,
     star.str_rotmodel,
     star.taudisk,star.wsat_scaled,star.Pini,star.Kw,star.K1,star.a,star.n,
     star.gins,star.Lins,star.Rins,star.Tins,
     star.logIconv,star.logIrad,star.logItot,
     star.Pconv,star.Prad,
     star.vsurf,
     star.fstar,star.Bstar,star.Ro,star.Mdot,star.RX,star.LX,star.LXUV,
     star.lins[0],star.lins[1],star.lins[2],
     star.louts[0],star.louts[1]
     ))
fh.close()

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
from BHM.BHMnum import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
bbox=dict(fc='w',ec='none')

ts,evotrack=interpMatrix(star.evotrack)
yplot=[evotrack[1](ts)/1E2/GRAVSUN,evotrack[2](ts)/TSUN,evotrack[3](ts),evotrack[4](ts)]
ax.plot(ts,evotrack[1](ts)/1E2/GRAVSUN,label=r"$g_{\\rm surf}$")
ax.plot(ts,evotrack[2](ts)/TSUN,label=r"$T_{\\rm eff}$")
ax.plot(ts,evotrack[3](ts),label=r"$R$")
ax.plot(ts,evotrack[4](ts),label=r"$L$")

ax.axvline(star.tau_ms,color='k',linestyle='--',label='Main Sequence')
ax.axvline(star.tau,color='k',linestyle='-',label='Stellar Age')

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_title(star.title,position=(0.5,1.02),fontsize=11)
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"Property in Solar Units")

ymin,ymean,ymax=minmeanmaxArrays(yplot)
ymin=max(0.1,ymin)
ymax=min(10.0,ymax)
ax.set_xlim((star.tau_min,star.tau_max))
ax.set_ylim((ymin,ymax))
ax.grid(which="both")

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes,bbox=bbox,zorder=10)

ax.legend(loc='lower left',ncol=3,prop=dict(size=10))
"""%(star_dir,star_dir,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-radius",\
"""
from BHM.BHMstars import *
from BHM.BHMnum import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
bbox=dict(fc='w',ec='none')

#EVOLUTIONARY TRACK
ts,evotrack=interpMatrix(star.evotrack)

#LIMITS
tini=0.1
tend=star.tau_ms

#TIMES
ts=ts[ts>=tini]
ts=ts[ts<=tend]

#DATA
logts=np.log10(ts)
Ts=evotrack[2](ts)
Rs=evotrack[3](ts)

#TRAJECTORY
ax.plot(Ts,Rs,"k-")

#EXTREMES
ax.plot([Ts[0]],[Rs[0]],
"go",markersize=10,markeredgecolor='none',label=r"$t_{\\rm ini}=$0.1 Gyr")

ax.plot([Ts[-1]],[Rs[-1]],
"ro",markersize=10,markeredgecolor='none',label=r"$t_{\\rm end}=$%%.1f Gyr"%%star.tau_ms)

#PRESENT PROPERTIES
ax.plot([star.Tins],[star.Rins],
"bo",markersize=10,markeredgecolor='none',label=r"$t=$%%.1f Gyr"%%star.tau)

#EVOLUTIONARY TRACK
dt=round((tend-tini)/20,1)
logts=np.log10(np.arange(tini,tend,dt))
Ts=evotrack[2](ts)
Rs=evotrack[3](ts)
ax.plot(Ts,Rs,"ko",label='Steps of %%.2f Gyr'%%dt,markersize=3)
ax.text(TSUN,1.0,r"$\odot$",fontsize=16)

if star.R>0:ax.axhline(star.R,color='g',label='Observed Value')
if star.T>0:ax.axvline(star.T,color='g')
if star.Rerr>0:
   ax.axhspan(star.R-star.Rerr,star.R+star.Rerr,color='g',alpha=0.2)
if star.Terr>0:
   ax.axvspan(star.T-star.Terr,star.T+star.Terr,color='g',alpha=0.2)

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$R/R_{\\rm Sun}$")

Tmin,Tmax=ax.get_xlim()
ax.set_xlim((Tmax,Tmin))

#MODEL WATERMARK
ax.text(0.5,0.95,
"%s",horizontalalignment="center",fontsize="10",color="k",bbox=bbox,zorder=10,alpha=0.3,transform=ax.transAxes)

ax.grid(which="both")
ax.legend(loc='upper left',prop=dict(size=10))
"""%(star_dir,star_dir,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#GRAVITATION EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-logg",\
"""
from BHM.BHMstars import *
from BHM.BHMnum import *
star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
bbox=dict(fc='w',ec='none')

#EVOLUTIONARY TRACK
ts,evotrack=interpMatrix(star.evotrack)

#LIMITS
tini=0.1
tend=star.tau_ms

#TIMES
ts=ts[ts>=tini]
ts=ts[ts<=tend]

#DATA
logts=np.log10(ts)
Ts=evotrack[2](ts)
loggs=np.log10(evotrack[1](ts))

#TRAJECTORY
ax.plot(Ts,loggs,"k-")

#EXTREMES
ax.plot([Ts[0]],[loggs[0]],
"go",markersize=10,markeredgecolor='none',label=r"$t_{\\rm ini}=$0.1 Gyr")

ax.plot([Ts[-1]],[loggs[-1]],
"ro",markersize=10,markeredgecolor='none',label=r"$t_{\\rm end}=$%%.1f Gyr"%%star.tau_ms)

#PRESENT PROPERTIES
ax.plot([star.Tins],[np.log10(star.gins)],
"bo",markersize=10,markeredgecolor='none',label=r"$t=$%%.1f Gyr"%%star.tau)

#EVOLUTIONARY TRACK
dt=round((tend-tini)/20,1)
logts=np.log10(np.arange(tini,tend,dt))
Ts=evotrack[2](ts)
loggs=np.log10(evotrack[1](ts))
ax.plot(Ts,loggs,"ko",label='Steps of %%.2f Gyr'%%dt,markersize=3)
ax.text(TSUN,np.log10(GRAVSUN*1E2),r"$\odot$",fontsize=16)

if star.logg>0:ax.axhline(star.logg,color='g',label='Observed Value')
if star.T>0:ax.axvline(star.T,color='g')
if star.loggerr>0:
   ax.axhspan(star.logg-star.loggerr,star.logg+star.loggerr,color='g',alpha=0.2)
if star.Terr>0:
   ax.axvspan(star.T-star.Terr,star.T+star.Terr,color='g',alpha=0.2)

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$\\log\,g$ [cm s$^{-2}$]")

Tmin,Tmax=ax.get_xlim()
ax.set_xlim((Tmax,Tmin))

#MODEL WATERMARK
ax.text(0.5,0.95,
"%s",horizontalalignment="center",fontsize="10",color="k",bbox=bbox,zorder=10,alpha=0.3,transform=ax.transAxes)

ax.grid(which="both")
ax.legend(loc='upper right',prop=dict(size=10))
"""%(star_dir,star_dir,modelwat))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#MOMENT OF INERTIA EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-moi",\
"""
from BHM.BHMstars import *
from BHM.BHMnum import *
bbox=dict(fc='w',ec='none')

star=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
bbox=dict(fc='w',ec='none')

#MAIN PLOT
ts,Ievo=interpMatrix(star.Ievo)

yplots=[Ievo[1](ts)]
ax.plot(ts/GIGA,Ievo[1](ts),color='r',label='Convective Envelope')
if star.M>=MMIN_CONV:
   cond=Ievo[2](ts)>0
   ax.plot(ts[cond]/GIGA,np.log10(Ievo[2](ts[cond])),color='b',label='Radiative Core')
   yplots+=[Ievo[1](ts)]

#DECORATIONS
ax.set_xscale("log")
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$\\log\, I$ (kg m$^2$)")

ymin,ymean,ymax=minmeanmaxArrays(yplots)
ax.set_ylim((44,ymax))
ax.set_xlim((ts[0]/GIGA,ts[-1]/GIGA))
ax.set_title(star.title,position=(0.5,1.02),fontsize=12)
ax.grid(which="both")
ax.legend(loc='upper right',prop=dict(size=11))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize=10,color="k",alpha=0.3,transform=ax.transAxes,bbox=bbox)

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

M=star.M
Z=star.Z
tau=star.tau
R=star.Rins
T=star.Tins

color=cm.RdYlBu((T-2000)/7000)

starc=patches.Circle((0.0,0.0),R,fc=color,ec='none')
sun=patches.Circle((0.0,0.0),1.0,
                   linestyle='dashed',fc='none',zorder=10)
ax.add_patch(starc)
ax.add_patch(sun)
ax.text(0.0,1.0,'Sun',
fontsize=12,transform=offSet(0,5),horizontalalignment='center',verticalalignment='bottom',color=cm.gray(0.5),bbox=bbox,zorder=10)
ax.text(0.0,-R,
star.str_StarID.replace("'",""),fontsize=12,transform=offSet(0,-5),horizontalalignment='center',verticalalignment='top',color=cm.gray(0.5),bbox=bbox,zorder=10)

if star.R>0:
   starobs=patches.Circle((0.0,0.0),star.R,
                          linestyle='solid',fc='none',zorder=10,color='b')
   ax.add_patch(starobs)

ax.set_xticks([])
ax.set_yticks([])

if len(star.str_StarID)>0:startitle="%%s: "%%star.str_StarID.replace("'","")
else:startitle=""
ax.set_title(r"%%s$M = %%.3f\,M_{\odot}$, $Z=$%%.4f, $\\tau=%%.3f$ Gyr, $R = %%.3f\,R_{\odot}$, $T_{\\rm eff} = %%.1f$ K"%%(startitle,M,Z,tau,R,T),
position=(0.5,0.05),fontsize=14)

rang=max(1.5*R,1.5)
ax.set_xlim((-rang,+rang))
ax.set_ylim((-rang,+rang))

#MODEL WATERMARK
ax.text(0.5,0.95,"%s",horizontalalignment="center",fontsize="10",color="k",alpha=0.3,transform=ax.transAxes)

"""%(star_dir,star_dir,modelwat),watermarkpos="inner")

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
bbox=dict(fc='w',ec='none')

ts=star.rotevol[:,0]
wconv=star.rotevol[:,1]
wrad=star.rotevol[:,2]

ax.plot(ts,wconv/OMEGASUN,'b-',label='Convective Envelope')
if star.M>=MMIN_CONV:
    ax.plot(ts,wrad/OMEGASUN,'b--',label='Radiative Core')
ax.plot(ts,(ts/TAGE)**(-0.5),'g-',label='Skumanich Relationship')

if star.Prot>0:ax.axhline(PSUN/DAY/star.Prot,color='b')
if star.Proterr>0:
     wmax=PSUN/DAY/(star.Prot-star.Proterr);wmin=PSUN/DAY/(star.Prot+star.Proterr);
     ax.axhspan(wmin,wmax,color='b',alpha=0.3)

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(star.title,position=(0.5,1.02),fontsize=12)

#ax.text(0.5,0.08,r"$\\tau_{\\rm disk}$=%%.3f Gyr, $\Omega_{\\rm sat}$ = %%.2f $\Omega_\odot$, $K_{\\rm W}$ = %%.2e"%%(star.taudisk,star.wsat_scaled,star.Kw),
#transform=ax.transAxes,horizontalalignment='center',bbox=bbox)

ax.set_xlim((star.tmoi_min,star.tmoi_max))

ax.text(1.07,0.5,r"$P$ (days)",rotation=90,verticalalignment='center',horizontalalignment='center',transform=ax.transAxes)

#DATA FOR OTHER STARS
for star_name in ROTAGE_STARS.keys():
    staro=ROTAGE_STARS[star_name]
    tau=staro["tau"]
    Prot=staro["Prot"]
    ax.plot([tau],[2*PI/(Prot*DAY)/OMEGASUN],'o',markersize=10,markeredgecolor='none',color=cm.gray(0.5),zorder=-10)
    ax.text(tau,2*PI/(Prot*DAY)/OMEGASUN,star_name,transform=offSet(-10,staro["up"]),horizontalalignment="right",color=cm.gray(0.1),zorder=-10,fontsize=10)

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
ax.set_xlim((TAU_ZAMS,star.tau_ms))

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
ax.set_xlim((TAU_ZAMS,star.tau_ms))

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

ax_R.legend(loc='best',prop=dict(size=12))
for ax in axs:
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim((TAU_ZAMS,star.tau_ms))
    ax.grid(which='both')

axs[-1].set_title(star.title,position=(0.5,1.02),fontsize=12)
axs[0].set_xlabel(r"$\\tau$ (Gyr)")

for ax in axs[1:]:
    ax.set_xticklabels([])

"""%(star_dir,star_dir))

###################################################
#CLOSE OBJECT
###################################################
closeObject(star_dir)
