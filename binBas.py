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
# Binary Basic Properties
# Inputs: 
# - Binary properties (binary.conf)
# - Stars properties (<star1>.conf,<star2>.conf)
# Outputs: 
# - Binary data (binary.data)
# - Html report (star.html)
###################################################
from BHM import *
from BHM.BHMplot import *
from BHM.BHMastro import *

###################################################
#CLI ARGUMENTS
###################################################
Usage=\
"""
Usage:
   python binBas.py <binary>.conf <star1>.conf <star1>.conf <qoverride>

   <binary>.conf (file): Configuration file with data about star.

   <star1>.conf,<star2>.conf (file): Configuration file with data
   about stars.

   <qoverride> (int 0/1): Override any previously existent
   calculation.
"""

binary_conf,star1_conf,star2_conf,qover=\
    readArgs(argv,
             ["str","str","str","int"],
             ["binary.conf","star1.conf","star2.conf","0"],
             Usage=Usage)
PRINTOUT("Executing for: %s, %s, %s"%(binary_conf,
                                      star1_conf,
                                      star2_conf))

###################################################
#LOAD PREVIOUS OBJECTS
###################################################
PRINTOUT("Loading other objects...")
#==================================================
#LOADING STAR 1
star1,star1_dir,star1_str,star1_hash,star1_liv,star1_stg=\
    signObject(star1_conf)
system("python stEvo.py %s %s"%(star1_conf,qover))
star1+=loadConf(star1_dir+"star.data")
#==================================================
#LOADING STAR 2
star2,star2_dir,star2_str,star2_hash,star2_liv,star2_stg=\
    signObject(star2_conf)
system("python stEvo.py %s %s"%(star2_conf,qover))
star2+=loadConf(star2_dir+"star.data")

###################################################
#LOAD BINARY OBJECT
###################################################
binary,binary_str,binary_hash,binary_dir=\
    makeObject(binary_conf,qover=qover)
binary_webdir=WEB_DIR+binary_dir

###################################################
#CALCULATE BASIC PROPERTIES OF BINARY
###################################################
#ORBITAL PARAMETERS
if binary.Pbin>0:
    binary.nbin=2*np.pi/binary.Pbin
    binary.abin=aKepler(binary.Pbin,star1.M,star2.M)
elif binary.abin>0:
    binary.Pbin=PKepler(binary.abin,star1.M,star2.M)
    binary.nbin=2*np.pi/binary.Pbin
else:
    PRINTERR("Stars are in contact: Pbin = %e, abin = %e"%(binary.Pbin,binary.abin))
    errorCode("PARAMETER_ERROR")

#OTHER PARAMETERS
binary.M=star1.M+star2.M
binary.mu=star1.M/binary.M
binary.q=star2.M/star1.M
binary.acrit=aCritical(binary.mu,binary.abin,binary.ebin)
binary.nsync=nSync(binary.ebin)
binary.Psync=binary.Pbin/binary.nsync
binary.Wsync=binary.nbin*binary.nsync
binary.title=r"$M_1/M_{\rm Sun}=$%.3f, $M_2/M_{\rm Sun}=$%.3f, $a_{\rm bin}=$%.3f AU, $e_{\rm bin}=$%.2f, $P_{\rm bin}=$%.3f d"%(star1.M,star2.M,binary.abin,binary.ebin,binary.Pbin)

###################################################
#EPHEMERIS OF BINARY ORBIT
###################################################
dt=0.5 #DAYS
ts=np.arange(0.0,1.1*binary.Pbin,dt)
rbins=stack(4)
tes=stack(1)
for t in ts:
    rbin=orbitalPosition(binary.nbin,
                         binary.abin,
                         binary.ebin,t)
    r1=star2.M/binary.M*rbin
    r2=-star1.M/binary.M*rbin
    rbins+=np.concatenate((r1,r2))
    tes+=[t]
ephemeris=tes|rbins

###################################################
#STORE BINARY DATA
###################################################
f=open(binary_dir+"binary.data","w")
f.write("""\
from numpy import array

#STARS
star1_dir="%s"
star2_dir="%s"

#DERIVATIVE BINARY PARAMETERS
Pbin=%.17e #days
abin=%.17e #AU
nbin=%.17e #rad days^-1

M=%.17e #MSun
mu=%.17e #M1/(M1+M2)
q=%.17e #M2/M1
acrit=%.17e 

nsync=%.17e #Fraction of period on which is synchronized
Psync=%.17e #days, Pseudo-synchronization period
Wsync=%.17e #Pseudo-synchronization angular velocity

#GRAPHICAL
title=r"%s"

#ORBITAL EPHEMERIS
ephemeris=%s
"""%(star1_dir,star2_dir,
     binary.Pbin,binary.abin,binary.nbin,
     binary.M,binary.mu,binary.q,binary.acrit,
     binary.nsync,binary.Psync,binary.Wsync,
     binary.title,
     array2str(ephemeris)))
f.close()

###################################################
#GENERATE PLOTS
###################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STELLAR PROPERTIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(binary_dir,"binary-orbit",\
"""
from BHM.BHMstars import *
binary=\
loadConf("%s"+"binary.conf")+\
loadConf("%s"+"binary.data")

fig=plt.figure(figsize=(8,8))
ax=fig.add_axes([0.02,0.02,0.96,0.96])
xs1=binary.ephemeris[:,1]
ys1=binary.ephemeris[:,2]
xs2=binary.ephemeris[:,3]
ys2=binary.ephemeris[:,4]

ax.plot(xs1,ys1,'b-',label='Primary')
ax.plot(xs2,ys2,'r-',label='Secondary')
ax.plot([xs1[0]],[ys1[0]],'bo',markersize=5,markeredgecolor='none')
ax.plot([xs2[0]],[ys2[0]],'ro',markersize=5,markeredgecolor='none')

rang=1.5*binary.mu*binary.abin*(1+binary.ebin)
ax.set_xlim((-rang,rang))
ax.set_ylim((-rang,rang))

xt=ax.get_xticks()
dx=xt[1]-xt[0]
dy=0.1
ax.axhline(-rang+dx/3,xmin=dy,xmax=dy+dx/(2*rang),color='k')
ax.text(dy+dx/(4*rang),dx/3/(2*rang)+0.01,
"%%.2f AU"%%dx,horizontalalignment='center',
transform=ax.transAxes)

ax.set_title(binary.title,position=(0.5,0.95),fontsize=14)

ax.set_xticklabels([])
ax.set_yticklabels([])
"""%(binary_dir,binary_dir),watermarkpos='inner')

###################################################
#GENERATE FULL REPORT
###################################################
fh=open(binary_dir+"binary.html","w")
fh.write("""\
<h2>Binary Properties</h2>
<h3>Basic Properties</h3>
<table width=300>
  <tr><td>M (M<sub>Sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>&mu; (M<sub>1</sub>/M<sub>Sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>q (M<sub>2</sub>/M<sub>1</sub>):</td><td>%.3f</td></tr>
  <tr><td>P<sub>bin</sub> (days):</td><td>%.3f</td></tr>
  <tr><td>a<sub>bin</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>e<sub>bin</sub>:</td><td>%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/binary-orbit.png">
	<img width=100%% src="%s/binary-orbit.png">
      </a>
      <br/>
      <i>Schematic Representation</i>
	(
	<a href="%s/binary-orbit.png.txt">data</a>|
	<a href="%s/web/replot.php?plot=binary-orbit.py">replot</a>
	)
  </td></tr>
</table>
<h3>Derivative properties:</h3>
<table width=300>
  <tr><td>a<sub>crit</a> (AU):</td><td>%.3f</td></tr>
  <tr><td>n<sub>sync</a> (P<sub>sync</sub>/P<sub>bin</sub>):</td><td>%.3f</td></tr>
  <tr><td>P<sub>sync</a> (days):</td><td>%.3f</td></tr>
</table>
"""%(binary.M,binary.mu,binary.q,
     binary.Pbin,binary.abin,binary.ebin,
     binary_webdir,binary_webdir,binary_webdir,WEB_DIR,
     binary.acrit,binary.nsync,binary.Psync
     ))
fh.close()

###################################################
#GENERATE SUMMARY
###################################################
fh=open(binary_dir+"binary_summary.html","w")
fh.write("""\
<table width=300>
  <tr><td>M (M<sub>Sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>&mu; (M<sub>1</sub>/M<sub>Sun</sub>):</td><td>%.3f</td></tr>
  <tr><td>q (M<sub>2</sub>/M<sub>1</sub>):</td><td>%.3f</td></tr>
  <tr><td>P<sub>bin</sub> (days):</td><td>%.3f</td></tr>
  <tr><td>a<sub>bin</sub> (AU):</td><td>%.3f</td></tr>
  <tr><td>e<sub>bin</sub>:</td><td>%.3f</td></tr>
  <tr><td colspan=2>
      <a href="%s/binary-orbit.png">
	<img width=100%% src="%s/binary-orbit.png">
      </a>
  </td></tr>
"""%(binary.M,binary.mu,binary.q,
     binary.Pbin,binary.abin,binary.ebin,
     binary_webdir,binary_webdir
     ))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
closeObject(binary_dir)
