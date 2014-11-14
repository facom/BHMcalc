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
exec("TAU_MIN=0.01");
exec("TAU_MAX=12.5");
exec("NTIMES=100");

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#OBJECT HASHABLES
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
exec("OBJECT_HASHABLES=dict()")
exec("OBJECT_HASHABLES['star']=dict(M='%.4f',Z='%.4f',FeH='%.4f',tau='%.4f')")
exec("OBJECT_HASHABLES['binary']=dict(Pbin='%.4f',abin='%.4f',ebin='%.4f')")
exec("OBJECT_HASHABLES['planet']=dict(M='%.4f',fHHe='%.4f',CMF='%.4f',tau='%.4f',aorb='%.4f',eorb='%.4f',Porb='%.4f',worb='%.4f',Prot='%.4f')")
exec("OBJECT_HASHABLES['rotation']=dict(k='%.4f')")
exec("OBJECT_HASHABLES['hz']=dict(incrit_wd='%s',incrit_nr='%s',outcrit_wd='%s',outcrit_nr='%s')")
exec("OBJECT_HASHABLES['interaction']=dict(tauini='%.4f',earlywind='%s',nM='%.2f',nP='%.2f',refobj='%s')")
