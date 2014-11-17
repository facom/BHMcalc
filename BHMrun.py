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
initializeEPIP()

###################################################
#CLI ARGUMENTS
###################################################
Usage=\
"""
Usage:
   python %s <script>.py <sysdir> [<module>.conf|CONFIG:<config_string>] <qoverride>

   <script>.py: Script to run

   <systdir>: Directory where the system configuration files lie

   <module>.conf (file): Configuration file for the module.

   or

   CONFIG:<config_string>: Configuration string.  Load system from a
   string instead of doing it from conf files.

   <qoverride> (int 0/1): Override any existent moduleect with the same hash.
"""%argv[0]

script,sys_dir,module_conf,qover=\
    readArgs(argv,
             ["str","str","str","int"],
             ["BHMstar.py","sys/template","star1.conf","0"],
             Usage=Usage)

###################################################
#PRELIMINARY VERIFICATIONS
###################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CHECK IF CONFIG STRING HAS BEEN PASSED
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 'CONFIG:' in module_conf:
    PRINTOUT("Parsing configuration script...")
    conf=module_conf
    conf=conf.replace("CONFIG:","")

    fields=conf.split("&")
    data=dict()
    for field in fields:
        if '_' not in field:continue
        parts=field.split("_")
        module=parts[0]
        if module not in data.keys():data[module]=dict()
        entry="_".join(parts[1:])
        vals=entry.split("=")
        key=vals[0]
        values=vals[1]
        data[module][key]=values

    if not DIREXISTS(sys_dir):System("mkdir -p %s"%sys_dir)
    for module in data.keys():
        print "Module:",module
        fm=open("%s/%s.conf"%(sys_dir,module),"w")
        for key in data[module].keys():
            value=data[module][key]
            if 'str' in key:
                entry="%s=\"'%s'\"\n"%(key,value)
            else:
                entry="%s=%s\n"%(key,value)
            fm.write(entry)
        fm.close()
    script="BHMinteraction.py"
    module_conf="interaction.conf"
    qover=2

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#HASH MODULE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
module_file="%s/%s"%(sys_dir,module_conf)
if not FILEEXISTS(module_file):
    PRINTERR("File '%s' does not exist."%module_file)
    errorCode("FILE_ERROR")

###################################################
#RUN MODULE
###################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#HASH MODULE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
module_type=module_conf
module_type=module_type.replace(".conf","")
module_name=module_type

PRINTOUT("*"*60)
PRINTOUT("STARTING BHMRUN FOR MODULE %s"%module_name)
PRINTOUT("*"*60)
PRINTERR("Error Output:")
PRINTOUT("System Directory: %s"%sys_dir)

module_type=module_type.replace("1","")
module_type=module_type.replace("2","")
module,module_dir,module_str,module_hash,module_liv,module_stg=\
    signObject(module_type,sys_dir+"/"+module_conf)
PRINTOUT("Module type: %s"%module_type)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CHECK-OUT MODULES ON WHICH IT DEPENDS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for depmod in OBJECT_PIPE[module_name]:
    #========================================
    #HASHING OBJECTS
    #========================================
    depmod_conf="%s.conf"%depmod
    depmod_type=depmod
    depmod_type=depmod_type.replace("1","")
    depmod_type=depmod_type.replace("2","")
    depmod,depmod_dir,depmod_str,depmod_hash,depmod_liv,depmod_stg=\
        signObject(depmod_type,sys_dir+"/"+depmod_conf)
    #========================================
    #HASHING OBJECTS
    #========================================
    if depmod_stg<10 or qover==2:
        if qover:PRINTOUT("Forcing %s"%depmod_type);
        else:PRINTOUT("Running %s (%s)"%(depmod_type,depmod_hash));
        System("python BHMrun.py BHM%s.py %s %s %d"%(depmod_type,sys_dir,depmod_conf,1),out=False)
    else:PRINTOUT("%s ready."%depmod_type);
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#EXECUTING MODULE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PRINTOUT("V"*60)
if module_stg<10 or qover>=1:
    if qover:PRINTOUT("Forcing %s"%module_type);
    System("python BHM%s.py %s %s %d"%(module_type,sys_dir,module_conf,qover),out=False)
    stage=System("cat %s/.stage"%module_dir,out=True)
    print "Stage:",stage
    if int(stage)<10:
        PRINTOUT("Task has ended with an error.")
    qupdate=True
else:
    qupdate=False
    PRINTOUT("%s ready."%module_type);

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#TAG MODULES DEPENDING ON THIS FOR RECAL
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if qupdate:
    for depmod in OBJECT_EPIP[module_name]:
        PRINTOUT("Signaling %s."%depmod)
        depmod_conf="%s.conf"%depmod
        depmod_type=depmod
        depmod_type=depmod_type.replace("1","")
        depmod_type=depmod_type.replace("2","")
        depmod,depmod_dir,depmod_str,depmod_hash,depmod_liv,depmod_stg=\
            signObject(depmod_type,sys_dir+"/"+depmod_conf)
        System("echo -1 > %s/.stage"%depmod_dir)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#OUTPUT
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print "--sig--\n%s"%module_hash
