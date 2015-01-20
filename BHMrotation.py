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
# Stellar Rotational Evolution in Binaries
###################################################
from BHM import *
from BHM.BHMplot import *
from BHM.BHMstars import *
from BHM.BHMastro import *

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

sys_dir,rot_conf,qover=\
    readArgs(argv,
             ["str","str","int"],
             ["sys/template","hz.conf","0"],
             Usage=Usage)

###################################################
#LOAD PREVIOUS OBJECTS
###################################################
PRINTOUT("Loading other objects...")
#==================================================
#LOADING STAR 1
star1_conf="star1.conf"
star1,star1_dir,star1_str,star1_hash,star1_liv,star1_stg=\
    signObject("star",sys_dir+"/"+star1_conf)
star1+=loadConf(star1_dir+"star.data")
evoInterpFunctions(star1)
#==================================================
#LOADING STAR 2
star2_conf="star2.conf"
star2,star2_dir,star2_str,star2_hash,star2_liv,star2_stg=\
    signObject("star",sys_dir+"/"+star2_conf)
star2+=loadConf(star2_dir+"star.data")
evoInterpFunctions(star2)
#==================================================
#LOADING BINARY
binary_conf="binary.conf"
binary,binary_dir,binary_str,binary_hash,binary_liv,binary_stg=\
    signObject("binary",sys_dir+"/"+binary_conf)
binary+=loadConf(binary_dir+"binary.data")
#==================================================

#ROTATION
PRINTOUT("Rotation interaction between M1 = %.2f and M2 = %.2f at a = %.2f, e = %.2f"%(star1.M,star2.M,binary.abin,binary.ebin))

#CHECK IF TWINS
qtwins=False
if star1_hash==star2_hash:
    qtwins=True
    star2=star1
    PRINTOUT("Stars are twins.")

###################################################
#LOAD ROT OBJECT
###################################################
rot,rot_str,rot_hash,rot_dir=\
    makeObject("rotation",sys_dir+"/"+rot_conf,qover=qover)
rot_webdir="/"+WEB_DIR+rot_dir
PRINTOUT("Object hash:%s"%rot_hash)

###################################################
#CALCULATE ROTATIONAL EVOLUTION
###################################################
stars=star1,star2
i=0

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INTEGRATION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PRINTOUT("Integrating rotation...")
i=0
for star in stars:
    #INITIALIZE INTERPOLATION FUNCTIONS
    evoInterpFunctions(star)

    #==============================
    #ROTATIONAL EVOLUTION
    #==============================
    tsmoi=10**star.Ievo[:,0]/GIGA
    star.taudisk=rot.tauint/1000
    rotpars=dict(\
        star=star,
        starf=stars[NEXT(i,2)],
        binary=binary,
        taucont=TAU_CONT,
        fdiss=rot.fdiss
        )
    wini=2*PI/(star.Pini*DAY)
    Omega_ini=np.array([wini,wini])
    star.binrotevol=odeint(rotationalTorques,Omega_ini,tsmoi*GYR,args=(rotpars,))
    star.binrotevol=toStack(tsmoi)|toStack(star.binrotevol)

    #==============================
    #COMBINED MASS-LOSS
    #==============================
    tsmoi=star.rotevol[:,0]
    Nfine=len(tsmoi)
    star.binactivity=stack(13)
    star.acceleration=stack(5)
    """
    Activity Data:
      1:tauc
      2:fstar
      3:Bequi
      4:Bphoto
      5:BTR
      6:Rossby
      7:Mdot
      8:Mdot_hot
      9:Mdot_cold
      10:MATR
      11:RX
      12:LX
      13:LXUV
    Acceleration Data:
      1:Tidal torque
      2:Contraction torque
      3:Magnetized wind torque
      4:Total torque
    """
    for i in range(0,Nfine):
        t=tsmoi[i]
        M=star.M
        R=star.Rfunc(t)
        L=star.Lfunc(t)
        w=star.binrotevol[i,1]
        Prot=2*PI/w/DAY
             
        #ROTATIONAL ACCELERATION
        accels=rotationalTorques(np.array([w,w]),t*GYR,rotpars,full=True)
        star.acceleration+=[accel[0] for accel in accels]
        #print t,[accel[0] for accel in accels]

        #SURFICIAL MAGNETIC CONDITIONS
        tauc,fstar,Bequi,Bphoto,BTR,Rossby,Mdot,Mdot_hot,Mdot_cold,MATR=\
            pyBoreas(M,R,L,Prot,star.FeH)
        
        #X-RAY EMMISION
        RX=starRX(Rossby,regime='custom',Rosat=star.Rosat,logRXsat=star.logRXsat,beta=star.beta)
        LX=L*RX*LSUN
        LXUV=starLXEUV(LX)
        
        star.binactivity+=[tauc,fstar,Bequi,Bphoto,BTR,Rossby,
                           Mdot,Mdot_hot,Mdot_cold,MATR,
                           RX,LX,LXUV]
    #exit(0)
    star.binactivity=toStack(tsmoi)|star.binactivity
    star.acceleration=toStack(tsmoi)|star.acceleration
    
    if qtwins:break
    i+=1

rot.taumaxrot=min(star1.binactivity[-1,0],star2.binactivity[-1,0])
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INSTANTANEOUS STELLAR PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PRINTOUT("Calculating instantaneous properties...")
i=0
for star in stars:
    if star.tau>rot.taumaxrot:
        PRINTERR("Reported age %e Gyr is larger than maximum rotational age: %e Gyr"%(star.tau,
                                                                                      rot.taumaxrot))
        star.tau=rot.taumaxrot
    
    tsrot,rotation=interpMatrix(star.binrotevol)
    tsact,activity=interpMatrix(star.binactivity)

    star.bomegaconv=rotation[1](star.tau)
    star.bomegarad=rotation[2](star.tau)

    star.bPconv=2*PI/star.bomegaconv/DAY
    star.bPrad=2*PI/star.bomegarad/DAY
    star.bvsurf=2*PI*star.Rins*RSUN/1E3*star.bomegaconv
    star.bfstar=activity[2](star.tau)
    star.bBstar=star.bfstar*activity[4](star.tau)
    star.bRo=activity[6](star.tau)
    star.bMdot=activity[7](star.tau)
    star.bRX=activity[11](star.tau)
    star.bLX=activity[12](star.tau)
    star.bLXUV=activity[13](star.tau)

    if qtwins:break
    i+=1

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INSTANTANEOUS BINARY PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
binary.LX=star1.bLX+star2.bLX
binary.LXUV=star1.bLXUV+star2.bLXUV
binary.Mdot=star1.bMdot+star2.bMdot

###################################################
#STORE ROTATIONAL EVOLUTION INFORMATION
###################################################
rot.title=r"$M_1/M_{\\rm Sun}=$%.3f, $M_2/M_{\\rm Sun}$=%.3f, $a_{\\rm bin}$=%.3f AU, $e_{\\rm bin}$=%.2f, $P_{\\rm bin}$=%.3f d"%(star1.M,star2.M,binary.abin,binary.ebin,binary.Pbin)

PRINTERR("Storing rotational and activity evolution data...")
f=open(rot_dir+"rotation.data","w")

f.write("""\
from numpy import array
#TITLE
title="%s"

#MAXIMUM ROTATION TIME
taumaxrot=%.17e

#ROTATIONAL EVOLUTION IN BINARY
star1_binrotevol=%s
star2_binrotevol=%s
star1_acceleration=%s
star2_acceleration=%s

#MASS-LOSS IN BINARY
star1_binactivity=%s
star2_binactivity=%s

#INSTANTANEOUS STELLAR PROPERTIES

#STAR 1
star1_omegaconv=%.17e #s^-1
star1_omegarad=%.17e #s^-1
star1_Pconv=%.17e #days
star1_Prad=%.17e #days
star1_vsurf=%.17e #km/s
star1_fstar=%.17e 
star1_Bstar=%.17e #Gauss
star1_Ro=%.17e
star1_Mdot=%.17e #Msun yr^-1
star1_RX=%.17e 
star1_LX=%.17e #W
star1_LXUV=%.17e #W

#STAR 2
star2_omegaconv=%.17e #s^-1
star2_omegarad=%.17e #s^-1
star2_Pconv=%.17e #days
star2_Prad=%.17e #days
star2_vsurf=%.17e #km/s
star2_fstar=%.17e 
star2_Bstar=%.17e #Gauss
star2_Ro=%.17e
star2_Mdot=%.17e #Msun yr^-1
star2_RX=%.17e 
star2_LX=%.17e #W
star2_LXUV=%.17e #W

#BINARY
binary_LX=%.17e #W
binary_LXUV=%.17e #W
binary_Mdot=%.17e #Msun yr^-1
"""%(rot.title,
     rot.taumaxrot,
     array2str(star1.binrotevol),
     array2str(star2.binrotevol),
     array2str(star1.acceleration),
     array2str(star2.acceleration),
     array2str(star1.binactivity),
     array2str(star2.binactivity),
     star1.bomegaconv,star1.bomegarad,
     star1.bPconv,star1.bPrad,star1.bvsurf,
     star1.bfstar,star1.bBstar,star1.bRo,star1.bMdot,
     star1.bRX,star1.bLX,star1.bLXUV,
     star2.bomegaconv,star2.bomegarad,
     star2.bPconv,star2.bPrad,star2.bvsurf,
     star2.bfstar,star2.bBstar,star2.bRo,star2.bMdot,
     star2.bRX,star2.bLX,star2.bLXUV,
     binary.LX,binary.LXUV,binary.Mdot
     ))
f.close()

###################################################
#GENERATE PLOTS
###################################################
PRINTOUT("Creating plots...")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ROTATIONAL EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(rot_dir,"rot-evolution",\
"""
from BHM.BHMstars import *
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
star1=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
star2=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

revol1=rot.star1_binrotevol
revol2=rot.star2_binrotevol

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

sts1=star1.rotevol[:,0]
sw1=star1.rotevol[:,1]
ts1=revol1[:,0]
w1=revol1[:,1]

sts2=star2.rotevol[:,0]
sw2=star2.rotevol[:,1]
ts2=revol2[:,0]
w2=revol2[:,1]

ax.plot(sts1,sw1/OMEGASUN,'b--',label='Star 1 (Free)')
ax.plot(ts1,w1/OMEGASUN,'b-',label='Star 1 (Tidal)')

ax.plot(sts2,sw2/OMEGASUN,'r--',label='Star 2 (Free)')
ax.plot(ts2,w2/OMEGASUN,'r-',label='Star 2 (Tidal)')

ax.axhline(PSUN/DAY/binary.Psync,color='k',label=r"$P_{\\rm sync}=P_{\\rm bin}/%%.2f$"%%binary.nsync)
ax.axhline(PSUN/DAY/binary.Pbin,color='k',linestyle='--',label=r"$P_{\\rm bin}$")

if binary.taumin>0:
     taumean=(binary.taumin+binary.taumax)/2
     tauerr=(binary.taumax-binary.taumin)/2

if star1.Prot>0:
     Prot=star1.Prot;
     Proterr=max(star1.Proterr,0.0);
     wmax1=PSUN/DAY/(Prot-Proterr);wmin1=PSUN/DAY/(Prot+Proterr);
     wmean1=(wmin1+wmax1)/2;werr1=(wmax1-wmin1)/2
     if binary.taumin>0:
         ax.errorbar(taumean,wmean1,xerr=tauerr,yerr=werr1,linewidth=2,color='b')
     else:
         ax.axhspan(wmin1,wmax1,color='b',alpha=0.3)

if star1.Protv>0:
     Protv=star1.Protv;
     Protverr=max(star1.Protverr,0.0);
     wmax1=PSUN/DAY/(Protv-Protverr);wmin1=PSUN/DAY/(Protv+Protverr);
     wmean1=(wmin1+wmax1)/2;werr1=(wmax1-wmin1)/2
     if binary.taumin>0:
         ax.errorbar(taumean,wmean1,xerr=tauerr,yerr=werr1,linewidth=2,color='c')
     else:
         ax.axhspan(wmin1,wmax1,color='c',alpha=0.3)

if star2.Prot>0:
     Prot=star2.Prot;
     Proterr=max(star2.Proterr,0.0);
     wmax2=PSUN/DAY/(Prot-Proterr);wmin2=PSUN/DAY/(Prot+Proterr);
     wmean2=(wmin2+wmax2)/2;werr2=(wmax2-wmin2)/2
     if binary.taumin>0:
         ax.errorbar(taumean,wmean2,xerr=tauerr,yerr=werr2,linewidth=2,color='r')
     else:
         ax.axhspan(wmin2,wmax2,color='r',alpha=0.3)

if star2.Protv>0:
     Protv=star2.Protv;
     Protverr=max(star2.Protverr,0.0);
     wmax2=PSUN/DAY/(Protv-Protverr);wmin2=PSUN/DAY/(Protv+Protverr);
     wmean2=(wmin2+wmax2)/2;werr2=(wmax2-wmin2)/2
     if binary.taumin>0:
         ax.errorbar(taumean,wmean2,xerr=tauerr,yerr=werr2,linewidth=2,color='g')
     else:
         ax.axhspan(wmin2,wmax2,color='g',alpha=0.3)

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(binary.title,position=(0.5,1.02),fontsize=12)

ax.text(1.07,0.5,r"$P$ (days)",rotation=90,verticalalignment='center',horizontalalignment='center',transform=ax.transAxes)

#PERIODS
wmin=min(min(w1),min(sw1),min(w2),min(sw2))/OMEGASUN
wmax=max(max(w1),max(sw1),max(w2),max(sw2))/OMEGASUN

ax.set_xlim((TAU_ZAMS,12.0))
ax.set_ylim((wmin,wmax))

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
ax.legend(loc='lower left',prop=dict(size=12))
"""%(rot_dir,rot_dir,
     binary_dir,binary_dir,
     star1_dir,star1_dir,
     star2_dir,star2_dir
     ))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ROTATIONAL ACCELERATION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(rot_dir,"rot-acceleration",\
"""
from BHM.BHMstars import *
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
star1=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
star2=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

raccel1=rot.star1_acceleration
raccel2=rot.star2_acceleration

fig=plt.figure(figsize=(8,12))
l=0.15;w=0.8;b=0.05;dh=0.02;h=(1.0-2*b-dh)/2;
ax2=fig.add_axes([l,b,w,h])
b+=h+dh
ax1=fig.add_axes([l,b,w,h])

scale=1E-21
ax1.plot(raccel1[:,0],raccel1[:,1]/scale,color='b',linestyle='--',label='Star 1 - Contraction')
ax1.plot(raccel1[:,0],raccel1[:,2]/scale,color='b',linestyle='-.',label='Star 1 - Differential Rotation')
ax1.plot(raccel1[:,0],raccel1[:,3]/scale,color='b',linestyle=':',label='Star 1 - Mass-loss')
ax1.plot(raccel1[:,0],raccel1[:,4]/scale,color='b',linestyle='-',label='Star 1 - Tides')
ax1.plot(raccel1[:,0],raccel1[:,5]/scale,color='b',linestyle='-',linewidth=5,zorder=10,alpha=0.2,label='Star 1 - Total')

ax2.plot(raccel2[:,0],raccel2[:,1]/scale,color='r',linestyle='--',label='Star 2 - Contraction')
ax2.plot(raccel2[:,0],raccel2[:,2]/scale,color='r',linestyle='-.',label='Star 2 - Differential Rotation')
ax2.plot(raccel2[:,0],raccel2[:,3]/scale,color='r',linestyle=':',label='Star 2 - Mass-loss')
ax2.plot(raccel1[:,0],raccel1[:,4]/scale,color='r',linestyle='-',label='Star 2 - Tides')
ax2.plot(raccel2[:,0],raccel2[:,5]/scale,color='r',linestyle='-',linewidth=5,zorder=10,alpha=0.2,label='Star 2 - Total')

tmax=min(star1.tau_ms,star2.tau_ms)
for ax in ax1,ax2:
    ax.set_xscale("log")
    #ax.set_yscale("log")
    ax.set_xlim((TAU_ZAMS,tmax))
    ax.set_ylabel(r"$\dot\Omega$ ($\\times\,10^{-21}$)")
    ax.legend(loc='best',prop=dict(size=12))
    #ax.grid(which='both')

ax1.set_xticklabels([])
ax1.set_title(binary.title,position=(0.5,1.02),fontsize=12)
ax2.set_xlabel(r"$\\tau$ (Gyr)")
"""%(rot_dir,rot_dir,
     binary_dir,binary_dir,
     star1_dir,star1_dir,
     star2_dir,star2_dir
     ))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#MASS-LOSS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(rot_dir,"binary-massloss",\
"""
from BHM.BHMstars import *
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
star1=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
star2=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.15,0.1,0.8,0.8])

ts1=rot.star1_binactivity[:,0]
Ml1=rot.star1_binactivity[:,7]
Ml1_func=interp1d(ts1,Ml1,kind='slinear')
sMl1=star1.activity[:,7]

ts2=rot.star2_binactivity[:,0]
Ml2=rot.star2_binactivity[:,7]
Ml2_func=interp1d(ts2,Ml2,kind='slinear')
sMl2=star2.activity[:,7]

tmin=max(min(ts1),min(ts2))*1.0001
tmax=min(max(ts1),max(ts2))*0.9999
ts=np.logspace(np.log10(tmin),np.log10(tmax),100)

ax.plot(ts1,Ml1,'b-',label='Star 1 (Tidal)')
ax.plot(ts1,sMl1,'b--',label='Star 1 (Free)')
ax.plot(ts2,Ml2,'r-',label='Star 2 (Tidal)')
ax.plot(ts2,sMl2,'r--',label='Star 2 (Free)')
ax.plot(ts,Ml1_func(ts)+Ml2_func(ts),'k-',linewidth=2,label='Total (Tidal)')

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(binary.title,position=(0.5,1.02),fontsize=12)
ax.set_xlim((TAU_ZAMS,12.0))

ax.set_ylabel(r"$\dot M$ ($M_\odot$/yr)")
ax.set_xlabel(r"$\\tau$ (Gyr)")

ax.grid(which='both')
ax.legend(loc='lower left',prop=dict(size=10))
"""%(rot_dir,rot_dir,
     binary_dir,binary_dir,
     star1_dir,star1_dir,
     star2_dir,star2_dir))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# XUV
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(rot_dir,"binary-XUV",\
"""
from BHM.BHMstars import *
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
star1=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
star2=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.15,0.1,0.8,0.8])

ts1=rot.star1_binactivity[:,0]
LXUV1=rot.star1_binactivity[:,13]
LXUV1_func=interp1d(ts1,LXUV1,kind='slinear')
sLXUV1=star1.activity[:,13]

ts2=rot.star2_binactivity[:,0]
LXUV2=rot.star2_binactivity[:,13]
LXUV2_func=interp1d(ts2,LXUV2,kind='slinear')
sLXUV2=star2.activity[:,13]

tmin=max(min(ts1),min(ts2))*1.0001
tmax=min(max(ts1),max(ts2))*0.9999
ts=np.logspace(np.log10(tmin),np.log10(tmax),100)

LSUN=LXUVSUN/1E7
ax.plot(ts1,LXUV1/LSUN,'b-',label='Star 1 (Tidal)')
ax.plot(ts1,sLXUV1/LSUN,'b--',label='Star 1 (Free)')
ax.plot(ts2,LXUV2/LSUN,'r-',label='Star 2 (Tidal)')
ax.plot(ts2,sLXUV2/LSUN,'r--',label='Star 2 (Free)')
ax.plot(ts,(LXUV1_func(ts)+LXUV2_func(ts))/LSUN,'k-',linewidth=2,label='Total (Tidal)')

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_title(binary.title,position=(0.5,1.02),fontsize=12)
ax.set_xlim((TAU_ZAMS,12.0))

ax.set_ylabel(r"$L_{\\rm XUV}/L_{\\rm XUV,\odot,present}$")
ax.set_xlabel(r"$\\tau$ (Gyr)")

ax.grid(which='both')
ax.legend(loc='lower left',prop=dict(size=10))
"""%(rot_dir,rot_dir,
     binary_dir,binary_dir,
     star1_dir,star1_dir,
     star2_dir,star2_dir))

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(rot_dir+"rotation.html","w")
fh.write("""\
<!--VERSION:%s-->
<html>
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>
<body>
<h2>Rotational Evolution in Binary</h2>

<h3>Plots</h3>

<h3>Rotation Evolution</h3>
<table>
  <tr><td colspan=2>
  <a target="_blank" href="%s/rot-evolution.png">
    <img width=100%% src="%s/rot-evolution.png?%s">
  </a>
  <br/>
  <div class="caption">
  <i>Rotational Evolution in binary</i>
  (
  <a target="_blank" href="%s/rot-evolution.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=rot-evolution.py">replot</a>
  )
  </div>
  </td></tr>

  <tr><td colspan=2>
  <a target="_blank" href="%s/rot-acceleration.png">
    <img width=100%% src="%s/rot-acceleration.png?%s">
  </a>
  <br/>
  <div class="caption">
  <i>Angular Accelerations</i>
  (
  <a target="_blank" href="%s/rot-acceleration.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=rot-acceleration.py">replot</a>
  )
  </div>
  </td></tr>
</table>

<h3>Activity</h3>
<table>
    <tr><td colspan=2>
  <a target="_blank" href="%s/binary-massloss.png">
    <img width=100%% src="%s/binary-massloss.png?%s">
  </a>
  <br/>
  <div class="caption">
  <i>Binary Mass-loss</i>
  (
  <a target="_blank" href="%s/binary-massloss.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=binary-massloss.py">replot</a>
  )
  </div>
  </td></tr>
  <tr><td colspan=2>
  <a target="_blank" href="%s/binary-XUV.png">
    <img width=100%% src="%s/binary-XUV.png?%s">
  </a>
  <br/>
  <div class="caption">
  <i>Binary XUV Luminosity</i>
  (
  <a target="_blank" href="%s/binary-XUV.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=binary-XUV.py">replot</a>
  )
  </div>
  </td></tr>
</table>

<h3>Input Parameters</h3>
<table>
  <tr><td>&tau;<sub>int</sub> (Myr):</td><td>%.3f</td></tr>
  <tr><td>f<sub>diss</sub>:</td><td>%.3f</td></tr>
</table>

<h3>Binary Properties</h3>
<table>
  <tr><td>&tau; (Gyr):</td><td>%.2f</td></tr>
  <tr><td>dM<sub>bin</sub>/dt (M<sub>Sun</sub>/year):</td><td>%.2e</td></tr>
  <tr><td>L<sub>X,bin</sub> (W L<sub>X,Sun</sub>):</td><td>%.3e, %.3e</td></tr>
  <tr><td>L<sub>XUV,bin</sub> (W, L<sub>XUV,Sun</sub>):</td><td>%.3e, %.3e</td></tr>
</table>

<h3>Stellar Properties in the Binary</h3>
<table>

  <tr><td colspan=2><b>Star1</b></td></tr>
  <tr><td>P<sub>conv,1</sub> (days):</td><td>%.2f</td></tr>
  <tr><td>P<sub>rad,1</sub> (days):</td><td>%.2f</td></tr>
  <tr><td>v<sub>surf,1</sub> (km/s):</td><td>%.2f</td></tr>
  <tr><td>f<sub>*,1</sub>:</td><td>%.2e</td></tr>
  <tr><td>B<sub>*,1</sub> (Gauss):</td><td>%.2f</td></tr>
  <tr><td>Ro<sub>1</sub>:</td><td>%.2f</td></tr>
  <tr><td>dM<sub>1</sub>/dt (M<sub>Sun</sub>/year):</td><td>%.2e</td></tr>
  <tr><td>R<sub>X,1</sub>:</td><td>%.2e</td></tr>
  <tr><td>L<sub>X,1</sub> (W L<sub>X,Sun</sub>):</td><td>%.3e, %.3e</td></tr>
  <tr><td>L<sub>XUV,1</sub> (W, L<sub>XUV,Sun</sub>):</td><td>%.3e, %.3e</td></tr>

  <tr><td colspan=2><b>Star2</b></td></tr>
  <tr><td>P<sub>conv,2</sub> (days):</td><td>%.2f</td></tr>
  <tr><td>P<sub>rad,2</sub> (days):</td><td>%.2f</td></tr>
  <tr><td>v<sub>surf,2</sub> (km/s):</td><td>%.2f</td></tr>
  <tr><td>f<sub>*,2</sub>:</td><td>%.2e</td></tr>
  <tr><td>B<sub>*,2</sub> (Gauss):</td><td>%.2f</td></tr>
  <tr><td>Ro<sub>2</sub>:</td><td>%.2f</td></tr>
  <tr><td>dM<sub>2</sub>/dt (M<sub>Sun</sub>/year):</td><td>%.2e</td></tr>
  <tr><td>R<sub>X,2</sub>:</td><td>%.2e</td></tr>
  <tr><td>L<sub>X,2</sub> (W L<sub>X,Sun</sub>):</td><td>%.3e, %.3e</td></tr>
  <tr><td>L<sub>XUV,2</sub> (W, L<sub>XUV,Sun</sub>):</td><td>%.3e, %.3e</td></tr>

</table>

</body>
</html>
"""%(VERSION,
     WEB_DIR,
     rot_webdir,rot_webdir,rot_hash,rot_webdir,WEB_DIR,rot_webdir,
     rot_webdir,rot_webdir,rot_hash,rot_webdir,WEB_DIR,rot_webdir,
     rot_webdir,rot_webdir,rot_hash,rot_webdir,WEB_DIR,rot_webdir,
     rot_webdir,rot_webdir,rot_hash,rot_webdir,WEB_DIR,rot_webdir,
     rot.tauint,rot.fdiss,
     star1.tau,
     binary.Mdot,
     binary.LX,binary.LX/(LXUVSUN/1E7),binary.LXUV,binary.LXUV/(LXUVSUN/1E7),     
     star1.bPconv,star1.bPrad,
     star1.bvsurf,
     star1.bfstar,star1.bBstar,star1.bRo,star1.bMdot,star1.bRX,
     star1.bLX,star1.bLX/(LXUVSUN/1E7),star1.bLXUV,star1.bLXUV/(LXUVSUN/1E7),     
     star2.bPconv,star2.bPrad,
     star2.bvsurf,
     star2.bfstar,star2.bBstar,star2.bRo,star2.bMdot,star2.bRX,
     star2.bLX,star2.bLX/(LXUVSUN/1E7),star2.bLXUV,star2.bLXUV/(LXUVSUN/1E7),     
     ))
fh.close()
       
###################################################
#CLOSE OBJECT
###################################################
closeObject(rot_dir)
