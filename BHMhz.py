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
# Habitable Zone
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

sys_dir,ihz_conf,qover=\
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
#LOADING PLANET
planet_conf="planet.conf"
planet,planet_dir,planet_str,planet_hash,planet_liv,planet_stg=\
    signObject("planet",sys_dir+"/"+planet_conf)
planet+=loadConf(planet_dir+"planet.data")

###################################################
#LOAD IHZ OBJECT
###################################################
PRINTOUT("Loading object from '%s'"%ihz_conf)
ihz,ihz_str,ihz_hash,ihz_dir=\
     makeObject("hz",sys_dir+"/"+ihz_conf,qover=qover)
PRINTOUT("Object directory '%s' created"%ihz_dir)
ihz_webdir="/"+WEB_DIR+ihz_dir
ihz.hash=ihz_hash

###################################################
#CALCULATE BINARY HABITABLE ZONE AT TAU
###################################################
ihz.tau=star1.tau

str_incrit_wd=ihz.str_incrit_wd.replace("'","")
str_outcrit_wd=ihz.str_outcrit_wd.replace("'","")
linwd,loutwd=HZbin(star2.M/star1.M,star1.Lins,star2.Lins,star1.Tins,
                   binary.abin,
                   crits=[str_incrit_wd,str_outcrit_wd])

Pinwd=PKepler(linwd,star1.M,star2.M);ninwd=2*np.pi/Pinwd
Poutwd=PKepler(loutwd,star1.M,star2.M);noutwd=2*np.pi/Poutwd

str_incrit_nr=ihz.str_incrit_nr.replace("'","")
str_outcrit_nr=ihz.str_outcrit_nr.replace("'","")
linnr,loutnr,leeq=HZbin(star2.M/star1.M,star1.Lins,star2.Lins,star1.Tins,
                        binary.abin,
                        crits=[str_incrit_nr,str_outcrit_nr],eeq=True)
Pinnr=PKepler(linnr,star1.M,star2.M);ninnr=2*np.pi/Pinnr
Poutnr=PKepler(loutnr,star1.M,star2.M);noutnr=2*np.pi/Poutnr
Peeq=PKepler(leeq,star1.M,star2.M);neeq=2*np.pi/Peeq
ihz.leeq=leeq

###################################################
#CALCULATE INSOLATION AND PHOTON FLUXES
###################################################
#EMISSION
power1=planckPower(LAMB0,LAMBINF,star1.Tins)
photons1=planckPhotons(LAMB1,LAMB2,star1.Tins)
power2=planckPower(LAMB0,LAMBINF,star2.Tins)
photons2=planckPhotons(LAMB1,LAMB2,star2.Tins)

#EPHEMERIS
binephem=binary.ephemeris
tb=binephem[:,0]
r1s=interpArray(tb,binephem[:,1:3])
r2s=interpArray(tb,binephem[:,3:5])

planephem=planet.ephemeris
tp=planephem[:,0]
rps=interpArray(tp,planephem[:,1:3])

dt=0.5 #DAYS
ts=np.arange(0.0,1.5*planet.Porb,dt)

"""
insolation:
0:t
1:inso.@rp
2:ppfd.@rp
3:inso.@req
4:ppfd.@req
5:inso.@rinwd
6:ppfd.@rinwd
7:inso.@routwd
8:ppfd.@routwd
9:inso.@rinnr
10:ppfd.@rinnr
11:inso.@routnr
12:ppfd.@routnr
"""

insolation=stack(12)
for t in ts:
    #TIMES
    tb=np.mod(t,binary.Pbin)
    tp=np.mod(t,planet.Porb)

    #POSITIONS
    r1=r1s(tb)
    r2=r2s(tb)
    rp=rps(tp)
    
    #POSITION IN LIMITS
    rinwd=np.array([linwd*cos(ninwd*t),linwd*sin(ninwd*t)])
    routwd=np.array([loutwd*cos(noutwd*t),loutwd*sin(noutwd*t)])

    rinnr=np.array([linnr*cos(ninnr*t),linnr*sin(ninnr*t)])
    routnr=np.array([loutnr*cos(noutnr*t),loutnr*sin(noutnr*t)])

    reeq=np.array([leeq*cos(neeq*t),leeq*sin(neeq*t)])
     
    insol=[]
    for r in rp,reeq,rinwd,routwd,rinnr,routnr:
        #RELATIVE POSITIONS
        R1=r-r1
        R2=r-r2

        #DISTANCES
        d1=norm(R1)
        d2=norm(R2)
        
        #DISSOLVE RATIO
        dis1=(star1.Rins*RSUN/(d1*AU))**2
        dis2=(star2.Rins*RSUN/(d2*AU))**2

        #FLUX
        flux1=power1*dis1
        flux2=power2*dis2
        flux=flux1+flux2

        #PHOTON DENSITY
        ppf1=photons1*dis1
        ppf2=photons2*dis2
        ppf=ppf1+ppf2
    
        insol+=[flux,ppf]

    insolation+=insol

insolation=toStack(ts)|insolation
fstats=stack(5)
pstats=stack(5)
for i in range(1,12,2):
    fstats+=[statsArray(insolation[:,i])]
    pstats+=[statsArray(insolation[:,i+1])]

###################################################
#INSOLATION AND PPFD FOR SINGLE PRIMARY
###################################################
leeqs=star1.lsun
dis=(star1.Rins*RSUN/(leeqs*AU))**2
ihz.fluxs=power1*dis
ihz.ppfds=photons1*dis

###################################################
#CALCULATE BINARY HABITABLE ZONE EVOLUTION
###################################################
taumax=min(star1.tau_max,star2.tau_max)
ts=star1.evotrack[:,0]
hz=stack(3)
shz=stack(3)
for tau in ts:
    lin,lout,leeq=HZbin(star2.M/star1.M,
                        star1.Lfunc(tau),star2.Lfunc(tau),star1.Tfunc(tau),
                        binary.abin,
                        crits=[str_incrit_wd,str_outcrit_wd],eeq=True)
    slin,sleeq,slout=HZ(star1.Lfunc(tau),star1.Tfunc(tau),
                        lin=str_incrit_wd,lout=str_outcrit_wd)
    hz+=[lin,leeq,lout]
    shz+=[slin,sleeq,slout]
hz=toStack(ts)|hz
shz=toStack(ts)|shz

#CONTINUOUS HABITABLE ZONE
tms=star1.tau_ms
cond=ts>=0.1
clout=min(hz[cond,3])
clin=np.interp(tms,ts,hz[:,1])
if clin<binary.acrit:
    clin=binary.acrit

#HZ PLANETARY EXIT TIME
ts=hz[:,0]
cond=hz[:,1]<planet.aorb
try:texit=ts[cond][-1]
except:texit=tms

#MAXIMUM OUTER LIMIT
cond=ts<tms
louts=hz[:,3]
try:loutmax=louts[cond][-1]
except:loutmax=max(ihz.hz[:,3])

###################################################
#STORE iHZ DATA
###################################################
if len(binary.str_SysID)>0:bintitle="%s: "%binary.str_SysID.replace("'","")
else:bintitle=""
ihz.title=r"%s$M_p=%.3f\,M_{\\rm Jup}$, $f_{\\rm H/He}=%.3f$, $\\tau=%.2f$ Gyr, $R_p=%.3f\,R_{\\rm Jup}$"%(bintitle,planet.Mg,planet.fHHe,planet.tau,planet.Rg)

#INITIALS
ini_inwd=initialsString(ihz.str_incrit_wd)
ini_outwd=initialsString(ihz.str_outcrit_wd)
ini_innr=initialsString(ihz.str_incrit_nr)
ini_outnr=initialsString(ihz.str_outcrit_nr)

fd=open(ihz_dir+"hz.data","w")
fd.write("""\
from numpy import array

#TITLE
title="%s"

#TIMES
tau = %.17e #Gyr
taumax = %.17e #Gyr
taums = %.17e #Gyr
tauhl = %.17e #Gyr

#BHZ INSTANTANEOUS LIMITS
linwd = %.17e #AU
loutwd = %.17e #AU
leeq = %.17e #AU
linnr = %.17e #AU
loutnr = %.17e #AU

#CHZ
clin = %.17e #Gyr
clout = %.17e #Gyr
loutmax = %.17e #Gyr

#HZ INITIALS
ini_inwd = "%s"
ini_outwd = "%s"
ini_innr = "%s"
ini_outnr = "%s"

#FLUX AND PHOTON DENSITY
insolation=%s
fluxs=%.17e #W m^-2
ppfds=%.17e #m^-2 s^-1

#FLUX AND PHOTON DENSITY STATS
#COLS:mean,min,max,range,st.dev.
#ROWS:planet,Earth-equivalent,inner(wide),outer(wide),inner(narrow),outer(narrow),single primary
fstats=%s
pstats=%s

#BINARY HABITABLE ZONE EVOLUTION
hz=%s

#PRIMARY HABITABLE ZONE EVOLUTION
shz=%s
"""%(ihz.title,
     ihz.tau,taumax,tms,texit,
     linwd,loutwd,
     ihz.leeq,
     linnr,loutnr,
     clin,clout,loutmax,
     ini_inwd,ini_outwd,ini_innr,ini_outnr,
     array2str(insolation),
     ihz.fluxs,ihz.ppfds,
     array2str(fstats.array),
     array2str(pstats.array),
     array2str(hz),
     array2str(shz)
     ))
fd.close()

###################################################
#GENERATE PLOTS
###################################################
PRINTOUT("Creating plots...")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INSTANTANEOUS HABITABLE ZONE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(ihz_dir,"iHZ",\
"""
from BHM.BHMstars import *
from BHM.BHMastro import *

binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
ihz=\
loadConf("%s"+"hz.conf")+\
loadConf("%s"+"hz.data")

fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.01,0.01,0.98,0.98])
ax.set_xticklabels([])
ax.set_yticklabels([])

bbox=dict(fc='w',ec='none')

#WIDE HZ
outwd=patches.Circle((0,0),ihz.loutwd,facecolor='g',
                     alpha=0.3,linewidth=2,zorder=-10)
ax.add_patch(outwd)
inwd=patches.Circle((0,0),ihz.linwd,facecolor='r',edgecolor='r',
                    alpha=0.2,linewidth=2,zorder=-5)
ax.add_patch(inwd)

#NARROW HZ
outnr=patches.Circle((0,0),ihz.loutnr,facecolor='g',
                     alpha=0.3,linewidth=2,zorder=-10)
ax.add_patch(outnr)

innr=patches.Circle((0,0),ihz.linnr,facecolor='r',edgecolor='r',
                    alpha=0.2,linewidth=2,zorder=-5)
ax.add_patch(innr)

#CONTINUOUS HZ
ccolor=cm.autumn(0.3)
cin=patches.Circle((0,0),ihz.clin,facecolor='none',edgecolor=ccolor,linestyle='solid',
                    alpha=1,linewidth=1,zorder=-5)
ax.add_patch(cin)

cout=patches.Circle((0,0),ihz.clout,facecolor='none',edgecolor=ccolor,linestyle='solid',
                    alpha=1,linewidth=1,zorder=-5)
ax.add_patch(cout)

#WHITE INNER AREA
inwd=patches.Circle((0,0),ihz.linwd,facecolor='w',edgecolor='g',
                    linewidth=2,zorder=-4)
ax.add_patch(inwd)

#EARTH EQUIVALENT DISTANCE
aeq=patches.Circle((0,0),ihz.leeq,facecolor='none',edgecolor=cm.gray(0.0),
                   linewidth=1,linestyle='dotted',zorder=20)
ax.add_patch(aeq)

#PLANET ORBIT
xs=planet.ephemeris[:,1]
ys=planet.ephemeris[:,2]
ax.plot(xs,ys,'k-',linewidth=2,label='Planet Orbit')
ax.plot([xs[0]],[ys[0]],'ko',markersize=5,markeredgecolor='none')

#BINARY ORBIT
xs1=binary.ephemeris[:,1]
ys1=binary.ephemeris[:,2]
xs2=binary.ephemeris[:,3]
ys2=binary.ephemeris[:,4]
ax.plot(xs1,ys1,'b-',label='Primary')
ax.plot(xs2,ys2,'r-',label='Secondary')
ax.plot([xs1[0]],[ys1[0]],'bo',markersize=5,markeredgecolor='none')
ax.plot([xs2[0]],[ys2[0]],'ro',markersize=5,markeredgecolor='none')

#CRITICAL DISTANCE
aCR=patches.Circle((0,0),binary.acrit,facecolor='none',edgecolor='k',
                   linewidth=2,linestyle='dashed',zorder=20)
ax.add_patch(aCR)

#TITLE
ax.set_title(binary.title,position=(0.5,0.95),fontsize=11)
ax.text(0.5,0.92,planet.orbit,fontsize=11,
transform=ax.transAxes,horizontalalignment='center')

#LIMITS
ax.text(0.5,0.08,r"$\\tau$ =%%.2f Gyr, $l_{\\rm in,%%s}$=%%.2f AU, $l_{\\rm in,%%s}$=%%.2f AU, $l_{\\rm E,eq}$=%%.2f AU, $l_{\\rm out,%%s}$=%%.2f AU, $l_{\\rm out,%%s}$=%%.2f AU"%%(planet.tau,ihz.ini_inwd,ihz.linwd,ihz.ini_innr,ihz.linnr,ihz.leeq,ihz.ini_outnr,ihz.loutnr,ihz.ini_outwd,ihz.loutwd),transform=ax.transAxes,horizontalalignment='center',fontsize=11)
ax.text(0.5,0.04,r"$a_{\\rm crit}=%%.2f$ AU, $l_{\\rm in,cont}=%%.2f$ AU, $l_{\\rm out,cont}$=%%.2f AU"%%(binary.acrit,ihz.clin,ihz.clout),transform=ax.transAxes,horizontalalignment='center',fontsize=11)

#RANGE
rang=1.5*max(ihz.loutwd,max(abs(xs)),max(abs(ys)))
ax.set_xlim((-rang,+rang))
ax.set_ylim((-rang,+rang))

#RESONANCES
imax=int(np.ceil(PKepler(np.sqrt(2)*rang,planet.Morb,0.0)/binary.Pbin))
for ires in xrange(2,imax):
    ares=aKepler(ires*binary.Pbin,planet.Morb,0.0)
    res=patches.Circle((0,0),ares,facecolor='none',edgecolor='k',linestyle='solid',
                       alpha=0.1,linewidth=1,zorder=-3)
    ax.add_patch(res)

#MEASURE MARK
xt=ax.get_xticks()
dx=xt[1]-xt[0]
dy=0.02
ax.axhline(-rang+dx/5,xmin=dy,xmax=dy+dx/(2*rang),color='k')
ax.text(dy+dx/(4*rang),dx/5/(2*rang)+0.01,
"%%.2f AU"%%dx,horizontalalignment='center',
transform=ax.transAxes)

"""%(binary_dir,binary_dir,
     planet_dir,planet_dir,
     ihz_dir,ihz_dir
     ),watermarkpos="inner")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#FLUX AND PHOTON DENSITY
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(ihz_dir,"insolation",\
"""
from BHM.BHMstars import *
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
ihz=\
loadConf("%s"+"hz.conf")+\
loadConf("%s"+"hz.data")

fig=plt.figure(figsize=(8,8))
axi=fig.add_axes([0.12,0.10,0.8,0.40])
axp=fig.add_axes([0.12,0.52,0.8,0.40])

insolation=ihz.insolation
fstats=ihz.fstats
pstats=ihz.pstats
ts=insolation[:,0]

#PLANET
axi.axhline(ihz.fstats[0,0]/SOLAR_CONSTANT,color='b',linestyle=':',linewidth=2,label='Average')
axp.axhline(ihz.pstats[0,0]/PPFD_EARTH,color='r',linestyle=':',linewidth=2,label='Average')

axi.plot(ts/planet.Porb,insolation[:,1]/SOLAR_CONSTANT,color='b',linestyle='-',linewidth=2,label='Instantaneous')
axp.plot(ts/planet.Porb,insolation[:,2]/PPFD_EARTH,color='r',linestyle='-',linewidth=1,label='Instantaneous')

#RANGE HZ 
axi.fill_between(ts/planet.Porb,insolation[:,5]/SOLAR_CONSTANT,insolation[:,7]/SOLAR_CONSTANT,
color='g',linestyle='-',linewidth=1,alpha=0.3)

axp.fill_between(ts/planet.Porb,insolation[:,6]/PPFD_EARTH,insolation[:,8]/PPFD_EARTH,
color='g',linestyle='-',linewidth=1,alpha=0.3)

#LABELS

axp.set_title(binary.title,position=(0.5,1.02),fontsize=11)

for ax in axi,axp:
    ax.plot([],[],"g-",linewidth=10,alpha=0.3,label="BHZ")
    ax.grid()
    ax.set_xlim((0.0,1.0))
    ax.legend(loc='best',prop=dict(size=10))

imin,imax=axi.get_ylim()
axp.set_ylim((imin,imax))

axp.set_yticks(ax.get_yticks()[1:])
axp.set_xticklabels([])

axi.set_xlabel('orbital phase',fontsize=12)
axi.set_ylabel('Insolation (PEL)',fontsize=12)
axp.set_ylabel(r'PPFD (PEL)',fontsize=12)
"""%(binary_dir,binary_dir,
     planet_dir,planet_dir,
     ihz_dir,ihz_dir
     ),watermarkpos="outer")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#EVOLUTION AND CONTINUOUS HABITABLE ZONE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(ihz_dir,"hz-evolution",\
"""
from BHM.BHMstars import *
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
ihz=\
loadConf("%s"+"hz.conf")+\
loadConf("%s"+"hz.data")

fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

ts=ihz.hz[:,0]

#BHZ
ax.plot(ts,ihz.hz[:,1],'r-',linewidth=2)
#ax.plot(ts,ihz.hz[:,2],'k:',linewidth=2)
ax.plot(ts,ihz.hz[:,3],'b-',linewidth=2)
ax.fill_between(ts,ihz.hz[:,1],ihz.hz[:,3],color='g',alpha=0.3)

#SHZ
ax.plot(ts,ihz.shz[:,1],'r--',linewidth=2)
ax.plot(ts,ihz.shz[:,3],'b--',linewidth=2)
ax.fill_between(ts,ihz.hz[:,1],ihz.hz[:,3],color='g',alpha=0.3)

#CRITICAL DISTANCE
ax.axhline(binary.acrit,color='k',linewidth=2,linestyle='--',label=r'$a_{\\rm crit}$')

#PLANET ORBIT
ax.axhline(planet.aorb,color='k',linewidth=2,label='Planet')

#DECORATION
ax.set_xlim((0.0,min(1.1*ihz.taums,ihz.ts[-1])))
ax.set_ylim((min(ihz.shz[:,1]),ihz.loutmax))

ax.set_xlabel(r"$\\tau$ (Gyr)",fontsize=12)
ax.set_ylabel(r"$r$ (AU)",fontsize=12)
ax.set_title(binary.title,position=(0.5,1.02),fontsize=11)

#CHZ
ymin,ymax=ax.get_ylim()
rchz=0.95*(ihz.clout-ymin)/(ymax-ymin)
rihz=1.05*(ihz.clin-ymin)/(ymax-ymin)
ax.axhspan(ihz.clin,ihz.clout,color='k',alpha=0.3,linewidth=3)
ax.text(0.5,rchz,"Continuous Habitable Zone",fontsize=18,
horizontalalignment='center',verticalalignment='top',transform=ax.transAxes)
ax.text(0.05,rchz,"%%.2f AU"%%(ihz.clout),fontsize=10,
horizontalalignment='center',verticalalignment='top',transform=ax.transAxes)
ax.text(0.05,rihz,"%%.2f AU"%%(ihz.clin),fontsize=10,
horizontalalignment='center',verticalalignment='bottom',transform=ax.transAxes)
ax.legend(loc='best',prop=dict(size=12))
"""%(binary_dir,binary_dir,
     planet_dir,planet_dir,
     ihz_dir,ihz_dir
     ),watermarkpos="outer")

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(ihz_dir+"hz.html","w")
fh.write("""\
<!--VERSION:%s-->
<html>
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>
<body>

<h2>BHZ of %s</h2>

<h3>Plots</h3>

<h4>Instantaneous BHZ</h4>

<table>
  <tr><td colspan=2>
      <a target="_blank" href="%s/iHZ.png">
	<img width=100%% src="%s/iHZ.png">
      </a>
      <br/>
      <div class="caption">
      <i>Instantaneous Habitable Zone</i>
	(
	<a target="_blank" href="%s/iHZ.png.txt">data</a>|
	<a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=iHZ.py">replot</a>
	)
      </div>
  </td></tr>
</table>

<h4>Insolation and Photosynthetic Photon Flux Density</h4>

<table>
  <tr><td colspan=2>
      <a target="_blank" href="%s/insolation.png">
	<img width=100%% src="%s/insolation.png">
      </a>
      <br/>
      <div class="caption">
      <i>Insolation</i>
	(
	<a target="_blank" href="%s/insolation.png.txt">data</a>|
	<a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=insolation.py">replot</a>
	)
      </div>
  </td></tr>
</table>

<h4>Continuous BHZ</h4>

<table>
  <tr><td colspan=2>
      <a target="_blank" href="%s/hz-evolution.png">
	<img width=100%% src="%s/hz-evolution.png">
      </a>
      <br/>
      <div class="caption">
      <i>Evolution of Habitable Zone</i>
	(
	<a target="_blank" href="%s/hz-evolution.png.txt">data</a>|
	<a target="_blank" href="%s/BHMreplot.php?dir=%s&plot=hz-evolution.py">replot</a>
	)
      </div>
  </td></tr>
</table>

<h3>Numerical Properties</h3>

<h3>Instantaneous BHZ Limits</h3>
<table>
  <tr><td>&tau;(Gyr)</td><td>%.3f</td></tr>
  <tr><td>l<sub>Earth,eq</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Wide HZ</b></td></tr>
  <tr><td>l<sub>in,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Narrow HZ</b></td></tr>
  <tr><td>l<sub>in,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,%s</sub> (AU):</td><td>%.3f</td></tr>
</table>
<h3>Continuous Habitable Zone</h3>
<table>
  <tr><td>&tau;<sub>MS</sub> (Gyr):</td><td>%.3f</td></tr>
  <tr><td>&tau;<sub>p,HL</sub> (Gyr):</td><td>%.3f</td></tr>
  <tr><td>l<sub>cin,max</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>cout,min</sub> (AU):</td><td>%.3f</td></tr>
</table>
<h3>Insolation and Photon Flux</h3>
<table>
  <tr><td>&lt;S(Planet,a=%.2f,e=%.2f)&gt; [W/m<sup>2</sup>,S<sub>Sun</sub>]:</td><td>%.3f, %.3f</td></tr>
  <tr><td>S(Planet)/S<sub>Sun</sub>(min,max,range,std):</td><td>%.3f,%.3f,%.3f,%.3f</td></tr>
</table>
</body>
</html>
"""%(VERSION,
     WEB_DIR,
     binary.str_SysID,
     ihz_webdir,ihz_webdir,ihz_webdir,WEB_DIR,ihz_webdir,
     ihz_webdir,ihz_webdir,ihz_webdir,WEB_DIR,ihz_webdir,
     ihz_webdir,ihz_webdir,ihz_webdir,WEB_DIR,ihz_webdir,
     ihz.tau,
     leeq,
     ini_inwd,linwd,ini_outwd,loutwd,
     ini_innr,linnr,ini_outnr,loutnr,
     tms,texit,
     clin,clout,
     planet.aorb,planet.eorb,fstats.array[0,0],fstats.array[0,0]/SOLAR_CONSTANT,
     fstats.array[0,1]/SOLAR_CONSTANT,fstats.array[0,2]/SOLAR_CONSTANT,
     fstats.array[0,3]/SOLAR_CONSTANT,fstats.array[0,4]/SOLAR_CONSTANT
     ))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
closeObject(ihz_dir)
