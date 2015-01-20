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
# Radiation and Plasma Environment around Binaries
# Inputs: 
# - Binary properties (binary.conf)
# - Stars properties (<star1>.conf,<star2>.conf)
# Outputs: 
# - Binary data (rot.data)
# - Html report (rot.html)
###################################################
from BHM import *
from BHM.BHMplot import *
from BHM.BHMstars import *
from BHM.BHMplanets import *
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

sys_dir,env_conf,qover=\
    readArgs(argv,
             ["str","str","int"],
             ["sys/template","hz.conf","0"],
             Usage=Usage)

###################################################
#LOAD PREVIOUS OBJECTS
###################################################
PRINTOUT("Loading other objects...")
#==================================================
#LOADING ROTATION
rot_conf="rotation.conf"
rot,rot_dir,rot_str,rot_hash,rot_liv,rot_stg=\
    signObject("rotation",sys_dir+"/"+rot_conf)
rot+=loadConf(rot_dir+"rotation.data")
tr,bin_rot1=interpMatrix(rot.star1_binrotevol)
tr,bin_rot2=interpMatrix(rot.star2_binrotevol)
#==================================================
#LOADING IHZ
ihz_conf="hz.conf"
ihz,ihz_dir,ihz_str,ihz_hash,ihz_liv,ihz_stg=\
    signObject("hz",sys_dir+"/"+ihz_conf)
ihz+=loadConf(ihz_dir+"hz.data")
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
tp,thermevol=interpMatrix(planet.thermevol)

###################################################
#LOAD ENV OBJECT
###################################################
env,env_str,env_hash,env_dir=\
    makeObject("interaction",sys_dir+"/"+env_conf,qover=qover)
env_webdir="/"+WEB_DIR+env_dir
PRINTOUT("Object hash:%s"%env_hash)
env.str_refobj=env.str_refobj.replace("'","")

###################################################
#CALCULATE ENVIRONMENTAL CONDITIONS
###################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#FLUXES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
LumFlux Data:
0:Time, 
1:LXUV1, 2:LXUV2, 3:LXUV,
4:ntLXUV1, 5:ntLXUV2, 6:ntLXUV,
7:ntLXUV/LXUV, 8:LXUV1/LXUV,
9:FXUVin, 10:FXUVout, 11:FXUVp,
12:ntFXUVin, 13:ntFXUVout, 14:ntFXUVp,
15:FXUVins, 16:FXUVouts, 17:FXUVeeqs,
18:PSWin, 19:FSWin, 20:PSWout, 21:FSWout, 22:PSWp, 23:FSWp
24:ntPSWin, 25:ntFSWin, 26:ntPSWout, 27:ntFSWout, 28:ntPSWp, 29:ntFSWp
30:PSWins, 31:FSWins, 32:PSWouts, 33:FSWouts, 34:PSWeeqs, 35:FSWeeqs
36:Rs,37:ntRs,38:sinRs,39:soutRs
"""

"""
Intflux Data:
0:Time
1:FXUVin, 2:FXUVout, 3:FXUVp,
4:ntFXUVin, 5:ntFXUVout, 6:ntFXUVp,
7:FXUVins, 8:FXUVouts, 9:FXUVeeqs,
10:PSWin, 11:FSWin, 12:PSWout, 13:FSWout, 14:PSWp, 15:FSWp
16:ntPSWin, 17:ntFSWin, 18:ntPSWout, 19:ntFSWout, 20:ntPSWp, 21:ntFSWp
22:PSWins, 23:FSWins, 24:PSWouts, 25:FSWouts, 26:PSWeeqs, 27:FSWeeqs
"""

#INTERPOLATION
ts,star1.activity_funcs=interpMatrix(star1.activity)
ts,star2.activity_funcs=interpMatrix(star2.activity)
ts,star1.binactivity_funcs=interpMatrix(rot.star1_binactivity)
ts,star2.binactivity_funcs=interpMatrix(rot.star2_binactivity)

ts=chopArray(rot.star1_binactivity[:,0],env.tauini,rot.taumaxrot)
PRINTOUT("Calculating radiation and plasma fluxes between %.3f - %.3f Gyr"%(ts[0],ts[-1]))

env.lumflux=stack(39)
for t in ts:
    
    #CUMULATOR
    lumflux=[]

    #STELLAR PROPERTIES AT t
    R1=star1.Rfunc(t)
    R2=star2.Rfunc(t)

    Mdot1=star1.binactivity_funcs[7](t)
    Mdot2=star2.binactivity_funcs[7](t)

    sMdot1=star1.activity_funcs[7](t)
    sMdot2=star2.activity_funcs[7](t)
    
    #//////////////////////////////
    #LUMINOSITIES
    #//////////////////////////////
    #XUV LUMINOSITIES (TIDAL)
    LXUV1=star1.binactivity_funcs[13](t)
    LXUVs=star1.activity_funcs[13](t)
    LXUV2=star2.binactivity_funcs[13](t)
    LXUV=LXUV1+LXUV2
    lumflux+=[LXUV1,LXUV2,LXUV]

    #XUV LUMINOSITIES (NO TIDAL)
    ntLXUV1=star1.activity_funcs[13](t)
    ntLXUV2=star2.activity_funcs[13](t)
    ntLXUV=ntLXUV1+ntLXUV2
    lumflux+=[ntLXUV1,ntLXUV2,ntLXUV]
    
    #CORRECTING FACTORS
    facnt=ntLXUV/LXUV
    facsn=LXUVs/LXUV
    lumflux+=[facnt,facsn]
    
    #//////////////////////////////
    #XUV FLUXES
    #//////////////////////////////
    pfluxbin=(LXUV*1E7)/(4*np.pi*(AU*1E2)**2)/PEL

    #%%%%%%%%%%%%%%%%%%%%
    #BINARY
    #%%%%%%%%%%%%%%%%%%%%
    #INNER EDGE
    r=ihz.linwd
    FXUVin=pfluxbin/r**2
    #OUTER EDGE
    r=ihz.loutwd
    FXUVout=pfluxbin/r**2
    #PLANET
    r=planet.aorb
    FXUVp=pfluxbin/r**2
    lumflux+=[FXUVin,FXUVout,FXUVp]

    #%%%%%%%%%%%%%%%%%%%%
    #BINARY (NO TIDAL)
    #%%%%%%%%%%%%%%%%%%%%
    #INNER EDGE
    ntFXUVin=facnt*FXUVin
    #OUTER EDGE
    ntFXUVout=facnt*FXUVout
    #PLANET
    ntFXUVp=facnt*FXUVp
    lumflux+=[ntFXUVin,ntFXUVout,ntFXUVp]

    #%%%%%%%%%%%%%%%%%%%%
    #SINGLE PRIMARY
    #%%%%%%%%%%%%%%%%%%%%
    #INNER EDGE
    r=star1.lins[0]
    FXUVins=facsn*pfluxbin/r**2
    #OUTER EDGE
    r=star1.louts[-1]
    FXUVouts=facsn*pfluxbin/r**2
    #EARTH-EQUIVALENT
    r=star1.lsun
    FXUVeeqs=facsn*pfluxbin/r**2
    lumflux+=[FXUVins,FXUVouts,FXUVeeqs]
    
    #//////////////////////////////
    #STELLAR WIND
    #//////////////////////////////

    #%%%%%%%%%%%%%%%%%%%%
    #BINARY
    #%%%%%%%%%%%%%%%%%%%%
    #INNER
    r=ihz.linwd
    PSWin,FSWin=binaryWind(star1.M,R1,Mdot1,
                           star2.M,R2,Mdot2,
                           r,
                           vtype='Terminal')
    #OUTER
    r=ihz.loutwd
    PSWout,FSWout=binaryWind(star1.M,R1,Mdot1,
                             star2.M,R2,Mdot2,
                             r,
                             vtype='Terminal')
    #PLANET
    r=planet.aorb
    PSWp,FSWp=binaryWind(star1.M,R1,Mdot1,
                         star2.M,R2,Mdot2,
                         r,
                         vtype='Terminal')

    lumflux+=[PSWin,FSWin/SWPEL,PSWout,FSWout/SWPEL,PSWp,FSWp/SWPEL]

    #%%%%%%%%%%%%%%%%%%%%
    #NO TIDAL
    #%%%%%%%%%%%%%%%%%%%%
    #INNER
    r=ihz.linwd
    ntPSWin,ntFSWin=binaryWind(star1.M,R1,sMdot1,
                               star2.M,R2,sMdot2,
                               r,
                               vtype='Terminal')

    #OUTER
    r=ihz.loutwd
    ntPSWout,ntFSWout=binaryWind(star1.M,R1,sMdot1,
                                 star2.M,R2,sMdot2,
                                 r,
                                 vtype='Terminal')
    
    #PLANET
    r=planet.aorb
    ntPSWp,ntFSWp=binaryWind(star1.M,R1,sMdot1,
                             star2.M,R2,sMdot2,
                             r,
                             vtype='Terminal')

    lumflux+=[ntPSWin,ntFSWin/SWPEL,ntPSWout,ntFSWout/SWPEL,ntPSWp,ntFSWp/SWPEL]
    
    #%%%%%%%%%%%%%%%%%%%%
    #SINGLE STAR
    #%%%%%%%%%%%%%%%%%%%%
    #INNER
    r=star1.lins[0]
    v,n=stellarWind(star1.M,R1,sMdot1,r,vtype='Terminal')
    PSWins,FSWins=0.6*MP*n*v**2,n*v
    
    #OUTER
    r=star1.louts[-1]
    v,n=stellarWind(star1.M,R1,sMdot1,r,vtype='Terminal')
    PSWouts,FSWouts=0.6*MP*n*v**2,n*v
    
    #LSUN
    r=star1.lsun
    v,n=stellarWind(star1.M,R1,sMdot1,r,vtype='Terminal')
    PSWeeqs,FSWeeqs=0.6*MP*n*v**2,n*v

    lumflux+=[PSWins,FSWins/SWPEL,PSWouts,FSWouts/SWPEL,PSWeeqs,FSWeeqs/SWPEL]

    #//////////////////////////////
    #STANDOFF DISTANCE
    #//////////////////////////////
    try:Mdip=thermevol[9](t)
    except:Mdip=thermevol[9](TAU_MIN)

    Rs=StandoffDistance(Mdip*MDIPE,PSWp,planet.R*REARTH,
                        objref=env.str_refobj,nM=env.nM,nP=env.nP)
    
    ntRs=StandoffDistance(Mdip*MDIPE,ntPSWp,planet.R*REARTH,
                          objref=env.str_refobj,nM=env.nM,nP=env.nP)

    sinRs=StandoffDistance(Mdip*MDIPE,PSWins,planet.R*REARTH,
                           objref=env.str_refobj,nM=env.nM,nP=env.nP)

    soutRs=StandoffDistance(Mdip*MDIPE,PSWouts,planet.R*REARTH,
                           objref=env.str_refobj,nM=env.nM,nP=env.nP)

    lumflux+=[Rs,ntRs,sinRs,soutRs]

    env.lumflux+=lumflux

env.lumflux=toStack(ts)|env.lumflux

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CUMULATIVE FLUXES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PRINTOUT("Calculating cumulative fluxes...")

n=len(ts)
intflux=[]
for j in xrange(9,36):
    intflux+=\
        [[trapezoidalArray(ts,env.lumflux[:,j],i) for i in xrange(n)]]

#ADD TIME COLUMN
intflux=toStack(ts)|toStack(np.transpose(intflux))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INSTANTANEOUS VALUES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tau=env.tauref
ts,lumflux_func=interpMatrix(env.lumflux)
ts,intflux_func=interpMatrix(intflux)

#XUV FLUX
env.FXUVin=lumflux_func[9](tau)
env.FXUVout=lumflux_func[10](tau)
env.FXUVp=lumflux_func[11](tau)

env.FXUVins=lumflux_func[15](tau)
env.FXUVouts=lumflux_func[16](tau)
env.FXUVeeqs=lumflux_func[17](tau)

#STELLAR WIND FLUX
env.FSWin=lumflux_func[19](tau)
env.FSWout=lumflux_func[21](tau)
env.FSWp=lumflux_func[23](tau)

env.FSWins=lumflux_func[31](tau)
env.FSWouts=lumflux_func[33](tau)
env.FSWeeqs=lumflux_func[35](tau)

#STELLAR WIND PRESSURE
env.PSWin=lumflux_func[18](tau)
env.PSWout=lumflux_func[20](tau)
env.PSWp=lumflux_func[22](tau)

env.PSWins=lumflux_func[30](tau)
env.PSWouts=lumflux_func[32](tau)
env.PSWeeqs=lumflux_func[34](tau)

#CUMULATIVE 

#XUV FLUX
env.intFXUVin=intflux_func[1](tau)
env.intFXUVout=intflux_func[2](tau)
env.intFXUVp=intflux_func[3](tau)

env.sintFXUVin=intflux_func[7](tau)
env.sintFXUVout=intflux_func[8](tau)
env.sintFXUVeeq=intflux_func[9](tau)

#STELLAR WIND FLUX
env.intFSWin=intflux_func[11](tau)
env.intFSWout=intflux_func[13](tau)
env.intFSWp=intflux_func[15](tau)

env.sintFSWin=intflux_func[23](tau)
env.sintFSWout=intflux_func[25](tau)
env.sintFSWp=intflux_func[27](tau)

#//////////////////////////////
#STANDOFF DISTANCE
#//////////////////////////////
env.Rs=lumflux_func[36](tau)
env.sinRs=lumflux_func[38](tau)
env.soutRs=lumflux_func[39](tau)

#//////////////////////////////
#FACTORS FOR MASS-LOSS
#//////////////////////////////
PRINTOUT("Calculating Mass-Loss...")
env.dotM,env.intM,env.dotNl,env.dotPl,env.intPl=calibrationFluxes(verbose=True)

#PHOTOEVAPORATION
env.facM=(1E3/planet.rho)
env.dotMp=env.dotM*env.facM*env.FXUVp
env.intMp=env.intM*env.facM*env.intFXUVp

#ENTRAINMENT
env.facN=(planet.Rp)**2*(env.alpha/0.3)*(env.muatm/16.0)
env.dotNp=env.dotNl*env.facN*env.FSWp
env.intNp=env.dotNl*env.facN*env.intFSWp
env.facP=(planet.g/10)*(env.alpha/0.3)*(env.muatm/16.0)
env.dotPp=env.dotPl*env.facP*env.FSWp
env.intPp=env.intPl*env.facP*env.intFSWp

###################################################
#STORE ENVIRONMENT EVOLUTION
###################################################
env.title="$M_1/M_{\\rm Sun}=$%.3f, $M_2/M_{\\rm Sun}$=%.3f, $a_{\\rm bin}$=%.3f AU, $e_{\\rm bin}$=%.2f, $P_{\\rm bin}$=%.3f d"%(star1.M,star2.M,binary.abin,binary.ebin,binary.Pbin)

PRINTERR("Storing rotational evolution data...")
f=open(env_dir+"interaction.data","w")

f.write("""\
from numpy import array
#TITLE
title=r"%s"

#REFERENCE VALUES
PEL=%.17e #W m^-2
SWPEL=%.17e #part m^-2 s^-1 

#NORMALIZATION FACTORS FOR MASS-LOSS
dotM=%.17e #kg s^-1 / PEL
intM=%.17e #Mearth / (PEL*GYR)
dotNl=%.17e #ions s^-1 / SWPEL
dotPl=%.17e #bars s^-1 / SWPEL
intPl=%.17e #bars / (SWPEL*GYR)
facM=%.17e #kg / PEL
facN=%.17e #ions / SWPEL
facP=%.17e #bars / SWPEL

#LUMFLUX
lumflux=%s

#INTEGRATED FLUXES
intflux=%s

#INSTANTANEOUS FLUXES AND DYNAMIC PRESSURE (AT TAUREF)
FXUVin=%.17e #PEL
FXUVout=%.17e #PEL
FXUVp=%.17e #EPL

FSWin=%.17e #SWPEL
FSWout=%.17e #SWPEL
FSWp=%.17e #SWPEL

PSWin=%.17e # Pa
PSWout=%.17e # Pa
PFSWp=%.17e # Pa

#INTEGRATED FLUXES AND DYNAMIC PRESSURE (FROM TAUINI TO TAUREF)
intFXUVin=%.17e #PEL*GYR
intFXUVout=%.17e #PEL*GYR
intFXUVp=%.17e #PEL*GYR

intFSWin=%.17e #SWPEL*GYR
intFSWout=%.17e #SWPEL*GYR
intFSWp=%.17e #SWPEL*GYR

#STANDOFF DISTANCE
Rs=%.17e #Rp
sinRs=%.17e #Rp
soutRs=%.17e #Rp

#PLANETARY MASS-LOSS

#PHOTO-EVAPORATION
dotMp=%.17e #kg s^-1
intMp=%.17e #Mearth

#ENTRAINMENT
dotNp=%.17e #kg s^-1
dotPp=%.17e #bars s^-1
intPp=%.17e #bars

"""%(env.title,
     PELSI,SWPEL,
     env.dotM,env.intM,
     env.dotNl,env.dotPl,env.intPl,
     env.facM,env.facN,env.facP,
     array2str(env.lumflux),
     array2str(intflux),
     env.FXUVin,env.FXUVout,env.FXUVp,
     env.FSWin,env.FSWout,env.FSWp,
     env.PSWin,env.PSWout,env.PSWp,
     env.intFXUVin,env.intFXUVout,env.intFXUVp,
     env.intFSWin,env.intFSWout,env.intFSWp,
     env.Rs,env.sinRs,env.soutRs,
     env.dotMp,env.intMp,
     env.dotNp,env.dotPp,env.intPp
     ))
f.close()
#### END COMMENT ####

###################################################
#GENERATE PLOTS
###################################################
PRINTERR("Creating plots...")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#XUV FLUX ABSOLUTE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(env_dir,"flux-XUV",\
"""
from BHM.BHMstars import *
env=\
loadConf("%s"+"interaction.conf")+\
loadConf("%s"+"interaction.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")

#LOADING REFERENCE SOLAR SYSTEM
from BHM.BHMdata import *
fast=loadResults(DATA_DIR+"SolarSystemReference/fast/")
tsfast=fast.interaction.lumflux[:,0]
slow=loadResults(DATA_DIR+"SolarSystemReference/slow/")
tsslow=slow.interaction.lumflux[:,0]
nominal=loadResults(DATA_DIR+"SolarSystemReference/nominal/")
tsnom=nominal.interaction.lumflux[:,0]

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax2=ax.twinx()

ts=env.lumflux[:,0]

#AREAS
ax.fill_between(tsnom,nominal.interaction.lumflux[:,15],
                   nominal.interaction.lumflux[:,16],color='r',alpha=0.2)
ax.fill_between(ts,env.lumflux[:,15],env.lumflux[:,16],color='k',alpha=0.2)
ax.fill_between(ts,env.lumflux[:,9],env.lumflux[:,10],color='g',alpha=0.3)
ax.plot([0],[0],color='g',alpha=0.3,linewidth=10,label='BHZ')
ax.plot([0],[0],color='k',alpha=0.3,linewidth=10,label='Single Primary HZ')
ax.plot([0],[0],color='r',alpha=0.3,linewidth=10,label='Solar Sytem HZ')

#PLANET
ax.plot(ts,env.lumflux[:,11],'k-',linewidth=2,label=r'Planet $a_{\\rm p}$=%%.2f AU'%%planet.aorb)
#ax.plot(ts,env.lumflux[:,17],'k--',linewidth=2,label='Single Primary Earth Analogue')

ax.text(4.56,1.0,r"$\\oplus$",
        horizontalalignment='center',verticalalignment='center',
        fontsize=20)

ax.set_xscale("log")
ax.set_xlim((env.tauini,rot.taumaxrot))

for axt in ax,ax2:
   axt.set_yscale("log")
ymin,ymax=ax.get_ylim()
ax2.set_ylim((ymin,ymax))

#MASS-LOSS AXIS
xl=[]
xt=ax2.get_yticks()
for x in xt:
   Ml=x*env.facM*env.dotM
   lexp=np.floor(np.log10(Ml))
   mant=Ml/10**lexp
   xl+=["$10^{%%d}$"%%lexp]
ax2.set_yticklabels(xl)
ax.text(1.07,0.5,r"${\\dot M}_{\\rm Photo}$ ($\\times %%.2f\\;{\\rm kg\\cdot\\,s}^{-1}$), $\\rho_p = %%.2f\\;{\\rm g/cm}^3$"%%(mant,planet.rho/1E3),
        rotation=90,
        horizontalalignment='left',verticalalignment='center',
        transform=ax.transAxes)

ax.set_title(env.title,position=(0.5,1.02),fontsize=12)
ax.legend(loc='lower left',prop=dict(size=10))
ax.grid(which="both",zorder=-10)

ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$F_{\\rm XUV}$ (PEL)")
"""%(env_dir,env_dir,
     planet_dir,planet_dir,
     rot_dir,rot_dir
     ),
           watermarkpos='inner')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#SW FLUX ABSOLUTE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(env_dir,"flux-SW",\
"""
from BHM.BHMstars import *
env=\
loadConf("%s"+"interaction.conf")+\
loadConf("%s"+"interaction.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")

#LOADING REFERENCE SOLAR SYSTEM
from BHM.BHMdata import *
fast=loadResults(DATA_DIR+"SolarSystemReference/fast/")
tsfast=fast.interaction.lumflux[:,0]
slow=loadResults(DATA_DIR+"SolarSystemReference/slow/")
tsslow=slow.interaction.lumflux[:,0]
nominal=loadResults(DATA_DIR+"SolarSystemReference/nominal/")
tsnom=nominal.interaction.lumflux[:,0]

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

ts=env.lumflux[:,0]

#AREAS
ax.fill_between(ts,env.lumflux[:,31],env.lumflux[:,33],color='k',alpha=0.2)
ax.fill_between(ts,env.lumflux[:,19],env.lumflux[:,21],color='g',alpha=0.3)
ax.fill_between(tsnom,nominal.interaction.lumflux[:,31],
                      nominal.interaction.lumflux[:,33],color='r',alpha=0.2)
ax.plot([0],[0],color='g',alpha=0.3,linewidth=10,label='BHZ')
ax.plot([0],[0],color='k',alpha=0.3,linewidth=10,label='Single Primary HZ')
ax.plot([0],[0],color='r',alpha=0.3,linewidth=10,label='Solar System HZ')

ax.plot(ts,env.lumflux[:,23],'k-',linewidth=2,label=r'Planet $a_{\\rm p}$=%%.2f AU'%%planet.aorb)
#ax.plot(ts,env.lumflux[:,35],'k--',linewidth=2,label='Single Primary Earth-analogue')

ax.text(4.56,1.0,r"$\\oplus$",
        horizontalalignment='center',verticalalignment='center',
        fontsize=20)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim((env.tauini,rot.taumaxrot))

#MASS-LOSS AXIS
xmin,xmax=ax.get_xlim()
xt=ax.get_yticks()
for x in xt:
   Ml=x*env.facN*env.dotNl
   lexp=np.floor(np.log10(Ml))
   mant=Ml/10**lexp
   ax.text(xmax,x,"$10^{%%d}$"%%lexp,verticalalignment='center',transform=offSet(5,0))
ax.text(1.07,0.5,r"${\\dot N}$ ($\\times %%.2f\;{\\rm ions\\cdot s}^{-1}$), $R_p = %%.2f\,R_\oplus$"%%(mant,planet.Rp),
        rotation=90,
        horizontalalignment='left',verticalalignment='center',
        transform=ax.transAxes)

ax.set_title(env.title,position=(0.5,1.02),fontsize=12)
ax.legend(loc='lower left',prop=dict(size=10))
ax.grid(which="both",zorder=-10)

ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$F_{\\rm SW}$ (PEL)")
"""%(env_dir,env_dir,
     planet_dir,planet_dir,
     rot_dir,rot_dir
     ),
           watermarkpos='inner')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#SW FLUX ABSOLUTE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(env_dir,"flux-PSW",\
"""
from BHM.BHMstars import *
env=\
loadConf("%s"+"interaction.conf")+\
loadConf("%s"+"interaction.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")

#LOADING REFERENCE SOLAR SYSTEM
from BHM.BHMdata import *
fast=loadResults(DATA_DIR+"SolarSystemReference/fast/")
tsfast=fast.interaction.lumflux[:,0]
slow=loadResults(DATA_DIR+"SolarSystemReference/slow/")
tsslow=slow.interaction.lumflux[:,0]
nominal=loadResults(DATA_DIR+"SolarSystemReference/nominal/")
tsnom=nominal.interaction.lumflux[:,0]

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.12,0.1,0.8,0.8])

ts=env.lumflux[:,0]

#AREAS
fac=1E-9
ax.fill_between(tsnom,nominal.interaction.lumflux[:,30]/fac,
                   nominal.interaction.lumflux[:,32]/fac,
                   color='r',alpha=0.3,label='Solar System HZ')
ax.fill_between(ts,env.lumflux[:,30]/fac,
                   env.lumflux[:,32]/fac,color='k',alpha=0.2,label='Single Primary HZ')
ax.fill_between(ts,env.lumflux[:,18]/fac,
                   env.lumflux[:,20]/fac,color='g',alpha=0.3,label='BHZ')

ax.plot([0],[0],color='g',alpha=0.3,linewidth=10,label='BHZ')
ax.plot([0],[0],color='k',alpha=0.3,linewidth=10,label='Single Primary HZ')
ax.plot([0],[0],color='r',alpha=0.3,linewidth=10,label='Solar System HZ')

ax.plot(ts,env.lumflux[:,22]/fac,'k-',linewidth=2,label=r'Planet $a_{\\rm p}$=%%.2f AU'%%planet.aorb)
#ax.plot(ts,env.lumflux[:,34]/fac,'k--',linewidth=2,label='Single Primary Earth-analogue')

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim((env.tauini,rot.taumaxrot))

ax.text(4.56,1.0,r"$\\oplus$",
        horizontalalignment='center',verticalalignment='center',
        fontsize=20)

ax.set_title(env.title,position=(0.5,1.02),fontsize=12)
ax.legend(loc='lower left',prop=dict(size=10))
ax.grid(which='both')
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$P_{\\rm SW}$ (${\\rm nPa}$)")
"""%(env_dir,env_dir,
     planet_dir,planet_dir,
     rot_dir,rot_dir
     ),
           watermarkpos='outer')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INTEGRATED FXUV
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(env_dir,"int-XUV",\
"""
from BHM.BHMstars import *
env=\
loadConf("%s"+"interaction.conf")+\
loadConf("%s"+"interaction.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")

#LOADING REFERENCE SOLAR SYSTEM
from BHM.BHMdata import *
fast=loadResults(DATA_DIR+"SolarSystemReference/fast/")
tsfast=fast.interaction.intflux[:,0]
slow=loadResults(DATA_DIR+"SolarSystemReference/slow/")
tsslow=slow.interaction.intflux[:,0]
nominal=loadResults(DATA_DIR+"SolarSystemReference/nominal/")
tsnom=nominal.interaction.intflux[:,0]


fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.80,0.8])

ts=env.intflux[:,0]

for tvec in 'ts','tsnom','tsfast','tsslow':
    exec("cond=%%s<env.tauref"%%tvec)
    exec("%%s=%%s[cond]"%%(tvec,tvec))

#RANGES
arrs=[]
facabs=1

arrs+=[facabs*nominal.interaction.intflux[cond,7],facabs*nominal.interaction.intflux[cond,8]]
ax.fill_between(tsnom,facabs*nominal.interaction.intflux[cond,7],facabs*nominal.interaction.intflux[cond,8],color='r',alpha=0.2,label='Single Primary HZ')

arrs+=[facabs*env.intflux[cond,7],facabs*env.intflux[cond,8]]
ax.fill_between(ts,facabs*env.intflux[cond,7],facabs*env.intflux[cond,8],color='k',alpha=0.2,label='Single Primary HZ')

arrs+=[facabs*env.intflux[cond,1],facabs*env.intflux[cond,2]]
ax.fill_between(ts,facabs*env.intflux[cond,1],facabs*env.intflux[cond,2],color='g',alpha=0.3,label='BHZ')

ax.plot([0],[0],color='g',alpha=0.3,linewidth=10,label='BHZ')
ax.plot([0],[0],color='k',alpha=0.3,linewidth=10,label='Single Primary HZ')
ax.plot([0],[0],color='r',alpha=0.3,linewidth=10,label='Solar System HZ')

#PLANET
arrs+=[facabs*env.intflux[cond,3],facabs*env.intflux[cond,9]]
ax.plot(ts,facabs*env.intflux[cond,3],'k-',linewidth=2,label=r'Planet $a_{\\rm p}$=%%.2f AU'%%planet.aorb)
#ax.plot(ts,facabs*env.intflux[cond,9],'k--',linewidth=2,label='Single Primary Earth-Analogue')

ymin,ymean,ymax=minmeanmaxArrays(arrs)

expscl=int(np.log10(ymax))
scl=10**expscl

ax.set_xscale("log")
#ax.set_xlim((env.tauini,rot.taumaxrot))
ax.set_xlim((env.tauini,env.tauref))

ax.set_yscale("log")
ylow=max(ymin,ymean/10)
ax.set_ylim((ylow,ymax))
xt=ax.get_yticks()
logTickLabels(ax,-1,3,(2,),axis="y",frm='%%.0f',fontsize=12)
xt2=ax.get_yticks()

#MASS-LOSS AXIS
xmin,xmax=ax.get_xlim()
for x in xt:
   if x<ylow or x>ymax:continue
   Ml=x*env.intM*env.facM
   lexp=np.floor(np.log10(Ml))
   mant=Ml/10**lexp
   ax.text(xmax,x,"$10^{%%d}$"%%lexp,verticalalignment='center',transform=offSet(5,0))

#SECONDARY TICKS
for x in xt2:
   if x<ylow or x>ymax:continue
   Ml=x*env.intM*env.facM
   lexp=np.floor(np.log10(Ml/mant))
   val=Ml/10**lexp/mant
   if np.abs(val-1)<1E-3:continue
   ax.text(xmax,x,r"$%%.0f\\times$"%%(val),verticalalignment='center',transform=offSet(5,0),fontsize=10)

ax.text(1.07,0.5,r"${\\Delta M}_{\\rm Photo}$ [$\\times %%.2f\;M_\oplus$], $\\rho_p = %%.2f\\;{\\rm g/cm}^3$"%%(mant,planet.rho/1E3),
        rotation=90,
        horizontalalignment='left',verticalalignment='center',
        transform=ax.transAxes)

ax.set_ylim((ylow,ymax))
ax.set_title(env.title,position=(0.5,1.02),fontsize=12)
ax.grid(which="both")
ax.legend(loc='lower right',prop=dict(size=10))
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$\\Phi_{\\rm XUV}(\\tau\,;\,\\tau_{\\rm ini})$")

"""%(env_dir,env_dir,
     planet_dir,planet_dir,
     rot_dir,rot_dir
     ),
           watermarkpos='inner')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#INTEGRATED FSW
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(env_dir,"int-SW",\
"""
from BHM.BHMstars import *
env=\
loadConf("%s"+"interaction.conf")+\
loadConf("%s"+"interaction.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")
rot=\
loadConf("%s"+"rotation.conf")+\
loadConf("%s"+"rotation.data")

#LOADING REFERENCE SOLAR SYSTEM
from BHM.BHMdata import *
fast=loadResults(DATA_DIR+"SolarSystemReference/fast/")
tsfast=fast.interaction.intflux[:,0]
slow=loadResults(DATA_DIR+"SolarSystemReference/slow/")
tsslow=slow.interaction.intflux[:,0]
nominal=loadResults(DATA_DIR+"SolarSystemReference/nominal/")
tsnom=nominal.interaction.intflux[:,0]

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.80,0.8])

ts=env.intflux[:,0]
for tvec in 'ts','tsnom','tsfast','tsslow':
    exec("cond=%%s<env.tauref"%%tvec)
    exec("%%s=%%s[cond]"%%(tvec,tvec))

#RANGES
arrs=[]
facabs=1

arrs+=[facabs*nominal.interaction.intflux[cond,23],facabs*nominal.interaction.intflux[cond,25]]
ax.fill_between(tsnom,facabs*nominal.interaction.intflux[cond,23],facabs*nominal.interaction.intflux[cond,25],color='r',alpha=0.2,label='Single Primary HZ')

arrs+=[facabs*env.intflux[cond,23],facabs*env.intflux[cond,25]]
ax.fill_between(ts,facabs*env.intflux[cond,23],facabs*env.intflux[cond,25],color='k',alpha=0.2,label='Single Primary HZ')

arrs+=[facabs*env.intflux[cond,11],facabs*env.intflux[cond,13]]
ax.fill_between(ts,facabs*env.intflux[cond,11],facabs*env.intflux[cond,13],color='g',alpha=0.3,label='BHZ')

ax.plot([0],[0],color='g',alpha=0.3,linewidth=10,label='BHZ')
ax.plot([0],[0],color='k',alpha=0.3,linewidth=10,label='Single Primary HZ')
ax.plot([0],[0],color='r',alpha=0.3,linewidth=10,label='Solar System HZ')

#PLANET
arrs+=[facabs*env.intflux[cond,15],facabs*env.intflux[cond,27]]
ax.plot(ts,facabs*env.intflux[cond,15],'k-',linewidth=2,label=r'Planet $a_{\\rm p}$=%%.2f AU'%%planet.aorb)
#ax.plot(ts,facabs*env.intflux[cond,27],'k--',linewidth=2,label='Single Primary Earth-Analogue')

ymin,ymean,ymax=minmeanmaxArrays(arrs)
expscl=int(np.log10(ymax))
scl=10**expscl

ax.set_xscale("log")
#ax.set_xlim((env.tauini,rot.taumaxrot))
ax.set_xlim((env.tauini,env.tauref))

ax.set_yscale("log")
ylow=max(ymin,ymean/10)
ax.set_ylim((ylow,ymax))
xt=ax.get_yticks()
logTickLabels(ax,-1,3,(2,),axis="y",frm='$%%.0f\\times$',notation="sci",fontsize=11)
xt2=ax.get_yticks()

#MASS-LOSS AXIS
xmin,xmax=ax.get_xlim()
#MAIN TICKS
mant=1.0
for x in xt:
   if x<ylow or x>ymax:continue
   Ml=x*env.intPl*env.facP
   lexp=np.floor(np.log10(Ml))
   mant=Ml/10**lexp
   ax.text(xmax,x,"$10^{%%d}$"%%lexp,verticalalignment='bottom',transform=offSet(5,0))

#SECONDARY TICKS
for x in xt2:
   if x<ylow or x>ymax:continue
   Ml=x*env.intPl*env.facP
   lexp=np.floor(np.log10(Ml/mant))
   val=Ml/10**lexp/mant
   if np.abs(val-1)<1E-3:continue
   ax.text(xmax,x,r"$%%.0f\\times$"%%(val),verticalalignment='center',transform=offSet(5,0),fontsize=10)

ax.text(1.07,0.5,r"${\\Delta P}_{\\rm Ent}$ [$\\times %%.2f\;{\\rm bars}$], $R_p = %%.2f\,R_\oplus$"%%(mant,planet.Rp),
        rotation=90,
        horizontalalignment='left',verticalalignment='center',
        transform=ax.transAxes)

ax.set_ylim((ylow,ymax))
ax.set_title(env.title,position=(0.5,1.02),fontsize=12)
ax.grid(which="both")
ax.legend(loc='lower right',prop=dict(size=10))
ax.set_xlabel(r"$\\tau$ [Gyr]")
ax.set_ylabel(r"$\\Phi_{\\rm SW}(\\tau\,;\,\\tau_{\\rm ini})$ [${\\rm SWPEL\\cdot\\,Gyr}$]")

"""%(env_dir,env_dir,
     planet_dir,planet_dir,
     rot_dir,rot_dir
     ),
           watermarkpos='inner')

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#STANDOFF DISTANCE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
plotFigure(env_dir,"standoff-distance",\
"""
from BHM.BHMstars import *
env=\
loadConf("%s"+"interaction.conf")+\
loadConf("%s"+"interaction.data")
planet=\
loadConf("%s"+"planet.conf")+\
loadConf("%s"+"planet.data")

#LOADING REFERENCE SOLAR SYSTEM
from BHM.BHMdata import *
fast=loadResults(DATA_DIR+"SolarSystemReference/fast/")
tsfast=fast.interaction.lumflux[:,0]
slow=loadResults(DATA_DIR+"SolarSystemReference/slow/")
tsslow=slow.interaction.lumflux[:,0]
nominal=loadResults(DATA_DIR+"SolarSystemReference/nominal/")
tsnom=nominal.interaction.lumflux[:,0]

fig=plt.figure(figsize=(8,6))
ax=fig.add_axes([0.1,0.1,0.8,0.8])

ts=env.lumflux[:,0]

ax.plot(ts,env.lumflux[:,36],'k-',label=r"Planet, $R_p$ = %%.2f $R_\\oplus$"%%planet.Rp)
ax.fill_between(tsnom,nominal.interaction.lumflux[:,38],
                   nominal.interaction.lumflux[:,39],color='r',alpha=0.2)
ax.fill_between(ts,env.lumflux[:,38],env.lumflux[:,39],color='k',alpha=0.2)
ax.plot([],[],'k-',linewidth=10,alpha=0.2,label='Single Primary HZ')
ax.plot([],[],'r-',linewidth=10,alpha=0.2,label='Solar System HZ')

ax.text(0.05,0.05,planet.orbit,transform=ax.transAxes)
ax.set_title(env.title,position=(0.5,1.02),fontsize=12)
ax.legend(loc='upper left',prop=dict(size=12))
ax.set_xlabel(r"$\\tau$ (Gyr)")
ax.set_ylabel(r"$R_{\\rm S}/R_{\\rm p}$")

ax.set_xscale("log")

#ymin,ymean,ymax=minmeanmaxArrays(arrs)
#ax.set_xlim((max(ymin,ymean/10),ymax))
"""%(env_dir,env_dir,
     planet_dir,planet_dir),
           watermarkpos='outer')

###################################################
#GENERATE FULL REPORT
###################################################
PRINTERR("Creating html report...")

fh=open(env_dir+"interaction.html","w")
fh.write("""\
<!--VERSION:%s-->
<head>
  <link rel="stylesheet" type="text/css" href="%s/web/BHM.css">
</head>

<h2>Stars-Planet Interaction</h2>

<h3>Plots</h3>

<h3>Fluxes and Mass-loss Rates</h3>

<table>

  <tr><td>
      <a href="%s/flux-XUV.png" target="_blank">
	<img width=100%% src="%s/flux-XUV.png?%s">
      </a>
      <br/>
      <div class="caption">
      <i>XUV Flux / Photoevaporation Mass-loss Rate</i>
	(
	<a href="%s/flux-XUV.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=flux-XUV.py" target="_blank">replot</a>
	)
      </div>
  </td></tr>

  <tr><td>
      <a href="%s/flux-SW.png" target="_blank">
	<img width=100%% src="%s/flux-SW.png?%s">
      </a>
      <br/>
      <div class="caption">
      <i>SW Flux / Entrainment Particle-loss Rate</i>
	(
	<a href="%s/flux-SW.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=flux-SW.py" target="_blank">replot</a>
	)
      </div>
  </td></tr>

</table>

<h3>Integrated Fluxes and Total Mass-losses</h3>

<table>

  <tr><td>
      <a href="%s/int-XUV.png" target="_blank">
	<img width=100%% src="%s/int-XUV.png?%s">
      </a>
      <br/>
      <div class="caption">
      <i>Integrated XUV Flux / Photoevaporation Total Mass-loss</i>
	(
	<a href="%s/int-XUV.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=int-XUV.py" target="_blank">replot</a>
	)
      </div>
  </td></tr>

  <tr><td>
      <a href="%s/int-SW.png" target="_blank">
	<img width=100%% src="%s/int-SW.png?%s">
      </a>
      <br/>
      <div class="caption">
      <i>Integrated SW Flux / Entrainment Total Particle-loss Rate</i>
	(
	<a href="%s/int-SW.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=int-SW.py" target="_blank">replot</a>
	)
      </div>
  </td></tr>

</table>

<h3>Dynamic Pressure and Standoff Distance</h3>

<table>

  <tr><td>
      <a href="%s/flux-PSW.png" target="_blank">
	<img width=100%% src="%s/flux-PSW.png?%s">
      </a>
      <br/>
      <div class="caption">
      <i>Dynamic Pressure</i>
	(
	<a href="%s/flux-PSW.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=flux-PSW.py" target="_blank">replot</a>
	)
      </div>
  </td></tr>

  <tr><td>
      <a href="%s/standoff-distance.png" target="_blank">
	<img width=100%% src="%s/standoff-distance.png?%s">
      </a>
      <br/>
      <div class="caption">
      <i>Standoff Distance</i>
	(
	<a href="%s/standoff-distance.png.txt" target="_blank">data</a>|
	<a href="%s/BHMreplot.php?dir=%s&plot=standoff-distance.py" target="_blank">replot</a>
	)
      </div>
  </td></tr>
</table>

<h3>Input Parameters</h3>
<table>
  <tr><td colspan=2><b>Times</b></td></tr>
  <tr><td>&tau;<sub>ini</sub> (Gyr)</td><td>%.3f</td></tr>
  <tr><td>&tau;<sub>ref</sub> (Gyr)</td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Entrainment Parameters</b></td></tr>
  <tr><td>&alpha;</td><td>%.3f</td></tr>
  <tr><td>&mu;<sub>atm</sub></td><td>%.3f</td></tr>
  <tr><td colspan=2><b>Magnetospheres</b></td></tr>
  <tr><td>Reference Object</td><td>%s</td></tr>
  <tr><td>n<sub>M</sub></td><td>%.1f</td></tr>
  <tr><td>n<sub>P</sub></td><td>%.1f</td></tr>
</table>

<h3>Reference Values</h3>
<table>
  <tr><td>PEL (W m<sup>-2</sup>)</td><td>%.3f</td></tr>
  <tr><td>SWPEL (part m<sup>-2</sup> s<sup>-1</sup>)</td><td>%.3e</td></tr>
</table>

<h3>Instantaneous values (&tau;=%.2f Gyr)</h3>
<table>
  <tr><td colspan=2><b>Fluxes</b></td></tr>
  <tr><td>F<sub>XUV</sub> (in,out,planet) [PEL]</td><td>%.2f,%.2f,<b>%.2f</b></td></tr>
  <tr><td>&Phi;<sub>XUV</sub> (in,out,planet) [SWPEL]</td><td>%.2e,%.2e,<b>%.2e</b></td></tr>
  <tr><td>F<sub>SW</sub> (in,out,planet) [SWPEL]</td><td>%.2f,%.2f,<b>%.2f</b></td></tr>
  <tr><td>&Phi;<sub>SW</sub> (in,out,planet) [SWPEL]</td><td>%.2e,%.2e,<b>%.2e</b></td></tr>
  <tr><td colspan=2><b>Standoff Distance</b></td></tr>
  <tr><td>P<sub>SW</sub> (in,out,planet) [SWPEL]</td><td>%.2e,%.2e,<b>%.2e</b></td></tr>
  <tr><td>R<sub>s</sub> [R<sub>p</sub>] (single in, out)</td><td>%.2f (%.2f, %.2f)</td></tr>
  <tr><td colspan=2><b>Mass-loss rates</b></td></tr>
  <tr><td>Photo evaporation, dM/dt [kg s<sup>-1</sup>]</td><td>%.2e</td></tr>
  <tr><td>Photo evaporation, &Delta;M [M<sub>Earth</sub>]</td><td>%.2e</td></tr>
  <tr><td>Entrainment, dN/dt [s<sup>-1</sup>]</td><td>%.2e</td></tr>
  <tr><td>Entrainment, dP/dt [bar s<sup>-1</sup>]</td><td>%.2e</td></tr>
  <tr><td>Entrainment, &Delta;P [bar]</td><td>%.2e</td></tr>
</table>
"""%(VERSION,
     WEB_DIR,
     env_webdir,env_webdir,env_hash,env_webdir,WEB_DIR,env_webdir,
     env_webdir,env_webdir,env_hash,env_webdir,WEB_DIR,env_webdir,
     env_webdir,env_webdir,env_hash,env_webdir,WEB_DIR,env_webdir,
     env_webdir,env_webdir,env_hash,env_webdir,WEB_DIR,env_webdir,
     env_webdir,env_webdir,env_hash,env_webdir,WEB_DIR,env_webdir,
     env_webdir,env_webdir,env_hash,env_webdir,WEB_DIR,env_webdir,
     env.tauini,env.tauref,env.alpha,env.muatm,
     env.str_refobj,env.nM,env.nP,
     PEL,SWPEL,
     env.tauref,
     env.FXUVin,env.FXUVout,env.FXUVp,
     env.intFXUVin,env.intFXUVout,env.intFXUVp,
     env.FSWin,env.FSWout,env.FSWp,
     env.intFSWin,env.intFSWout,env.intFSWp,
     env.PSWin,env.PSWout,env.PSWp,
     env.Rs,env.sinRs,env.soutRs,
     env.dotMp,env.intMp,
     env.dotNp,env.dotPp,env.intPp
     ))
fh.close()

###################################################
#CLOSE OBJECT
###################################################
closeObject(env_dir)
