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

plotAllMoIs()
