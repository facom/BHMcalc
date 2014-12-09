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
from BHM.BHMplot import *
from BHM.BHMstars import *
from BHM.BHMplanets import *
from BHM.BHMdata import *

###################################################
#CONSTANTS
###################################################
PROTSUN=26*DAY #s
OMEGASUN=2*PI/PROTSUN #rad s^-1
DOMEGASUN=4.8E-7 #Omega(theta) = Omega_eq - dOmega sin^2(theta), rad s^-1
VSINISUN=OMEGASUN*RSUN #m/s
ISUN=6.4E53/1E3*(1E-2)**2 #kg m^2
MOISUN=ISUN/(MSUN*RSUN**2)
JSUN=1.8E48/1E3*(1E-2)**2 #kg m^2 s^-1, Pinto et al. (2011)
TAUWSUN=1.0*GYR
DJDTSUN=JSUN/TAUWSUN
MDOTSUN=0.6*MP*NSUN*VSUN*4*PI*AU**2 #MASS-LOSS SUN
RASUN=50*RSUN #ALFVENIC RADIUS

###################################################
#CRITICAL VELOCITY
###################################################
def criticalVrot(M,R):
    vrot=np.sqrt(2*GCONST*M*MSUN/(3*R*RSUN))
    return vrot

###################################################
#SCRIPT
###################################################
def Test():
    print VSINISUN
    print criticalVrot(1,1)
    print ISUN,MOISUN,JSUN
    print TAUWSUN
    print DJDTSUN
    print MDOTSUN/MSUN*YEAR
    
    DJDTSUN=(2./3)*OMEGASUN*MDOTSUN*RASUN**2
    
    print DJDTSUN
    print JSUN/DJDTSUN/GYR
    
    print 2*PI*RSUN/(maxPeriod(1,1)*DAY)/1E3
    
    Ms=1
    Rs=1
    Po=Prot(4.56,Ms=Ms,Rs=Rs)
    Pini=Prot(0.1,Ms=Ms,Rs=Rs)
    print Po/DAY
    print Pini/DAY
    print 2*PI*(Rs*RSUN)/Pini/1E3
    
    num=loadIsochroneSet(verbose=True,Zs=ZSVEC_siblings)

    """
    tau=1.0
    g,T,R,L=StellarGTRL(0.0152,Ms,tau)
    Pini=Prot(tau,Ms=Ms,Rs=R)/DAY
    print Pini
    
    Ms=0.5
    tau=8.0
    g,T,R,L=StellarGTRL(0.0152,Ms,tau)
    Pini=Prot(tau,Ms=Ms,Rs=R)/DAY
    print Pini
    exit(0)

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    Prot=np.logspace(np.log10(0.1),np.log10(100),100)*DAY
    for R in np.linspace(0.5,1.5,10):
    plt.plot(Prot/DAY,2*PI*R*RSUN/Prot/1E3,label='R = %.2f'%R)
    ax.set_xscale("log")
    #ax.set_yscale("log")
    ax.set_xlabel("P(days)")
    ax.set_ylabel("v (km/s)")
    ax.legend(loc='best')
    saveFig("tests/rot-vsini.png")
    """
    
    tauref=0.2
    Ms=1.0
    g,T,R,L=StellarGTRL(0.0152,Ms,tauref)
    tcsun=dissipationTime(Ms,R,L)/(3.48*DAY)
    
    Ms=0.5
    g,T,R,L=StellarGTRL(0.0152,Ms,tauref)
    tc=dissipationTime(Ms,R,L)/(3.48*DAY)
    
    print tcsun/tc
    
    exit(0)
    
    tauref=8

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    
    
    Msvec=np.linspace(0.1,1.0,10)
    Psvec=[]
    for Ms in Msvec:
        g,T,R,L=StellarGTRL(0.0152,Ms,tauref)
        print Ms,dissipationTime(Ms,R,L)/(3.48*DAY)
        P=Prot(tauref,Ms=Ms,Rs=R)/DAY
        Psvec+=[P]

    plt.plot(Msvec,Psvec)
    ax.set_yscale("log")
    ax.set_xlabel("M (Msun)")
    ax.set_ylabel("P (days)")
    ax.set_xlim((1.0,0.1))
    ax.set_ylim((0.1,100.0))
    #ax.legend(loc='best')
    saveFig("tests/Prot-Ms-tau_%.3f.png"%tauref)
    
def TestTorque():
    
    num=loadIsochroneSet(verbose=True,Zs=ZSVEC_siblings)

    tau=0.5
    
    M=1.0
    MoI=stellarMoI(M)
    Z=0.0152

    #INITIAL CONDITIONS
    tau_disk=0.01
    Pini=3*DAY
    wini=2*PI/Pini

    #MODEL PARAMETERS
    wsat=10*OMEGASUN #Krishnamurthi et al.,1997
    Kw=2.1E40
    print Kw
    
    #TORQUE
    """
    See pag. 1026 of Bouvier (1997)
    """
    def dwdt(y,t,params):
        MoI=params['MoI']
        w=y[0]
        g,T,R,L=StellarGTRL(Z,M,t/GYR)
        I=MoI*M*MSUN*(R*RSUN)**2
        facw=R**0.5/M**0.5

        #print "Time = ",t

        dwdt=0.0
        
        #MASS-LOSS TORQUE
        if w<=wsat:
            dJdtw=-Kw*w**3*facw
        else:
            dJdtw=-Kw*w*wsat**2*facw
        print "Mass-loss torque = ",dJdtw/I

        dwdt+=dJdtw/I

        #CONTRACTION TORQUE
        dt=0.001*GYR
        g,T,Rm,L=StellarGTRL(Z,M,(t-dt)/GYR)
        #print Rm
        g,T,Rp,L=StellarGTRL(Z,M,(t+dt)/GYR)
        #print Rp
        dRdt=(Rp-Rm)/(2*dt)
        #print dRdt*RSUN/GYR
        dIdt=2*MoI*(M*MSUN)*(R*RSUN)*(dRdt*RSUN)
        #print "Contraction torque = ",w*dIdt/I

        dwdt+=-w*dIdt/I
        print t/GYR,I,dIdt,dwdt
        exit(0)
        #print "Total torque = ",dwdt

        if t/GYR<tau_disk:
            dwdt=0

        return [dwdt]

    ts=np.logspace(np.log10(0.012),np.log10(10.0),30)*GYR
    yini=[wini]
    pars=dict(MoI=MoI)
    sol=odeint(dwdt,yini,ts,args=(pars,))
    
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(ts/GYR,sol[:,0]/OMEGASUN,'b+-')
    ax.plot(ts/GYR,1.0*(ts/(4.56*GYR))**(-0.5),'r+-')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid()
    ax.axvline(4.56)
    ax.axhline(1.00)
    saveFig("tests/w-evol.png")

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(ts/GYR,2*PI/sol[:,0]/DAY,'b+-')
    ax.set_xscale("log")
    ax.set_yscale("log")
    saveFig("tests/P-evol.png")

def MomentOfInertia():
    
    num=loadIsochroneSet(verbose=True,Zs=ZSVEC_siblings)

    tau=0.5
    
    M=0.6
    Z=0.0152

    ts=np.logspace(np.log10(1E-2),np.log10(1E-0),30)

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    
    Ms=np.array([0.2,0.5,1.0,1.2])

    Ms=np.array([1.0])
    for M in Ms:
        Is=[]
        Rs=[]
        MoI=stellarMoI(M)
        print M,MoI
        for t in ts:
            g,T,R,L=StellarGTRL(Z,M,t)
            I=MoI*M*MSUN*(R*RSUN)**2
            print t,R
            Rs+=[R]
            Is+=[I]
        #ax.plot(ts,array(Is)/ISUN,'b+-',label='M=%.2f'%M)
        ax.plot(ts,array(Rs),'+-',label='M=%.2f'%M)

    ax.legend(loc="best")
    ax.set_xscale("log")
    #ax.set_yscale("log")
    #saveFig("tests/I-evol.png")
    saveFig("tests/R-evol.png")

def rotationFit():
    rotpars=dict(\
        star=star,
        starf=None,binary=None,
        taudisk=star.taudisk,
        Kw=star.Kw,
        wsat=star.wsat*OMEGASUN
        )
    rotevol=odeint(rotationalAcceleration,wini,tsmoi*GYR,args=(rotpars,))

def evolutionaryTrack():

    #"""
    #KEPLER-16A
    M=0.69
    Mb=0.70
    Z=8E-3
    Robs=0.649;Rerr=0.001
    Tobs=4337.0;Terr=80.0
    Lobs=Robs**2*(Tobs/5770)**4
    Lerr=Lobs*(2*Rerr/Robs+4*Terr/Tobs)
    cond="NOS" #No Overshooting
    #"""

    """
    #kEPLER-47C
    Mb=1.00
    M=1.04
    Z=8E-3
    Robs=0.964;Rerr=0.017
    Tobs=5636.0;Terr=100.0
    Lobs=Robs**2*(Tobs/5770)**4
    Lerr=Lobs*(2*Rerr/Robs+4*Terr/Tobs)
    cond="NOS" #No Overshooting
    #"""

    #BARAFFE
    data_bf98=np.loadtxt("tests/comparisons/bcah98.txt")
    Ms=data_bf98[:,0]
    inds=array(range(len(Ms)))
    cinds=inds[Ms==Mb]
    ts=data_bf98[cinds,1]
    Teff_func=interp1d(ts,data_bf98[cinds,2])
    logL_func=interp1d(ts,data_bf98[cinds,4])
    logg_func=interp1d(ts,data_bf98[cinds,3]-2.0)
    logReff_func=lambda t:0.5*(np.log10(GCONST*Mb*MSUN)-logg_func(t))-np.log10(RSUN)
    logReff2_func=lambda t:0.5*(logL_func(t)-4*(np.log10(Teff_func(t))-np.log10(5770.0)))
    #print logL_func(0.1)
    #print logg_func(0.1)
    #print logReff_func(0.1)
    #print logReff2_func(0.1)
    #exit(0)

    datapoint="M_%.2f-Z_%.0e-C_%s"%(M,Z,cond)
    PRINTOUT("Data point: %s"%datapoint)
    try:
        data=np.loadtxt("tests/comparisons/%s.txt"%(datapoint))
    except:
        PRINTERR("No BaSTI data available for point %s"%datapoint)
        exit(0)

    zsvec=chooseZsvecSingle(Z)
    num=loadIsochroneSet(Zs=zsvec,verbose=True)

    ts=10**(data[:,0])/1E9
    tsvec=[]
    evol=stack(6)
    barf=stack(4)
    for i in xrange(len(ts)-1):
        j=i+1
        t=ts[j]
        try:
            barf+=[Teff_func(t),10**logReff_func(t),10**logReff2_func(t),10**logL_func(t)]
        except:break
        iso=StellarGTRL(Z,M,t)
        if iso[0]<0:
            print "Maximum age: %.2f"%t
            break
        evol+=[t,iso[1],iso[2],iso[3],10**data[j,3],10**data[j,2]]

    ts=evol.array[:,0]

    Tpad=evol.array[:,1]
    Rpad=evol.array[:,2]
    Lpad=evol.array[:,3]

    Tbas=evol.array[:,4]
    Lbas=evol.array[:,5]
    Rbas=np.sqrt(Lbas/(Tbas/5770)**4)

    Tbrf=barf.array[:,0]
    Rbrf=barf.array[:,1]
    Rbrf2=barf.array[:,2]
    Lbrf=barf.array[:,3]

    Tmin=min(min(Tpad),min(Tbas),min(Tbrf),Tobs)
    Tmax=max(max(Tpad),max(Tbas),max(Tbrf),Tobs)
    Lmin=min(min(Lpad),min(Lbas),min(Lbrf),Lobs)
    Lmax=max(max(Lpad),max(Lbas),max(Lbrf),Lobs)
    Rmin=min(min(Rpad),min(Rbas),min(Rbrf),Robs)
    Rmax=max(max(Rpad),max(Rbas),max(Rbrf),Robs)

    title="M=%.2f, Z=%.0e"%(M,Z)

    #############################################################
    #COMPARE TRACK
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    ax.plot(Tpad,Lpad,'b+-',label='PADOVA')
    ax.plot(Tbas,Lbas,'r+-',label='BASTI')
    ax.plot(Tbrf,Lbrf,'g+-',label='BARAFFE')

    ax.plot([Tobs],[Lobs],'o',markersize=10)
    ax.errorbar(Tobs,Lobs,xerr=Terr,yerr=Lerr,linewidth=2)

    ax.legend(loc='best')
    ax.set_yscale("log")
    ax.set_xlabel("Teff")
    ax.set_ylabel("Lbol")

    ax.set_xlim((Tmax,Tmin))
    ax.set_ylim((Lmin,Lmax))

    ax.set_title(title,position=(0.5,1.02))

    fig.savefig("tests/comparisons/compare-track-%s.png"%(datapoint))

    #############################################################
    #COMPARE TEMPERATURE
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    ax.plot(ts,Tpad,'b+-',label='PADOVA')
    ax.plot(ts,Tbas,'r+-',label='BASTI')
    ax.plot(ts,Tbrf,'g+-',label='BARAFFE')

    ax.axhspan(Tobs-Terr,Tobs+Terr,color='k',alpha=0.2)

    ax.legend(loc='best')
    
    ax.set_xscale("log")
    #ax.set_yscale("log")

    ax.set_xlabel("t")
    ax.set_ylabel("Teff")

    ax.set_ylim((Tmin,Tmax))

    ax.set_title(title,position=(0.5,1.02))

    fig.savefig("tests/comparisons/compare-temperature-%s.png"%(datapoint))

    #############################################################
    #COMPARE RADIUS
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    ax.plot(ts,Rpad,'b+-',label='PADOVA')
    ax.plot(ts,Rbas,'r+-',label='BASTI')
    ax.plot(ts,Rbrf2,'g+-',label='BARAFFE')
    ax.plot(ts,Rbrf,'c+-',label='BARAFFE (g)')

    ax.axhspan(Robs-Rerr,Robs+Rerr,color='k',alpha=0.2)

    ax.legend(loc='best')
    ax.set_xscale("log")
    #ax.set_yscale("log")
    ax.set_xlabel("t")
    ax.set_ylabel("R")

    ax.set_ylim((Rmin,min(2.0,Rmax)))

    ax.set_title(title,position=(0.5,1.02))

    fig.savefig("tests/comparisons/compare-radius-%s.png"%(datapoint))

    #############################################################
    #COMPARE LUMINOSITY
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    ax.plot(ts,Lpad,'b+-',label='PADOVA')
    ax.plot(ts,Lbas,'r+-',label='BASTI')
    ax.plot(ts,Lbrf,'g+-',label='BARAFFE')

    ax.axhspan(Lobs-Lerr,Lobs+Lerr,color='k',alpha=0.2)

    ax.legend(loc='best')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("t")
    ax.set_ylabel("Lbol")

    ax.set_ylim((Lmin,Lmax))

    ax.set_title(title,position=(0.5,1.02))

    fig.savefig("tests/comparisons/compare-luminosity-%s.png"%(datapoint))


def findTrack(model,Z,M,verbose=False):
    modeldir=DATA_DIR+"Stars/EvoTracks/%s"%model
    if verbose:PRINTOUT("Looking for closest track to Z = %.5f and M = %.2f in model '%s'..."%(Z,M,model))

    if not DIREXISTS(modeldir):
        PRINTERR("Model '%s' not found."%modeldir)
        exit(0)

    #FIND THE CLOSEST Z
    Zdirs=listDirectory(modeldir,"Z*")
    Zvals=np.array([])
    for Zdir in Zdirs:
        matches=re.search("/Z(.+)",Zdir)
        Zval=float(matches.group(1))
        Zvals=np.append([Zval],Zvals)

    dlogZ=np.abs(np.log10(Z)-np.log10(Zvals))
    iZ=dlogZ.argmin()
    Zfind=Zvals[iZ]
    dZfind=dlogZ[iZ]/abs(np.log10(Z))
    Zdir=modeldir+"/Z%.2e"%Zfind
    if verbose:
        PRINTOUT("Closest metallicity in model: Z = %.5f (closeness %.1e)."%(Zfind,dZfind))
        
    #FIND THE CLOSEST M
    Mdirs=listDirectory(Zdir,"M_*")
    Mvals=np.array([])
    for Mdir in Mdirs:
        matches=re.search("/M_(.+)\.dat",Mdir)
        Mval=float(matches.group(1))
        Mvals=np.append([Mval],Mvals)

    dM=np.abs(M-Mvals)
    iM=dM.argmin()
    Mfind=Mvals[iM]
    dMfind=dM[iM]/M
    if verbose:
        PRINTOUT("Closest mass in model: M = %.2f (closeness %.1e)."%(Mfind,dMfind))

    #TRACK LOADING ROUTINE
    track=loadConf(modeldir+"/track.py")
    
    #READ EVOLUTIONARY TRACK
    try:
        tfile=Zdir+"/M_%.2f.dat"%Mfind
        datatrack=track.getTrack(Zfind,Mfind,tfile)
    except:
        tfile=Zdir+"/M_%.3f.dat"%Mfind
        datatrack=track.getTrack(Zfind,Mfind,tfile)

    return [Zfind,dZfind,Mfind,dMfind],datatrack

def loadModel():
    Z=0.005
    M=0.7
    #model="BASTI"
    #model="PARSEC"
    model="BCA98"
    #model="YZVAR"
    tfind,datatrack=findTrack(model,Z,M,verbose=False)
    
    ts=datatrack["qt_fun"](datatrack["qt"])/1E9
    title="Model %s, Z = %.5f, M = %.2f"%(model,tfind[0],tfind[2])
    suffix="Z_%.2e-M_%.2f-%s.png"%(tfind[0],tfind[2],model)

    #############################################################
    #TEMPERATURE PLOT
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    Teff=datatrack["qT_fun"](datatrack["qT"])
    ax.plot(ts,Teff)

    ax.set_xscale("log")
    #ax.set_yscale("log")

    tmin,tmax=ax.get_xlim()
    ax.set_xlim((1E-3,13.7))

    ax.set_xlabel("t")
    ax.set_ylabel("Teff")
    ax.set_title(title,position=(0.5,1.02))

    ax.grid(which='both')
    #ax.legend(loc='best')
    fig.savefig("tests/models-Teff-%s.png"%suffix)

    #############################################################
    #LUMINOSITY PLOT
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    L=datatrack["qL_fun"](datatrack["qL"])
    ax.plot(ts,L)

    ax.set_xscale("log")
    ax.set_yscale("log")

    tmin,tmax=ax.get_xlim()
    ax.set_xlim((1E-3,13.7))

    ax.set_xlabel("t")
    ax.set_ylabel("L")
    ax.set_title(title,position=(0.5,1.02))

    ax.grid(which='both')
    #ax.legend(loc='best')
    fig.savefig("tests/models-L-%s.png"%suffix)

    #############################################################
    #RADIUS PLOT
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    R=datatrack["qR_fun"](datatrack["qR"])
    ax.plot(ts,R)

    ax.set_xscale("log")
    ax.set_yscale("log")

    tmin,tmax=ax.get_xlim()
    ax.set_xlim((1E-3,13.7))

    ax.set_xlabel("t")
    ax.set_ylabel("R")
    ax.set_title(title,position=(0.5,1.02))

    ax.grid(which='both')
    #ax.legend(loc='best')
    fig.savefig("tests/models-R-%s.png"%suffix)

    #############################################################
    #GRAVITY
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    logg=np.log10(datatrack["qg_fun"](datatrack["qg"])*100)
    ax.plot(ts,logg,'b+-')

    ax.set_xscale("log")
    ax.set_yscale("log")

    tmin,tmax=ax.get_xlim()
    ax.set_xlim((1E-3,13.7))

    ax.set_xlabel("t")
    ax.set_ylabel("g")
    ax.set_title(title,position=(0.5,1.02))
    ax.grid(which='both')

    #ax.legend(loc='best')
    fig.savefig("tests/models-logg-%s.png"%suffix)

def testStellarWind():
    M=1.0
    Z=0.0152
    FeH=0.0
    t=1.00
    model="BCA98"
    tfind,datatrack=findTrack(model,Z,M,verbose=False)
    ts=datatrack["qt_fun"](datatrack["qt"])/1E9
    Rs=datatrack["qR_fun"](datatrack["qR"])
    Ts=datatrack["qT_fun"](datatrack["qT"])
    Ls=datatrack["qL_fun"](datatrack["qL"])
    Rfunc=interp1d(ts,Rs)
    Tfunc=interp1d(ts,Ts)
    Lfunc=interp1d(ts,Ls)
    R=Rfunc(t)
    T=Tfunc(t) 
    L=Lfunc(t)
    Prot=PSUN*(t/4.56)**0.5/DAY

    tauc,fstar,Bequi,Bphoto,BTR,Rossby,Mdotcr,Mdot_hot,Mdot_cold,MATR=\
        pyBoreas(M,R,L,Prot,FeH)

    lin,lsun,lout=HZ(L,T,lin='recent venus',lout='early mars')

    wcranmer=stack(4)
    wgreissmeier=stack(4)
    rs=np.logspace(np.log10(10*R*RSUN/AU),np.log10(lout),50)
    #rs=np.logspace(np.log10(lin),np.log10(lout),50)
    for r in rs:

        v,n=stellarWind(M,R,Mdotcr,r,type='Terminal')
        wcranmer+=[v,n,n*v,0.5*MP*n*v**2]
        #print "Cranmer (n,v),Mdot: ",n,v,Mdotcr

        v,n=vnGreissmeier(r,t,M,R)
        Mdot=MP*n*v*(4*PI*r**2)*YEAR/MSUN
        wgreissmeier+=[v,n,n*v,0.5*MP*n*v**2]
        #print "Greissmeier (n,v),Mdot: ",n,v,Mdot

    wcranmer=toStack(rs)|wcranmer
    wgreissmeier=toStack(rs)|wgreissmeier

    fig=plt.figure()
    l=0.1;b=0.1;w=0.8;h=0.8
    ax=fig.add_axes([l,b,w,h])
    ax.plot(wcranmer[:,0],wcranmer[:,2],label='Cranmer')
    ax.plot(wgreissmeier[:,0],wgreissmeier[:,2],label='Greissmeier')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("r(AU)")
    ax.set_ylabel("n (1/m$^3$)")
    ax.plot([1.0],[6.8E6],'+',markersize=20)
    ax.set_xlim((rs[0],rs[-1]))
    ax.legend(loc='best')
    fig.savefig("tests/wind-n.png")

    fig=plt.figure()
    l=0.1;b=0.1;w=0.8;h=0.8
    ax=fig.add_axes([l,b,w,h])
    ax.plot(wcranmer[:,0],wcranmer[:,1],label='Cranmer')
    ax.plot(wgreissmeier[:,0],wgreissmeier[:,1],label='Greissmeier')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("v(m/s)")
    ax.plot([1.0],[4.25E5],'+',markersize=20)
    ax.set_xlim((rs[0],rs[-1]))
    ax.legend(loc='best')
    fig.savefig("tests/wind-v.png")

    fig=plt.figure()
    l=0.1;b=0.1;w=0.8;h=0.8
    ax=fig.add_axes([l,b,w,h])
    ax.plot(wcranmer[:,0],wcranmer[:,3],label='Cranmer')
    ax.plot(wgreissmeier[:,0],wgreissmeier[:,3],label='Greissmeier')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("F (1/s m$^3$)")
    ax.plot([1.0],[6.8E6*4.25E5],'+',markersize=20)
    ax.set_xlim((rs[0],rs[-1]))
    ax.legend(loc='best')
    fig.savefig("tests/wind-F.png")

    fig=plt.figure()
    l=0.1;b=0.1;w=0.8;h=0.8
    ax=fig.add_axes([l,b,w,h])
    ax.plot(wcranmer[:,0],wcranmer[:,4],label='Cranmer')
    ax.plot(wgreissmeier[:,0],wgreissmeier[:,4],label='Greissmeier')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("F (Pa)")
    ax.plot([1.0],[0.5*MP*6.8E6*4.25E5**2],'+',markersize=20)
    ax.set_xlim((rs[0],rs[-1]))
    ax.legend(loc='best')
    fig.savefig("tests/wind-P.png")

def evolutionaryTracksKCBHZP():

    #LOAD CATALOGUE
    fpickle="BHM/data/BHMcat/BHMcat.pickle"
    fl=open(fpickle,'r')
    systems=pickle.load(fl)
    fl.close()

    #TEST MODEL
    model="PARSEC"
    #model="BCA98"
    #model="BASTI"
    #model="YZVAR"
    print "Model: %s"%model

    ###############################
    #SYSTEM: 
    ###############################
    #STAR
    star=2

    #kEPLER 16
    #systemid="BHMCatS0001D"
    #KEPLER 47
    #systemid="BHMCatS0005D"
    #KIC 9632895
    systemid="BHMCatS0008D"

    system=systems[systemid]
    
    starid=system["star%d_str_StarID"%star]
    Mobs=system["star%d_M"%star]
    FeH=system["binary_FeHobs"]
    Zobs=scaledZ(FeH)
    Tobs=system["star%d_T"%star];Terr=system["star%d_Terr"%star];
    Robs=system["star%d_R"%star];Rerr=system["star%d_Rerr"%star];
    Lobs=Robs**2*(Tobs/TSUN)**4
    Lerr=Lobs*(2*Rerr/Robs+4*Terr/Tobs)

    print "Input system properties:"
    print "Star : %s"%starid
    print "\tM = %.2f, [Fe/H] = %.2f"%(Mobs,FeH)
    print "\tZ (scaled) = %.5f"%(Zobs)
    print "\tT = %.2f +/- %.2f"%(Tobs,Terr)
    print "\tR = %.2f +/- %.4f"%(Robs,Rerr)
    print "\tL = %.2f +/- %.4f"%(Lobs,Lerr)
    
    ###############################
    #FIND CLOSEST TRACKS
    ###############################
    track_finds,track_data=findTracks(model,Zobs,Mobs,verbose=False)

    #############################################################
    #HR TRACK
    #############################################################
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])

    Tarr=[]
    Rarr=[]
    if Tobs>0:
        ax.axvline(Tobs,color='g',linewidth=2)
        ax.axvspan(Tobs-Terr,Tobs+Terr,color='g',alpha=0.2)
        Tarr=[[Tobs]]
    if Robs>0:
        ax.axhline(Robs,color='g',linewidth=2)
        ax.axhspan(Robs-Rerr,Robs+Rerr,color='g',alpha=0.2)
        Rarr=[[Robs]]

    colors=['r','k','b']
    styles=['--','-',':']
    for i in xrange(len(track_finds)):
        j=i%3
        k=int(i/3)

        Z,M=track_finds[i]
        track=trackArrays(track_data[i])
        print "Plotting track for Z = %.4f, M = %.2f..."%(Z,M)

        ts=track.ts/1E9
        tmin=ts[0]
        tmax=ts[-1]

        Ts=track.T
        Rs=track.R
        
        Tarr+=[Ts]
        Rarr+=[Rs]

        style=dict(color=colors[k],markersize=10)
        ax.plot(Ts,Rs,'-',color=colors[k],linestyle=styles[j],label='Z=%.4f,M=%.2f'%(Z,M))
        ax.plot([Ts[0]],[Rs[0]],'v',**style)
        ax.plot([Ts[-1]],[Rs[-1]],'^',**style)
    
    Tmin,Tmax=minmaxArrays(Tarr)
    Rmin,Rmax=minmaxArrays(Rarr)

    fac=1.1
    ax.set_xlim((fac*Tmax,1/fac*Tmin))
    ax.set_ylim((1/fac*Rmin,fac*Rmax))

    #ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(r"$T_{\rm eff}$ (K)")
    ax.set_ylabel("$R/R_\odot$")
    
    ax.set_title("Star %s, M = %.2f, Z = %.4f, Model %s"%(starid,Mobs,Zobs,model),
                 position=(0.5,1.02),fontsize=11)

    ax.grid(which='both')
    ax.legend(loc='best',prop=dict(size=10))

    fmodel="tests/%s-model_%s.png"%(starid.replace(" ","_"),model)
    print "Saving file %s..."%fmodel
    fig.savefig(fmodel)
 
def coreEnvelopeCoupling():

    #INPUT PARAMETERS
    model="PARSEC"
    star=dict2obj(dict())

    star.Pini=10.0
    star.M=0.90
    star.Z=0.0152
    star.taudisk=10E-3
    star.K1=1.0*4
    star.tauc=60.0
    #star.Kw=5.5E39
    star.Kw=500E39
    star.wsat=30.0
    star.taucont=0.1
    star.n=3./7
    star.a=1.0
    
    track_find,track_data=findTrack(model,star.Z,star.M,verbose=False)
    track=trackFunctions(track_data)
    
    ###################################################
    #MOI EVOLUTION
    ###################################################
    print "MoI evolution..."
    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    Ms=np.linspace(0.1,2.0,10.0)
    ts=np.logspace(np.log10(1E-3),np.log10(1.0E-2),100)
    for M in Ms:
        MoIs=[]
        for t in ts:
            MoIs+=[stellarMoIt(M,t)]
        ax.plot(ts,MoIs,label='M = %.2f'%M)
    ax.set_xscale("log")
    ax.set_ylabel("$r_g^2$")
    ax.set_xlabel(r"$\tau$ (Gyr)")
    ax.legend(loc="best")
    fig.savefig("tests/rotevol-MoI.png")

    ###################################################
    #ROTATIONAL INTEGRATION
    ###################################################
    wini=2*PI/(star.Pini*DAY)
    star.tau_ms=4.5
    star.Rfunc=lambda t:track.R(t*GIGA)
    star.Tfunc=lambda t:track.T(t*GIGA)
    star.Lfunc=lambda t:track.L(t*GIGA)
    star.FeH=0.0
    Nfine=100
    ts=np.logspace(np.log10(1.0E-3),np.log10(5.0),Nfine)

    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    #INERTIA MOMENTUM
    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    print "I evolution..."
    Rs=[]
    for t in ts:
        R=track.R(t*GIGA)
        Rs+=[R]
    Rfunc=interp1d(ts,Rs,kind='slinear')
    dRdts=[0]
    for i in range(1,Nfine-1):
        dt=(ts[i+1]-ts[i-1])/4
        dRdts+=[(Rfunc(ts[i]+dt)-Rfunc(ts[i]-dt))/(2*dt)]
    dRdts[0]=dRdts[1]
    dRdts+=[dRdts[-1]]

    Ievo=[]
    star.taurad=tauRad(star.M)
    #MoI=stellarMoI(star.M)
    for i in range(Nfine):
        t=ts[i]
        R=Rs[i]
        dRdt=dRdts[i]
        MoI=stellarMoIt(star.M,t)
        facI=MoI*star.M
        I=facI*R**2
        dIdt=2**facI*R*dRdt
        gamma=gammaInertia(star.M,t)
        beta_conv=1/(1+gamma)
        beta_core=gamma*beta_conv
        Ievo+=[[I,dIdt,beta_conv*I,beta_conv*dIdt,beta_core*I,beta_core*dIdt]]

    Ievo=np.array(Ievo)
    star.Ifunc=interp1d(ts,Ievo[:,0],kind='slinear')
    star.dIdtfunc=interp1d(ts,Ievo[:,1],kind='slinear')

    fig=plt.figure(figsize=(8,12))
    axI=fig.add_axes([0.1,0.05,0.85,0.43])
    axdI=fig.add_axes([0.1,0.52,0.85,0.43])

    axI.plot(ts,np.log10(Ievo[:,0]*MSUN*RSUN**2),label=r'Total')
    axI.plot(ts,np.log10(Ievo[:,2]*MSUN*RSUN**2),label=r'Convective')
    #axI.plot(ts,np.log10(Ievo[:,4]*MSUN*RSUN**2),label=r'Core')

    axdI.plot(ts,np.abs(Ievo[:,1]/Ievo[:,0]/GYR),label=r'Total')
    axdI.plot(ts,np.abs(Ievo[:,3]/Ievo[:,2]/GYR),label=r'Convective')
    #axdI.plot(ts,np.abs(Ievo[:,5]/Ievo[:,4]/GYR),label=r'Core')

    axdI.set_yscale("log")

    axI.set_ylabel("$\log I$")
    axdI.set_ylabel("$dI/dt/I$")

    axI.legend(loc="best")
    axdI.legend(loc="best")
    axI.set_xlabel(r"$\tau$ (Gyr)")
    for ax in axI,axdI:
        ax.grid(which="both")
        ax.set_xscale("log")
    fig.savefig("tests/rotevol-IEvol.png")

    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    #ROTATIONAL EVOLUTION INCLUDING DIFFERENTIAL ROTATION EFFECTS
    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    print "Rotational evolution including differential rotation effects..."

    #CHABOYER, NO DIFFERENTIAL ROTATION
    rotpars=dict(\
        star=star,
        starf=None,binary=None,
        taudisk=star.taudisk,
        model='Kawaler',
        Kw=star.Kw,
        wsat=star.wsat,
        tauc=star.tauc,
        K1=star.K1,
        n=star.n,
        a=star.a,
        taucont=star.taucont,
        qdifr=True,
        qcont=True
        )

    """
    t=4.57
    wini=OMEGASUN
    Omega_ini=np.array([wini,wini])
    output=rotationalAccelerationFull(Omega_ini,t*GYR,rotpars,full=True,verbose=True)
    exit(0)
    #"""
    #star.Pini=1.0
    #wini=2*PI/(star.Pini*DAY)
    #Omega_ini=np.array([wini,2*wini])

    Omega_ini=np.array([wini,wini])
    #ts=ts[ts>=0.1]
    ws=odeint(rotationalAccelerationFull,Omega_ini,ts*GYR,args=(rotpars,))

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(ts,ws[:,0]/OMEGASUN,'r-')
    ax.plot(ts,ws[:,1]/OMEGASUN,'b--')
    ax.plot([4.57],[1.0],'o',color='k',markersize=10)
    ax.plot(ts,1.0*(ts/TAGE)**-0.5,'k-')
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel(r"$\Omega/\Omega_\odot$")
    ax.set_xlabel(r"$\tau$ (Gyr)")
    #ax.legend(loc="best")
    ax.grid(which="both")
    fig.savefig("tests/rotevol-OmegaEvol.png")

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(ts,2*PI/ws[:,0]/DAY,'r-')
    ax.plot(ts,2*PI/ws[:,1]/DAY,'b--')
    ax.plot([4.57],[PSUN/DAY],'o',color='k',markersize=10)
    ax.plot(ts,PSUN/DAY*(ts/TAGE)**0.5,'k-')
    ax.set_xscale("log")
    ax.set_ylabel(r"$P$ (days)")
    ax.set_xlabel(r"$\tau$ (Gyr)")
    #ax.legend(loc="best")
    ax.grid(which="both")
    fig.savefig("tests/rotevol-PEvol.png")
    exit(0)

    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    #ROTATIONAL EVOLUTION
    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    print "Rotational evolution..."

    rotpars=dict(\
        star=star,
        starf=None,binary=None,
        taudisk=0.01,
        Kw=1.0,
        wsat=1.0
        )
    ws=odeint(rotationalAcceleration,wini,ts*GYR,args=(rotpars,))

    fig=plt.figure()
    ax=fig.add_axes([0.1,0.1,0.8,0.8])
    ax.plot(ts,ws/OMEGASUN)
    ax.plot([4.57],[1.0],'o',color='k',markersize=10)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylabel("$\Omega/\Omega_\odot$")
    ax.set_xlabel("$\tau$ (Gyr)")
    #ax.legend(loc="best")
    ax.grid(which="both")
    fig.savefig("tests/rotevol-OmegaEvol.png")


#MomentOfInertia()
#evolutionaryTrack()
#loadModel()
#testStellarWind()
#evolutionaryTracksKCBHZP()
coreEnvelopeCoupling()
