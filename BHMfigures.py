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
# EXAMPLE SCRIPTS OF PAPER FIGURE PREPARATION
###################################################
from BHM import *
from BHM.BHMdata import *
from BHM.BHMplot import *
from BHM.BHMstars import *
from BHM.BHMplanets import *
from BHM.BHMastro import *

FIGDIR="figures/"

def CompareLuminositiesMassLoss():
    """
    Compare XUV luminosities and mass-loss from a single solar star
    with different rotational parameters.

    This calculation has been done in part with BHMcalc2
    """
    DATADIR=FIGDIR+"CompSolar/"
    
    """
    Fast rotator:
      tau = 4.56
      Pini = 1.5 days Gallat & Bouvier 
      taudisk = 2 Myrs
      tauc = 1 Myrs
      Kw = 5.4x10^40
    """
    fast=loadResults(DATADIR+"fast/")
    
    """
    Nominal parameters:
      tau = 4.56
      Pini = 7 days Gallat & Bouvier 
      taudisk = 2 Myrs
      tauc = 7 Myrs
      Kw = 5.0x10^40
    """
    nominal=loadResults(DATADIR+"nominal/")

    """
    Slow rotator:
      tau = 4.56
      Pini = 12.0 days Gallat & Bouvier 
      taudisk = 2 Myrs
      tauc = 1 Myrs
      Kw = 4.6x10^40
    """
    slow=loadResults(DATADIR+"slow/")

    #############################################################
    #PLOT ROTATION
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    tsnom=nominal.star1.rotevol[:,0]
    Onom=nominal.star1.rotevol[:,1]/OMEGASUN

    tsfast=fast.star1.rotevol[:,0]
    Ofast=fast.star1.rotevol[:,1]/OMEGASUN

    tsslow=slow.star1.rotevol[:,0]
    Oslow=slow.star1.rotevol[:,1]/OMEGASUN

    ax.plot(tsnom,Onom,label="Nominal")
    ax.plot(tsfast,Ofast,label="Fast")
    ax.plot(tsslow,Oslow,label="Slow")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(loc="best",prop=dict(size=10))

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel("$\Omega/\Omega_\odot$")

    tmin,tmax=ax.get_xlim()
    wmin,wmax=ax.get_ylim()
    Pmin=2*PI/(wmax*OMEGASUN)/DAY
    Pmax=2*PI/(wmin*OMEGASUN)/DAY
    for P in np.logspace(np.log10(Pmin),np.log10(Pmax),10):
        if P>Pmax:break
        w=2*PI/(P*DAY)/OMEGASUN
        ax.axhline(w,xmin=0.98,xmax=1.00,color='k')
        ax.text(tmax,w,"%.1f"%P,transform=offSet(5,0),verticalalignment='center',horizontalalignment='left',fontsize=10)

    fig.savefig(DATADIR+"rot.png")

    #############################################################
    #PLOT XUV LUMINOSITY
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    tsnom=nominal.star1.activity[:,0]
    LXUVnom=nominal.star1.activity[:,13]/(LXSUN/1E7)

    tsfast=fast.star1.activity[:,0]
    LXUVfast=fast.star1.activity[:,13]/(LXSUN/1E7)

    tsslow=slow.star1.activity[:,0]
    LXUVslow=slow.star1.activity[:,13]/(LXSUN/1E7)

    ax.plot(tsnom,LXUVnom,label="Nominal")
    ax.plot(tsfast,LXUVfast,label="Fast")
    ax.plot(tsslow,LXUVslow,label="Slow")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(loc="best",prop=dict(size=10))

    #DATA FOR OTHER STARS
    for star_name in ROTAGE_STARS.keys():
        staro=ROTAGE_STARS[star_name]
        tau=staro["tau"]
        Prot=staro["Prot"]
        ax.plot([tau],[2*PI/(Prot*DAY)/OMEGASUN],'o',markersize=10,markeredgecolor='none',color=cm.gray(0.5),zorder=-10)
        ax.text(tau,2*PI/(Prot*DAY)/OMEGASUN,star_name,transform=offSet(-10,staro["up"]),horizontalalignment="right",color=cm.gray(0.1),zorder=-10,fontsize=10)

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$L_{\rm XUV}/L_{\rm XUV,\odot,today}$")

    fig.savefig(DATADIR+"XUV.png")

    #############################################################
    #PLOT XUV LUMINOSITY
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    tsnom=nominal.star1.activity[:,0]
    LXUVnom=nominal.star1.activity[:,13]/(LXSUN/1E7)

    tsfast=fast.star1.activity[:,0]
    LXUVfast=fast.star1.activity[:,13]/(LXSUN/1E7)

    tsslow=slow.star1.activity[:,0]
    LXUVslow=slow.star1.activity[:,13]/(LXSUN/1E7)

    ax.plot(tsnom,LXUVnom,label="Nominal")
    ax.plot(tsfast,LXUVfast,label="Fast")
    ax.plot(tsslow,LXUVslow,label="Slow")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(loc="best",prop=dict(size=10))

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$L_{\rm XUV}/L_{\rm XUV,\odot,today}$")

    fig.savefig(DATADIR+"ML.png")


CompareLuminositiesMassLoss()

