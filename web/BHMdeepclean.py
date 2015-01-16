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
# Deep clean the syte
###################################################
from BHM import *

###################################################
# CLEAN LINKS
###################################################
System("mkdir tmp/Links")
confs=open("sys/template/configurations.html")
PRINTOUT("Finding community configurations...")
for conf in confs:
    matches=re.search("href=\".*\/links\/(.+)\"",conf)
    if not matches:continue
    configuration=matches.group(1)
    PRINTOUT("\tConfiguration '%s' saved..."%configuration)
    System("cp -r links/\"%s\" tmp/Links"%configuration)
    System("git add links/\"%s\""%configuration)
confs.close()
PRINTOUT("Cleaning links...")
System("rm -rf links/*")
System("mv tmp/Links/* links/")

###################################################
# CLEAN OBJECTS
###################################################
listobj=System("ls -md objs/*",out=True).split(",")
System("mkdir tmp/Objs")
PRINTOUT("Preserving blocked objects...")
for obj in listobj:
    obj=obj.strip()
    if not FILEEXISTS("%s/.block"%obj):continue
    #PRINTOUT("\tObject '%s' saved..."%obj)
    System("cp -rf %s tmp/Objs/"%obj)
PRINTOUT("Cleaning objects...")
System("rm -rf objs/*")
System("mv tmp/Objs/* objs/")

###################################################
# CLEAN TEMPORARY
###################################################
PRINTOUT("Cleaning temporal...")
System("rm -rf tmp/*")

PRINTOUT("Cleaning system...")
System("make cleanall")

###################################################
# SETTING PERMISSIONS
###################################################
PRINTOUT("Setting up permissions...")
System("make permissions")
