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
# - Binary data (rot.data)
# - Html report (rot.html)
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
   python %s <rot>.conf <binary>.conf <star1>.conf <star1>.conf <qoverride>

   <rot>.conf (file): Configuration of the rotational evolution model.

   <binary>.conf (file): Configuration file with data about binary.

   <star1>.conf,<star2>.conf (file): Configuration file with data
   about stars.

   <qoverride> (int 0/1): Override any previously existent
   calculation.
"""%(argv[0])

rot_conf,binary_conf,star1_conf,star2_conf,qover=\
    readArgs(argv,
             ["str","str","str","str","int"],
             ["rot.conf","binary.conf","star1.conf","star2.conf","0"],
             Usage=Usage)

PRINTOUT("Executing for: %s, %s, %s, %s"%(rot_conf,
                                          binary_conf,
                                          star1_conf,
                                          star2_conf))

###################################################
#LOAD PREVIOUS OBJECTS
###################################################
PRINTOUT("Loading other objects...")
#==================================================
#LOADING BINARY
binary,binary_dir,binary_str,binary_hash,binary_liv,binary_stg=\
    signObject(binary_conf)
system("python binBas.py %s %s %s %d"%(binary_conf,
                                       star1_conf,star2_conf,
                                       qover))
binary+=loadConf(binary_dir+"binary.data")
#==================================================
#LOADING STAR 1
star1,star1_dir,star1_str,star1_hash,star1_liv,star1_stg=\
    signObject(star1_conf)
star1+=loadConf(star1_dir+"star.data")
#==================================================
#LOADING STAR 2
star2,star2_dir,star2_str,star2_hash,star2_liv,star2_stg=\
    signObject(star2_conf)
star2+=loadConf(star2_dir+"star.data")
#==================================================
#CHECK IF TWINS
qnotwins=False
if star1_hash==star2_hash:
    qnotwins=True
    star2=star1

###################################################
#LOAD ROT OBJECT
###################################################
rot,rot_str,rot_hash,rot_dir=\
    makeObject(rot_conf,qover=qover)
rot_webdir=WEB_DIR+rot_dir
PRINTOUT("Object hash:%s"%rot_hash)

###################################################
#CALCULATE ROTATIONAL EVOLUTION
###################################################
stars=star1,star2
i=0

for star in stars:
    #==============================
    #LOAD STELLAR EVOLUTION
    #==============================
    evoInterpFunctions(star)

    #==============================
    #INITIAL ROTATION RATES
    #==============================
    star.Pmax=maxPeriod(star.M,star.R)
    star.Pini=Prot(TAU_MIN,Ms=star.M,Rs=star.Rfunc(TAU_MIN))/DAY
    if star.Pini<star.Pmax:star.Pmax=2*star.Pini
    star.W=2*PI/star.Pini
    
exit(0)

###################################################
#CLOSE OBJECT
###################################################
#closeObject(rot_dir)
