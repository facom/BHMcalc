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
   python %s <script>.py <sysdir> [<module>.conf|CONFIG:<config_string>] <sleep_before> <qoverride>

   <script>.py: Script to run

   <systdir>: Directory where the system configuration files lie

   <module>.conf (file): Configuration file for the module.

   or

   CONFIG:<config_string>: Configuration string.  Load system from a
   string instead of doing it from conf files.

   <sleep_before>: wait this seconds to start.

   <qoverride> (int 0/1): Override any existent moduleect with the same hash.
"""%argv[0]

script,sys_dir,module_conf,sleep_before,qover=\
    readArgs(argv,
             ["str","str","str","int","int"],
             ["BHMstar.py","sys/template","star1.conf","0","0"],
             Usage=Usage)

###################################################
#SLEEP BEFORE
###################################################
if sleep_before>0:
    PRINTOUT("Sleeping %d seconds before start..."%sleep_before)
    sleep(sleep_before)

###################################################
#PRELIMINARY VERIFICATIONS
###################################################
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CHECK IF CONFIG STRING HAS BEEN PROVIDED
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 'LOADCONFIG' in module_conf:
    PRINTOUT("Parsing query string...")
    conf=module_conf
    fields=conf.split("&")
    sys_str=MD5STR(conf)

    #LOAD DATA IN QSTRING INTO DICTIONARY
    data=dict()
    PRINTOUT("Loading variables into dictionary...")
    for field in fields:
        if '_' not in field:continue
        print field
        parts=field.split("_")
        module=parts[0]
        if module not in data.keys():data[module]=dict()
        entry="_".join(parts[1:])
        vals=entry.split("=")
        key=vals[0]
        values=vals[1]
        values=values.replace("%20"," ")
        values=values.replace("%27","")
        data[module][key]=values

    #CREATE CONFIGURATION FILE
    if not DIREXISTS(sys_dir):System("mkdir -p %s"%sys_dir)
    PRINTOUT("Saving parameters into configuration file...")
    for module in data.keys():
        print "Module:",module
        fm=open("%s/%s.conf"%(sys_dir,module),"w")
        for key in data[module].keys():
            value=data[module][key]
            if 'str' in key:
                if "'" not in value:
                    entry="%s=\"'%s'\"\n"%(key,value)
                else:
                    entry="%s=\"%s\"\n"%(key,value)
            else:
                entry="%s=%s\n"%(key,value)
            print "Entry: ",entry
            fm.write(entry)
        fm.write("str_sys=\"'%s'\"\n"%sys_str)
        fm.close()
        
    #PREPARE TO RUN
    if script=='-':exit(0)
    else:
        module_conf="interaction.conf"

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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CHECK IF MODULES DEPENDING ON THIS ARE RUNNING
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
MAXTRIALS=10
for depmod in OBJECT_EPIP[module_name]:
    PRINTOUT("Checking for blocks over %s."%depmod)
    depmod_name=depmod
    depmod_conf="%s.conf"%depmod
    depmod_type=depmod
    depmod_type=depmod_type.replace("1","")
    depmod_type=depmod_type.replace("2","")
    depmod,depmod_dir,depmod_str,depmod_hash,depmod_liv,depmod_stg=\
        signObject(depmod_type,sys_dir+"/"+depmod_conf)
    trials=0
    fblock=depmod_dir+".block"
    PRINTOUT("\tLooking for blocking file: %s"%fblock)
    while FILEEXISTS(fblock) and trials<MAXTRIALS:
        PRINTOUT("Waiting for %s to finish (trial %d)..."%(depmod_name,trials))
        sleep(1.0)
        trials+=1

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#CHECK-OUT MODULES ON WHICH IT DEPENDS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
depseed="";
PRINTOUT("Objects to precheck:"+str(OBJECT_PIPE[module_name]))
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
    depseed+=depmod_hash;

    #========================================
    #HASHING OBJECTS
    #========================================
    if depmod_stg<10 or qover==2:
        if qover:PRINTOUT("Forcing %s"%depmod_type);
        else:PRINTOUT("Running %s (%s)"%(depmod_type,depmod_hash));
        System("python BHMrun.py BHM%s.py %s %s %d"%(depmod_type,sys_dir,depmod_conf,1),out=False)
    else:PRINTOUT("%s %s ready."%(depmod_type,depmod_hash));
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#EXECUTING MODULE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PRINTOUT("V"*60)
if module_stg<10 or qover>=1:
    stagefile="%s/.stage"%module_dir
    if FILEEXISTS(stagefile):stage=System("cat "+stagefile,out=True)
    else:stage=0
    if qover:PRINTOUT("Forcing %s"%module_type);
    else:PRINTOUT("Executing module %s for %s in stage %s"%(module_type,module_hash,stage));
    System("touch %s/.block"%module_dir)
    System("python BHM%s.py %s %s %d"%(module_type,sys_dir,module_conf,qover),out=False)
    System("rm %s/.block"%module_dir)
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
