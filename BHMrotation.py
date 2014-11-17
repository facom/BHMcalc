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
PRINTOUT("Rotation interaction between M1 = %.2f and M2 = %.2f at a = %.2f"%(star1.M,star2.M,binary.abin))

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
#INITIAL CONDITIONS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PRINTOUT("Stellar initial conditions...")
h=1E100
for star in stars:
    #INITIALIZE INTERPOLATION FUNCTIONS
    evoInterpFunctions(star)

    #INITIAL CONDITIONS
    star.R=star.Rfunc(TAU_MIN)

    #MAXIMUM ATTAINABLE ROTATION
    star.Pmax=maxPeriod(star.M,star.R)

    #EXTRAPOLATE ROTATION
    star.Pini=theoProt(TAU_MIN,star.protfit)

    #IF EXTRAPOLATED IS LARGER THAN MAXIMUM START CLOSE TO MAX.
    if star.Pini<star.Pmax:star.Pini=2*star.Pmax

    #INITIAL CONDITIONS (SI)
    star.P=star.Pini*DAY
    star.W=2*PI/star.P

    #ACCELERATION TIME-SCALE
    acc,acc_tid,acc_ML=totalAcceleration(TAU_MIN,star,
                                         stars[NEXT(i,2)],binary,
                                         verbose=False,qreturn=True)
    star.tsync=(star.W/abs(acc))/GYR
    h=min(h,star.tsync/50)
    
    #IF TWINS AVOID REPEAT
    if qtwins:break

h=min(1E-3,h)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TIDAL INTEGRATION
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
verbose=False

#MAXIMUM INTEGRATION TIME
tau_max=min(star1.taums,star2.taums)

ts=star.evotrack[:,0]
cond=ts<tau_max
ts=np.append(ts[cond],[tau_max])
#ts=np.logspace(np.log10(TAU_MIN),np.log10(tau_max),50)

dt=ts[1::]-ts[:-1:]
i=0
for star in stars:
    PRINTOUT("Integrating star rotation between %.3f-%.3f Gyr..."%(ts[0],ts[-1]))
    j=0
    star.binrotevol=stack(2)
    star.binrotevol+=[TAU_MIN,star.P/DAY]
    for t in ts[:-1]:
        if verbose and i==1:
            print "*"*40
            print "t = %.17e"%t
            print "\tW = %.17e"%star.W
            print "\tP = %.5e"%(star.P/DAY)

        ti=t
        tn=t+dt[j]
        while ti<tn:

            if verbose and i==1:
                print star.protfit
                print "W = ",star.W
                print "P = ",star.P/DAY

            W=star.W
            
            #RUNGE-KUTTA4
            star.W=W
            star.P=2*PI/star.W
            acc=totalAcceleration(t,star,stars[NEXT(i,2)],binary,
                                  verbose=False)
            k1=acc*(h*GYR)

            dW=k1

            #RUNGE-KUTTA 4 INTEGRATION
            star.W=W+0.5*k1
            star.P=2*PI/star.W
            acc=totalAcceleration(t+0.5*h,star,stars[NEXT(i,2)],binary,
                                  verbose=False)
            k2=acc*(h*GYR)

            star.W=W+0.5*k2
            star.P=2*PI/star.W
            acc=totalAcceleration(t+0.5*h,star,stars[NEXT(i,2)],binary,
                                  verbose=False)
            k3=acc*(h*GYR)

            star.W=W+k3
            star.P=2*PI/star.W
            acc=totalAcceleration(t+h,star,stars[NEXT(i,2)],binary,
                                  verbose=False)
            k4=acc*(h*GYR)

            dW=1./6*(k1+2*k2+2*k3+k4)

            if verbose and i==1:
                print "k1 = ",k1
                raw_input()

            star.W=W+dW
            star.P=2*PI/star.W
            ti+=h

        tau_rot=tfromProt(star.P/DAY,star.protfit)
        star.binrotevol+=[tau_rot,star.P/DAY]
        j+=1
    PRINTOUT("Storing rotational evolution...")
    star.binrotevol=toStack(ts)|star.binrotevol
    if qtwins:break
    i+=1

###################################################
#STORE ROTATIONAL EVOLUTION INFORMATION
###################################################
rot.title=r"$M_1/M_{\\rm Sun}=$%.3f, $M_2/M_{\\rm Sun}$=%.3f, $a_{\\rm bin}$=%.3f AU, $e_{\\rm bin}$=%.2f, $P_{\\rm bin}$=%.3f d"%(star1.M,star2.M,binary.abin,binary.ebin,binary.Pbin)

PRINTERR("Storing rotational evolution data...")
f=open(rot_dir+"rotation.data","w")

f.write("""\
from numpy import array
#TITLE
title="%s"

#INTEGRATION TIME-SPAN
taums=%.17e #Gyr

#INITIAL ROTATION RATES
star1_Pini=%.17e #days
star2_Pini=%.17e #days

#INITIAL ACCELERATION TIME SCALE
star1_tsync=%.17e #Gyr
star2_tsync=%.17e #Gyr

#EVOLUTIONARY TRACK
star1_binrotevol=%s
star2_binrotevol=%s
"""%(rot.title,tau_max,
     star1.Pini,star2.Pini,
     star1.tsync,star2.tsync,
     array2str(star1.binrotevol),
     array2str(star2.binrotevol)))
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

fig=plt.figure(figsize=(8,8))

l=0.1;b=0.08;w=0.84;h=0.2;i=0.12
ax=fig.add_axes([l,b,w,h])

ax.plot(revol1[:,0],revol1[:,1],'b-',linewidth=2)
ax.plot(revol2[:,0],revol2[:,1],'r-',linewidth=2)
ax.fill_between(revol2[:,0],revol2[:,0],0*revol2[:,0],color='r',alpha=0.1)
ax.fill_between(revol2[:,0],revol2[:,0]+rot.taums,revol2[:,0],color='g',alpha=0.1)

ax.set_xlim((0,rot.taums))
ax.set_ylim((0,max(revol2[:,1])))

ax.grid()
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$\\tau_{\\rm rot}$ (Gyr)")
ax.set_title("Rotational Ages",position=(0.5,1.01),fontsize=12)

b=h+i;h=0.6
ax=fig.add_axes([l,b,w,h])

ax.plot(revol1[:,0],revol1[:,2],'b-',label="Star 1",
linewidth=2)
ax.plot(revol2[:,0],revol2[:,2],'r-',label="Star 2",
linewidth=2)

ax.plot(star1.protevol[:,0],star1.protevol[:,1],'b--',label="Star 1 (No tidal)",
linewidth=1)
ax.plot(star2.protevol[:,0],star2.protevol[:,1],'r--',label="Star 2 (No tidal)",
linewidth=1)

ax.axhline(binary.Pbin,label=r"$P_{\\rm bin}$",
linewidth=2,linestyle='-',color='k')
ax.axhline(binary.Psync,label=r"$P_{\\rm sync}$=$P_{\\rm bin}$/%%.2f"%%binary.nsync,
linewidth=2,linestyle='--',color='k')

ax.set_xticklabels([])

ax.set_ylabel(r"$P_{\\rm rot}$ (days)")

ax.set_xlim((0,rot.taums))
ax.set_ylim((0,2*binary.Pbin))
ax.set_title(rot.title,position=(0.5,1.02),fontsize=12)
ax.grid()
ax.legend(loc='lower right',prop=dict(size=12))

"""%(rot_dir,rot_dir,
     binary_dir,binary_dir,
     star1_dir,star1_dir,
     star2_dir,star2_dir
     ))

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
<h3>Initial Conditions</h3>
<table>
  <tr><td>P<sub>rot,1,ini</sub> (days):</td><td>%.3f</td></tr>
  <tr><td>t<sub>sync,1,ini</sub> (Gyr):</td><td>%.3f</td></tr>
  <tr><td>P<sub>rot,1,ini</sub> (days):</td><td>%.3f</td></tr>
  <tr><td>t<sub>sync,2,ini</sub> (Gyr):</td><td>%.3f</td></tr>
</table>
"""%(WEB_DIR,rot_webdir,rot_webdir,rot_webdir,WEB_DIR,rot_webdir,
     rot.k,
     star1.Pini,star1.tsync,
     star2.Pini,star2.tsync
     ))
fh.close()
       
###################################################
#CLOSE OBJECT
###################################################
closeObject(rot_dir)
