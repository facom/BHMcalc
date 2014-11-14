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
# Return object directories for a given sysdir
###################################################
from BHM import *

###################################################
#CLI ARGUMENTS
###################################################
Usage=\
"""
Usage:
   python %s <script>.py <sysdir>

   <sysdir>: Directory where the system configuration files lie

"""%argv[0]

sys_dir,=\
    readArgs(argv,
             ["str"],
             ["sys/template"],
             Usage=Usage)

###################################################
#PRELIMINARY VERIFICATIONS
###################################################
if not DIREXISTS(sys_dir):
    PRINTERR("Directory '%s' does not exist."%sys_dir)
    errorCode("FILE_ERROR")
PRINTERR("Error Output:")

###################################################
#LOADING ALREADY CALCULATED MODULES
###################################################
for depmod in OBJECTS_ALL:
    #========================================
    #HASHING OBJECTS
    #========================================
    depmod_conf="%s.conf"%depmod
    depmod_type=depmod
    depmod_type=depmod_type.replace("1","")
    depmod_type=depmod_type.replace("2","")
    depmod,depmod_dir,depmod_str,depmod_hash,depmod_liv,depmod_stg=\
        signObject(depmod_type,sys_dir+"/"+depmod_conf)
    if DIREXISTS(depmod_dir):
        print "%s:%s"%(depmod_type,depmod_hash)

        
