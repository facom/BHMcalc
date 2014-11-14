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
# Master running script
###################################################
from BHM import *

###################################################
#CLI ARGUMENTS
###################################################
Usage=\
"""
Usage:
   python %s <script>.py <sysdir> <module>.conf <qoverride>

   <script>.py: Script to run

   <systdir>: Directory where the system configuration files lie

   <module>.conf (file): Configuration file for the module.

   <qoverride> (int 0/1): Override any existent object with the same hash.
"""%argv[0]

script,sys_dir,module_conf,qover=\
    readArgs(argv,
             ["str","str","str","int"],
             ["BHMstar.py","sys/template","star1.conf","0"],
             Usage=Usage)

###################################################
#PRELIMINARY VERIFICATIONS
###################################################
module_file="%s/%s"%(sys_dir,module_conf)
if not FILEEXISTS(module_file):
    PRINTERR("File '%s' does not exist."%module_file)
    errorCode("FILE_ERROR")
PRINTERR("Error Output:")
###################################################
#RUN STAR
###################################################
PRINTOUT("System Directory: %s"%sys_dir)

if False:pass

elif "star" in script:

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CONFIGURATION FILES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    star_conf=module_conf
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #HASH OBJECT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    star,star_dir,star_str,star_hash,star_liv,star_stg=\
        signObject("star",sys_dir+"/"+star_conf)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #RUN SCRIPT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PRINTOUT("Running star script")
    out=System("python BHMstar.py %s %s %d"%(sys_dir,star_conf,qover),out=False)
    #PRINTOUT("\n--START EXTERNAL--\n"+out+"\n--END EXTERNAL--")
    print "--sig--\n%s"%star_hash

elif "planet" in script:

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CONFIGURATION FILES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    planet_conf=module_conf
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #HASH OBJECT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    planet,planet_dir,planet_str,planet_hash,planet_liv,planet_stg=\
        signObject("planet",sys_dir+"/"+planet_conf)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #RUN SCRIPT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    PRINTOUT("Running planet script")
    out=System("python BHMplanet.py %s %s %d"%(sys_dir,planet_conf,qover),out=False)
    #PRINTOUT("\n--START EXTERNAL--\n"+out+"\n--END EXTERNAL--")
    print "--sig--\n%s"%planet_hash

else:
    PRINTERR("Script '%s' not available."%script)
