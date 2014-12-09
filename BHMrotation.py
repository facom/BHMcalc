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
rot_webdir=WEB_DIR+rot_dir
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
    tsmoi=star.RMoI[:,0]
    rotpars=dict(\
        star=star,
        starf=stars[NEXT(i,2)],
        binary=binary,
        taudisk=star.taudisk,
        model='Chaboyer',
        Kw=star.Kw,
        wsat=star.wsat,
        tauc=50.0,
        qdifr=False,
        qcont=False
        )
    wini=2*PI/(star.Pini*DAY)
    Omega_ini=np.array([wini,wini])
    star.binrotevol=odeint(rotationalAccelerationFull,Omega_ini,tsmoi*GYR,args=(rotpars,))
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
        accels=rotationalAccelerationFull(np.array([w,w]),t*GYR,rotpars,full=True)
        star.acceleration+=[accel[0] for accel in accels]
        #print t,[accel[0] for accel in accels]

        #SURFICIAL MAGNETIC CONDITIONS
        tauc,fstar,Bequi,Bphoto,BTR,Rossby,Mdot,Mdot_hot,Mdot_cold,MATR=\
            pyBoreas(M,R,L,Prot,star.FeH)
        
        #X-RAY EMMISION
        RX=starRX(Rossby)
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
"""%(rot.title,
     rot.taumaxrot,
     array2str(star1.binrotevol),
     array2str(star2.binrotevol),
     array2str(star1.acceleration),
     array2str(star2.acceleration),
     array2str(star1.binactivity),
     array2str(star2.binactivity)
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

if star2.Prot>0:
     Prot=star2.Prot;
     Proterr=max(star2.Proterr,0.0);
     wmax2=PSUN/DAY/(Prot-Proterr);wmin2=PSUN/DAY/(Prot+Proterr);
     wmean2=(wmin2+wmax2)/2;werr2=(wmax2-wmin2)/2
     if binary.taumin>0:
         ax.errorbar(taumean,wmean2,xerr=tauerr,yerr=werr2,linewidth=2,color='b')
     else:
         ax.axhspan(wmin2,wmax2,color='b',alpha=0.3)

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
l=0.1;w=0.8;b=0.05;dh=0.02;h=(1.0-2*b-dh)/2;
ax1=fig.add_axes([l,b,w,h])
b+=h+dh
ax2=fig.add_axes([l,b,w,h])

scale=1E-21
ax1.plot(raccel1[:,0],raccel1[:,1]/scale,color='b',linestyle='--',label='Star 1 - Contraction')
ax1.plot(raccel1[:,0],raccel1[:,2]/scale,color='b',linestyle='-.',label='Star 1 - Differential Rotation')
ax1.plot(raccel1[:,0],raccel1[:,3]/scale,color='b',linestyle=':',label='Star 1 - Mass-loss')
ax1.plot(raccel1[:,0],raccel1[:,4]/scale,color='b',linestyle='-',label='Star 1 - Tides')
ax1.plot(raccel1[:,0],raccel1[:,5]/scale,color='b',linestyle='-',linewidth=5,zorder=10,alpha=0.2,label='Star 1 - Total')

ax2.plot(raccel2[:,0],raccel2[:,1]/scale,color='r',linestyle='--',label='Star 2 - Contraction')
ax2.plot(raccel2[:,0],raccel2[:,2]/scale,color='r',linestyle='-.',label='Star 2 - Differential Rotation')
ax2.plot(raccel2[:,0],raccel2[:,3]/scale,color='r',linestyle=':',label='Star 2 - Mass-loss')
ax1.plot(raccel1[:,0],raccel1[:,4]/scale,color='r',linestyle='-',label='Star 2 - Tides')
ax2.plot(raccel2[:,0],raccel2[:,5]/scale,color='r',linestyle='-',linewidth=5,zorder=10,alpha=0.2,label='Star 2 - Total')

tmax=min(star1.tau_ms,star2.tau_ms)
for ax in ax1,ax2:
    ax.set_xscale("log")
    #ax.set_yscale("log")
    ax.set_xlim((TAU_ZAMS,tmax))
    ax.set_ylabel(r"$\dot\Omega$ ($\\times\,10^{-21}$)")
    ax.legend(loc='best',prop=dict(size=12))
    #ax.grid(which='both')

ax2.set_xticklabels([])
ax2.set_title(binary.title,position=(0.5,1.02),fontsize=12)
ax1.set_xlabel(r"$\\tau$ (Gyr)")
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

tmin=max(min(ts1),min(ts2))
tmax=min(max(ts1),max(ts2))
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
#MASS-LOSS
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

tmin=max(min(ts1),min(ts2))
tmax=min(max(ts1),max(ts2))
ts=np.logspace(np.log10(tmin),np.log10(tmax),100)

LSUN=LXSUN/1E7
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
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>
<h2>Rotational Evolution in Binary</h2>
<center>
  <a target="_blank" href="%s/rot-evolution.png">
    <img width=60%% src="%s/rot-evolution.png">
  </a>
  <br/>
  <i>Rotational Evolution</i>
  (
  <a target="_blank" href="%s/rot-evolution.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=rot-evolution.py">replot</a>
  )
</center>
<h3>Input Parameters</h3>
<table>
  <tr><td>k:</td><td>%.3f</td></tr>
</table>
<h3>Rotation Evolution</h3>
<table>
  <tr><td colspan=2>
  <a target="_blank" href="%s/rot-evolution.png">
    <img width=100%% src="%s/rot-evolution.png">
  </a>
  <br/>
  <i>Rotational Evolution in binary</i>
  (
  <a target="_blank" href="%s/rot-evolution.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=rot-evolution.py">replot</a>
  )
  </td></tr>

  <tr><td colspan=2>
  <a target="_blank" href="%s/rot-acceleration.png">
    <img width=100%% src="%s/rot-acceleration.png">
  </a>
  <br/>
  <i>Rotational Acceleration in binary</i>
  (
  <a target="_blank" href="%s/rot-acceleration.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=rot-acceleration.py">replot</a>
  )
  </td></tr>

  <tr><td colspan=2>
  <a target="_blank" href="%s/binary-massloss.png">
    <img width=100%% src="%s/binary-massloss.png">
  </a>
  <br/>
  <i>Mass-loss in binary</i>
  (
  <a target="_blank" href="%s/binary-massloss.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=binary-massloss.py">replot</a>
  )
  </td></tr>
  <tr><td colspan=2>
  <a target="_blank" href="%s/binary-XUV.png">
    <img width=100%% src="%s/binary-XUV.png">
  </a>
  <br/>
  <i>Binary XUV Luminosity</i>
  (
  <a target="_blank" href="%s/binary-XUV.png.txt">data</a>|
  <a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=binary-XUV.py">replot</a>
  )
  </td></tr>
</table>
"""%(WEB_DIR,rot_webdir,rot_webdir,rot_webdir,WEB_DIR,rot_webdir,
     rot.k,
     rot_webdir,rot_webdir,rot_webdir,WEB_DIR,rot_webdir,
     rot_webdir,rot_webdir,rot_webdir,WEB_DIR,rot_webdir,
     rot_webdir,rot_webdir,rot_webdir,WEB_DIR,rot_webdir,
     rot_webdir,rot_webdir,rot_webdir,WEB_DIR,rot_webdir
     ))
fh.close()
       
###################################################
#CLOSE OBJECT
###################################################
closeObject(rot_dir)
