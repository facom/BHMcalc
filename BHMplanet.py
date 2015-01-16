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
# Planetary Basic Properties
# Inputs: 
# - Planetary properties (planet.conf)
# Outputs: 
# - Planetary data (planet.data)
###################################################
from BHM import *
from BHM.BHMplot import *
from BHM.BHMplanets import *

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

sys_dir,planet_conf,qover=\
    readArgs(argv,
             ["str","str","int"],
             ["sys/template","planet.conf","0"],
             Usage=Usage)

###################################################
#LOAD PLANETARY OBJECT
###################################################
PRINTOUT("Loading object from '%s'"%(planet_conf))
planet,planet_str,planet_hash,planet_dir=makeObject("planet",
                                            sys_dir+"/"+planet_conf,
                                            qover=qover)
planet_webdir="/"+WEB_DIR+planet_dir
PRINTOUT("Object hash:%s"%planet_hash)
planet.hash=planet_hash

###################################################
#CALCULATE PROPERTIES OF THE PLANET
###################################################
planet.Mp=planet.M
planet.Mg=planet.M*MEARTH/MJUP
PRINTOUT("Mass of the planet = %.3f MEarth = %.3f MJup"%(planet.M,planet.Mg))

if planet.M>7 and planet.Mg<0.05:
    PRINTERR("No model available for this mass.  Instead we will calculate the evolution of a 7 Earth Masses rocky planet.")
    planet.M=7

if planet.M<=7:
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #SOLID PLANET
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PRINTOUT("Planet is Solid")
    dirplgrid=DATA_DIR+"SolidPlanets/MobileLids"
    loadSolidPlanetsGrid(dirplgrid,verbose=VERBOSE)
    planet.type="Solid Planet"

    #----------------------------------------
    #GET CELL IN PARAMETER SPACE
    #----------------------------------------
    PRINTOUT("Calculating properties for Solid planet with CMF = %.3f"%planet.CMF)
    try:
        pcell=loadPlanetCell(Mp=planet.M,CMF=planet.CMF,IMF=0.0,dirplgrid=dirplgrid,verbose=False)
    except:
        PRINTOUT("Planet properties out of range.")
        errorCode("RANGE_ERROR")

    #----------------------------------------
    #BULK PROPERTIES
    #----------------------------------------
    planet.Rp=planetProperty(pcell,"Radius",
                            data="struct")
    planet.A=4*PI*(planet.Rp*Rp_E)**2
    planet.Rg=planet.Rp*Rp_E/RJUP
    planet.rho=planet.M*MEARTH/(4./3*PI*(planet.Rp*Rp_E)**3)
    planet.g=GCONST*(planet.M*MEARTH)/(planet.Rp*REARTH)**2
    planet.Rc=planetProperty(pcell,"CoreRadius",
                             data="struct")
    planet.rhoc=planetProperty(pcell,"CoreDensity",
                             data="struct")
    planet.tdyn=planetProperty(pcell,"DynamoLifetime",
                               data="tevol")/GIGA
    planet.sigma=sigma_E
    planet.kappa=kappa_E
    planet.Mdipmax=planetProperty(pcell,
                                  "AbsoluteMaximumDipoleMoment",
                                  data="tevol",
                                  R=planet.Rp,
                                  M=planet.M,
                                  Rc=planet.Rc,
                                  rhoc=planet.rhoc,
                                  P=planet.Prot,
                                  sigma=planet.sigma,
                                  kappa=planet.kappa)/MDIPE

    planet.tMdipmax=planetProperty(pcell,
                                   "TimeMaximumDipoleMoment",
                                   data="tevol",
                                   R=planet.Rp,
                                   M=planet.M,
                                   Rc=planet.Rc,
                                   rhoc=planet.rhoc,
                                   P=planet.Prot,
                                   sigma=planet.sigma,
                                   kappa=planet.kappa)/GIGA

    #----------------------------------------
    #INSTANTANEOUS PROPERTIES
    #----------------------------------------
    planet.Q=planetProperty(pcell,"SurfaceHeat",
                             data="tevol",t=planet.tau)
    planet.T=(planet.Q/(planet.A*SIGMA))**0.25

    planet.Ric=planetProperty(pcell,"InnerCoreRadius",
                              data="tevol",t=planet.tau)

    planet.Qconv=planetProperty(pcell,"ConvectiveHeat",
                                data="tevol",t=planet.tau)

    planet.Mdip=planetaryDipoleMoment(planet)/MDIPE

    planet.Mdipmaxt=planetProperty(pcell,
                                  "TemporalMaximumDipoleMoment",
                                   t=planet.tau,
                                   data="tevol",
                                   R=planet.Rp,
                                   M=planet.M,
                                   Rc=planet.Rc,
                                   rhoc=planet.rhoc,
                                   P=planet.Prot,
                                   sigma=planet.sigma,
                                   kappa=planet.kappa)/MDIPE

    #----------------------------------------
    #THERMAL EVOLUTION
    #----------------------------------------
    ts=np.linspace(TAU_MIN,TAU_MAX,NTIMES)
    thermevol=stack(9)
    tplanet=copyObject(planet)
    PRINTOUT("Calculating thermal evolution of Solid Planet...")
    for t in ts:
        tplanet.Q=planetProperty(pcell,"SurfaceHeat",
                                data="tevol",t=t)
        if tplanet.Q==0:
            tplanet.Q=0
            tplanet.T=0
            tplanet.Qconv=0
            tplanet.Ric=0
            tplanet.Mdip=0
        else:
            tplanet.T=(tplanet.Q/(planet.A*SIGMA))**0.25
            tplanet.Ric=planetProperty(pcell,"InnerCoreRadius",
                                       data="tevol",t=t)
            tplanet.Qconv=planetProperty(pcell,"ConvectiveHeat",
                                         data="tevol",t=t)
            tplanet.Mdip=planetaryDipoleMoment(tplanet)/MDIPE

        thermevol+=[tplanet.Rg,tplanet.Rc,tplanet.Ric,tplanet.rho,tplanet.rhoc,tplanet.Q,tplanet.Qconv,tplanet.T,tplanet.Mdip]
    thermevol=toStack(ts)|thermevol

elif planet.Mg>=0.05:
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #ICE GASS GIANTS
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PRINTOUT("Planet is an Ice-Gas Giant, Mg = %.3f"%planet.Mg)
    loadIceGasGiantsGrid(DATA_DIR+"IceGasGiants/",
                         verbose=True)
    planet.type="Ice-Gas Giant"

    #----------------------------------------
    #BULK (INSTANTANEOUS) PROPERTIES
    #----------------------------------------
    if planet.tau>=10:planet.tau=9.0
    planet.Rg,planet.T,planet.Q=PlanetIceGasProperties(planet.Mg,
                                                       planet.tau,
                                                       planet.fHHe,
                                                       verbose=VERBOSE)
    if planet.Rg<0:
        PRINTERR("No planetary model for giants with this mass and composition.")
        errorCode("RANGE_ERROR");
    planet.Qconv=planet.Q
    planet.Rp=planet.Rg*RJUP/REARTH
    
    planet.A=4*PI*(planet.Rp*Rp_E)**2
    planet.g=GCONST*(planet.M*MEARTH)/(planet.Rp*REARTH)**2

    #----------------------------------------
    #INTERIOR PROPERTIES
    #----------------------------------------
    planet.Rc,planet.Ric,planet.rho,\
        planet.rhoc,planet.sigma,planet.kappa=\
        giantStructure(planet.Mg,planet.Rg)
    planet.Mdip=planetaryDipoleMoment(planet)/MDIPE

    #----------------------------------------
    #THERMAL EVOLUTION
    #----------------------------------------
    ts=np.linspace(TAU_MIN,TAU_MAX,NTIMES)
    thermevol=stack(9)
    tplanet=copyObject(planet)
    PRINTOUT("Calculating thermal evolution of IceGas Giant...")
    for t in ts:
        tplanet.Rg,tplanet.T,tplanet.Q=\
            PlanetIceGasProperties(tplanet.Mg,t,tplanet.fHHe)
        tplanet.Qconv=tplanet.Q
        tplanet.Rc,tplanet.Ric,tplanet.rho,tplanet.rhoc,\
            tplanet.sigma,tplanet.kappa=\
            giantStructure(tplanet.Mg,tplanet.Rg)
        tplanet.Mdip=planetaryDipoleMoment(tplanet)/MDIPE
        thermevol+=[tplanet.Rg,tplanet.Rc,tplanet.Ric,
                    tplanet.rho,tplanet.rhoc,tplanet.Q,
                    tplanet.Qconv,tplanet.T,tplanet.Mdip]
    thermevol=toStack(ts)|thermevol

    #----------------------------------------
    #OTHER
    #----------------------------------------
    planet.tdyn=ts[-1]
    tcond=ts<planet.tau
    Mdips=thermevol[:,9]
    Mdipts=thermevol[tcond,9]
    try:
        planet.Mdipmax=max(Mdips)
        planet.Mdipmaxt=max(Mdipts)
        planet.tMdipmax=ts[Mdips.argmax()]
    except ValueError:
        planet.Mdipmax=Mdips[0]
        planet.Mdipmaxt=Mdips[0]
        planet.tMdipmax=ts[0]
    
else:
    if planet.M<1.0:
        PRINTOUT("Planet is Sub-Earth")
        errorCode("RANGE_ERROR")
    else:
        PRINTOUT("Planet is out of range")
        errorCode("RANGE_ERROR")
    planet.type="Sub-Earth"

if planet.worb<0:planet.worb=0
if planet.Mg<0.05:
    planet.title=r"$M_p=%.3f\,M_{\\rm Earth}$, CMF=%.2f, $\\tau=%.2f$ Gyr, $R_p=%.3f\,R_{\\rm Earth}$"%(planet.M,planet.CMF,planet.tau,planet.Rp)
else:
    planet.title=r"$M_p=%.3f\,M_{\\rm Jup}$, $f_{\\rm H/He}=%.3f$, $\\tau=%.2f$ Gyr, $R_p=%.3f\,R_{\\rm Jup}$"%(planet.Mg,planet.fHHe,planet.tau,planet.Rg)

if len(planet.str_PlanetID)>0:pltitle="%s: "%planet.str_PlanetID.replace("'","")
else:pltitle=""

###################################################
#PLANETARY ORBIT
###################################################
#ORBITAL PARAMETERS
if planet.aorb==0 and planet.Porb>0:
    planet.aorb=aKepler(planet.Porb,planet.M*MEARTH/MSUN,planet.Morb)

if planet.Porb==0 and planet.aorb>0:
    planet.Porb=PKepler(planet.aorb,planet.M*MEARTH/MSUN,planet.Morb)

if planet.Porb>0 and planet.aorb>0:
    Porbt=PKepler(planet.aorb,planet.M*MEARTH/MSUN,planet.Morb)
    aorbt=aKepler(planet.Porb,planet.M*MEARTH/MSUN,planet.Morb)
    if abs(Porbt-planet.Porb)/planet.Porb>1E-2 or abs(aorbt-planet.aorb)/planet.aorb>1E-2:
        PRINTERR("You have provided simultaneously a semimajor axis (aorb=%e) and period (Porb=%e) but they are not compatible.  The right pair will be (a,P)=(%e,%e) or (a,P)=(%e,%e)."%(planet.aorb,
                                                                                                                                                                                            planet.Porb,
                                                                                                                                                                                            planet.aorb,
                                                                                                                                                                                            Porbt,
                                                                                                                                                                                            aorbt,
                                                                                                                                                                                            planet.Porb))
        PRINTERR("Using the second one.")
        planet.aorb=aorbt

if planet.Porb==0 and planet.aorb==0:
    PRINTERR("Planet is inside star: Porb = %e, aorb = %e"%(planet.Porb,
                                                             planet.aorb))
    errorCode("PARAMETER_ERROR")


planet.norb=2*np.pi/planet.Porb
planet.orbit=r"%s$a_{\\rm orb}$=%.2f AU, $e_{\\rm orb}$=%.2f, $P_{\\rm orb}$=%.2f days, $\omega_{\\rm orb}=%.1f^{\\rm o}$"%(pltitle,planet.aorb,planet.eorb,planet.Porb,planet.worb)

###################################################
#EPHEMERIS
###################################################
dt=0.5 #DAYS
ts=np.arange(0.0,1.1*planet.Porb,dt)
rorbs=stack(2)
for t in ts:
    rorb=orbitalPosition(planet.norb,
                         planet.aorb,
                         planet.eorb,t,
                         w=planet.worb*DEG)
    rorbs+=rorb
ephemeris=toStack(ts)|rorbs

###################################################
#STORE PLANETARY DATA
###################################################
fd=open(planet_dir+"planet.data","w")
fd.write("""\
from numpy import array
#OBJECT HASH
hash="%s"

#BULK PROPERTIES
type = "%s"
Mp=%.17e #Mearth
Rp=%.17e #Rearth
Mg = %.17e #Mjup
Rg=%.17e #Rjup
A=%.17e #m^2
g=%.17e #m/s^2
rho=%.17e #kg m^-3

#INTERIOR PROPERTIES
Rc=%.17e #Core Radius/R
Ric=%.17e #Inner core Radius/R
rhoc=%.17e #Inner core density
sigma=%.17e #Sigma in dynamo region
kappa=%.17e #Kappa in dynamo region

#THERMAL AND MAGNETIC (INSTANTANEOUS) PROPERTIES
tdyn=%.17e #Estimated dynamo lifetime 
Q=%.17e #Total heat emitted
T=%.17e #Effective black body temperature
Qconv=%.17e #Heat dissipated in a dynamo
Mdip=%.17e #MdipEarth
Mdipmax=%.17e #Maximum dipole moment (whole evolution)
tMdipmax=%.17e #Time of maximum dipole moment
Mdipmaxt=%.17e #Maximum dipole moment (until age)

#THERMAL OUTPUT EVOLUTION
thermevol=%s

#ORBITAL PROPERTIES
Porb=%.17e #days
aorb=%.17e #AU
norb=%.17e #rad days^-1

#ORBIT EPHEMERIS
ephemeris=%s

#TITLE
title="%s"
orbit="%s"
"""%(planet.hash,
     planet.type,
     planet.Mp,planet.Rp,
     planet.Mg,planet.Rg,
     planet.A,planet.g,planet.rho,
     planet.Rc,planet.Ric,planet.rhoc,planet.sigma,planet.kappa,
     planet.tdyn,
     planet.Q,planet.T,planet.Qconv,
     planet.Mdip,planet.Mdipmax,planet.tMdipmax,planet.Mdipmaxt,
     array2str(thermevol),
     planet.Porb,planet.aorb,planet.norb,
     array2str(ephemeris),
     planet.title,planet.orbit))
fd.close()

###################################################
#GENERATE PLOTS
###################################################
PRINTOUT("Creating plots...")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS SCHEMATIC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(planet_dir,"planet-schematic",\
"""
from BHM.BHMstars import *
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")

fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.0,0.0,1.0,1.0])

RJ=11.2
color='c'

plan=patches.Circle((0.0,0.0),planet.Rp,fc=color,ec='none',zorder=-10)
core=patches.Circle((0.0,0.0),planet.Rc*planet.Rp,fc='b',alpha=0.3,ec='none',zorder=-5)
icore=patches.Circle((0.0,0.0),planet.Ric*planet.Rp,fc='r',alpha=0.3,ec='none',zorder=-5)

earth=patches.Circle((0.0,0.0),1.0,
                     linestyle='dashed',fc='none',zorder=10)
jupiter=patches.Circle((0.0,0.0),RJ,
                       linestyle='dotted',fc='none',zorder=10)

ax.add_patch(plan)
ax.add_patch(core)
ax.add_patch(icore)
ax.add_patch(earth)
ax.add_patch(jupiter)

ax.text(0.0,1.0,'Earth',fontsize=12,transform=offSet(0,5),horizontalalignment='center')
ax.text(0.0,RJ,'Jupiter',fontsize=12,transform=offSet(0,5),horizontalalignment='center')
ax.text(0.0,-planet.Rp,'%%s'%%planet.str_PlanetID.replace("'",""),fontsize=14,transform=offSet(0,-10),horizontalalignment='center',verticalalignment='top')

ax.set_xticks([])
ax.set_yticks([])

ax.set_title(planet.title,position=(0.5,0.05),fontsize=16)

if planet.Mg<0.05:Rscale=1.0
else:Rscale=RJ
rang=max(1.5*Rscale,1.5*planet.Rp)
ax.set_xlim((-rang,+rang))
ax.set_ylim((-rang,+rang))
"""%(planet_dir,planet_dir),watermarkpos="inner")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#THERMAL EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(planet_dir,"thermal-evolution",\
"""
from BHM.BHMstars import *
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

thermevol=planet.thermevol
ts=thermevol[:,0]

props={
r"$\langle{\cal M}_{\\rm dip}\\rangle/{\cal M}_{\\rm Earth}$":
dict(
lstyle=dict(color='b'),
pcol=9),
r"$\langle Q\\rangle$ (W)":
dict(
lstyle=dict(color='k'),
pcol=6),
r"$\langle Q_{\\rm conv}\\rangle$ (W)":
dict(
lstyle=dict(color='r'),
pcol=7),
r"$\langle R_{\\rm ic}\\rangle/R_{\\rm p}$":
dict(
lstyle=dict(color='c'),
pcol=3),
r"$\langle R_{\\rm c}\\rangle/R_{\\rm p}$":
dict(
lstyle=dict(color='r'),
pcol=2),
r"$\langle \\rho_{\\rm c}\\rangle$ (kg m$^{-3}$)":
dict(
lstyle=dict(color='g'),
pcol=5),
r"$\langle \\rho\\rangle$ (kg m$^{-3}$)":
dict(
lstyle=dict(color='g'),
pcol=4),
}

for prop in props.keys():
    pdict=props[prop]
    exec("ps=thermevol[:,%%d]"%%(pdict["pcol"]))
    pm=ps.mean()
    if pm==0:pm=1
    st=pdict["lstyle"]
    ax.plot(ts,ps/pm,label="%%s=%%.2e"%%(prop,pm),**st)

ax.set_yscale("log")

if 'Gas' in planet.type:
    ax.set_xscale("log")

ax.set_xlim((0.1,10.0))
ax.legend(loc='best',prop=dict(size=10))

ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"Property/Mean value")

ax.grid()
ax.set_xlim((TAU_MIN,planet.tdyn))
ax.set_title(planet.title,position=(0.5,1.02),fontsize=16)
"""%(planet_dir,planet_dir),watermarkpos="outer")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#ORBIT
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(planet_dir,"planet-orbit",\
"""
from BHM.BHMstars import *
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")

fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.02,0.02,0.96,0.96])
xs=planet.ephemeris[:,1]
ys=planet.ephemeris[:,2]

ax.plot(xs,ys,'k-',label='Planet Orbit')
ax.plot([xs[0]],[ys[0]],'ko',markersize=5,markeredgecolor='none')

rang=1.2*planet.aorb*(1+planet.eorb)
ax.set_xlim((-rang,rang))
ax.set_ylim((-rang,rang))

xt=ax.get_xticks()
dx=xt[1]-xt[0]
dy=0.1
ax.axhline(-rang+dx/3,xmin=dy,xmax=dy+dx/(2*rang),color='k')
ax.text(dy+dx/(4*rang),dx/3/(2*rang)+0.01,
"%%.2f AU"%%dx,horizontalalignment='center',
transform=ax.transAxes)

ax.set_title(planet.title,position=(0.5,0.95),fontsize=14)
ax.text(0.5,0.92,planet.orbit,transform=ax.transAxes,horizontalalignment="center")
ax.plot([0],[0],'x')

ax.set_xticklabels([])
ax.set_yticklabels([])
"""%(planet_dir,planet_dir),watermarkpos='inner')

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(planet_dir+"planet.html","w")
fh.write("""\
<!--VERSION:%s-->
<html>
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>
<body>
<h2>Properties of Planet %s</h2>

<h3>Plots</h3>
<h4>Schematic Representation</h4>
<table>
<tr><td>
    <a href="%s/planet-schematic.png" target="_blank">
      <img width=100%% src="%s/planet-schematic.png">
    </a>
    <br/>
    <div class="caption">
    <i>Schematic Representation</i>
    (
    <a href="%s/planet-schematic.png.txt" target="_blank">data</a>|
    <a href="%s/BHMreplot.php?dir=%s&plot=planet-schematic.py" target="_blank">replot</a>
    )
    </div>
</td></tr>
</table>

<h3>Thermal and magnetic evolution:</h3>
<table>
  <tr><td>
      <a target="_blank" href="%s/thermal-evolution.png">
	<img width=100%% src="%s/thermal-evolution.png">
      </a>
      <br/>
      <div class="caption">
      <i>Evolution of stellar properties</i>
	(
	<a target="_blank" href="%s/thermal-evolution.png.txt">data</a>|
	<a target="_blank" href="%s/BHMreplot?dir=%s&plot=thermal-evolution.py">replot</a>
	)
      </div>
  </td></tr>
</table>

<h3>Planetary Orbit:</h3>
<table>
  <tr><td colspan=2>
      <a target="_blank" href="%s/planet-orbit.png">
	<img width=100%% src="%s/planet-orbit.png">
      </a>
      <br/>
      <div class="caption">
      <i>Orbit</i>
	(
	<a target="_blank" href="%s/planet-orbit.png.txt">data</a>|
	<a target="_blank" href="%s/BHMreplot?dir=%s&plot=planet-orbit.py">replot</a>
	)
      </div>
  </td></tr>
</table>

<h3>Numerical Properties</h3>

<h3>Basic Input Properties</h3>
<table>
  <tr><td>Mass (M<sub>E</sub>,M<sub>Jup</sub>):</td><td>%.3f, %.3f</td></tr>
  <tr><td>&tau; (Gyr):</td><td>%.2f</td></tr>
  <tr><td>CMF (Earth = 0.34):</td><td>%.2f</td></tr>
  <tr><td>f<sub>H/He</sub>:</td><td>%.3f</td></tr>
  <tr><td>P<sub>rot</sub> (days):</td><td>%.3f</td></tr>
</table>

<h3>Observed Properties</h3>
<table>
  <tr><td>R (R<sub>Earth</sub>):</td><td>%s &pm; %s</td></tr>
  <tr><td>M (M<sub>Earth</sub>):</td><td>%s &pm; %s</td></tr>
  <tr><td>a<sub>orb</sub> (AU):</td><td>%s &pm; %s</td></tr>
  <tr><td>e<sub>orb</sub>:</td><td>%s &pm; %s</td></tr>
  <tr><td>P<sub>orb</sub>:</td><td>%s &pm; %s</td></tr>
  <tr><td>&omega;<sub>orb</sub>:</td><td>%s &pm; %s</td></tr>
</table>

<h3>Bulk Properties:</h3>
<table>
  <tr><td>Planet type:</td><td>%s</td></tr>
  <tr><td>M<sub>p</sub> (M<sub>Earth</sub>,M<sub>Jupiter</sub>):</td><td>%.3f,%.3f</td></tr>
  <tr><td>R<sub>p</sub> (R<sub>Earth</sub>,R<sub>Jupiter</sub>):</td><td>%.3f,%.3f</td></tr>
  <tr><td>A (m<sup>2</sup>)):</td><td>%.2e</td></tr>
  <tr><td>g (m/s<sup>2</sup>):</td><td>%.3f</td></tr>
  <tr><td>&rho; (kg/m<sup>3</sup>):</td><td>%.3f</td></tr>
</table>

<h3>Interior Structure Properties:</h3>
<table>
  <tr><td>R<sub>core</sub> (R<sub>p</sub>):</td><td>%.2f</td></tr>
  <tr><td>R<sub>inner,core</sub> (R<sub>p</sub>):</td><td>%.2f</td></tr>
  <tr><td>&rho;<sub>core</sub> (kg/m<sup>3</sup>):</td><td>%.1f</td></tr>
  <tr><td>&sigma;</sub> (S/m):</td><td>%.3e</td></tr>
  <tr><td>&kappa;</sub>:</td><td>%.3e</td></tr>
</table>

<h3>Thermal and magnetic properties:</h3>
<table>
  <tr><td>t<sub>dyn</sub> (Gyr):</td><td>%.2f</td></tr>
  <tr><td>Q (W):</td><td>%.2e</td></tr>
  <tr><td>T<sub>eff</sub> (K):</td><td>%.2f</td></tr>
  <tr><td>Q<sub>conv</sub> (W):</td><td>%.2e</td></tr>
  <tr><td>M<sub>dip</sub> (M<sub>dip,Earth</sub>):</td><td>%.2f</td></tr>
  <tr><td>M<sub>dip,max</sub> (M<sub>dip,Earth</sub>):</td><td>%.2f</td></tr>
  <tr><td>t<sub>dip,max</sub> (Gyr):</td><td>%.2f</td></tr>
  <tr><td>M<sub>dip,max,t</sub> (M<sub>dip,Earth</sub>):</td><td>%.2f</td></tr>
</table>

<h3>Planetary Orbit Properties:</h3>
<table >
  <tr><td>P (days):</td><td>%.2f</td></tr>
  <tr><td>a (AU):</td><td>%.2f</td></tr>
  <tr><td>n (rad/day):</td><td>%.2f</td></tr>
</table>
</body>
</html>
"""%(VERSION,
     WEB_DIR,
     planet.str_PlanetID,
     planet_webdir,planet_webdir,planet_webdir,WEB_DIR,planet_webdir,
     planet_webdir,planet_webdir,planet_webdir,WEB_DIR,planet_webdir,
     planet_webdir,planet_webdir,planet_webdir,WEB_DIR,planet_webdir,
     planet.Mp,planet.Mg,
     planet.tau,planet.CMF,planet.fHHe,planet.Prot,
     tableValue(planet.R,"%.4f",">0","-"),tableValue(planet.Rerr,"%.4f",">0","-"),
     tableValue(planet.M,"%.4f",">0","-"),tableValue(planet.Merr,"%.4f",">0","-"),
     tableValue(planet.aorb,"%.4f",">0","-"),tableValue(planet.aorberr,"%.4f",">0","-"),
     tableValue(planet.eorb,"%.4f",">0","-"),tableValue(planet.eorberr,"%.4f",">0","-"),
     tableValue(planet.Porb,"%.4f",">0","-"),tableValue(planet.Porberr,"%.4f",">0","-"),
     tableValue(planet.worb,"%.4f",">0","-"),tableValue(planet.worberr,"%.4f",">0","-"),
     planet.type,
     planet.Mp,planet.Mg,
     planet.Rp,planet.Rg,
     planet.A,planet.g,planet.rho,
     planet.Rc,planet.Ric,planet.rhoc,planet.sigma,planet.kappa,
     planet.tdyn,planet.Q,planet.T,planet.Qconv,
     planet.Mdip,planet.Mdipmax,planet.tMdipmax,planet.Mdipmaxt,
     planet.Porb,planet.aorb,planet.norb
     ))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
closeObject(planet_dir)
