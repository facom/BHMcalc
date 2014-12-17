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

    #DATA FOR OTHER STARS
    for star_name in ROTAGE_STARS.keys():
        staro=ROTAGE_STARS[star_name]
        tau=staro["tau"]
        Prot=staro["Prot"]
        ax.plot([tau],[2*PI/(Prot*DAY)/OMEGASUN],'o',markersize=10,markeredgecolor='none',color=cm.gray(0.5),zorder=-10)
        ax.text(tau,2*PI/(Prot*DAY)/OMEGASUN,star_name,transform=offSet(-10,staro["up"]),horizontalalignment="right",color=cm.gray(0.1),zorder=-10,fontsize=10)

    tmin,tmax=ax.get_xlim()
    wmin,wmax=ax.get_ylim()
    Pmin=1.0*(2*PI/(wmax*OMEGASUN)/DAY)
    Pmax=1.0*(2*PI/(wmin*OMEGASUN)/DAY)
    #Pvec=np.logspace(np.log10(Pmin),np.log10(Pmax),10)
    Pvec=np.arange(Pmin,Pmax,1.0)
    i=-1
    for P in Pvec:
        i+=1
        if P>Pmax:break
        w=2*PI/(P*DAY)/OMEGASUN
        ax.axhline(w,xmin=0.98,xmax=1.00,color='k')
        if (i%5)!=0 or w<0.8:continue
        ax.text(tmax,w,"%.1f"%P,transform=offSet(5,0),verticalalignment='center',horizontalalignment='left',fontsize=10)

    ax.text(1.07,0.5,r"$P$ (days)",rotation=90,verticalalignment='center',horizontalalignment='center',transform=ax.transAxes)

    ymin,ymax=ax.get_ylim()
    ax.set_ylim((0.8,ymax))
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

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$L_{\rm XUV}/L_{\rm XUV,\odot,today}$")

    fig.savefig(DATADIR+"XUV.png")

    #############################################################
    #PLOT MASS-LOSS
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    tsnom=nominal.star1.activity[:,0]
    MLnom=nominal.star1.activity[:,7]

    tsfast=fast.star1.activity[:,0]
    MLfast=fast.star1.activity[:,7]

    tsslow=slow.star1.activity[:,0]
    MLslow=slow.star1.activity[:,7]

    ax.plot(tsnom,MLnom,label="Nominal")
    ax.plot(tsfast,MLfast,label="Fast")
    ax.plot(tsslow,MLslow,label="Slow")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(loc="best",prop=dict(size=10))

    ax.text(4.56,MSTSUN*YEAR/MSUN,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_ylabel(r"$\dot M$ ($M_\odot$/yr)")
    ax.set_xlabel(r"$\tau$ (Gyr)")

    fig.savefig(DATADIR+"ML.png")

def IntegratedReferenceFluxes():
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
    #PLOT FLUXES
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    tsnom=nominal.interaction.lumflux[:,0]
    FXUVnom_earth=nominal.interaction.lumflux[:,17]
    FXUVnom_venus=nominal.interaction.lumflux[:,15]
    FXUVnom_mars=nominal.interaction.lumflux[:,16]

    tsfast=fast.interaction.lumflux[:,0]
    FXUVfast_earth=fast.interaction.lumflux[:,17]
    FXUVfast_venus=fast.interaction.lumflux[:,15]
    FXUVfast_mars=fast.interaction.lumflux[:,16]
    
    tsslow=slow.interaction.lumflux[:,0]
    FXUVslow_earth=slow.interaction.lumflux[:,17]
    FXUVslow_venus=slow.interaction.lumflux[:,15]
    FXUVslow_mars=slow.interaction.lumflux[:,16]

    #PLOT
    ax.fill_between(tsslow,FXUVslow_earth,FXUVfast_earth,color='b',alpha=0.3)
    ax.plot(tsnom,FXUVnom_earth,'b-',label='Earth')

    ax.fill_between(tsslow,FXUVslow_venus,FXUVfast_venus,color='g',alpha=0.3)
    ax.plot(tsnom,FXUVnom_venus,'g-',label='Venus')

    ax.fill_between(tsslow,FXUVslow_mars,FXUVfast_mars,color='r',alpha=0.3)
    ax.plot(tsnom,FXUVnom_mars,'r-',label='Mars')

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xscale("log")
    ax.set_yscale("log")
    
    ax.legend(loc='upper right',prop=dict(size=10))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$F_{\rm XUV}$ (PEL)")

    fig.savefig(DATADIR+"XUV-Flux.png")

    #############################################################
    #PLOT FLUXES
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    tsnom=nominal.interaction.lumflux[:,0]
    FSWnom_earth=nominal.interaction.lumflux[:,35]
    FSWnom_venus=nominal.interaction.lumflux[:,31]
    FSWnom_mars=nominal.interaction.lumflux[:,33]

    tsfast=fast.interaction.lumflux[:,0]
    FSWfast_earth=fast.interaction.lumflux[:,35]
    FSWfast_venus=fast.interaction.lumflux[:,31]
    FSWfast_mars=fast.interaction.lumflux[:,33]
    
    tsslow=slow.interaction.lumflux[:,0]
    FSWslow_earth=slow.interaction.lumflux[:,35]
    FSWslow_venus=slow.interaction.lumflux[:,31]
    FSWslow_mars=slow.interaction.lumflux[:,33]

    #PLOT
    ax.fill_between(tsslow,FSWslow_earth,FSWfast_earth,color='b',alpha=0.3)
    ax.plot(tsnom,FSWnom_earth,'b-',label='Earth')

    ax.fill_between(tsslow,FSWslow_venus,FSWfast_venus,color='g',alpha=0.3)
    ax.plot(tsnom,FSWnom_venus,'g-',label='Venus')

    ax.fill_between(tsslow,FSWslow_mars,FSWfast_mars,color='r',alpha=0.3)
    ax.plot(tsnom,FSWnom_mars,'r-',label='Mars')

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xscale("log")
    ax.set_yscale("log")
    
    ax.legend(loc='upper right',prop=dict(size=10))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$F_{\rm SW}$ (PEL)")

    fig.savefig(DATADIR+"SW-Flux.png")

    #############################################################
    #PLOT INTEGRATED FLUXES
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.15,0.1,0.8,0.8])
    
    tsnom=nominal.interaction.intflux[:,0]
    FiXUVnom_earth=nominal.interaction.intflux[:,9]
    FiXUVnom_venus=nominal.interaction.intflux[:,7]
    FiXUVnom_mars=nominal.interaction.intflux[:,8]

    tsfast=fast.interaction.intflux[:,0]
    FiXUVfast_earth=fast.interaction.intflux[:,9]
    FiXUVfast_venus=fast.interaction.intflux[:,7]
    FiXUVfast_mars=fast.interaction.intflux[:,8]
    
    tsslow=slow.interaction.intflux[:,0]
    FiXUVslow_earth=slow.interaction.intflux[:,9]
    FiXUVslow_venus=slow.interaction.intflux[:,7]
    FiXUVslow_mars=slow.interaction.intflux[:,8]

    #PLOT
    facabs=GYR*PELSI
    ax.fill_between(tsslow,facabs*FiXUVslow_earth,facabs*FiXUVfast_earth,color='b',alpha=0.3)
    ax.plot(tsnom,facabs*FiXUVnom_earth,'b-',label='Earth')

    ax.fill_between(tsslow,facabs*FiXUVslow_venus,facabs*FiXUVfast_venus,color='g',alpha=0.3)
    ax.plot(tsnom,facabs*FiXUVnom_venus,'g-',label='Venus')

    ax.fill_between(tsslow,facabs*FiXUVslow_mars,facabs*FiXUVfast_mars,color='r',alpha=0.3)
    ax.plot(tsnom,facabs*FiXUVnom_mars,'r-',label='Mars')

    ax.set_xscale("log")
    ax.set_yscale("log")

    ymin,ymax=ax.get_ylim()
    ax.set_ylim((1E12,ymax))

    ax.legend(loc='upper right',prop=dict(size=10))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$\int_{%.2f\,{\rm Gyr}}^{\tau} F_{\rm XUV}(t)\,dt$ (${\rm j/m}^2$)"%(nominal.interaction.tauini))

    fig.savefig(DATADIR+"iXUV-Flux.png")

    #############################################################
    #PLOT INTEGRATED FLUXES
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.15,0.1,0.8,0.8])
    
    tsnom=nominal.interaction.intflux[:,0]
    FiSWnom_earth=nominal.interaction.intflux[:,27]
    FiSWnom_venus=nominal.interaction.intflux[:,23]
    FiSWnom_mars=nominal.interaction.intflux[:,25]

    tsfast=fast.interaction.intflux[:,0]
    FiSWfast_earth=fast.interaction.intflux[:,27]
    FiSWfast_venus=fast.interaction.intflux[:,23]
    FiSWfast_mars=fast.interaction.intflux[:,25]
    
    tsslow=slow.interaction.intflux[:,0]
    FiSWslow_earth=slow.interaction.intflux[:,27]
    FiSWslow_venus=slow.interaction.intflux[:,23]
    FiSWslow_mars=slow.interaction.intflux[:,25]

    #PLOT
    facabs=GYR*SWPEL
    ax.fill_between(tsslow,facabs*FiSWslow_earth,facabs*FiSWfast_earth,color='b',alpha=0.3)
    ax.plot(tsnom,facabs*FiSWnom_earth,'b-',label='Earth')

    ax.fill_between(tsslow,facabs*FiSWslow_venus,facabs*FiSWfast_venus,color='g',alpha=0.3)
    ax.plot(tsnom,facabs*FiSWnom_venus,'g-',label='Venus')

    ax.fill_between(tsslow,facabs*FiSWslow_mars,facabs*FiSWfast_mars,color='r',alpha=0.3)
    ax.plot(tsnom,facabs*FiSWnom_mars,'r-',label='Mars')

    ax.set_xscale("log")
    ax.set_yscale("log")

    ymin,ymax=ax.get_ylim()
    ax.set_ylim((1E25,ymax))

    ax.legend(loc='upper right',prop=dict(size=10))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$\int_{%.2f\,{\rm Gyr}}^{\tau} F_{\rm SW}(t)\,dt$ (${\rm ions/m}^2$)"%(nominal.interaction.tauini))

    fig.savefig(DATADIR+"iSW-Flux.png")

def IntegratedReferenceValues():
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

    #HABITABLE TIME
    tmars=1.5
    tearth=4.54
    tvenus=3.5

    tmars=tearth=tvenus=4.54

    #VALUES FOR MARS
    facabs=GYR*SWPEL

    ts,intflux_slow=interpMatrix(slow.interaction.intflux)
    ts,intflux_nominal=interpMatrix(nominal.interaction.intflux)
    ts,intflux_fast=interpMatrix(fast.interaction.intflux)

    iSW_mars_min=intflux_slow[25](tmars)*facabs
    iSW_mars_nom=intflux_nominal[25](tmars)*facabs
    iSW_mars_max=intflux_fast[25](tmars)*facabs

    iSW_earth_min=intflux_slow[27](tearth)*facabs
    iSW_earth_nom=intflux_nominal[27](tearth)*facabs
    iSW_earth_max=intflux_fast[27](tearth)*facabs

    iSW_venus_min=intflux_slow[23](tvenus)*facabs
    iSW_venus_nom=intflux_nominal[23](tvenus)*facabs
    iSW_venus_max=intflux_fast[23](tvenus)*facabs

    facabs=GYR*PELSI
    iXUV_venus_min=intflux_slow[7](tvenus)*facabs
    iXUV_venus_nom=intflux_nominal[7](tvenus)*facabs
    iXUV_venus_max=intflux_fast[7](tvenus)*facabs

    iXUV_earth_min=intflux_slow[9](tearth)*facabs
    iXUV_earth_nom=intflux_nominal[9](tearth)*facabs
    iXUV_earth_max=intflux_fast[9](tearth)*facabs
    
    print "Range of Stellar Wind flux on Mars: %e - %e ions/m^2"%(iSW_mars_min,iSW_mars_max)
    print "Range of Stellar Wind flux on Earth: %e - %e ions/m^2"%(iSW_earth_min,iSW_earth_max)
    print "Range of Stellar Wind flux on Venus: %e - %e ions/m^2"%(iSW_venus_min,iSW_venus_max)

    print "Range of XUV flux on Venus: %e - %e j/m^2"%(iXUV_venus_min,iXUV_venus_max)
    print "Range of Stellar Wind flux on Mars: %e - %e j/m^2"%(iXUV_earth_min,iXUV_earth_max)

    #########################################
    #CONVERT STELLAR WIND FLUX IN BARS
    #########################################

    #==============================
    #MARS
    #==============================
    Amars=4*PI*RMARS**2
    Ml_mars_min=massLoss(Amars,iSW_mars_min,
                         mu=nominal.interaction.muatm,alpha=nominal.interaction.alpha)
    Pl_mars_min=surfacePressure(Ml_mars_min,MMARS/MEARTH,RMARS/REARTH)
    Ml_mars_max=massLoss(Amars,iSW_mars_max,
                         mu=nominal.interaction.muatm,alpha=nominal.interaction.alpha)
    Pl_mars_max=surfacePressure(Ml_mars_max,MMARS/MEARTH,RMARS/REARTH)
    print "Pressure removed from Mars: %e - %e bars"%(Pl_mars_min,Pl_mars_max)

    #==============================
    #EARTH
    #==============================
    Aearth=4*PI*REARTH**2
    Ml_earth_min=massLoss(Aearth,iSW_earth_min,
                         mu=nominal.interaction.muatm,alpha=nominal.interaction.alpha)
    Pl_earth_min=surfacePressure(Ml_earth_min,MEARTH/MEARTH,REARTH/REARTH)
    Ml_earth_max=massLoss(Aearth,iSW_earth_max,
                         mu=nominal.interaction.muatm,alpha=nominal.interaction.alpha)
    Pl_earth_max=surfacePressure(Ml_earth_max,MEARTH/MEARTH,REARTH/REARTH)
    print "Pressure removed from Earth: %e - %e bars"%(Pl_earth_min,Pl_earth_max)

    #==============================
    #VENUS
    #==============================
    Avenus=4*PI*RVENUS**2
    Ml_venus_min=massLoss(Avenus,iSW_venus_min,
                         mu=nominal.interaction.muatm,alpha=nominal.interaction.alpha)
    Pl_venus_min=surfacePressure(Ml_venus_min,MVENUS/MEARTH,RVENUS/REARTH)
    Ml_venus_max=massLoss(Avenus,iSW_venus_max,
                         mu=nominal.interaction.muatm,alpha=nominal.interaction.alpha)
    Pl_venus_max=surfacePressure(Ml_venus_max,MVENUS/MEARTH,RVENUS/REARTH)
    print "Pressure removed from Venus: %e - %e bars"%(Pl_venus_min,Pl_venus_max)

    #########################################
    #CONVERT XUV FLUX IN MASS-LOSS
    #########################################

    #==============================
    #VENUS
    #==============================
    HMl_venus_min=massLossGiant(3.0e3,iXUV_venus_min)/MVENUS
    HMl_venus_max=massLossGiant(3.0e3,iXUV_venus_max)/MVENUS
    print HMl_venus_min,HMl_venus_max

    #==============================
    #EARTH
    #==============================
    HMl_earth_min=massLossGiant(3.0e3,iXUV_earth_min)/MEARTH
    HMl_earth_max=massLossGiant(3.0e3,iXUV_earth_max)/MEARTH
    print HMl_earth_min,HMl_earth_max
    
    #########################################
    #SAVING REFERENCE VALUES
    #########################################
    

#CompareLuminositiesMassLoss()
#IntegratedReferenceFluxes()
IntegratedReferenceValues()

