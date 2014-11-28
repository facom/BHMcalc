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
# DATA INSTALLES
###################################################
if [ ! -d BHM/data/Stars ]
then
    echo "Reconstructing data tarball..."
    cat BHM/.data/data_* > /tmp/BHMdata.tgz
    echo "Unpacking data into data directory..."
    tar zxf /tmp/BHMdata.tgz -C BHM/
else
    echo "Data already unpacked."
fi


