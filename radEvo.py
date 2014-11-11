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
   python %s <rad>.py <rot>.conf <binary>.conf <star1>.conf <star1>.conf <planet>.conf <qoverride>

   <rad>.conf (file): Configuration of the environmental evolution model.

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
