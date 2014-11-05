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
# Inputs: 
# - Stellar properties (star.conf)
# Outputs: 
# - Star data file (star.data)
# - Html report (star.html)
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
   python stEvo.py <star>.conf <qoverride>

   <star>.conf (file): Configuration file with data about star.

   <qoverride> (int 0/1): Override any previously existent
   calculation.
"""

star_conf,qover=\
    readArgs(argv,
             ["str","int"],
             ["star.conf","0"],
             Usage=Usage)

###################################################
#LOAD STAR PROPERTIES
###################################################
PRINTOUT("Loading object from '%s'"%star_conf)
star,star_str,star_hash,star_dir=makeObject(star_conf,
                                           qover=qover)
if star is None:
    PRINTERR("Object '%s' already exists."%star_str)
    exit(0)

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
PRINTERR("Estimating maximum age...")
tau_max=TAU_MAX
for t in np.linspace(TAU_MIN,TAU_MAX,NTIMES):
    data=StellarGTRL(star.Z,star.M,t)
    if data[1]<0:
        tau_max=t
        break

#SAMPLING TIMES
exp_ts1=np.linspace(np.log10(TAU_MIN),np.log10(tau_max/2),NTIMES/2)
exp_ts2=-np.linspace(-np.log10(min(TAU_MAX,1.5*tau_max)),-np.log10(tau_max/2),NTIMES/2)
ts=np.unique(np.concatenate((10**exp_ts1,(10**exp_ts2)[::-1])))

#EVOLUTIONARY MATRIX
PRINTERR("Calculating Evolutionary Matrix...")
evodata=np.array([np.array([t]+list(StellarGTRL(star.Z,star.M,t))) for t in ts])
maxdata=evodata[:,1]>0
evodata=evodata[maxdata]
evodata_str=array2str(evodata)

#MAXIMUM ALLOWABLE TIME
tau_max=evodata[-1,0]
PRINTERR("Maximum age = %.3f"%tau_max)

###################################################
#CALCULATE DERIVATIVE PROPERTIES
###################################################
#BASIC PROPERTIES
g,Teff,R,L=StellarGTRL(star.Z,star.M,star.tau)

#HABITABLE ZONE LIMITS
PRINTERR("Calculating HZ...")
lins=[]
for incrit in IN_CRITS:
    lin,lsun,lout=HZ(L,Teff,lin=incrit)
    lins+=[lin]
louts=[]
for outcrit in OUT_CRITS:
    lin,lsun,lout=HZ(L,Teff,lout=outcrit)
    louts+=[lout]

#GIRATION RADIUS
MoI=np.sqrt(stellarMoI(star.M))

#DISSIPATION TIME
tdiss=dissipationTime(star.M,R,L)

###################################################
#STORE STELLAR DATA
###################################################
PRINTERR("Storing stellar data...")
f=open(star_dir+"star.data","w")
f.write("""\
from numpy import array
#MAXIMUM AGE
taumax=%.17e #Gyr

#INSTANTANEOUS PROPERTIES
g=%.17e #m/s^2
T=%.17e #L
R=%.17e #Rsun
L=%.17e #Lsun
MoI=%.17e #Gyration radius (I/M R^2)
tdiss=%.17e #s

#OTHER PROPERTIES
lins=%s #AU
lsun=%.17e #AU
louts=%s #AU

#EVOLUTIONARY TRACK
evotrack=\
%s
"""%(tau_max,g,Teff,R,L,MoI,tdiss,
     array2str(lins),lsun,array2str(louts),
     evodata_str,
     ))
f.close()

###################################################
#GENERATE PLOTS
###################################################
PRINTERR("Creating plots...")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STELLAR PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"stellar-props",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
evodata=%s
ts=evodata[:,0]
logrho_func,Teff_func,logR_func,logL_func=evoFunctions(evodata)

ax.plot(ts,10**logrho_func(np.log10(ts))/GRAVSUN,label=r"$g_{\\rm surf}$")
ax.plot(ts,Teff_func(np.log10(ts))/TSUN,label=r"$T_{\\rm eff}$")
ax.plot(ts,10**logR_func(np.log10(ts)),label=r"$R$")
ax.plot(ts,10**logL_func(np.log10(ts)),label=r"$L$")

ax.set_xscale('log')
ax.set_yscale('log')

logTickLabels(ax,-2,1,(3,),axis='x',frm='%%.2f')
ax.set_title("Stellar Properties",position=(0.5,1.02))
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"Property in Solar Units")

ymin,ymax=ax.get_ylim()
ax.set_xlim((0,%.17e))
ax.set_ylim((ymin,ymax))

ax.legend(loc='best')
"""%(evodata_str,tau_max))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#EVOLUTIONARY TRACK
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-track",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
evodata=%s
ts=evodata[:,0]
logrho_func,Teff_func,logR_func,logL_func=evoFunctions(evodata)

bbox=dict(fc='w',ec='none')

#LINE
logts=np.log10(ts)
Teffs=Teff_func(logts)
Leffs=10**logL_func(logts)
ax.plot(Teffs,Leffs,"k-")
ax.plot(Teffs[0:1],Leffs[0:1],"ko",markersize=5)
ax.text(Teffs[0],Leffs[0],r"$t_{\\rm ini}$=10 Myr",transform=offSet(5,5),bbox=bbox)
ax.plot([Teffs[-1]],[Leffs[-1]],"ko",markersize=5)
ax.text(Teffs[-1],Leffs[-1],r"$t_{\\rm end}=$%.1f Gyr",horizontalalignment='right',transform=offSet(-5,5),bbox=bbox)

#MARKS
dt=round(%.17e/20,1)
logts=np.log10(np.arange(TAU_MIN,%.17e,dt))
Teffs=Teff_func(logts)
Leffs=10**logL_func(logts)
ax.plot(Teffs,Leffs,"ko",label='Steps of %%.1f Gyr'%%dt,markersize=3)
ax.text(TSUN,1.0,r"$\odot$",fontsize=14)

ax.set_yscale('log')
ax.set_title("Evolutionary Track",position=(0.5,1.02))
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$L/L_{\\rm Sun}$")

Tmin,Tmax=ax.get_xlim()
ax.set_xlim((1E4,1E3))

ax.legend(loc='lower right')
"""%(evodata_str,tau_max,tau_max,tau_max))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS EVOLUTION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"evol-radius",\
"""
from BHM.BHMstars import *

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
evodata=%s
ts=evodata[:,0]
logrho_func,Teff_func,logR_func,logL_func=evoFunctions(evodata)

bbox=dict(fc='w',ec='none')

#LINES
logts=np.log10(ts)
Teffs=Teff_func(logts)
Rs=10**logR_func(logts)
ax.plot(Teffs,Rs,"k-")
ax.plot(Teffs[0:1],Rs[0:1],"ko",markersize=5)
ax.text(Teffs[0],Rs[0],r"$t_{\\rm ini}$=10 Myr",transform=offSet(5,5),bbox=bbox)
ax.plot([Teffs[-1]],[Rs[-1]],"ko",markersize=5)
ax.text(Teffs[-1],Rs[-1],r"$t_{\\rm end}=$%.1f Gyr",horizontalalignment='right',transform=offSet(-5,5),bbox=bbox)

#EVOLUTIONARY TRACK
dt=round(%.17e/20,1)
logts=np.log10(np.arange(TAU_MIN,%.17e,dt))
Teffs=Teff_func(logts)
Rs=10**logR_func(logts)
ax.plot(Teffs,Rs,"ko",label='Steps of %%.1f Gyr'%%dt,markersize=3)
ax.text(1.0,1.0,r"$\odot$",fontsize=14)

ax.set_title("Evolutionary Track in Radius",position=(0.5,1.02))
ax.set_xlabel(r"$T_{\\rm eff}$ (K)")
ax.set_ylabel(r"$R/R_{\\rm Sun}$")

Tmin,Tmax=ax.get_xlim()
ax.set_xlim((Tmax,Tmin))

ax.legend(loc='lower right')
"""%(evodata_str,tau_max,tau_max,tau_max))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#RADIUS SCHEMATIC
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(star_dir,"radius-schematic",\
"""

from BHM.BHMstars import *
fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.0,0.0,1.0,1.0])

M=%.3f
Z=%.4f
tau=%.3f
R=%.3f
T=%.1f

color=cm.RdYlBu((T-2000)/7000)

star=patches.Circle((0.0,0.0),R,fc=color,ec='none')
sun=patches.Circle((0.0,0.0),1.0,
                   linestyle='dashed',fc='none',zorder=10)
ax.add_patch(star)
ax.add_patch(sun)
ax.text(0.0,1.0,'Sun',fontsize=20,transform=offSet(0,5),horizontalalignment='center')

ax.set_xticks([])
ax.set_yticks([])

ax.set_title(r"$M = %%.3f\,M_{\odot}$, $Z=$%%.4f, $\\tau=%%.3f$ Gyr, $R = %%.3f\,R_{\odot}$, $T_{\\rm eff} = %%.1f$ K"%%(M,Z,tau,R,T),
position=(0.5,0.05),fontsize=16)

rang=max(1.5*R,1.5)
ax.set_xlim((-rang,+rang))
ax.set_ylim((-rang,+rang))
"""%(star.M,star.Z,star.tau,R,Teff),watermarkpos="inner")

###################################################
#GENERATE SUMMARY
###################################################
PRINTERR("Creating HTML report...")
fh=open(star_dir+"star_summary.html","w")
fh.write("""\
<table width=300>
  <tr><td>g (m/s<sup>2</sup>):</td><td>%.2f</td></tr>
  <tr><td>T<sub>eff</sub> (K):</td><td>%.2f</td></tr>
  <tr><td>R/R<sub>sun</sub>:</td><td>%.3f</td></tr>
  <tr><td>L/L<sub>sun</sub>:</td><td>%.3f</td></tr>
  <tr><td>MoI=I/MR<sup>2</sup>:</td><td>%.3f</td></tr>
  <tr><td>t<sub>diss</sub> (yr):</td><td>%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/radius-schematic.png">
	<img width=100%% src="%s/radius-schematic.png">
      </a>
  </td></tr>
</table>
"""%(g,Teff,R,L,MoI,tdiss,
star_webdir,star_webdir
))
fh.close()

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(star_dir+"star.html","w")
fh.write("""\
<h2>Stellar Properties</h2>
<h3>Input properties</h3>
<table>
  <tr><td>Mass (M<sub>sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>Z:</td><td>%.4f</td></tr>
  <tr><td>[Fe/H] (dex):</td><td>%.2f</td></tr>
  <tr><td>&tau; (Gyr):</td><td>%.2f</td></tr>
</table>
<h3>Instantaneous theoretical properties:</h3>
<table width=300>
  <tr><td colspan=2>
      <a href="%s/radius-schematic.png">
	<img width=100%% src="%s/radius-schematic.png">
      </a>
      <br/>
      <i>Schematic Representation</i>
	(
	<a href="%s/radius-schematic.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=radius-schematic.py">replot</a>
	)
  </td></tr>
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

<h3>Properties Evolution:</h3>
<table>
  <tr><td>
      <a href="%s/stellar-props.png">
	<img width=50%% src="%s/stellar-props.png">
      </a>
      <br/>
      <i>Evolution of stellar properties</i>
	(
	<a href="%s/stellar-props.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=stellar-props.py">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/evol-track.png">
	<img width=50%% src="%s/evol-track.png">
      </a>
      <br/>
      <i>Evolutionary Track</i>
	(
	<a href="%s/evol-track.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=evol-track.py">replot</a>
	)
  </td></tr>
  <tr><td>
      <a href="%s/evol-radius.png">
	<img width=50%% src="%s/evol-radius.png">
      </a>
      <br/>
      <i>Radius Evolution</i>
	(
	<a href="%s/evol-radius.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=evol-radius.py">replot</a>
	)
  </td></tr>
</table>

"""%(star.M,star.Z,star.FeH,star.tau,
star_webdir,star_webdir,star_webdir,WEB_DIR,
g,Teff,R,L,MoI,tdiss,
lins[0],lins[1],lins[2],
louts[0],louts[1],
star_webdir,star_webdir,star_webdir,WEB_DIR,
star_webdir,star_webdir,star_webdir,WEB_DIR,
star_webdir,star_webdir,star_webdir,WEB_DIR,
))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
closeObject(star_dir)
