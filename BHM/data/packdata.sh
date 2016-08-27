#!/bin/bash
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
# PACK DATA
###################################################
DATADIR="../.data"
EXCLUDE="--exclude BHMcat --exclude packdata.sh"
echo "Preparing tarball..."
tar zcf $DATADIR/data.tgz $EXCLUDE *
cd $DATADIR
echo "Splitting tarball..."
rm data_*
split -b 1000000 data.tgz data_
rm data.tgz
cd -
echo "Done."
