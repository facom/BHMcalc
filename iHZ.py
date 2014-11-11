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
# Instantaneous Habitable Zone
# Inputs: 
# - Stellar properties (star1.conf,star2.conf)
# - Binary properties (binary.conf)
# - Planetary properties (planet.conf)
# Outputs: 
# - iHZ data (iHZ.data)
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
   python %s <ihz>.conf <binary>.conf <star1>.conf <star1>.conf <planet>.conf <qoverride>

   <ihz>.conf (file): Module configuration

   <binary>.conf (file): Configuration file with data about binary.

   <star1>.conf,<star2>.conf (file): Configuration file with data
   about stars.

   <planet>.conf (file): Configuration file with data about planet.

   <qoverride> (int 0/1): Override any previously existent
   calculation.
"""%argv[0]

ihz_conf,binary_conf,star1_conf,star2_conf,planet_conf,qover=\
    readArgs(argv,
             ["str","str","str","str","str","int"],
             ["ihz.conf",
              "binary.conf","star1.conf","star2.conf",
              "planet.conf","0"],
             Usage=Usage)

###################################################
#LOAD PREVIOUS OBJECTS
###################################################
PRINTOUT("Loading other objects...")
#==================================================
#LOADING BINARY
binary,binary_dir,binary_str,binary_hash,binary_liv,binary_stg=\
    signObject(binary_conf)
binary+=loadConf(binary_dir+"binary.data")
#==================================================
#LOADING STAR 1
star1,star1_dir,star1_str,star1_hash,star1_liv,star1_stg=\
    signObject(star1_conf)
star1+=loadConf(star1_dir+"star.data")
evoInterpFunctions(star1)
#==================================================
#LOADING STAR 2
star2,star2_dir,star2_str,star2_hash,star2_liv,star2_stg=\
    signObject(star2_conf)
star2+=loadConf(star2_dir+"star.data")
evoInterpFunctions(star2)
#==================================================
#LOADING PLANET
planet,planet_dir,planet_str,planet_hash,planet_liv,planet_stg=\
    signObject(planet_conf)
planet+=loadConf(planet_dir+"planet.data")
###################################################
#LOAD IHZ OBJECT
###################################################
ihz,ihz_str,ihz_hash,ihz_dir=\
    makeObject(ihz_conf,qover=qover)
ihz_webdir=WEB_DIR+ihz_dir
PRINTOUT("Object hash:%s"%ihz_hash)

###################################################
#CALCULATE BINARY HABITABLE ZONE AT TAU
###################################################
ihz.tau=star1.tau

incrit_wd=ihz.incrit_wd.replace("'","")
outcrit_wd=ihz.outcrit_wd.replace("'","")
linwd,loutwd=HZbin(star2.M/star1.M,star1.L,star2.L,star1.T,
                   binary.abin,
                   crits=[incrit_wd,outcrit_wd])
Pinwd=PKepler(linwd,star1.M,star2.M);ninwd=2*np.pi/Pinwd
Poutwd=PKepler(loutwd,star1.M,star2.M);noutwd=2*np.pi/Poutwd

incrit_nr=ihz.incrit_nr.replace("'","")
outcrit_nr=ihz.outcrit_nr.replace("'","")
linnr,loutnr,leeq=HZbin(star2.M/star1.M,star1.L,star2.L,star1.T,
                        binary.abin,
                        crits=[incrit_nr,outcrit_nr],eeq=True)
Pinnr=PKepler(linnr,star1.M,star2.M);ninnr=2*np.pi/Pinnr
Poutnr=PKepler(loutnr,star1.M,star2.M);noutnr=2*np.pi/Poutnr
Peeq=PKepler(leeq,star1.M,star2.M);neeq=2*np.pi/Peeq

###################################################
#CALCULATE INSOLATION AND PHOTON FLUXES
###################################################
#EMISSION
power1=planckPower(LAMB0,LAMBINF,star1.T)
photons1=planckPhotons(LAMB1,LAMB2,star1.T)
power2=planckPower(LAMB0,LAMBINF,star2.T)
photons2=planckPhotons(LAMB1,LAMB2,star2.T)

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
        dis1=(star1.R*RSUN/(d1*AU))**2
        dis2=(star2.R*RSUN/(d2*AU))**2

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
#CALCULATE BINARY HABITABLE ZONE EVOLUTION
###################################################
taumax=min(star1.taumax,star2.taumax)
ts=star1.evotrack[:,0]
hz=stack(3)
shz=stack(3)
for tau in ts:
    lin,lout,leeq=HZbin(star2.M/star1.M,
                        star1.Lfunc(tau),star2.Lfunc(tau),star1.Tfunc(tau),
                        binary.abin,
                        crits=[incrit_wd,outcrit_wd],eeq=True)
    slin,sleeq,slout=HZ(star1.Lfunc(tau),star1.Tfunc(tau),
                        lin=incrit_wd,lout=outcrit_wd)
    hz+=[lin,leeq,lout]
    shz+=[slin,sleeq,slout]
hz=toStack(ts)|hz
shz=toStack(ts)|shz

#CONTINUOUS HABITABLE ZONE
tms=star1.taums
clout=min(hz[:,3])
clin=np.interp(tms,ts,hz[:,1])
if clin<binary.acrit:
    clin=binary.acrit

###################################################
#STORE iHZ DATA
###################################################
ihz.title=r"$M_p=%.3f\,M_{\\rm Jup}$, $f_{\\rm H/He}=%.3f$, $\\tau=%.2f$ Gyr, $R_p=%.3f\,R_{\\rm Jup}$"%(planet.Mg,planet.fHHe,planet.tau,planet.Rg)

#INITIALS
ini_inwd=initialsString(ihz.incrit_wd)
ini_outwd=initialsString(ihz.outcrit_wd)
ini_innr=initialsString(ihz.incrit_nr)
ini_outnr=initialsString(ihz.outcrit_nr)

fd=open(ihz_dir+"ihz.data","w")
fd.write("""\
from numpy import array

#TITLE
title="%s"

#HZ INITIALS
ini_inwd = "%s"
ini_outwd = "%s"
ini_innr = "%s"
ini_outnr = "%s"

#HZ EDGES
taumax = %.17e #Gyr
tau = %.17e #Gyr
leeq = %.17e #AU
linwd = %.17e #AU
loutwd = %.17e #AU
linnr = %.17e #AU
loutnr = %.17e #AU

#CHZ
taums = %.17e #Gyr
clin = %.17e #Gyr
clout = %.17e #Gyr

#FLUX AND PHOTON DENSITY STATS
#COLS:mean,min,max,range,st.dev.
#ROWS:planet,Earth-equivalent,inner(wide),outer(wide),inner(narrow),outer(narrow)
fstats=%s
pstats=%s

#FLUX AND PHOTON DENSITY
insolation=%s

#BINARY HABITABLE ZONE EVOLUTION
hz=%s

#PRIMARY HABITABLE ZONE EVOLUTION
shz=%s
"""%(ihz.title,
     ini_inwd,ini_outwd,ini_innr,ini_outnr,
     taumax,ihz.tau,
     leeq,
     linwd,loutwd,
     linnr,loutnr,
     tms,clin,clout,
     array2str(fstats.array),
     array2str(pstats.array),
     array2str(insolation),
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
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
ihz=\
loadConf("%s"+"ihz.conf")+\
loadConf("%s"+"ihz.data")

fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.01,0.01,0.98,0.98])
ax.set_xticklabels([])
ax.set_yticklabels([])

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

#WHITE INNER AREA
inwd=patches.Circle((0,0),ihz.linwd,facecolor='w',edgecolor='r',
                    linewidth=2,zorder=0)
ax.add_patch(inwd)

#EARTH EQUIVALENT DISTANCE
aeq=patches.Circle((0,0),ihz.leeq,facecolor='none',edgecolor=cm.gray(0.5),
                   linewidth=2,linestyle='dotted',zorder=20)
ax.add_patch(aeq)

#PLANET ORBIT
xs=planet.ephemeris[:,1]
ys=planet.ephemeris[:,2]
ax.plot(xs,ys,'k-',label='Planet Orbit')
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
ax.set_title(binary.title,position=(0.5,0.95),fontsize=14)
ax.text(0.5,0.92,planet.orbit,fontsize=12,
transform=ax.transAxes,horizontalalignment='center')

#LIMITS
ax.text(0.5,0.08,r"$a_{\\rm crit}=%%.2f$ AU, $l_{\\rm E,eq}$=%%.2f AU, $l_{\\rm in,%%s}$=%%.2f AU, $l_{\\rm in,%%s}$=%%.2f AU, $l_{\\rm out,%%s}$=%%.2f AU, $l_{\\rm out,%%s}$=%%.2f AU"%%(binary.acrit,ihz.leeq,ihz.ini_inwd,ihz.linwd,ihz.ini_innr,ihz.linnr,ihz.ini_outwd,ihz.loutwd,ihz.ini_outnr,ihz.loutnr),transform=ax.transAxes,horizontalalignment='center',fontsize=12)

#RANGE
rang=1.5*max(ihz.loutwd,max(abs(xs)),max(abs(ys)))
ax.set_xlim((-rang,+rang))
ax.set_ylim((-rang,+rang))

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
loadConf("%s"+"ihz.conf")+\
loadConf("%s"+"ihz.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

insolation=ihz.insolation
fstats=ihz.fstats
pstats=ihz.pstats
ts=insolation[:,0]

#PLANET
ax.plot(ts/planet.Porb,insolation[:,1]/SOLAR_CONSTANT,
color='k',linestyle='-',linewidth=2,
label=r"Planet, $a_{\\rm orb}$=%%.2f AU,$e_{\\rm orb}$=%%.2f"%%(planet.aorb,planet.eorb))
ax.plot(ts/planet.Porb,insolation[:,2]/PPFD_EARTH,
color='k',linestyle='-',linewidth=1)
ax.axhline(ihz.fstats[0,0]/SOLAR_CONSTANT,color='k',linestyle='-.',linewidth=2,label='Planet average')

#EARTH EQUIVALENT
ax.plot(ts/planet.Porb,insolation[:,3]/SOLAR_CONSTANT,
color='k',linestyle='--',linewidth=2,
label=r"$a_{\\rm E,eq}$=%%.2f AU"%%(ihz.leeq))
ax.plot(ts/planet.Porb,insolation[:,4]/PPFD_EARTH,
color='k',linestyle='--',linewidth=1)

#RANGE HZ INSOLATION
ax.fill_between(ts/planet.Porb,
insolation[:,5]/SOLAR_CONSTANT,
insolation[:,7]/SOLAR_CONSTANT,
color='g',linestyle='-',linewidth=1,alpha=0.3)

#RANGE HZ PHOTON FLUX
ax.fill_between(ts/planet.Porb,
insolation[:,6]/PPFD_EARTH,
insolation[:,8]/PPFD_EARTH,
color='g',linestyle='-',linewidth=1,alpha=0.3)

ax.set_title(binary.title,position=(0.5,1.02),fontsize=12)
ax.legend(loc='best',prop=dict(size=10))
ax.grid()

ax.set_xlim((0.0,1.0))
ax.set_xlabel('orbital phase',fontsize=12)
ax.set_ylabel('Insolation, PPFD (PEL)',fontsize=12)
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
loadConf("%s"+"ihz.conf")+\
loadConf("%s"+"ihz.data")

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

ts=ihz.hz[:,0]

#BHZ
ax.plot(ts,ihz.hz[:,1],'r-',linewidth=2)
ax.plot(ts,ihz.hz[:,2],'k:',linewidth=2)
ax.plot(ts,ihz.hz[:,3],'b-',linewidth=2)
ax.fill_between(ts,ihz.hz[:,1],ihz.hz[:,3],color='g',alpha=0.3)

#SHZ
ax.plot(ts,ihz.shz[:,1],'r--',linewidth=2)
ax.plot(ts,ihz.shz[:,3],'b--',linewidth=2)
ax.fill_between(ts,ihz.hz[:,1],ihz.hz[:,3],color='g',alpha=0.3)

#CRITICAL DISTANCE
ax.axhline(binary.acrit,linewidth=2)

#DECORATION
ax.set_xlim((0.0,ihz.taums))
ax.set_ylim((min(ihz.shz[:,1]),max(ihz.hz[:,3])))

ax.set_xlabel(r"$\\tau$ (Gyr)",fontsize=12)
ax.set_ylabel(r"$r$ (AU)",fontsize=12)
ax.set_title(binary.title,position=(0.5,1.02),fontsize=12)

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

"""%(binary_dir,binary_dir,
     planet_dir,planet_dir,
     ihz_dir,ihz_dir
     ),watermarkpos="outer")

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(ihz_dir+"ihz.html","w")
fh.write("""\
<h2>Instantaneous Circumbinary Habitable Zone (HZ)</h2>
<h3>HZ Edges</h3>
<table width=300>
  <tr><td>l<sub>Earth,eq</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Wide HZ</b></td></tr>
  <tr><td>l<sub>in,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Narrow HZ</b></td></tr>
  <tr><td>l<sub>in,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/iHZ.png">
	<img width=100%% src="%s/iHZ.png">
      </a>
      <br/>
      <i>Instantaneous Habitable Zone</i>
	(
	<a href="%s/iHZ.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=iHZ.py">replot</a>
	)
  </td></tr>
</table>
<h3>Continuous Habitable Zone</h3>
<table width=300>
  <tr><td>&tau;<sub>MS</sub> (Gyr):</td><td>%.3f</td></tr>
  <tr><td>l<sub>in,max</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,min</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/hz-evolution.png">
	<img width=100%% src="%s/hz-evolution.png">
      </a>
      <br/>
      <i>Instantaneous Habitable Zone</i>
	(
	<a href="%s/hz-evolution.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=hz-evolution.py">replot</a>
	)
  </td></tr>
</table>
<h3>Insolation and Photon Flux</h3>
<table width=500>
  <tr><td>&lt;S(Planet,a=%.2f,e=%.2f)&gt; [W/m<sup>2</sup>,S<sub>Sun</sub>]:</td><td>%.3f, %.3f</td></tr>
  <tr><td>S(Planet)/S<sub>Sun</sub>(min,max,range,std):</td><td>%.3f,%.3f,%.3f,%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/insolation.png">
	<img width=100%% src="%s/insolation.png">
      </a>
      <br/>
      <i>Instantaneous Habitable Zone</i>
	(
	<a href="%s/insolation.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=insolation.py">replot</a>
	)
  </td></tr>
</table>
"""%(leeq,
     ini_inwd,linwd,ini_outwd,loutwd,
     ini_innr,linnr,ini_outnr,loutnr,
     ihz_webdir,ihz_webdir,ihz_webdir,WEB_DIR,
     tms,clin,clout,
     ihz_webdir,ihz_webdir,ihz_webdir,WEB_DIR,
     planet.aorb,planet.eorb,fstats.array[0,0],fstats.array[0,0]/SOLAR_CONSTANT,
     fstats.array[0,1]/SOLAR_CONSTANT,fstats.array[0,2]/SOLAR_CONSTANT,
     fstats.array[0,3]/SOLAR_CONSTANT,fstats.array[0,4]/SOLAR_CONSTANT,
     ihz_webdir,ihz_webdir,ihz_webdir,WEB_DIR
     ))
fh.close()

###################################################
#GENERATE SUMMARY REPORT
###################################################
fh=open(ihz_dir+"ihz-summary.html","w")
fh.write("""\
<table width=300>
  <tr><td>l<sub>Earth,eq</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Wide HZ</b></td></tr>
  <tr><td>l<sub>in,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Narrow HZ</b></td></tr>
  <tr><td>l<sub>in,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>l<sub>out,%s</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/iHZ.png">
	<img width=100%% src="%s/iHZ.png">
      </a>
  </td></tr>
  <tr><td colspan=2>
      <a href="%s/insolation.png">
	<img width=100%% src="%s/insolation.png">
      </a>
  </td></tr>
</table>
"""%(leeq,
     ini_inwd,linwd,ini_outwd,loutwd,
     ini_innr,linnr,ini_outnr,loutnr,
     ihz_webdir,ihz_webdir,
     ihz_webdir,ihz_webdir,
     ))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
#closeObject(ihz_dir)
