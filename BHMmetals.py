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
# CONVERTS FROM Z TO FE/H AND VICEVERSA
###################################################
from BHM import *
from BHM.BHMstars import *

###################################################
#OPTIONS
###################################################
PRINTERR("Argv: %s"%str(argv));

try:
    parts=argv[1].split("&")
    value=float(parts[1].split("=")[1])
except:
    pass

PRINTERR("parts[0]=%s,val=%f"%(parts[0],value))

###################################################
#CONVERT
###################################################
if parts[0]=="ZtoFeH":
    FeH=FeHfromZ(value)
    print FeH
    PRINTERR(str(FeH))
else:
    Z,dZ=ZfromFHe(value)
    print Z
    PRINTERR(str(Z))
