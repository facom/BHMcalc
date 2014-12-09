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
# BHM Configuration File
###################################################
from numpy import array

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#DIRECTORIES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exec("TMP_DIR='tmp/'");
exec("OBJ_DIR='objs/'");
exec("LOG_DIR='logs/'");
exec("DATA_DIR='BHM/data/'");
exec("WEB_COMMON='/var/www'");

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#BEHAVIOR
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exec("LOG_MODE=0");
exec("VERBOSE=0");

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#PHYSICAL
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exec("IN_CRITS=('recent venus','runaway greenhouse','moist greenhouse')");
exec("OUT_CRITS=('maximum greenhouse','early mars')");
exec("TAU_MIN=0.001");
exec("TAU_ZAMS=0.1");
exec("TAU_MAX=12.5");
exec("NTIMES=100");

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#OBJECT HASHABLES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exec("OBJECT_HASHABLES=dict()")
exec("OBJECT_HASHABLES['star']=dict(M='%.4f',Z='%.4f',FeH='%.4f',tau='%.4f',str_model='%s')")
exec("OBJECT_HASHABLES['binary']=dict(Pbin='%.4f',abin='%.4f',ebin='%.4f',str_sys='%s')")
exec("OBJECT_HASHABLES['planet']=dict(M='%.4f',fHHe='%.4f',CMF='%.4f',tau='%.4f',aorb='%.4f',eorb='%.4f',Porb='%.4f',worb='%.4f',Prot='%.4f')")
exec("OBJECT_HASHABLES['rotation']=dict(k='%.4f',str_sys='%s')")
exec("OBJECT_HASHABLES['hz']=dict(str_incrit_wd='%s',str_incrit_nr='%s',str_outcrit_wd='%s',str_outcrit_nr='%s',str_sys='%s')")
exec("OBJECT_HASHABLES['interaction']=dict(tauini='%.4f',tauref='%.4f',nM='%.2f',nP='%.2f',str_refobj='%s',str_sys='%s')")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#PIPE TREE
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exec("OBJECT_PIPE=dict()")
exec("OBJECT_PIPE['star1']=[]")
exec("OBJECT_PIPE['star2']=[]")
exec("OBJECT_PIPE['planet']=[]")
exec("OBJECT_PIPE['binary']=['star1','star2']")
exec("OBJECT_PIPE['hz']=['binary','planet','star1','star2']")
exec("OBJECT_PIPE['rotation']=['binary','star1','star2']")
exec("OBJECT_PIPE['interaction']=['star1','star2','binary','rotation','hz','planet']")
exec("OBJECT_EPIP=dict()")
exec("OBJECTS_ALL=['star1','star2','planet','binary','rotation','hz','interaction']")
