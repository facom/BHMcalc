from BHM.isochrones import *
from BHM.plot import *
from BHM.BHM import *
from BHM.keplerbin import *
from numpy import *

############################################################
#CONFIGURATION
############################################################
TMPDIR="tmp/"

############################################################
#INPUT PARAMETERS
############################################################

############################################################
#PREPARATION
############################################################
plt.close("all")

############################################################
#LOAD DATA
############################################################
#loadData(True)
num=loadIsochroneSet(Zs=ZSVEC_siblings,verbose=True)

############################################################
#TEST CODE
############################################################
def HZ():
    tau=1.0
    Z=0.0152
    M=1.6
    g,T,R,L=StellarGTRL(Z,M,tau)
    lin,aE,lout=HZ2013(L,T)
    aHZ=(lin+lout)/2
    print "Stellar properties:"
    print "\tZ = %.4f"%Z
    print "\tM = %.2f"%M
    print "\tT = %.2f"%T
    print "\tg = %.2f"%g
    print "\tR = %.2f"%R
    print "\tL = %e"%L
    print "Habitability zone:"
    print "\tHZ = [%e,%e(%e),%e]"%(lin,aE,aHZ,lout)

############################################################
#CALL TEST CODE
############################################################
HZ()
