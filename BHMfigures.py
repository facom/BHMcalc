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
TMIN=1E-3
#TMIN_INT=7E-1
TMIN_INT=1E-2
TMAX=8.0

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

    ax.plot(tsnom,Onom,label=r"Nominal: $P_{\rm ini}=7$ days, $\tau_{\rm ce}=7$ Myrs, $K_C=5\times 10^{40}$")
    ax.plot(tsfast,Ofast,label=r"Fast: $P_{\rm ini}=1.5$ days, $\tau_{\rm ce}=15$ Myrs, $K_C=5.4\times 10^{40}$")
    ax.plot(tsslow,Oslow,label=r"Slow: $P_{\rm ini}=12$ days, $\tau_{\rm ce}=1$ Myrs, $K_C=4.6\times 10^{40}$")

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
    ax.set_xlim((TMIN,TMAX))
    ax.set_ylim((0.8,ymax))
    ax.grid(which='both')
    fig.savefig(DATADIR+"Solar-rot.png")

    #############################################################
    #PLOT XUV LUMINOSITY
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.12,0.12,0.8,0.8])
    
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
    ax.set_xlim((TMIN,TMAX))
    ax.legend(loc="best",prop=dict(size=12))

    ax.text(4.56,1.0,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$L_{\rm XUV}/L_{\rm XUV,\odot}$")
    ax.grid(which='both')

    fig.savefig(DATADIR+"Solar-XUV.png")

    #############################################################
    #PLOT MASS-LOSS
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.12,0.12,0.8,0.8])
    
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
    ax.set_xlim((TMIN,TMAX))
    ax.legend(loc="best",prop=dict(size=12))
    ax.set_xlim((TMIN,TMAX))

    ax.text(4.56,MSTSUN*YEAR/MSUN,r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ax.set_ylabel(r"$\dot M$ ($M_\odot$/yr)")
    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.grid(which='both')

    fig.savefig(DATADIR+"Solar-ML.png")

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
    
    ax.legend(loc='upper right',prop=dict(size=12))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$F_{\rm XUV}$ (PEL)")
    ax.set_xlim((TMIN_INT,TMAX))
    ax.set_ylim((1E-1,2E3))
    ax.grid(which='both')

    fig.savefig(DATADIR+"Solar-XUV-Flux.png")

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
    
    ax.legend(loc='upper right',prop=dict(size=12))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$F_{\rm SW}$ (PEL)")
    ax.set_xlim((TMIN_INT,TMAX))
    ax.set_ylim((1E-1,3E2))
    ax.grid(which='both')

    fig.savefig(DATADIR+"Solar-SW-Flux.png")
    return;

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
    ax.set_xlim((TMIN_INT,TMAX))

    fig.savefig(DATADIR+"Solar-iXUV-Flux.png")

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
    ax.set_xlim((TMIN_INT,TMAX))

    fig.savefig(DATADIR+"Solar-iSW-Flux.png")

def IntegratedReferenceFluxesTini():
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
    #PLOT INTEGRATED XUV FLUX
    #############################################################
    fig=plt.figure()
    
    tsnom=nominal.interaction.intflux[:,0]
    FiXUVnom_earthf=interp1d(tsnom,nominal.interaction.intflux[:,9],kind='slinear')
    FiXUVnom_venusf=interp1d(tsnom,nominal.interaction.intflux[:,7],kind='slinear')
    FiXUVnom_marsf=interp1d(tsnom,nominal.interaction.intflux[:,8],kind='slinear')

    tsfast=fast.interaction.intflux[:,0]
    FiXUVfast_earthf=interp1d(tsfast,fast.interaction.intflux[:,9],kind='slinear')
    FiXUVfast_venusf=interp1d(tsfast,fast.interaction.intflux[:,7],kind='slinear')
    FiXUVfast_marsf=interp1d(tsfast,fast.interaction.intflux[:,8],kind='slinear')
    
    tsslow=slow.interaction.intflux[:,0]
    FiXUVslow_earthf=interp1d(tsslow,slow.interaction.intflux[:,9],kind='slinear')
    FiXUVslow_venusf=interp1d(tsslow,slow.interaction.intflux[:,7],kind='slinear')
    FiXUVslow_marsf=interp1d(tsslow,slow.interaction.intflux[:,8],kind='slinear')

    #PLOT GLOBAL
    tref=1E-2
    facabs=GYR*PELSI
    ax.fill_between(tsslow,
                    facabs*(FiXUVslow_earthf(tsnom)-FiXUVslow_earthf(tref)),
                    facabs*(FiXUVfast_earthf(tsnom)-FiXUVfast_earthf(tref)),
                    color='b',alpha=0.3)
    ax.plot(tsnom,facabs*(FiXUVnom_earthf(tsnom)-FiXUVnom_earthf(tref)),'b-',label='Earth')

    ax.fill_between(tsslow,
                    facabs*(FiXUVslow_venusf(tsslow)-FiXUVslow_venusf(tref)),
                    facabs*(FiXUVfast_venusf(tsslow)-FiXUVfast_venusf(tref)),
                    color='g',alpha=0.3)
    ax.plot(tsslow,facabs*(FiXUVnom_venusf(tsslow)-FiXUVnom_venusf(tref)),'g-',label='Venus')

    ax.fill_between(tsslow,
                    facabs*(FiXUVslow_marsf(tsslow)-FiXUVslow_marsf(tref)),
                    facabs*(FiXUVfast_marsf(tsslow)-FiXUVfast_marsf(tref)),
                    color='r',alpha=0.3)
    ax.plot(tsslow,facabs*(FiXUVnom_marsf(tsslow)-FiXUVnom_marsf(tref)),'r-',label='Mars')
    logTickLabels(ax,-2,1,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)
    ax.set_xlim((tref,1.0))
    ax.set_ylim((1E12,2E16))
    ax.legend(loc='upper left',prop=dict(size=12))
    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$\Phi_{\rm XUV}(\tau\,;\,\tau_{\rm ini})$=$\int_{;\tau_{\rm ini}}\,F_{\rm XUV}(t)\,dt$   [j/m$^2$]")
    ax.grid(which='both')

    #PLOT SECONDARY
    tref=0.7
    facabs=GYR*PELSI
    axi.fill_between(tsslow,
                    facabs*(FiXUVslow_earthf(tsnom)-FiXUVslow_earthf(tref)),
                    facabs*(FiXUVfast_earthf(tsnom)-FiXUVfast_earthf(tref)),
                    color='b',alpha=0.3)
    axi.plot(tsnom,facabs*(FiXUVnom_earthf(tsnom)-FiXUVnom_earthf(tref)),'b-',label='Earth')

    axi.fill_between(tsslow,
                    facabs*(FiXUVslow_venusf(tsslow)-FiXUVslow_venusf(tref)),
                    facabs*(FiXUVfast_venusf(tsslow)-FiXUVfast_venusf(tref)),
                    color='g',alpha=0.3)
    axi.plot(tsslow,facabs*(FiXUVnom_venusf(tsslow)-FiXUVnom_venusf(tref)),'g-',label='Venus')

    axi.fill_between(tsslow,
                    facabs*(FiXUVslow_marsf(tsslow)-FiXUVslow_marsf(tref)),
                    facabs*(FiXUVfast_marsf(tsslow)-FiXUVfast_marsf(tref)),
                    color='r',alpha=0.3)
    axi.plot(tsslow,facabs*(FiXUVnom_marsf(tsslow)-FiXUVnom_marsf(tref)),'r-',label='Mars')
    logTickLabels(axi,-1,1,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)
    axi.set_xlim((tref,TMAX))
    axi.set_ylim((1E12,2E15))
    axi.set_title(r"$\tau_{\rm ini}=%.2f$ Gyr"%tref,position=(0.5,1.02))

    fig.savefig(DATADIR+"Solar-iXUV-Flux-Sec.png")

    #############################################################
    #PLOT INTEGRATED SW FLUX
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.15,0.1,0.8,0.8])
    axi=fig.add_axes([0.40,0.15,0.52,0.32])
    for axs in ax,axi:
        axs.set_xscale("log")
        axs.set_yscale("log")
    
    tsnom=nominal.interaction.intflux[:,0]
    FiSWnom_earthf=interp1d(tsnom,nominal.interaction.intflux[:,27],kind='slinear')
    FiSWnom_venusf=interp1d(tsnom,nominal.interaction.intflux[:,23],kind='slinear')
    FiSWnom_marsf=interp1d(tsnom,nominal.interaction.intflux[:,25],kind='slinear')

    tsfast=fast.interaction.intflux[:,0]
    FiSWfast_earthf=interp1d(tsfast,fast.interaction.intflux[:,27],kind='slinear')
    FiSWfast_venusf=interp1d(tsfast,fast.interaction.intflux[:,23],kind='slinear')
    FiSWfast_marsf=interp1d(tsfast,fast.interaction.intflux[:,25],kind='slinear')
    
    tsslow=slow.interaction.intflux[:,0]
    FiSWslow_earthf=interp1d(tsslow,slow.interaction.intflux[:,27],kind='slinear')
    FiSWslow_venusf=interp1d(tsslow,slow.interaction.intflux[:,23],kind='slinear')
    FiSWslow_marsf=interp1d(tsslow,slow.interaction.intflux[:,25],kind='slinear')

    #PLOT GLOBAL
    tref=1E-2
    facabs=GYR*SWPEL
    ax.fill_between(tsslow,
                    facabs*(FiSWslow_earthf(tsnom)-FiSWslow_earthf(tref)),
                    facabs*(FiSWfast_earthf(tsnom)-FiSWfast_earthf(tref)),
                    color='b',alpha=0.3)
    ax.plot(tsnom,facabs*(FiSWnom_earthf(tsnom)-FiSWnom_earthf(tref)),'b-',label='Earth')

    ax.fill_between(tsslow,
                    facabs*(FiSWslow_venusf(tsslow)-FiSWslow_venusf(tref)),
                    facabs*(FiSWfast_venusf(tsslow)-FiSWfast_venusf(tref)),
                    color='g',alpha=0.3)
    ax.plot(tsslow,facabs*(FiSWnom_venusf(tsslow)-FiSWnom_venusf(tref)),'g-',label='Venus')

    ax.fill_between(tsslow,
                    facabs*(FiSWslow_marsf(tsslow)-FiSWslow_marsf(tref)),
                    facabs*(FiSWfast_marsf(tsslow)-FiSWfast_marsf(tref)),
                    color='r',alpha=0.3)
    ax.plot(tsslow,facabs*(FiSWnom_marsf(tsslow)-FiSWnom_marsf(tref)),'r-',label='Mars')
    logTickLabels(ax,-2,1,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)
    ax.set_xlim((tref,1.0))
    ax.set_ylim((1E26,1E31))
    ax.legend(loc='upper left',prop=dict(size=12))
    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$\Phi_{\rm SW}(\tau\,;\,\tau_{\rm ini})$=$\int_{\tau_{\rm ini}}\,F_{\rm SW}(t)\,dt$   [part./m$^2$]")
    #ax.set_title(r"$\tau_{\rm ini}=%.2f$ Gyr"%tref,position=(0.5,1.02))
    ax.grid(which='both')

    #PLOT SECONDARY
    tref=0.7
    facabs=GYR*SWPEL
    axi.fill_between(tsslow,
                    facabs*(FiSWslow_earthf(tsnom)-FiSWslow_earthf(tref)),
                    facabs*(FiSWfast_earthf(tsnom)-FiSWfast_earthf(tref)),
                    color='b',alpha=0.3)
    axi.plot(tsnom,facabs*(FiSWnom_earthf(tsnom)-FiSWnom_earthf(tref)),'b-',label='Earth')

    axi.fill_between(tsslow,
                    facabs*(FiSWslow_venusf(tsslow)-FiSWslow_venusf(tref)),
                    facabs*(FiSWfast_venusf(tsslow)-FiSWfast_venusf(tref)),
                    color='g',alpha=0.3)
    axi.plot(tsslow,facabs*(FiSWnom_venusf(tsslow)-FiSWnom_venusf(tref)),'g-',label='Venus')

    axi.fill_between(tsslow,
                    facabs*(FiSWslow_marsf(tsslow)-FiSWslow_marsf(tref)),
                    facabs*(FiSWfast_marsf(tsslow)-FiSWfast_marsf(tref)),
                    color='r',alpha=0.3)
    axi.plot(tsslow,facabs*(FiSWnom_marsf(tsslow)-FiSWnom_marsf(tref)),'r-',label='Mars')
    logTickLabels(axi,-1,1,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)
    axi.set_xlim((tref,TMAX))
    axi.set_ylim((1E28,5E30))
    axi.set_title(r"$\tau_{\rm ini}=%.2f$ Gyr"%tref,position=(0.5,1.02))

    fig.savefig(DATADIR+"Solar-iSW-Flux-Sec.png")

def IntegratedMassLoss():
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

    ###################################################
    #STELLAR WIND EFFECTS
    ###################################################
    #PRIMARY CO_2 RICH ATMOSPHERES
    tini=1E-2
    tend=0.3

    #SECONDARY CO_2 RICH ATMOSPHERES
    #tini=0.7
    #tend=4.5
    
    facabs=GYR*SWPEL

    ts,intflux_slow=interpMatrix(slow.interaction.intflux)
    ts,intflux_nominal=interpMatrix(nominal.interaction.intflux)
    ts,intflux_fast=interpMatrix(fast.interaction.intflux)

    iSW_mars_min=(intflux_slow[25](tend)-intflux_slow[25](tini))*facabs
    iSW_mars_nom=(intflux_nominal[25](tend)-intflux_nominal[25](tini))*facabs
    iSW_mars_max=(intflux_fast[25](tend)-intflux_fast[25](tini))*facabs

    iSW_earth_min=(intflux_slow[27](tend)-intflux_slow[27](tini))*facabs
    iSW_earth_nom=(intflux_nominal[27](tend)-intflux_nominal[27](tini))*facabs
    iSW_earth_max=(intflux_fast[27](tend)-intflux_fast[27](tini))*facabs

    iSW_venus_min=(intflux_slow[23](tend)-intflux_slow[23](tini))*facabs
    iSW_venus_nom=(intflux_nominal[23](tend)-intflux_nominal[23](tini))*facabs
    iSW_venus_max=(intflux_fast[23](tend)-intflux_fast[23](tini))*facabs

    facabs=GYR*PELSI
    iXUV_venus_min=(intflux_slow[7](tend)-intflux_slow[7](tini))*facabs
    iXUV_venus_nom=(intflux_nominal[7](tend)-intflux_nominal[7](tini))*facabs
    iXUV_venus_max=(intflux_fast[7](tend)-intflux_fast[7](tini))*facabs

    iXUV_earth_min=(intflux_slow[9](tend)-intflux_slow[9](tini))*facabs
    iXUV_earth_nom=(intflux_nominal[9](tend)-intflux_nominal[9](tini))*facabs
    iXUV_earth_max=(intflux_fast[9](tend)-intflux_fast[9](tini))*facabs

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
    print "Hydrogen mass-loss Venus:",HMl_venus_min,HMl_venus_max

    #==============================
    #EARTH
    #==============================
    HMl_earth_min=massLossGiant(3.0e3,iXUV_earth_min)/MEARTH
    HMl_earth_max=massLossGiant(3.0e3,iXUV_earth_max)/MEARTH
    print "Hydrogen mass-loss Earth:",HMl_earth_min,HMl_earth_max
    
    #########################################
    #SAVING REFERENCE VALUES
    #########################################
 
def analyseKeplerSystems():
    #SOLAR REFERENCE
    DATADIR=FIGDIR+"CompSolar/"

    #SOLAR REFERENCE
    try:argv[1]
    except:
        print "You should provide a system name."
        exit(1)
    if argv[1]=="KIC-9632895":
        systemid="KIC-9632895";taumin=1.0;taumax=2.5
        planetid="%sb"%systemid
        SWmin_out=1E26;SWmax_out=1E31
        SWmin_in=1E28;SWmax_in=5E30
        XUVmin_out=1E12;XUVmax_out=2E16
        XUVmin_in=1E13;XUVmax_in=2E15
    elif argv[1]=="Kepler-16":
        systemid="Kepler-16";taumin=2.0;taumax=4.0
        planetid="%sb"%systemid
        SWmin_out=1E24;SWmax_out=1E31
        SWmin_in=1E27;SWmax_in=5E30
        XUVmin_out=1E12;XUVmax_out=2E16
        XUVmin_in=1E13;XUVmax_in=2E15
    elif argv[1]=="Kepler-47":
        systemid="Kepler-47";taumin=2.0;taumax=4.0
        planetid="%sc"%systemid
        SWmin_out=1E26;SWmax_out=1E31
        SWmin_in=1E27;SWmax_in=5E30
        XUVmin_out=1E12;XUVmax_out=2E16
        XUVmin_in=1E13;XUVmax_in=2E15
    else:
        print "No valid system provided."
        exit(1)

    fast=loadResults(DATADIR+"fast/")
    nominal=loadResults(DATADIR+"nominal/")
    slow=loadResults(DATADIR+"slow/")

    DATADIR=FIGDIR+"Systems/"+systemid+"/"
    system=loadResults(DATADIR)

    ###################################################
    # COMPARE SW FLUXES
    ###################################################
    tsslow=slow.interaction.lumflux[:,0]
    FSWslow_mars=slow.interaction.lumflux[:,33]
    FSWfast_mars=fast.interaction.lumflux[:,33]
    FSWslow_venus=slow.interaction.lumflux[:,31]
    FSWfast_venus=fast.interaction.lumflux[:,31]
    FSWslow_earth=slow.interaction.lumflux[:,35]
    FSWfast_earth=fast.interaction.lumflux[:,35]
    FSWnom_earth=nominal.interaction.lumflux[:,35]
    FSWnom_venus=nominal.interaction.lumflux[:,31]
    FSWnom_mars=nominal.interaction.lumflux[:,33]

    ts=system.interaction.lumflux[:,0]
    FSW=system.interaction.lumflux[:,23]
    FSWin=system.interaction.lumflux[:,19]
    FSWout=system.interaction.lumflux[:,21]

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    ax.plot(tsslow,FSWnom_mars,color='r',linewidth=2)
    ax.fill_between(tsslow,FSWslow_mars,FSWfast_mars,color='r',alpha=0.2,zorder=10)

    ax.plot(tsslow,FSWnom_earth,color='b',linewidth=2)
    ax.fill_between(tsslow,FSWslow_earth,FSWfast_earth,color='b',alpha=0.2,zorder=10)

    ax.plot(tsslow,FSWnom_venus,color='g',linewidth=2)
    ax.fill_between(tsslow,FSWslow_venus,FSWfast_venus,color='g',alpha=0.2,zorder=10)

    ax.plot(ts,FSW,color='k',linewidth=5,label='%s'%planetid)
    ax.fill_between(ts,FSWin,FSWout,color='k',alpha=0.3)

    ax.plot([],[],linewidth=10,color='k',alpha=0.3,label='%s BHZ'%systemid)
    ax.plot([],[],linewidth=10,color='r',alpha=0.3,label='Mars Reference')
    ax.plot([],[],linewidth=10,color='b',alpha=0.3,label='Earth Reference')
    ax.plot([],[],linewidth=10,color='g',alpha=0.3,label='Venus Reference')

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim((1E-2,5.0))
    ax.axvspan(taumin,taumax,color='k',alpha=0.2)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$F_{\rm SW}$ (PEL)")
    ax.grid(which='both')

    ax.legend(loc='lower left')
    fig.savefig(FIGDIR+"Kepler-SW-%s.png"%systemid)

    ###################################################
    # COMPARE XUV FLUXES
    ###################################################
    tsslow=slow.interaction.lumflux[:,0]
    FXUVslow_mars=slow.interaction.lumflux[:,16]
    FXUVfast_mars=fast.interaction.lumflux[:,16]
    FXUVnom_mars=nominal.interaction.lumflux[:,16]

    FXUVslow_earth=slow.interaction.lumflux[:,17]
    FXUVfast_earth=fast.interaction.lumflux[:,17]
    FXUVnom_earth=nominal.interaction.lumflux[:,17]

    FXUVslow_venus=slow.interaction.lumflux[:,15]
    FXUVfast_venus=fast.interaction.lumflux[:,15]
    FXUVnom_venus=nominal.interaction.lumflux[:,15]

    ts=system.interaction.lumflux[:,0]
    FXUV=system.interaction.lumflux[:,11]
    FXUVin=system.interaction.lumflux[:,9]
    FXUVout=system.interaction.lumflux[:,10]

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    ax.plot(tsslow,FXUVnom_mars,color='r',linewidth=2)
    ax.fill_between(tsslow,FXUVslow_mars,FXUVfast_mars,color='r',alpha=0.2,zorder=10)

    ax.plot(tsslow,FXUVnom_earth,color='b',linewidth=2)
    ax.fill_between(tsslow,FXUVslow_earth,FXUVfast_earth,color='b',alpha=0.2,zorder=10)

    ax.plot(tsslow,FXUVnom_venus,color='g',linewidth=2)
    ax.fill_between(tsslow,FXUVslow_venus,FXUVfast_venus,color='g',alpha=0.2,zorder=10)

    ax.plot(ts,FXUV,color='k',linewidth=5,label='%s'%planetid)
    ax.fill_between(ts,FXUVin,FXUVout,color='k',alpha=0.3)

    ax.plot([],[],linewidth=10,color='k',alpha=0.3,label='%s BHZ'%systemid)
    ax.plot([],[],linewidth=10,color='r',alpha=0.3,label='Mars Reference')
    ax.plot([],[],linewidth=10,color='b',alpha=0.3,label='Earth Reference')
    ax.plot([],[],linewidth=10,color='g',alpha=0.3,label='Venus Reference')

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim((1E-2,5.0))
    ax.axvspan(taumin,taumax,color='k',alpha=0.2)

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$F_{\rm XUV}$ (PEL)")
    ax.grid(which='both')

    ax.legend(loc='lower left',prop=dict(size=10))
    fig.savefig(FIGDIR+"Kepler-XUV-%s.png"%systemid)

    ###################################################
    # COMPARE INTEGRATED SW FLUXES
    ###################################################
    tini=1E-2
    tmax=1.0
    facabs=GYR*SWPEL

    tsslow=slow.interaction.intflux[:,0]
    FiSWslow_marsf=interp1d(tsslow,slow.interaction.intflux[:,25],kind='slinear')
    FiSWfast_marsf=interp1d(tsslow,fast.interaction.intflux[:,25],kind='slinear')
    FiSWnom_marsf=interp1d(tsslow,nominal.interaction.intflux[:,25],kind='slinear')

    FiSWslow_venusf=interp1d(tsslow,slow.interaction.intflux[:,23],kind='slinear')
    FiSWfast_venusf=interp1d(tsslow,fast.interaction.intflux[:,23],kind='slinear')
    FiSWnom_venusf=interp1d(tsslow,nominal.interaction.intflux[:,23],kind='slinear')

    FiSWslow_earthf=interp1d(tsslow,slow.interaction.intflux[:,27],kind='slinear')
    FiSWfast_earthf=interp1d(tsslow,fast.interaction.intflux[:,27],kind='slinear')
    FiSWnom_earthf=interp1d(tsslow,nominal.interaction.intflux[:,27],kind='slinear')

    ts=system.interaction.intflux[:,0]
    FiSWf=interp1d(ts,system.interaction.intflux[:,15],kind='slinear')
    FiSWinf=interp1d(ts,system.interaction.intflux[:,11],kind='slinear')
    FiSWoutf=interp1d(ts,system.interaction.intflux[:,13],kind='slinear')

    fig=plt.figure()
    ax=fig.add_axes([0.12,0.1,0.8,0.8])
    axi=fig.add_axes([0.37,0.15,0.52,0.32])
    for axs in ax,axi:
        axs.set_xscale("log")
        axs.set_yscale("log")
    
    ax.plot(tsslow,facabs*(FiSWnom_marsf(tsslow)-FiSWnom_marsf(tini)),color='r',linewidth=2,zorder=10)
    ax.fill_between(tsslow,facabs*(FiSWslow_marsf(tsslow)-FiSWslow_marsf(tini)),facabs*(FiSWfast_marsf(tsslow)-FiSWfast_marsf(tini)),color='r',alpha=0.2,zorder=10)

    ax.plot(tsslow,facabs*(FiSWnom_earthf(tsslow)-FiSWnom_earthf(tini)),color='b',linewidth=2,zorder=10)
    ax.fill_between(tsslow,facabs*(FiSWslow_earthf(tsslow)-FiSWslow_earthf(tini)),facabs*(FiSWfast_earthf(tsslow)-FiSWfast_earthf(tini)),color='b',alpha=0.2,zorder=10)
    
    ax.plot(tsslow,facabs*(FiSWnom_venusf(tsslow)-FiSWnom_venusf(tini)),color='g',linewidth=2,zorder=10)
    ax.fill_between(tsslow,facabs*(FiSWslow_venusf(tsslow)-FiSWslow_venusf(tini)),facabs*(FiSWfast_venusf(tsslow)-FiSWfast_venusf(tini)),color='g',alpha=0.2,zorder=10)
    
    ax.plot(ts,facabs*(FiSWf(ts)-FiSWf(tini)),color='k',linewidth=5,label='%s'%planetid)
    ax.fill_between(ts,facabs*(FiSWinf(ts)-FiSWinf(tini)),facabs*(FiSWoutf(ts)-FiSWoutf(tini)),color='k',alpha=0.5)

    ax.plot([],[],linewidth=10,color='k',alpha=0.3,label='%s BHZ'%systemid)
    ax.plot([],[],linewidth=10,color='r',alpha=0.3,label='Mars Reference')
    ax.plot([],[],linewidth=10,color='b',alpha=0.3,label='Earth Reference')
    ax.plot([],[],linewidth=10,color='g',alpha=0.3,label='Venus Reference')

    ax.set_xlim((tini,tmax))
    ax.set_ylim((SWmin_out,SWmax_out))
    ax.grid(which="both")
    logTickLabels(ax,-2,0,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)
    
    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$\Phi_{\rm SW}(\tau\,;\,\tau_{\rm ini})$ [part./m$^2$]")

    ax.legend(loc='upper left',prop=dict(size=10))

    tini=0.7
    tmax=5.0

    axi.plot(tsslow,facabs*(FiSWnom_marsf(tsslow)-FiSWnom_marsf(tini)),color='r',linewidth=1,zorder=10)
    axi.fill_between(tsslow,facabs*(FiSWslow_marsf(tsslow)-FiSWslow_marsf(tini)),facabs*(FiSWfast_marsf(tsslow)-FiSWfast_marsf(tini)),color='r',alpha=0.2,zorder=10)

    axi.plot(tsslow,facabs*(FiSWnom_earthf(tsslow)-FiSWnom_earthf(tini)),color='b',linewidth=1,zorder=10)
    axi.fill_between(tsslow,facabs*(FiSWslow_earthf(tsslow)-FiSWslow_earthf(tini)),facabs*(FiSWfast_earthf(tsslow)-FiSWfast_earthf(tini)),color='b',alpha=0.2,zorder=10)
    
    axi.plot(tsslow,facabs*(FiSWnom_venusf(tsslow)-FiSWnom_venusf(tini)),color='g',linewidth=1,zorder=10)
    axi.fill_between(tsslow,facabs*(FiSWslow_venusf(tsslow)-FiSWslow_venusf(tini)),facabs*(FiSWfast_venusf(tsslow)-FiSWfast_venusf(tini)),color='g',alpha=0.2,zorder=10)
    
    axi.plot(ts,facabs*(FiSWf(ts)-FiSWf(tini)),color='k',linewidth=2,label='%s'%planetid)
    axi.fill_between(ts,facabs*(FiSWinf(ts)-FiSWinf(tini)),facabs*(FiSWoutf(ts)-FiSWoutf(tini)),color='k',alpha=0.5)
    axi.axvspan(taumin,taumax,color='k',alpha=0.2)

    logTickLabels(axi,-1,1,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)

    axi.set_xlim((tini,tmax))
    axi.set_ylim((SWmin_in,SWmax_in))
    axi.set_title(r"$\tau_{\rm ini}=%.2f$ Gyr"%tini,position=(0.5,1.02))

    fig.savefig(FIGDIR+"Kepler-iSW-%s.png"%systemid)

    ###################################################
    # COMPARE INTEGRATED XUV FLUXES
    ###################################################
    tini=1E-2
    tmax=1.0
    facabs=GYR*PELSI

    tsslow=slow.interaction.intflux[:,0]
    FiXUVslow_marsf=interp1d(tsslow,slow.interaction.intflux[:,8],kind='slinear')
    FiXUVfast_marsf=interp1d(tsslow,fast.interaction.intflux[:,8],kind='slinear')
    FiXUVnom_marsf=interp1d(tsslow,nominal.interaction.intflux[:,8],kind='slinear')

    FiXUVslow_venusf=interp1d(tsslow,slow.interaction.intflux[:,7],kind='slinear')
    FiXUVfast_venusf=interp1d(tsslow,fast.interaction.intflux[:,7],kind='slinear')
    FiXUVnom_venusf=interp1d(tsslow,nominal.interaction.intflux[:,7],kind='slinear')

    FiXUVslow_earthf=interp1d(tsslow,slow.interaction.intflux[:,9],kind='slinear')
    FiXUVfast_earthf=interp1d(tsslow,fast.interaction.intflux[:,9],kind='slinear')
    FiXUVnom_earthf=interp1d(tsslow,nominal.interaction.intflux[:,9],kind='slinear')

    ts=system.interaction.intflux[:,0]
    FiXUVf=interp1d(ts,system.interaction.intflux[:,3],kind='slinear')
    FiXUVinf=interp1d(ts,system.interaction.intflux[:,1],kind='slinear')
    FiXUVoutf=interp1d(ts,system.interaction.intflux[:,2],kind='slinear')

    fig=plt.figure()
    ax=fig.add_axes([0.12,0.1,0.8,0.8])
    axi=fig.add_axes([0.37,0.15,0.52,0.32])
    for axs in ax,axi:
        axs.set_xscale("log")
        axs.set_yscale("log")
    
    ax.plot(tsslow,facabs*(FiXUVnom_marsf(tsslow)-FiXUVnom_marsf(tini)),color='r',linewidth=2,zorder=10)
    ax.fill_between(tsslow,facabs*(FiXUVslow_marsf(tsslow)-FiXUVslow_marsf(tini)),facabs*(FiXUVfast_marsf(tsslow)-FiXUVfast_marsf(tini)),color='r',alpha=0.2,zorder=10)

    ax.plot(tsslow,facabs*(FiXUVnom_earthf(tsslow)-FiXUVnom_earthf(tini)),color='b',linewidth=2,zorder=10)
    ax.fill_between(tsslow,facabs*(FiXUVslow_earthf(tsslow)-FiXUVslow_earthf(tini)),facabs*(FiXUVfast_earthf(tsslow)-FiXUVfast_earthf(tini)),color='b',alpha=0.2,zorder=10)
    
    ax.plot(tsslow,facabs*(FiXUVnom_venusf(tsslow)-FiXUVnom_venusf(tini)),color='g',linewidth=2,zorder=10)
    ax.fill_between(tsslow,facabs*(FiXUVslow_venusf(tsslow)-FiXUVslow_venusf(tini)),facabs*(FiXUVfast_venusf(tsslow)-FiXUVfast_venusf(tini)),color='g',alpha=0.2,zorder=10)
    
    ax.plot(ts,facabs*(FiXUVf(ts)-FiXUVf(tini)),color='k',linewidth=5,label='%s'%planetid)
    ax.fill_between(ts,facabs*(FiXUVinf(ts)-FiXUVinf(tini)),facabs*(FiXUVoutf(ts)-FiXUVoutf(tini)),color='k',alpha=0.5)

    ax.plot([],[],linewidth=10,color='k',alpha=0.3,label='%s BHZ'%systemid)
    ax.plot([],[],linewidth=10,color='r',alpha=0.3,label='Mars Reference')
    ax.plot([],[],linewidth=10,color='b',alpha=0.3,label='Earth Reference')
    ax.plot([],[],linewidth=10,color='g',alpha=0.3,label='Venus Reference')

    ax.set_xlim((tini,tmax))
    ax.set_ylim((XUVmin_out,XUVmax_out))
    ax.grid(which="both")
    logTickLabels(ax,-2,0,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)
    
    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel(r"$\Phi_{\rm XUV}(\tau\,;\,\tau_{\rm ini})$ [part./m$^2$]")

    ax.legend(loc='upper left',prop=dict(size=10))

    tini=0.7
    tmax=5.0

    axi.plot(tsslow,facabs*(FiXUVnom_marsf(tsslow)-FiXUVnom_marsf(tini)),color='r',linewidth=1,zorder=10)
    axi.fill_between(tsslow,facabs*(FiXUVslow_marsf(tsslow)-FiXUVslow_marsf(tini)),facabs*(FiXUVfast_marsf(tsslow)-FiXUVfast_marsf(tini)),color='r',alpha=0.2,zorder=10)

    axi.plot(tsslow,facabs*(FiXUVnom_earthf(tsslow)-FiXUVnom_earthf(tini)),color='b',linewidth=1,zorder=10)
    axi.fill_between(tsslow,facabs*(FiXUVslow_earthf(tsslow)-FiXUVslow_earthf(tini)),facabs*(FiXUVfast_earthf(tsslow)-FiXUVfast_earthf(tini)),color='b',alpha=0.2,zorder=10)
    
    axi.plot(tsslow,facabs*(FiXUVnom_venusf(tsslow)-FiXUVnom_venusf(tini)),color='g',linewidth=1,zorder=10)
    axi.fill_between(tsslow,facabs*(FiXUVslow_venusf(tsslow)-FiXUVslow_venusf(tini)),facabs*(FiXUVfast_venusf(tsslow)-FiXUVfast_venusf(tini)),color='g',alpha=0.2,zorder=10)
    
    axi.plot(ts,facabs*(FiXUVf(ts)-FiXUVf(tini)),color='k',linewidth=2,label='%s'%planetid)
    axi.fill_between(ts,facabs*(FiXUVinf(ts)-FiXUVinf(tini)),facabs*(FiXUVoutf(ts)-FiXUVoutf(tini)),color='k',alpha=0.5)
    axi.axvspan(taumin,taumax,color='k',alpha=0.2)

    logTickLabels(axi,-1,1,(1,),frm="%.2f",axis='x',notation='sci',fontsize=10)

    axi.set_xlim((tini,tmax))
    axi.set_ylim((XUVmin_in,XUVmax_in))
    axi.set_title(r"$\tau_{\rm ini}=%.2f$ Gyr"%tini,position=(0.5,1.02))

    fig.savefig(FIGDIR+"Kepler-iXUV-%s.png"%systemid)

    exit(0)
    
#CompareLuminositiesMassLoss()
#IntegratedReferenceFluxes()
#IntegratedMassLoss()
#analyseKeplerSystems()
#IntegratedReferenceFluxesTini()

#################################################################################
# BHM CALCULATOR PAPER
#################################################################################
def plotAllMoIs():
    #Msvec=np.arange(0.2,1.25,0.10)
    Msvec=np.arange(0.2,1.25,0.40)
    Msvec=np.concatenate((Msvec,np.arange(0.15,1.25,0.40),[1.2]))
    Msvec.sort()

    Msvec=np.array([0.15,0.3,0.45,0.6,0.75,0.9,1.15])

    figk2=plt.figure()
    ax_k2=figk2.add_axes([0.12,0.12,0.8,0.8])

    figMoI=plt.figure()
    ax_MoI=figMoI.add_axes([0.1,0.1,0.8,0.8])

    figRad=plt.figure()
    ax_Rad=figRad.add_axes([0.1,0.1,0.8,0.8])

    for M in Msvec:
        data=interpolMoI(M,verbose=True)

        #CONVECTIVE
        line,=ax_MoI.plot(data[:,0],data[:,2],'-',label="M=%.2f"%M)
        color=plt.getp(line,'color')

        #RADIATIVE
        ax_MoI.plot(data[:,0],data[:,3],'--',color=color)

        #TOTAL
        ax_MoI.plot(data[:,0],data[:,4],'-',color=color,linewidth=4,alpha=0.3,zorder=-10)

        #K2
        ax_k2.plot(data[:,0],data[:,8],'-',color=color,label="M=%.2f"%M)
        #ax_k2.plot(data[:,0],data[:,11],'-',color=color,linewidth=5,alpha=0.3,zorder=-5)

        #K2
        ax_k2.plot(data[:,0],data[:,9],'--',color=color)
        ax_k2.plot(data[:,0],data[:,10],'-.',color=color)

        #RAD
        ax_Rad.plot(data[:,0],data[:,14],'-',color=color,label="M=%.2f"%M)
        ax_Rad.plot(data[:,0],data[:,15],'--',color=color)

    logtmin=6.0;logtmax=10.0

    ax_MoI.plot([],[],'--',color='k',label="Radiative")
    ax_MoI.plot([],[],'-',color='k',label="Convective")
    ax_MoI.plot([],[],'-',color='k',linewidth=4,alpha=0.3,label="Total")
    ax_MoI.legend(loc="best",ncol=3,prop=dict(size=10))
    ax_MoI.set_ylim((50.5,56.0))
    ax_MoI.set_xlim((logtmin,logtmax))
    ax_MoI.grid(which='both')

    ax_k2.plot([],[],'-.',color='k',label="Radiative")
    ax_k2.plot([],[],'--',color='k',label="Convective")
    ax_k2.plot([],[],'-',color='k',linewidth=4,alpha=0.3,label="Total")
    ax_k2.legend(loc="lower left",ncol=1,prop=dict(size=10))
    #ax_k2.grid(which='both')
    ax_k2.set_ylabel(r"$k^2$")
    ax_k2.set_xlabel(r"$\log\,\tau$ (yr)")
    ax_k2.set_xlim((logtmin,logtmax))

    ax_Rad.plot([],[],'-',color='k',label=r"$R_{\rm rad}$ ($R_\odot$)")
    ax_Rad.plot([],[],'--',color='k',label=r"$M_{\rm rad}$ ($M_\odot$)")
    ax_Rad.legend(loc="best",ncol=3,prop=dict(size=10))
    ax_Rad.grid(which='both')
    ax_Rad.set_ylabel(r"$R_{\rm rad}$, $M_{\rm rad}$")
    ax_Rad.set_xlim((logtmin,logtmax))

    figk2.savefig("figures/MoI-all-k2.png")
    figMoI.savefig("figures/MoI-all-MoIs.png")
    figRad.savefig("figures/MoI-all-Rad.png")

def compareMoIs():
    figMoI=plt.figure()
    ax_MoI=figMoI.add_axes([0.1,0.1,0.8,0.8])

    M=1.1

    ###################################################
    #PARSEC, Z=0.015
    ###################################################
    model="PARSEC"
    Z=0.015

    #INERTIA MOMENT MODEL
    dataMoI=interpolMoI(M,verbose=True)
    logtmoi,MoIfunc=interpMatrix(dataMoI)

    #EVOLUTIONARY TRACK
    pfind,startrack=findTrack(model,Z,M,verbose=True)
    evoFunc=trackFunctions(startrack)

    tmin=evoFunc.R.x[0]
    tmax=evoFunc.R.x[-1]
    logtmoi=logtmoi[(logtmoi>np.log10(tmin))*(logtmoi<np.log10(tmax))]

    Ievo=stack(4)
    for logt in logtmoi:
        t=10**logt

        #BULK MOI
        logMR2=np.log10((M*MSUN*1E3)*(evoFunc.R(t)*RSUN*1E2)**2)

        #TOTAL K2 AND MOI
        k2=MoIfunc[8](logt)
        logk2=np.log10(k2)
        logItot=logk2+logMR2

        #CONVECTIVE K2 AND MOI
        kconv2=MoIfunc[9](logt)
        logkconv2=np.log10(kconv2)
        logIconv=logkconv2+logMR2

        #RADIATIVE K2 AND MOI
        krad2=MoIfunc[10](logt)
        Irad=krad2*10**logMR2

        Ievo+=[logt,logItot,logIconv,np.log10(Irad)]

    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,1],'k-',label='PARSEC, $Z=0.015$')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,2],'k--')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,3],'k:')

    ###################################################
    #PARSEC, Z=0.005
    ###################################################
    model="PARSEC"
    Z=0.005

    #INERTIA MOMENT MODEL
    dataMoI=interpolMoI(M,verbose=True)
    logtmoi,MoIfunc=interpMatrix(dataMoI)

    #EVOLUTIONARY TRACK
    pfind,startrack=findTrack(model,Z,M,verbose=True)
    evoFunc=trackFunctions(startrack)

    tmin=evoFunc.R.x[0]
    tmax=evoFunc.R.x[-1]
    logtmoi=logtmoi[(logtmoi>np.log10(tmin))*(logtmoi<np.log10(tmax))]

    Ievo=stack(4)
    for logt in logtmoi:
        t=10**logt

        #BULK MOI
        logMR2=np.log10((M*MSUN*1E3)*(evoFunc.R(t)*RSUN*1E2)**2)

        #TOTAL K2 AND MOI
        k2=MoIfunc[8](logt)
        logk2=np.log10(k2)
        logItot=logk2+logMR2

        #CONVECTIVE K2 AND MOI
        kconv2=MoIfunc[9](logt)
        logkconv2=np.log10(kconv2)
        logIconv=logkconv2+logMR2

        #RADIATIVE K2 AND MOI
        krad2=MoIfunc[10](logt)
        Irad=krad2*10**logMR2

        Ievo+=[logt,logItot,logIconv,np.log10(Irad)]

    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,1],'b-',label='PARSEC, $Z=0.005$')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,2],'b--')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,3],'b:')

    ###################################################
    #BCA98, Z=0.015
    ###################################################
    model="BCA98"
    Z=0.015

    #INERTIA MOMENT MODEL
    dataMoI=interpolMoI(M,verbose=True)
    logtmoi,MoIfunc=interpMatrix(dataMoI)

    #EVOLUTIONARY TRACK
    pfind,startrack=findTrack(model,Z,M,verbose=True)
    evoFunc=trackFunctions(startrack)

    tmin=evoFunc.R.x[0]
    tmax=evoFunc.R.x[-1]
    logtmoi=logtmoi[(logtmoi>np.log10(tmin))*(logtmoi<np.log10(tmax))]

    Ievo=stack(4)
    for logt in logtmoi:
        t=10**logt

        #BULK MOI
        logMR2=np.log10((M*MSUN*1E3)*(evoFunc.R(t)*RSUN*1E2)**2)

        #TOTAL K2 AND MOI
        k2=MoIfunc[8](logt)
        logk2=np.log10(k2)
        logItot=logk2+logMR2

        #CONVECTIVE K2 AND MOI
        kconv2=MoIfunc[9](logt)
        logkconv2=np.log10(kconv2)
        logIconv=logkconv2+logMR2

        #RADIATIVE K2 AND MOI
        krad2=MoIfunc[10](logt)
        Irad=krad2*10**logMR2

        Ievo+=[logt,logItot,logIconv,np.log10(Irad)]

    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,1],'g-',label='BCA98, $Z=0.015$')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,2],'g--')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,3],'g:')

    ###################################################
    #BCA98, Z=0.005
    ###################################################
    model="BCA98"
    Z=0.005

    #INERTIA MOMENT MODEL
    dataMoI=interpolMoI(M,verbose=True)
    logtmoi,MoIfunc=interpMatrix(dataMoI)

    #EVOLUTIONARY TRACK
    pfind,startrack=findTrack(model,Z,M,verbose=True)
    evoFunc=trackFunctions(startrack)

    tmin=evoFunc.R.x[0]
    tmax=evoFunc.R.x[-1]
    logtmoi=logtmoi[(logtmoi>np.log10(tmin))*(logtmoi<np.log10(tmax))]

    Ievo=stack(4)
    for logt in logtmoi:
        t=10**logt

        #BULK MOI
        logMR2=np.log10((M*MSUN*1E3)*(evoFunc.R(t)*RSUN*1E2)**2)

        #TOTAL K2 AND MOI
        k2=MoIfunc[8](logt)
        logk2=np.log10(k2)
        logItot=logk2+logMR2

        #CONVECTIVE K2 AND MOI
        kconv2=MoIfunc[9](logt)
        logkconv2=np.log10(kconv2)
        logIconv=logkconv2+logMR2

        #RADIATIVE K2 AND MOI
        krad2=MoIfunc[10](logt)
        Irad=krad2*10**logMR2

        Ievo+=[logt,logItot,logIconv,np.log10(Irad)]

    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,1],'c-',label='BCA98, $Z=0.005$')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,2],'c--')
    ax_MoI.plot(Ievo.array[:,0],Ievo.array[:,3],'c:')

    logtmin=6.0;logtmax=9.0
    ax_MoI.legend(loc="best",ncol=1,prop=dict(size=10))
    ax_MoI.set_ylim((50.5,56.0))
    ax_MoI.set_xlim((logtmin,logtmax))
    ax_MoI.set_xlabel(r"$\log\,\tau$ (yr)")
    ax_MoI.set_ylabel(r"$\log\,I$ (kg m$^{-2}$)")
    #ax_MoI.grid(which='both')

    figMoI.savefig("figures/MoI-compared.png")

def evolutionaryTracks():

    #LOAD CATALOGUE
    fpickle="BHM/data/BHMcat/BHMcat.pickle"
    fl=open(fpickle,'r')
    systems=pickle.load(fl)
    fl.close()

    ###############################
    #SYSTEM: 
    ###############################
    #SUN
    #"""
    M=1.0
    Tobs=TSUN
    Terr=0.0
    Robs=1.0
    Rerr=0.0
    Tomax=7000;Tomin=4000
    Romin=-1;Romax=10.0
    #"""

    #KEPLER-16A
    """
    M=0.7
    Tobs=4337
    Terr=80.0
    Robs=0.649
    Rerr=0.001
    Tomax=6000;Tomin=3500
    Romin=-1;Romax=10.0
    #"""
    
    #############################################################
    #HR TRACK
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    Tarr=[]
    Rarr=[]

    colors=['r','k','b','c']
    styles=['-','--',':']
    
    models=dict(
        PARSEC=[0.017,0.004,0.03],
        YZVAR=[0.017,0.004,0.04],
        BASTI=[0.01,0.004,0.04],
        BCA98=[0.015,0.005])

    mkeys=models.keys()
    mkeys=["BCA98","PARSEC","BASTI","YZVAR"]
    #mkeys=["BCA98"]
    
    j=0
    for model in mkeys:
        i=0
        print "Model: %s"%model
        for Z in models[model][0:2]:
            k=i%3
            print "Plotting track for Z = %.4f, M = %.2f..."%(Z,M)
            track_finds,track_data=findTracks(model,Z,M,verbose=False)
            Zi=track_finds[1][0]
            track=trackArrays(track_data[1])
            
            ts=track.ts/GIGA
            tmin=ts[0]
            tmax=ts[-1]
            print "tmin,tmax = ",tmin,tmax

            Ts=track.T
            Rs=track.R
            
            #cond=(ts<4.56)
            cond=(ts<20.0)
            ts=ts[cond]
            Ts=Ts[cond]
            Rs=Rs[cond]
            
            Tarr+=[Ts]
            Rarr+=[Rs]
            
            style=dict(color=colors[j],markersize=5,markeredgecolor='none')

            ax.plot(Ts,Rs,color=colors[j],linestyle=styles[k],label='%s, Z=%.4f'%(model,Z))
            ax.plot([Ts[0]],[Rs[0]],'s',**style)
            ax.plot([Ts[-1]],[Rs[-1]],'o',**style)
            i+=1

        j+=1
    
    Tmin,Tmax=minmaxArrays(Tarr)
    Rmin,Rmax=minmaxArrays(Rarr)

    fac=1.1
    
    ax.text(Tobs,Robs,r"$\star$",color='g',
            fontsize=25,horizontalalignment='center',verticalalignment='center')

    ax.axvspan(Tobs-Terr,Tobs+Terr,color='g',alpha=0.3)
    ax.axvline(Tobs,color='g')

    ax.axhspan(Robs-Rerr,Robs+Rerr,color='g',alpha=0.3)
    ax.axhline(Robs,color='g')

    if Tomin<0:Tmin=1/fac*Tmin
    else:Tmin=Tomin

    if Tomax<0:Tmax=fac*Tmax
    else:Tmax=Tomax

    if Romin<0:Rmin=1/fac*Rmin
    else:Rmin=Romin

    if Romax<0:Rmax=fac*Rmax
    else:Rmax=Romax
    
    ax.set_yscale("log")

    logTickLabels(ax,-1,1,(2,1),frm="%.1f",axis='y',notation='normal',fontsize=12)

    ax.set_xlim((Tmax,Tmin))
    ax.set_ylim((Rmin,Rmax))

    ax.set_xlabel(r"$T_{\rm eff}$ (K)",fontsize=14)
    ax.set_ylabel("$R/R_\odot$",fontsize=14)
    
    ax.set_title("$M = %.1f\,M_\odot$"%(M),
                 position=(0.5,1.02),fontsize=14)

    #ax.grid(which='both')
    ax.legend(loc='best',prop=dict(size=10))

    fmodel="figures/EvoTrack-M_%.2f.png"%M
    print "Saving file %s..."%fmodel
    fig.savefig(fmodel)
    
def massRadiusSolid():
    
    qsave=True

    fig=plt.figure()
    ax=fig.add_axes([0.12,0.1,0.8,0.8])

    dirplgrid=DATA_DIR+"SolidPlanets/MobileLids"
    loadSolidPlanetsGrid(dirplgrid,verbose=False)

    NC=30
    NM=10

    CMFs=np.linspace(0.1,0.8,NC)
    Ms=np.linspace(1.0,7.0,NM)
    
    CM,MSS=np.meshgrid(CMFs,Ms)
    RMS=np.zeros_like(CM)
    i=0
    colmap=cm.rainbow
    for CMF in CMFs:
        print "Mass-radius relationship for CMF = %.2f"%CMF
        Rs=[]
        j=0
        for M in Ms:
            print "\tM = %.2f"%M
            pcell=loadPlanetCell(Mp=M,CMF=CMF,IMF=0.0,dirplgrid=dirplgrid,verbose=False)
            R=planetProperty(pcell,"Radius",
                             data="struct")
            Rs+=[R]
            RMS[j,i]=R
            j+=1
            del(pcell)
        color=colmap((CMF-CMFs[0])/(CMFs[-1]-CMFs[0]))
        if i==0 or i==NC-1:
            label="CMF %.1f"%CMF
        else:label=""
        ax.plot(Ms,Rs,label=label,color=color)
        i+=1

    #EARTH COMPOSITION
    Rs=[]
    for M in Ms:
        pcell=loadPlanetCell(Mp=M,CMF=0.34,IMF=0.0,dirplgrid=dirplgrid,verbose=False)
        R=planetProperty(pcell,"Radius",
                         data="struct")
        Rs+=[R]
    ax.plot(Ms,Rs,label="Earth Composition",color='k',linewidth=2,zorder=10)

    if qsave:
        np.savetxt("figures/CM-solid.dat",CM)
        np.savetxt("figures/MS-solid.dat",MSS)
        np.savetxt("figures/RM-solid.dat",RMS)

    #SUPER EARTHS
    for planet in SuperEarths.keys():
        Mp=SuperEarths[planet]["Mp"]
        Mperr1=SuperEarths[planet]["Mperr1"]
        Mperr2=SuperEarths[planet]["Mperr2"]
        Rp=SuperEarths[planet]["Rp"]
        Rperr1=SuperEarths[planet]["Rperr1"]
        Rperr2=SuperEarths[planet]["Rperr2"]
        line,=ax.plot([Mp],[Rp],'o',markersize=5,markeredgecolor='none')
        color=plt.getp(line,"color")
        ax.errorbar(Mp,Rp,xerr=(Mperr2-Mperr1)/2,yerr=(Rperr2-Rperr1)/2,color=color,zorder=1000)
        planetn=planet.replace("_","-")
        ax.text(Mp,Rp,planetn,
                horizontalalignment='left',verticalalignment='top',fontsize=10,
                transform=offSet(5,-5))

    ax.legend(loc="upper left",prop=dict(size=10))
    ax.set_xlabel(r"$M_{\rm p}$ ($M_\oplus$)",fontsize=14)
    ax.set_ylabel(r"$R_{\rm p}$ ($M_\oplus$)",fontsize=14)
    ax.set_xlim((1.0,7.0))
    fig.savefig("figures/RM-Solid.png")

def massRadiusSolidContours():
    
    figc=plt.figure()
    axc=figc.add_axes([0.1,0.1,0.85,0.8])

    CM=np.loadtxt("figures/CM-solid.dat")
    MS=np.loadtxt("figures/MS-solid.dat")
    RM=np.loadtxt("figures/RM-solid.dat")

    Rmin=0.8
    Rmax=1.8

    #CONTOUR
    cont=axc.contourf(MS,CM,RM,levels=np.linspace(Rmin,Rmax,1000.0),cmap=cm.spectral)
    cbar=plt.colorbar(cont)
    cbar.ax.set_ylabel(r"$R_{\rm p}$ ($R_\oplus$)",fontsize=14)
    xts=cbar.ax.get_yticks()
    xls=[]
    levels=[]
    for xt in xts:
        rs=xt*(Rmax-Rmin)+Rmin
        levels+=[rs]
        xls+=["%.2f"%(rs)]
    cbar.ax.set_yticklabels(xls)
    cont=axc.contour(MS,CM,RM,levels=levels,
                     colors=['k']*len(levels),linestyles=[':']*len(levels),linewidth=2)

    planets=[]
    planets+=['Kepler_10b']
    planets+=['Kepler_36b']
    ##planets+=['Kepler_57c']
    ##planets+=['Kepler_68c']
    planets+=['Kepler_78b']
    ##planets+=['Kepler_93b']
    ##planets+=['Kepler_97b']
    planets+=['Kepler_99b']
    ##planets+=['Kepler_100b']
    ##planets+=['Kepler_102b']
    ##planets+=['Kepler_406b']
    for planet in planets:
        print "Planet ",planet
        Mp=SuperEarths[planet]["Mp"]
        Mperr1=SuperEarths[planet]["Mperr1"]
        Mperr2=SuperEarths[planet]["Mperr2"]
        Rp=SuperEarths[planet]["Rp"]
        Rperr1=SuperEarths[planet]["Rperr1"]
        Rperr2=SuperEarths[planet]["Rperr2"]
        planetn=planet.replace("_","-")
        compositionRegion(axc,planetn,Mp,Mperr1,Mperr2,Rp,Rperr1,Rperr2,MS,CM,RM,
                          color='k',alphalines=0.0,fontsize=10)

    axc.set_xlabel(r"$M_{\rm p}$ ($M_\oplus$)",fontsize=14)
    axc.set_ylabel(r"CMF",fontsize=14)
    figc.savefig("figures/RM-Solid-Contour.png")

def massRadiusGas():
    
    qsave=True

    fig=plt.figure()
    ax=fig.add_axes([0.12,0.1,0.8,0.8])
    
    loadIceGasGiantsGrid(DATA_DIR+"IceGasGiants/",
                         verbose=True)
    Mvec=np.logspace(np.log10(0.03),np.log10(11.0),300)
    for C in '0','S','10','25','50','100':
        planet=Giants[C]
        Mmin=planet.time[7].Mjmin
        Mmax=planet.time[7].Mjmax
        tau=4.56
        
        Ms=[]
        Rs=[]
        for M in np.logspace(np.log10(0.03),np.log10(11.0),300):
            try:
                R=planet.Radius(M,tau)
            except:continue
            Ms+=[M]
            Rs+=[R]
            
        ax.plot(Ms,Rs,label='C : %s'%C)

    NM=100
    NF=100
    logMvec=np.linspace(np.log10(0.03),np.log10(2.0),NM)
    logfs=np.linspace(np.log10(0.01),np.log10(1.0),NF)

    lFS,lMS=np.meshgrid(logfs,logMvec)
    lRM=np.zeros_like(lFS)

    i=0
    for logfHHe in logfs:
        fHHe=10**logfHHe
        print "Mass-radius relationship for fHHe = %.4f"%fHHe
        Ms=[]
        Rs=[]
        j=0
        for logM in logMvec:
            M=10**logM
            #print "\tM = %.2f"%M
            R,T,Q=PlanetIceGasProperties(M,tau,fHHe,verbose=False)
            if R<0:Rq=1E-3
            else:Rq=R
            lRM[j,i]=np.log10(Rq)
            #print "\t\t",Rq
            j+=1
            if R<0:continue
            Ms+=[M]
            Rs+=[R]
        ax.plot(Ms,Rs,label='%.2f'%fHHe)
        i+=1
        
    if qsave:
        np.savetxt("figures/FS-gas.dat",lFS)
        np.savetxt("figures/MS-gas.dat",lMS)
        np.savetxt("figures/RM-gas.dat",lRM)

    ax.legend(loc="lower right",prop=dict(size=10))
    ax.set_xlabel(r"$M_{\rm p}$ ($M_{\rm Jup}$)",fontsize=14)
    ax.set_ylabel(r"$R_{\rm p}$ ($R_{\rm Jup}$)",fontsize=14)
    ax.set_xlim((0.03,10.0))
    ax.set_ylim((0.2,1.1))
    ax.set_xscale("log")
    ax.set_yscale("log")
    fig.savefig("figures/RM-IceGas.png")

def massRadiusGasContours():
    
    figc=plt.figure()
    axc=figc.add_axes([0.12,0.1,0.85,0.82])

    FS=np.loadtxt("figures/FS-gas.dat")
    MS=np.loadtxt("figures/MS-gas.dat")
    RM=np.loadtxt("figures/RM-gas.dat")

    logMmin=MS.min()
    logMmax=MS.max()

    logfmin=FS.min()
    logfmax=FS.max()

    cond=RM>-3
    sRM=RM[cond]

    logRmin=sRM.min()
    logRmax=sRM.max()

    #CONTOUR
    cont=axc.contourf(MS,FS,RM,levels=np.linspace(logRmin,logRmax,1000),cmap=cm.spectral)
    cbar=plt.colorbar(cont)
    #"""
    cbar.ax.set_ylabel(r"$R_{\rm p}$ ($R_{\rm Jup}$)",fontsize=14)
    xts=cbar.ax.get_yticks()
    rs=np.arange(0.2,1.1,0.1)
    xls=[]
    levels=[]
    for xt in xts:
        es=xt*(logRmax-logRmin)+logRmin
        rs=10**(xt*(logRmax-logRmin)+logRmin)
        xls+=["%.2f"%(rs)]
        levels+=[es]
    cbar.ax.set_yticklabels(xls)
    print levels
    #"""
    cont=axc.contour(MS,FS,RM,levels=levels,
                     colors=['k']*len(levels),linestyles=[':']*len(levels))

    cont=axc.contourf(MS,FS,RM,levels=[-3,logRmin],colors=['w','w'])

    #"""
    #YTICKS
    xt=[]
    xl=[]
    fmin=10**logfmin
    fmax=10**logfmax
    for f in np.concatenate((np.arange(0.01,0.09,0.02),
                            np.arange(0.1,1.0,0.2))):
        xt+=[np.log10(f)]
        xl+=["%.0f%%"%(f*100)]
    axc.set_yticks(xt)
    axc.set_yticklabels(xl,fontsize=12)

    #XTICKS
    xt=[]
    xl=[]
    Mmin=10**logMmin
    Mmax=10**logMmax
    for M in np.concatenate((np.arange(10,90,20),
                             np.arange(100,1000,100))):
        xt+=[np.log10(M*MEARTH/MJUP)]
        xl+=["%.0f"%(M)]
    axc.set_xticks(xt)
    axc.set_xticklabels(xl,fontsize=12)
    #"""

    #BINARY PLANETS
    fpickle="BHM/data/BHMcat/BHMcat.pickle"
    fl=open(fpickle,'r')
    systems=pickle.load(fl)
    fl.close()
    
    sysids=[]
    logfps=dict()
    sysids+=["BHMCatS0001D"];logfps["BHMCatPD0001"]=-2.680055e-01
    sysids+=["BHMCatS0002D"];logfps["BHMCatPD0002"]=-2.238595e-01
    sysids+=["BHMCatS0003D"];logfps["BHMCatPD0003"]=-2.243038e-01
    #sysids+=["BHMCatS0004D"]
    sysids+=["BHMCatS0005D"];logfps["BHMCatPD0006"]=-8.846251e-01
    #sysids+=["BHMCatS0006D"]
    sysids+=["BHMCatS0007D"];logfps["BHMCatPD0008"]=-1.123994e+00
    sysids+=["BHMCatS0008D"];logfps["BHMCatPD0009"]=-4.753510e-01
    for sysid in sysids:
        system=systems[sysid]
        plids=system["Planets"].split(";")
        for plid in plids:
            if plid=="":continue
            planet=system["PlanetsModel"][plid]
            pname=planet["PlanetID"]
            Mp=planet["planet_M"]*MEARTH/MJUP
            if planet["planet_M"]<15:continue
            Rp=planet["planet_R"]*REARTH/RJUP
            print "Planet %s : Mp = %e"%(pname,Mp)
            print "\tRp = %e"%(Rp)
            print "\tPlanet id: %s"%plid
            logMp=np.log10(Mp)
            logRp=np.log10(Rp)
            logfp=logfps[plid]
            """
            cont=axc.contour(MS,FS,RM,levels=[logRp],colors=['w'],
                             linestyles='-',linewidth=2,alpha=1.0)
            path=cont.collections[0].get_paths()[0].vertices
            #cond=path[:,1]<logfpmax
            cond=path[:,1]<-0.1
            xs=path[cond,0];#xs=xs[::-1]
            ys=path[cond,1];#ys=ys[::-1]
            path_fun=lambda x:np.interp(x,xs,ys)
            axc.plot(xs,path_fun(xs),'w:',linewidth=2)
            logfp=path_fun(logMp)
            axc.axvline(logMp,color='k',linestyle=':',linewidth=2)
            #"""
            print "\tlog(f_H/He) = %e, f_H/He = %e"%(logfp,10**logfp)
            axc.plot([logMp],[logfp],'w^',markersize=10,markeredgecolor='none')
            axc.text(logMp,logfp,pname,
                     horizontalalignment='center',verticalalignment='center',
                     rotation=0,transform=offSet(5,-20),fontsize=10)
        
    #SOLAR SYSTEM GIANTS
    planets=[]
    logfps=dict()
    planets+=['Jupiter'];logfpmax=-0.01;logfps["Jupiter"]=-0.06
    planets+=['Saturn'];logfpmax=-0.01;logfps["Saturn"]=-1.511201E-1
    planets+=['Uranus'];logfpmax=-0.8;logfps["Uranus"]=-8.494529E-1
    planets+=['Neptune'];logfpmax=-0.8;logfps["Neptune"]=-9.335701E-1
    for planetn in planets:
        print "Finding ",planetn
        planet=Planets[planetn]
        Mp=planet["Mp"]/MJUP
        Rp=planet["Rp"]/RJUP
        print "\tRp = %e"%Rp
        logRp=np.log10(Rp)
        logMp=np.log10(Mp)
        logfp=logfps[planetn]
        """
        cont=axc.contour(MS,FS,RM,levels=[logRp],colors=['w'],
                         linestyles='-',linewidth=2,alpha=1.0)
        path=cont.collections[0].get_paths()[0].vertices
        #cond=path[:,1]<logfpmax
        cond=path[:,1]<10.0
        xs=path[cond,0];#xs=xs[::-1]
        ys=path[cond,1];#ys=ys[::-1]
        path_fun=lambda x:np.interp(x,xs,ys)
        axc.plot(xs,path_fun(xs),'w:',linewidth=2)
        logfp=path_fun(logMp)
        axc.axvline(logMp,color='w',linestyle=':',linewidth=2)
        #"""
        print "log(f_H/He) = %e, f_H/He = %e"%(logfp,10**logfp)
        axc.plot([logMp],[logfp],'wo',markersize=10,markeredgecolor='none')

        
        axc.text(logMp,logfp,planetn,
                horizontalalignment='left',verticalalignment='center',fontsize=10,
                transform=offSet(10,10),color='k')
        
    axc.set_xlabel(r"$M_{\rm p}$ ($M_{\rm Jup}$)",fontsize=14)
    axc.set_ylabel(r"$f_{\rm H/He}$ (%)",fontsize=14)
    axc.grid(axis="both")
    xmin,xmax=axc.get_xlim()
    axc.set_xlim((-1.4,0.2))
    figc.savefig("figures/RM-Gas-Contour.png")

def dipoleMomentGiants():
    loadIceGasGiantsGrid(DATA_DIR+"IceGasGiants/",
                         verbose=True)

    qsaved=False
    qsaved=True
    fig=plt.figure()
    ax=fig.add_axes([0.12,0.12,0.8,0.8])

    fs=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    fs=[0.5,0.9]
    fs=np.concatenate(([0.1],np.arange(0.2,1.1,0.2)))

    planet=dict2obj(dict())
    planet.Prot=0.5
    planet.tau=4.56
    Mdipmin=1E100
    Mdipmax=0
    NF=len(fs)
    NM=50
    Mpvec=np.logspace(np.log10(0.03),np.log10(2.0),NM)

    i=0
    for f in fs:
        print "Calculating magnetic field for f_H/He = %.3f"%f
        Ms=[]
        Mdips=[]
        if not qsaved:
            for Mp in Mpvec:
                planet.Mg=Mp
                planet.fHHe=f
                planet.Rg,planet.T,planet.Qconv=PlanetIceGasProperties(planet.Mg,
                                                                       planet.tau,
                                                                       planet.fHHe,
                                                                       verbose=False)
                if planet.Rg<0:continue
                planet.R=planet.Rg*RJUP/REARTH
                planet.M=planet.Mg*RJUP/REARTH
                planet.Rc,planet.Ric,planet.rho,\
                    planet.rhoc,planet.sigma,planet.kappa=\
                    giantStructure(planet.Mg,planet.Rg)
                planet.Mdip=planetaryDipoleMoment(planet)/MDIPE
                Ms+=[planet.Mg]
                Mdips+=[planet.Mdip]
                #print "\tMp=%.2f, Rp=%.2f, Mdip=%e"%(planet.Mg,planet.Rg,planet.Mdip)
            np.savetxt("figures/Ms-f-%.2e.dat"%f,Ms)
            np.savetxt("figures/Mdip-f-%.2e.dat"%f,Mdips)
        else:
            Ms=np.loadtxt("figures/Ms-f-%.2e.dat"%f)
            Mdips=np.loadtxt("figures/Mdip-f-%.2e.dat"%f)

        Mdipmin=min(Mdipmin,min(Mdips))
        Mdipmax=max(Mdipmax,max(Mdips))
        ax.plot(np.array(Ms)*MJUP/MEARTH,Mdips,'-',label=r'$f_{\rm H/He}=%.2f$'%f)
        i+=1
    
    #GIANT PLANETS
    planets=[]
    planets+=['Jupiter'];
    planets+=['Saturn'];
    planets+=['Uranus'];
    planets+=['Neptune'];
    for planetn in planets:
        planeta=Planets[planetn]
        Mp=planeta["Mp"]/MJUP
        Mdip=planeta["Mdip"]/MDIPE
        ax.plot([Mp*MJUP/MEARTH],[Mdip],"ks",markersize=10)
        ax.text(Mp*MJUP/MEARTH,Mdip,planetn,
                horizontalalignment='left',verticalalignment='center',fontsize=10,
                transform=offSet(10,10),color='k')

    #CIRCUMBINARY PLANETS
    fpickle="BHM/data/BHMcat/BHMcat.pickle"
    fl=open(fpickle,'r')
    systems=pickle.load(fl)
    fl.close()
    sysids=[]
    logfps=dict()
    sysids+=["BHMCatS0001D"];logfps["BHMCatPD0001"]=-2.680055e-01
    sysids+=["BHMCatS0002D"];logfps["BHMCatPD0002"]=-2.238595e-01
    sysids+=["BHMCatS0003D"];logfps["BHMCatPD0003"]=-2.243038e-01
    sysids+=["BHMCatS0005D"];logfps["BHMCatPD0006"]=-8.846251e-01
    sysids+=["BHMCatS0007D"];logfps["BHMCatPD0008"]=-1.123994e+00
    sysids+=["BHMCatS0008D"];logfps["BHMCatPD0009"]=-4.753510e-01
    fpickle="BHM/data/BHMcat/BHMcat.pickle"
    for sysid in sysids:
        system=systems[sysid]
        plids=system["Planets"].split(";")
        for plid in plids:
            if plid=="":continue
            planeta=system["PlanetsModel"][plid]
            pname=planeta["PlanetID"]
            planet.M=planeta["planet_M"]
            planet.Mg=planet.M*MEARTH/MJUP
            if planet.M<15:continue

            planet.Rg=planeta["planet_R"]*REARTH/RJUP
            print "Planet %s (%s) : Mp = %e"%(pname,plid,planet.M)
            print "\tRp = %e"%(planet.Rg)

            f=10**logfps[plid]
            planet.fHHe=f
            print "\tf = %e"%f

            planet.Rg,planet.T,planet.Qconv=PlanetIceGasProperties(planet.Mg,
                                                                   planet.tau,
                                                                   planet.fHHe,
                                                                   verbose=False)

            planet.R=planet.Rg*RJUP/REARTH
            planet.Rc,planet.Ric,planet.rho,\
                planet.rhoc,planet.sigma,planet.kappa=\
                giantStructure(planet.Mg,planet.Rg)
            planet.Mdip=planetaryDipoleMoment(planet)/MDIPE
            ax.plot([planet.M],[planet.Mdip],'rv',markersize=10,markeredgecolor='none')
            ax.text(planet.M,planet.Mdip,pname,
                    horizontalalignment='left',verticalalignment='center',fontsize=10,
                    transform=offSet(10,10),color='k')
            
    ax.set_xlabel(r"$M_p$ ($M_\oplus$)",fontsize=14)
    ax.set_ylabel(r"${\cal M}_{\rm dip}$ (${\cal M}_{{\rm dip}\oplus}$)",fontsize=14)
    
    ax.set_xscale("log")
    ax.set_yscale("log")
    logTickLabels(ax,1,3,(3,),frm='%.0f',axis='x',notation='normal',fontsize=10)
    ax.set_xlim((Mpvec[0]*MJUP/MEARTH,Mpvec[-1]*MJUP/MEARTH))
    ax.set_ylim((10.0,Mdipmax))
    ax.grid(which='both')
    ax.legend(loc='best')
    fig.savefig("figures/Gas-DipoleMoment.png")

def acritPlot():

    fig=plt.figure()
    ax=fig.add_axes([0.12,0.12,0.8,0.8])

    Z=0.015
    model="PARSEC"
    mu=0.15
    Ms=[0.5,0.7,1.0]
    ebins=np.logspace(np.log10(1E-2),np.log10(0.7),10)

    i=0
    rmin=1E100
    rmax=0.0

    P1=10.0
    P2=20.0
    
    for M1 in Ms:
        
        pfind,startrack=findTrack(model,Z,M1,verbose=True)
        trackfunc1=trackFunctions(startrack)
        tau=(startrack['qt'][-1]+startrack['qt'][0])/2
        
        M2=mu/(1-mu)*M1
        pfind,startrack=findTrack(model,Z,M1,verbose=True)
        trackfunc2=trackFunctions(startrack)

        print "Calculating for M1 = %.2f, M2 = %.2f at tau = %.2f Gyr"%(M1,M2,tau/GIGA)

        L1=trackfunc1.L(tau)
        T1=trackfunc1.T(tau)

        L2=trackfunc2.L(tau)
        T2=trackfunc2.T(tau)
        
        q=M2/M1

        Pbin=P1
        abin=aKepler(Pbin,M1,M2)
        lin,lout=HZbin(q,L1,L2,T1,abin,crits=['recent venus','early mars'])
        acs1=aCritical(mu,abin,ebins)/abin
        lin1=lin*np.ones_like(ebins)/abin
        line,=ax.plot(ebins,lin1)
        color=plt.getp(line,"color")
        rmin=min(rmin,acs1.min(),lin1.min())
        rmax=max(rmax,acs1.max(),lin1.max())

        if i==len(Ms)-1:
            ax.text(ebins[-1],lin1[0],r"$P_{\rm bin}=%.0f$ days"%Pbin,transform=offSet(-5,5),
                    horizontalalignment='right',verticalalignment='bottom',fontsize=12)

        Pbin=P2
        abin=aKepler(Pbin,M1,M2)
        lin,lout=HZbin(q,L1,L2,T1,abin,crits=['recent venus','early mars'])
        lin2=lin*np.ones_like(ebins)/abin
        acs2=aCritical(mu,abin,ebins)/abin
        ax.plot(ebins,lin2,color=color)
        rmin=min(rmin,acs2.min(),lin2.min())
        rmax=max(rmax,acs2.max(),lin2.max())

        if i==len(Ms)-1:
            ax.text(ebins[-1],lin2[0],r"$P_{\rm bin}=%.0f$ days"%Pbin,transform=offSet(-5,-5),
                    horizontalalignment='right',verticalalignment='top',fontsize=12)
        
        ax.fill_between(ebins,lin1,lin2,color=color,alpha=0.3)
        ax.text(1E-2,lin1[0],r"$M_1=%.2f\,M_\odot$"%M1,transform=offSet(5,-5),
                horizontalalignment='left',verticalalignment='top',fontsize=14)
        
        i+=1

    print "rmin,rmax:",rmin,rmax

    mus=[0.1,0.2,0.3,0.4,0.5]
    #mus=[mu]
    mus=[0.1,0.5]
    M1=1.0
    colors=['r','b']
    i=0
    for mu in mus:
        M2=mu/(1-mu)*M1
        Pbin=30.0
        abin=aKepler(Pbin,M1,M2)
        acs=aCritical(mu,abin,ebins)/abin
        ax.plot(ebins,acs,label=r"$\mu$ = %.1f"%mu,linewidth=2,color=colors[i])
        i+=1

    ax.set_yscale("log")
    ax.set_xscale("log")

    ax.set_xlabel(r"$e$",fontsize=14)
    ax.set_ylabel(r"$a_{\rm crit}/a_{\rm bin}$ , $l_{\rm in}/a_{\rm bin}$",fontsize=14)

    logTickLabels(ax,0,2,(1,),frm="%.1f",axis="y",notation="normal",fontsize=12)
    logTickLabels(ax,-2,0,(3,2),frm="%.2f",axis="x",notation="normal",fontsize=12)

    ax.set_xlim(ebins[0],ebins[-1])
    ax.set_ylim((1.5,1.2*rmax))

    ax.grid(which='both')
    ax.legend(loc='lower right')
    fig.savefig("figures/CriticalDistance.png")

def plotBinarySpectrum():

    from numpy import *
    #////////////////////////////////////////
    #BINARY PROPERTIES
    #////////////////////////////////////////
    Z=0.015
    M1=1.0
    M2=0.8
    q=M2/M1
    Pbin=15
    ebin=0.3
    tau=2.0
    model="PARSEC"

    pfind,startrack=findTrack(model,Z,M1,verbose=True)
    trackfunc1=trackFunctions(startrack)

    pfind,startrack=findTrack(model,Z,M2,verbose=True)
    trackfunc2=trackFunctions(startrack)

    #////////////////////////////////////////
    #DERIVED PROPERTIES
    #////////////////////////////////////////
    lambo=10*NANO
    lambi=1E+4*NANO
    lambs=logspace(log10(lambo),log10(lambi),1000)
    for i in xrange(1):

        #ORBITAL
        abin=aKepler(Pbin,M1,M2)
        #print abin

        #STELLAR PROPERTIES
        g1,T1,R1,L1=StellarGTRLTrack(Z,M1,tau,trackfunc1)
        g2,T2,R2,L2=StellarGTRLTrack(Z,M2,tau,trackfunc2)
        #print g1,T1,R1,L1
        #print g2,T2,R2,L2

        #HABITABLE ZONE
        lin,lout,aHZ=HZbin(M2/M1,L1,L2,T1,abin,
                           crits=['recent venus','early mars'],
                           eeq=True
                           )
        #print lin,aHZ,lout

        #TEST EFFECTIVE TEMPERATURE VARIATIONS
        """
        EFFECTIVE TEMPERATURES FOR WHICH THE HZ LIMITS ARE THE SAME IN
        A RANGE 2.5%
        """
        atol=3.5/100
        filetrange="tmp/Trange-%.1f-%.1e"%(T1,atol)
        if not FILEEXISTS(filetrange):
            aH,mid,lou=HZ(L1,T1)
            #print aH
            Ttu=T1;Ttd=T1
            deltaT=10.0
            qup=0
            qdown=0
            print deltaT
            while True:
                aHZtu,mid,loutt=HZ(L1,Ttu)
                aHZtd,mid,loutt=HZ(L1,Ttd)
                #print aHZtu,aHZtd

                #print Ttd,Ttu
                Ttu=Ttu+deltaT
                Ttd=Ttd-deltaT
                #print Ttd,Ttu
                if (fabs(aHZtu-aH)/aH>atol or Ttu>=7200) and not qup:
                    Ttup=Ttu
                    qup=True
                    print "qup found..."
                if (fabs(aHZtd-aH)/aH>atol or Ttd<=2600) and not qdown:
                    Ttdown=Ttd
                    qdown=True
                    print "qdown found..."
                if qdown and qup:break
                #raw_input()
            savetxt(filetrange,[Ttd,Ttu])
        else:
            Ttd,Ttu=loadtxt(filetrange)

        print "Temperature Range: ",Ttd,Ttu

        #BINARY PHASE
        a1=q*abin/(1+q)
        a2=abin/(1+q)

        fig=plt.figure()
        ax=fig.add_axes([0.12,0.1,0.8,0.8])

        r=aHZ
        r=lin
        i=0
        for theta in [-90*DEG,90*DEG]:
            R1=sqrt((r+a1*sin(theta))**2+(a1*cos(theta))**2)
            R2=sqrt((r-a2*sin(theta))**2+(a2*cos(theta))**2)
   
            A1=(4*pi*(R1*AU)**2)
            A2=(4*pi*(R2*AU)**2)
            
            #COMPUTE THE STELLAR FLUX
            #Component 1
            I1=planckDistrib(lambs,T1)/A1
            I2=planckDistrib(lambs,T2)/A2
            IT=I1+I2
        
            I1func=interp1d(lambs/NANO,I1,kind='slinear')
            I2func=interp1d(lambs/NANO,I2,kind='slinear')
            ITfunc=interp1d(lambs/NANO,IT,kind='slinear')
           
            N1,dN=integrate(I1func,lambo/NANO,lambi/NANO)
            N2,dN=integrate(I2func,lambo/NANO,lambi/NANO)
            NT,dN=integrate(ITfunc,lambo/NANO,lambi/NANO)
    
            ax.plot(lambs/NANO,I1/N1,'b--',linewidth=2)
            ax.plot(lambs/NANO,I2/N2,'r-.',linewidth=2)
            ax.plot(lambs/NANO,IT/NT,'k-',linewidth=2)

        #RANGE OF EFFECTIVE TEMPERATURES OF SINGLE STAR HAVING THE SAME LIMITS AS T1
        Itu=planckDistrib(lambs,Ttu)/A1
        Itfuncu=interp1d(lambs/NANO,Itu,kind='slinear')
        Ntu,dN=integrate(Itfuncu,lambo/NANO,lambi/NANO)

        Itd=planckDistrib(lambs,Ttd)/A1
        Itfuncd=interp1d(lambs/NANO,Itd,kind='slinear')
        Ntd,dN=integrate(Itfuncd,lambo/NANO,lambi/NANO)

        ax.fill_between(lambs/NANO,Itu/Ntu,Itd/Ntd,color='k',alpha=0.2)

        #DECORATION
        ax.set_yscale('log')
        ax.set_xlim((10,3000))
        ymax=max(Itu/Ntu)
        ax.set_ylim((ymax/100,ymax))
        ax.set_xlabel("$\lambda$ (nm)",fontsize=14)
        ax.set_ylabel("Normalized spectra",fontsize=14)

        ax.plot([],[],'b--',label='Primary')
        ax.plot([],[],'r-.',label='Secondary')
        ax.plot([],[],'k-',label='Combined')
        ax.plot([],[],'k-',label='%.1f%% Tolerance'%(atol*100),linewidth=5,alpha=0.3)
        
        ax.set_title(r"$M_1$ = %.2f, $M_2$ = %.2f, $P_{\rm bin}$ = %.0f, $e_{\rm bin}$ = %0.1f"%(M1,M2,Pbin,ebin),position=(0.5,1.02))
        plt.legend(loc='upper right',prop=dict(size=12))
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        saveFig("figures/BinarySpectrum-M1_%.2f-M2_%.2f-P_%.0f-e_%.1f.png"%(M1,M2,Pbin,ebin),watermark="")

def compareRotationEvolution():
    DATADIR=FIGDIR+"RotSolar/"
    C95=loadResults(DATADIR+"C95/")
    K88=loadResults(DATADIR+"K88/")
    M12=loadResults(DATADIR+"M12/")
    
    fig=plt.figure()
    ax=fig.add_axes([0.12,0.1,0.8,0.8])

    tC95=C95.star1.rotevol[:,0]
    PconvC95=C95.star1.rotevol[:,1]/OMEGASUN
    PradC95=C95.star1.rotevol[:,2]/OMEGASUN
    ax.plot(tC95,PconvC95,'b-',label=r"Chaboyer et al. (1995): $K_C=%.2e$"%C95.star1.Kc)
    ax.plot(tC95,PradC95,'b--')

    tK88=K88.star1.rotevol[:,0]
    PconvK88=K88.star1.rotevol[:,1]/OMEGASUN
    PradK88=K88.star1.rotevol[:,2]/OMEGASUN
    ax.plot(tK88,PconvK88,'r-',label=r"Kawaler (1988): $a=%.1f$, $n=%.2f$, $K_W=%.2e$"%(K88.star1.a,K88.star1.n,K88.star1.Kw))
    ax.plot(tK88,PradK88,'r--')

    tM12=M12.star1.rotevol[:,0]
    PconvM12=M12.star1.rotevol[:,1]/OMEGASUN
    PradM12=M12.star1.rotevol[:,2]/OMEGASUN
    ax.plot(tM12,PconvM12,'g-',label=r"Matt et al. (2012): $K_1=%.2f$"%(M12.star1.K1))
    ax.plot(tM12,PradM12,'g--')

    #DATA FOR OTHER STARS
    for star_name in ROTAGE_STARS.keys():
        if ('Proxima' in star_name) or ('Barnard' in star_name):continue
        staro=ROTAGE_STARS[star_name]
        tau=staro["tau"]
        Prot=staro["Prot"]
        ax.plot([tau],[2*PI/(Prot*DAY)/OMEGASUN],'o',markersize=10,markeredgecolor='none',color=cm.gray(0.5),zorder=-10)
        ax.text(tau,2*PI/(Prot*DAY)/OMEGASUN,star_name,transform=offSet(-10,staro["up"]),horizontalalignment="right",color=cm.gray(0.1),zorder=-10,fontsize=10)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend(loc="best",prop=dict(size=11))

    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.set_ylabel("$\Omega/\Omega_\odot$")

    ax.set_ylim((0.5,300))
    
    tmin,tmax=ax.get_xlim()
    wmin,wmax=ax.get_ylim()
    Pmin=1.0*(2*PI/(wmax*OMEGASUN)/DAY)
    Pmax=1.0*(2*PI/(wmin*OMEGASUN)/DAY)
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

    #ymin,ymax=ax.get_ylim()
    #ax.set_xlim((TMIN,TMAX))
    #ax.set_ylim((0.8,ymax))
    ax.grid(which='both')

    saveFig("figures/RotSolar.png",watermark="")

def binaryHZPanels():

    from numpy import *
    #//////////////////////////////////////////////////
    #FIGURE CREATION
    #//////////////////////////////////////////////////
    fig=plt.figure()
    l=0.1;w=0.42;b=0.1;h=0.8;
    axT=fig.add_axes([l,b,w,h])

    l+=w
    axD=fig.add_axes([l,b,w,h])
    axD.set_yticklabels([])

    #//////////////////////////////////////////////////
    #CONSTANTS
    #//////////////////////////////////////////////////
    stylesingle="--"
    stylebinary="-"
    tau=4.56

    #################################################################################
    #DISPARATE CASE
    #################################################################################

    #//////////////////////////////////////////////////
    #PARAMETERS
    #//////////////////////////////////////////////////
    model="PARSEC"
    Z=0.015
    M1=1.0 #Msun

    pfind,startrack=findTrack(model,Z,M1,verbose=True)
    trackfunc1=trackFunctions(startrack)
    g1,Teff1,R1,Ls1=StellarGTRLTrack(Z,M1,tau,trackfunc1)
    lin1,aHZ1,lout1=HZ(Ls1,Teff1)
    
    #//////////////////////////////////////////////////
    #PROPERTIES
    #//////////////////////////////////////////////////
    print "Disparate Primary component:"
    print "\tMs = %.2f Msun, Ls = %.2e Lsun, Teff = %.1f"%(M1,Ls1,Teff1)
    print "\tHabitable Zone: %.2f,%.2f,%.2f AU"%(lin1,aHZ1,lout1)

    #M2s=[0.2,0.6,1.0] #Msun
    M2s=linspace(0.2,1.0,30)
    M2s=arange(0.2,1.1,0.05)

    #Pbins=[5*DAY,90*DAY] #seconds
    Pbins=[15*DAY] #seconds

    #//////////////////////////////////////////////////
    #CALCULATIONS
    #//////////////////////////////////////////////////
    linsgs=[];aHZsgs=[];loutsgs=[]
    arg=[dict(linewidth=2),dict(linewidth=1)]
    i=0
    for Pbin in Pbins:
        linbs=[];aHZbs=[];loutbs=[]
        linTbs=[];aHZTbs=[];loutTbs=[]
        acTs=[];acDs=[]
        Mss=[]
        for M2 in M2s:
            pfind,startrack=findTrack(model,Z,M2,verbose=True)
            trackfunc2=trackFunctions(startrack)

            g2,Teff2,R2,Ls2=StellarGTRLTrack(Z,M2,tau,trackfunc2)
            linsg,aHZsg,loutsg=HZ(Ls2,Teff2)

            linsgs+=[linsg];aHZsgs+=[(linsg+loutsg)/2];loutsgs+=[loutsg]
            print "Disparate Secondary component:"
            print "\tMs = %.2f Msun, Ls = %.2e Lsun, Teff = %.1f"%(M2,Ls2,Teff2)
            print "\tHZ: %e,%e,%e AU"%(linsg,aHZsg,loutsg)
            
            #Distance
            abin=(Pbin**2*GCONST*((M1+M2)*MSUN)/(2*np.pi**2))**(1./3)
            abinT=(Pbin**2*GCONST*((M2+M2)*MSUN)/(2*np.pi**2))**(1./3)

            acTs+=[aCritical(1.0,abinT/AU,0.3)]
            acDs+=[aCritical(M2/M1,abinT/AU,0.3)]

            #Binary effective temperature
            Teffbin=Teff1
            TeffbinT=Teff2

            #Disparate Binary HZ limits
            lin,lout,aHZ=HZbin(M2/M1,Ls1,Ls2,Teffbin,abin/AU,eeq=True)
            linbs+=[lin];aHZbs+=[aHZ];loutbs+=[lout]

            #Twin Binary HZ limits
            linT,loutT,aHZT=HZbin(1.0,Ls2,Ls2,TeffbinT,abinT/AU,eeq=True)
            if linT>0:
                linTbs+=[linT];aHZTbs+=[aHZT];loutTbs+=[loutT]
                Mss+=[M2]

            print "Disparate Binary system:"
            print "\tBinary period: %e days"%(Pbin/DAY)
            print "\tBinary semimajor axis: %e AU"%(abin/AU)
            print "\tHZ: %e,%e,%e AU"%(lin,aHZ,lout)

            print "Twin Binary system:"
            print "\tBinary period: %e days"%(Pbin/DAY)
            print "\tBinary semimajor axis: %e AU"%(abinT/AU)
            print "\tHZ: %e,%e,%e AU"%(linT,aHZT,loutT)

            """
            linT,aHZT,loutT,R1in,R2in,R1out,R2out=HZbin3(1.0,Ls2,Ls2,TeffbinT,abinT,
                                                         extra=True)
            print R1in,R2in,R1out,R2out
            exit(0)
            """

        axD.plot(linbs,M2s,linestyle=stylebinary,color='g',**arg[i])
        axD.plot(aHZbs,M2s,linestyle=stylebinary,color='b',**arg[i])
        axD.plot(loutbs,M2s,linestyle=stylebinary,color='r',**arg[i])

        axT.plot(linTbs,Mss,linestyle=stylebinary,color='g',**arg[i])
        axT.plot(aHZTbs,Mss,linestyle=stylebinary,color='b',**arg[i])
        axT.plot(loutTbs,Mss,linestyle=stylebinary,color='r',**arg[i])
        
        if i==0:
            for ax in axD,axT:
                ax.plot(linsgs,M2s,linestyle=stylesingle,color='g')
                ax.plot(aHZsgs,M2s,linestyle=stylesingle,color='b')
                ax.plot(1.05*array(loutsgs),M2s,linestyle=stylesingle,color='r')
        
        axT.plot(acTs,M2s,linestyle='-',color='k')
        axD.plot(acDs,M2s,linestyle='-',color='k')
        i+=1

    #//////////////////////////////////////////////////
    #DECORATION
    #//////////////////////////////////////////////////
        
    axT.text(acTs[-1]+0.01,M2s[-1]-0.05,"$a_{\rm crit}(e=0.5)$",fontsize=10,rotation=270)
    axD.text(acTs[-1]+0.1,M2s[-1]-0.02,"$a_{\rm crit}(e=0.5)$",fontsize=10,rotation=280,
             rotation_mode='anchor',horizontalalignment='left')

    axT.text(0.9,0.05,r'$P_{\rm bin}$=%.0f days'%(Pbins[0]/DAY),color='k',fontsize=14,
             horizontalalignment='right',transform=ax.transAxes)

    #axT.plot([0],[0],color='k',label=r'$P_{\rm bin}$=%.1f days'%(Pbins[0]/DAY),**arg[0])
    #axT.plot([0],[0],color='k',label=r'$P_{\rm bin}$=%.1f days'%(Pbins[1]/DAY),**arg[1])

    axT.set_ylabel("$M_\star$ ($M_\odot$)",fontsize=14)
    for ax in axD,axT:
        ax.set_xlabel("a (AU)",fontsize=14)
        ax.set_ylim((M2s[0],M2s[-1]))
        #ax.set_xscale('log')
        #ax.grid()

    axD.axvspan(lin1,lout1,alpha=0.1)
    axT.set_xticks(axT.get_xticks()[:-1])
    axD.set_title("Disparate, $M_1=1.0$ $M_\odot$, $M_2=M_\star$",
                  position=(0.5,1.02))
    axT.set_title("Twins, $M_1=M_2=M_\star$",
                  position=(0.5,1.02))

    axT.legend(loc='best')

    axD.grid(which="both")
    axT.grid(which="both")
    
    #//////////////////////////////////////////////////
    #SAVE FIGURE
    #//////////////////////////////////////////////////
    saveFig("figures/BinaryHZ",watermark="")

def compareInsolation():

    fig=plt.figure(figsize=(8,8))

    axd=fig.add_axes([0.12,0.08,0.8,0.25])
    axa=fig.add_axes([0.12,0.35,0.8,0.60])

    DATADIR=FIGDIR+"InsoPPFD/"
    inso=loadResults(DATADIR)
    ihz=inso.hz
    planet=inso.planet

    fac=0.99
    SOLAR_CONSTANT=ihz.fluxs*fac
    PPFD_EARTH=ihz.ppfds*fac
    
    insolation=ihz.insolation
    fstats=ihz.fstats
    pstats=ihz.pstats
    ts=insolation[:,0]
    
    axa.plot(ts/planet.Porb,insolation[:,1]/SOLAR_CONSTANT,
            color='b',linestyle='-',linewidth=2,
            label=r"Insolation")
    axa.plot(ts/planet.Porb,insolation[:,2]/PPFD_EARTH,
             color='g',linestyle='-',linewidth=2,
             label=r"PPFD")

    axa.axhline(ihz.fstats[0,0]/SOLAR_CONSTANT,color='b',linestyle='--',
               linewidth=2)

    axa.axhline(ihz.pstats[0,0]/PPFD_EARTH,color='g',linestyle='--',
               linewidth=2)

    axd.plot(ts/planet.Porb,insolation[:,2]/PPFD_EARTH-insolation[:,1]/SOLAR_CONSTANT,
             color='g',linewidth=2)

    axa.plot([],[],'k--',label='Average')

    for ax in axa,axd:
        ax.set_xlim((0.0,1.0))

    axd.set_xlabel('orbital phase',fontsize=12)
    axa.set_ylabel('Insolation, PPFD (PEL)',fontsize=12)

    axd.set_yticks(axd.get_yticks()[:-1])
    axa.legend(loc='best',prop=dict(size=12))

    axd.set_ylabel(r"$\Delta {\rm PPFD}$")
    axa.set_xticklabels([])

    saveFig("figures/CompareInsolation.png",watermark="")

def stellarActivity():
    DATADIR=FIGDIR+"CompSolar/"
    nominal=loadResults(DATADIR+"nominal/")
    star=nominal.star1
    
    Ni=5
    fig=plt.figure(figsize=(8,4*(Ni-1)))
    b=0.05
    l=0.1;dh=0.02;h=(1.0-2*b-(Ni-1)*dh)/Ni;w=1.0-1.5*l
    
    ax_R=fig.add_axes([l,b,w,h])
    b+=h+dh
    ax_f=fig.add_axes([l,b,w,h])
    b+=h+dh
    ax_B=fig.add_axes([l,b,w,h])
    b+=h+dh
    ax_L=fig.add_axes([l,b,w,h])
    b+=h+dh
    ax_ML=fig.add_axes([l,b,w,h])
    
    ts=star.activity[:,0]
    f=star.activity[:,2]
    B=star.activity[:,4]
    R=star.activity[:,6]
    Ml=star.activity[:,7]
    L=star.activity[:,13]/(LXSUN/1E7)

    axs=[ax_R,ax_f,ax_B,ax_ML,ax_L]
    
    args=dict(color='b')

    ax_R.plot(ts,R,**args)
    ax_R.set_ylabel("Rossby Number")
    ax_R.axhline(0.13,linestyle='--',color='r',linewidth=2,label='Saturation Level')
    ax_R.text(4.56,ROSUN,r"$\odot$",
               horizontalalignment='center',verticalalignment='center',
               fontsize=24)
    
    ax_f.plot(ts,f,**args)
    ax_f.set_ylabel("Filling factor, $f_\star$")
    ax_f.errorbar(4.56,5E-3,yerr=4E-3,color='k',linewidth=2)

    ax_B.plot(ts,B,**args)
    ax_B.set_ylabel("Photospheric field, $B_\star$")
    ax_B.set_ylim((1e3,2.5e3))
    ax_B.text(4.56,1400,r"$\odot$",
               horizontalalignment='center',verticalalignment='center',
               fontsize=24)

    ax_ML.plot(ts,Ml,**args)
    ax_ML.set_ylabel("Mass-loss, $\dot M$")
    ax_ML.text(4.56,MSTSUN*YEAR/MSUN,r"$\odot$",
               horizontalalignment='center',verticalalignment='center',
               fontsize=24)

    ax_L.plot(ts,L,**args)
    ax_L.set_ylabel(r"$L_{\rm X}/L_{\rm X,\odot}$")
    ax_L.text(4.56,1.0,r"$\odot$",
               horizontalalignment='center',verticalalignment='center',
               fontsize=24)

    ax_R.legend(loc='best',prop=dict(size=12))
    for ax in axs:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim((TAU_ZAMS,6))
        ax.grid(which='both')

    axs[0].set_xlabel(r"$\tau$ (Gyr)")

    for ax in axs[1:]:
        ax.set_xticklabels([])

    saveFig("figures/StellarActivity.png",watermark="")

def plotRX():
    
    ############################################################
    #READ DATA
    ############################################################

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #SOLAR NOMINAL
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    DATADIR=FIGDIR+"CompSolar/"
    nominal=loadResults(DATADIR+"nominal/")
    star=nominal.star1

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #ROTXRAYCAT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    lines=open("BHM/data/Stars/ROTXRAYCAT.dat")
    n=0
    Xcat=stack(6)
    for line in lines:
        if "#" in line:continue
        entry=line.strip("")
        fields=entry.split(",")
        M=float(fields[8])
        logRX=float(fields[5])
        Prot=float(fields[6])
        X=float(fields[7])
        if X<=3.5:logtauc=0.73+0.22*X
        else:logtauc=-2.16+1.50*X-0.13*X**2
        logRo=np.log10(Prot)-logtauc
        if n==0:ROSUN=10**logRo
        Xcat+=[logRX,Prot,X,logtauc,logRo,M]
        n+=1
    Xcat=Xcat.array
    print "Objects read: ",n

    ############################################################
    #PLOT RX VS ROSSBY
    ############################################################
    #RX VS. ROSSBY
    fig=plt.figure()
    ax=fig.add_axes([0.12,0.12,0.8,0.8])

    Ms=Xcat[:,5]
    Ros=10**Xcat[:,4]
    RXs=10**Xcat[:,0]

    msize=4
    style=dict(markersize=4,markeredgecolor='none')

    ax.plot([],[],'ok',markersize=2,label=r"${\rm\tt ROTXRAYCAT}$ (Wright et al., 2011)")
    
    Mmin=0.1;Mmax=0.4
    cond=(Ms>=Mmin)*(Ms<Mmax)
    nstar=len(Ms[cond])
    print "Plotting %d stars with %.2f < M < %.2f..."%(nstar,Mmin,Mmax)
    ax.plot(Ros[cond],RXs[cond],'or',label=r"$M\in[%.1f,%.2f)$"%(Mmin,Mmax),**style)

    Mmin=0.4;Mmax=0.8
    cond=(Ms>=Mmin)*(Ms<Mmax)
    nstar=len(Ms[cond])
    print "Plotting %d stars with %.2f < M < %.2f..."%(nstar,Mmin,Mmax)
    ax.plot(Ros[cond],RXs[cond],'^g',label=r"$M\in[%.1f,%.2f)$"%(Mmin,Mmax),**style)

    Mmin=0.8;Mmax=1.2
    cond=(Ms>=Mmin)*(Ms<Mmax)
    nstar=len(Ms[cond])
    print "Plotting %d stars with %.2f < M < %.2f..."%(nstar,Mmin,Mmax)
    ax.plot(Ros[cond],RXs[cond],'sb',label=r"$M\in[%.1f,%.2f)$"%(Mmin,Mmax),**style)

    Romin=Ros.min()
    Romax=Ros.max()
    RXmin=RXs.min()
    RXmax=RXs.max()

    Ros=np.logspace(np.log10(Romin),np.log10(Romax))

    tRXs=[starRX(Ro) for Ro in Ros]
    tRXs1=[starRX(Ro,regime='high') for Ro in Ros]
    tRXs2=[starRX(Ro,regime='low') for Ro in Ros]
    ax.fill_between(Ros,tRXs1,tRXs2,color='b',alpha=0.3)
    ax.plot([],[],'b-',linewidth=10,alpha=0.3,label="Empirical Fit")

    ax.text(ROSUN,(LXSUN/1E7/LSUN),r"$\odot$",
            horizontalalignment='center',verticalalignment='center',
            fontsize=24)

    ts=star.activity[:,0]
    R=star.activity[:,6]
    LX=star.activity[:,13]
    L=np.interp(ts,star.evotrack[:,0],star.evotrack[:,4])*LSUN
    ax.plot(R,LX/L,'k-',markersize=2,markeredgecolor='none',label="Solar model")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim((Romin,Romax))
    ax.set_ylim((RXmin,RXmax))

    ax.legend(loc='lower left',prop=dict(size=12))

    ax.set_xlabel(r"${\rm Ro}$",fontsize=14)
    ax.set_ylabel(r"$R_{\rm X}$",fontsize=14)

    saveFig("figures/RX.png",watermark="")


#plotAllMoIs()
#compareMoIs()
#evolutionaryTracks()
#massRadiusSolid()
#massRadiusSolidContours()
#massRadiusGas()
#massRadiusGasContours()
#dipoleMomentGiants()
#acritPlot()
#plotBinarySpectrum()
#ocompareRotationEvolution()
#binaryHZPanels()
#compareInsolation()
#stellarActivity()
plotRX()
