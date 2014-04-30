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
Z=float(argv[1])
M1=float(argv[2])
M2=float(argv[3])
e=float(argv[4])
Pbin=float(argv[5])
TAU=float(argv[6])
Mp=float(argv[7])
ap=float(argv[8])
tau1=float(argv[9])
qintegration=int(argv[10])
sessid=argv[11]
zsvec=argv[12]

suffix="%.2f%.2f%.3f%.2f-%s"%(M1,M2,e,Pbin,sessid)
fout=open(TMPDIR+"output-%s.log"%sessid,"w")

############################################################
#PREPARATION
############################################################
plt.close("all")

############################################################
#LOAD DATA
############################################################
exec("num=loadIsochroneSet(verbose=True,Zs=%s)"%zsvec)

############################################################
#ROUTINES
############################################################
def Run():

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CONSTANT PROPERTIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    qtid=1
    qML=1

    #VERBOSITY
    verbose=False

    #PAUSE CALCULATION
    pause=False

    #STELLAR METALLICITY

    #BIRTH AGE
    tau0=0.01
    tauM=12.5
    
    #INITIAL PERIOD OF ROTATION ABOVE DISRUPTION
    PFAC=2
    
    #HZ ZONE AGE
    tauHZ=TAU

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #BINARY PROPERTIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    g1,T1,R1,L1=StellarGTRL(Z,M1,TAU)
    Rmin1,Rmax1=minmaxRadius(Z,M1,tmax=TAU)
    Pmax1=maxPeriod(M1,R1)
    Pini1=10*Pmax1
    Prot1=Prot(TAU,Ms=M1,Rs=R1)/DAY
    g1i,T1i,R1i,L1i=StellarGTRL(Z,M1,tau0)
    Pini1=PFAC*Prot(tau0,Ms=M1,Rs=R1i)/DAY
    W1o=2*pi/Pini1

    print>>fout,g1,T1,R1,L1,Rmin1,Rmax1,Pini1,Prot1

    gZ1,TZ1,RZ1,LZ1=StellarGTRL(Z,M1,tauHZ)
    lin1,aE1,lout1=HZ2013(LZ1,TZ1)
    aHZ1=(lin1+lout1)/2

    print>>fout,lin1,aE1,aHZ1,lout1

    g2,T2,R2,L2=StellarGTRL(Z,M2,TAU)
    Rmin2,Rmax2=minmaxRadius(Z,M2,tmax=TAU)
    Pmax2=maxPeriod(M2,R2)
    Pini2=10*Pmax2
    Prot2=Prot(TAU,Ms=M2,Rs=R2)/DAY
    g2i,T2i,R2i,L2i=StellarGTRL(Z,M2,tau0)
    Pini2=PFAC*Prot(tau0,Ms=M2,Rs=R2i)/DAY
    W2o=2*pi/Pini2

    print>>fout,g2,T2,R2,L2,Rmin2,Rmax2,Pini2,Prot2

    gZ2,TZ2,RZ2,LZ2=StellarGTRL(Z,M2,tauHZ)
    lin2,aE2,lout2=HZ2013(LZ2,TZ2)
    aHZ2=(lin2+lout2)/2

    print>>fout,lin2,aE2,aHZ2,lout2
    
    nbin=2*np.pi/Pbin
    abin=aKepler(Pbin,M1,M2)
    mu=M2/(M1+M2)
    acrit=aCritical(mu,abin,e)

    nsync=nSync(e)
    Psync=Pbin/nsync
    Wsync=nbin*nsync

    print>>fout,abin,acrit,nsync,Psync

    lin,aE,lout=HZbin4(M2/M1,LZ1,LZ2,TZ1,abin)
    aHZ=(lin+lout)/2

    print>>fout,lin,aE,aHZ,lout
    
    d="\t"*1
    print "Binary properties:"
    print d,"a = %f AU"%abin
    print d,"ac = %f AU"%acrit
    print d,"e = %f"%e
    print d,"P = %f days"%Pbin
    print d,"n = %f rad/day"%nbin
    print d,"Psync = %f days"%Psync
    print d,"tau = %f Gyr"%TAU
    print d,"HZ = ",lin,aE,aHZ,lout

    print d,"Main component:"
    d="\t"*2
    print d,"Z = %f"%Z
    print d,"M = %f Msun"%M1
    print d,"T = %f K"%T1
    print d,"R = %f Rsun"%R1
    print d,"Rmin,Rmax = %f,%f Rsun"%(Rmin1,Rmax1)
    print d,"L = %f Lsun"%L1
    print d,"Pmax = %f days"%Pmax1
    print d,"Pini = %f days"%Pini1
    print d,"Omega_ini = %f rad/day"%W1o
    print d,"Prot = %f days"%Prot1
    print d,"HZ = ",lin1,aE1,aHZ1,lout1
    d="\t"*1
    print d,"Secondary component:"
    d="\t"*2
    print d,"Z = %f"%Z
    print d,"M = %f Msun"%M2
    print d,"T = %f K"%T2
    print d,"R = %f Rsun"%R2
    print d,"Rmin,Rmax = %f,%f Rsun"%(Rmin2,Rmax2)
    print d,"L = %f Lsun"%L2
    print d,"Pmax = %f days"%Pmax2
    print d,"Pini = %f days"%Pini2
    print d,"Omega_ini = %f rad/day"%W2o
    print d,"Prot = %f days"%Prot2
    print

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #ESTIMATED SYNC. TIME
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #NOTE: TO CONVER W TO SI YOU SHOULD DIVIDE BY DAYS
    acc1=tidalAcceleration(M1,R1i,L1i,M2,abin,e,nbin/DAY,W1o/DAY)
    tsync1=-(W1o/DAY)/acc1/GYR
    
    acc2=tidalAcceleration(M2,R2i,L2i,M1,abin,e,nbin/DAY,W2o/DAY)
    tsync2=-(W2o/DAY)/acc1/GYR

    d="\t"*0
    print d,"Tidal properties:"
    d="\t"*1
    print d,"Main component:"
    d="\t"*2
    print d,"Hut synchronization time: %e Gyr"%(tsync1)
    print d,"Hut tidal acceleration: %e s^-1"%(acc1)
    d="\t"*1
    print d,"Secondary component:"
    d="\t"*2
    print d,"Hut synchronization time: %e Gyr"%(tsync2)
    print d,"Hut tidal acceleration: %e s^-1"%(acc2)
    print 

    print>>fout,tsync1,tsync2

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #FIND OPTIMUM POINT INSIDE HABITABLE ZONE
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    tauvec=np.linspace(0.1,tauM,200)
    lins=[]
    louts=[]
    slins=[]
    slouts=[]
    i=0
    for tau in tauvec:
        #print "Time: %e"%tau
        g1e,T1e,R1e,L1e=StellarGTRL(Z,M1,tau)
        #print "\tStar 1: g,T,R,L=",g1,T1,R1,L1
        g2e,T2e,R2e,L2e=StellarGTRL(Z,M2,tau)
        #print "\tStar 2: g,T,R,L=",g2,T2,R2,L2
        try:
            lin1e,aE1e,lout1e=HZ2013(L1e,T1e)
            #print "\tPrimary HZ=",lin1,aE1,lout1
        except:
            #print "The most massive star has passed away at tau = %e"%tau
            break
        line,aEe,loute=HZbin4(M2/M1,L1e,L2e,T1e,abin)
        tausys=tau
        lins+=[line]
        louts+=[loute]
        slins+=[lin1e]
        slouts+=[lout1e]
        i+=1
    tauvec=tauvec[:i]
    lins=np.array(lins)
    louts=np.array(louts)
    print "Maximum age of the system: %.3f"%(tausys)
 
    #FIND CONTINUOUS HABITABLE ZONE
    dlins=np.log10(lins[1::])-np.log10(lins[:-1:])
    dlins=np.append([0],dlins)
    imax=-1
    epsmax=0
    dlinold=dlins[-1]
    for i in arange(10,len(dlins))[::-3]:
        eps=2*abs(dlins[i]-dlinold)/(dlins[i]+dlinold)
        #print tauvec[i],eps,epsmax
        if eps>epsmax:
            imax=i
            epsmax=eps
        dlinold=dlins[i]
        if tauvec[i]<tausys/2:break
    lincont=lins[imax]
    loutcont=min(louts)

    print "Continuous HZ: ",lincont,loutcont

    #PLOT HABITABLE ZONE
    fig=plt.figure()
    plt.axhline(loutcont,color='k',linewidth=3)
    plt.plot([],[],'k-',linewidth=3,label='Optimum distance')
    plt.axhspan(lincont,loutcont,color='k',alpha=0.3)

    plt.text(tauvec[-1]/2,1.02*lincont,'Continuous Habitable Zone',
             horizontalalignment='center',fontsize=18)

    plt.text(1.05*tauvec[0],0.98*loutcont,'%.2f AU'%loutcont,
             horizontalalignment='left',
             verticalalignment='top',
             fontsize=12)
    plt.text(1.05*tauvec[0],1.02*lincont,'%.2f AU'%lincont,
             horizontalalignment='left',
             verticalalignment='bottom',
             fontsize=12)

    plt.xlabel(r"$\tau$ (Gyr)")
    plt.xlabel(r"$a$ (AU)")

    plt.fill_between(tauvec,lins,louts,color='g',alpha=0.3)
    plt.plot(tauvec,lins,'r-',linewidth=2,label='Recent Venus')
    plt.plot(tauvec,louts,'b-',linewidth=2,label='Early Mars')
    plt.plot(tauvec,slins,'r--',linewidth=2)
    plt.plot(tauvec,slouts,'b--',linewidth=2)
    plt.yscale('log')
    logTickLabels(plt.gca(),-1,2,(1,),frm='%.1f',axis='y',notation='normal',fontsize=12)
    plt.ylim((min(lins),max(louts)))
    plt.xlim((tauvec[0],tauvec[-1]))
    plt.legend(loc='upper left')
    plt.title(r"$M_1=%.3f$, $M_2=%.3f$, $a_{\rm bin}=%.3f$ AU, $e=%.3f$, $P_{\rm bin}=%.3f$ days"%(M1,M2,abin,e,Pbin),position=(0.5,1.02),fontsize=16)
    plt.savefig(TMPDIR+"/HZevol-%s.png"%suffix)
    
    print>>fout,tausys,lincont,loutcont

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #PLOT HABITABLE ZONE AND BINARY ORBIT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    rang=1.2*lout
    fig=plt.figure(figsize=(8,8))
    ax=fig.add_axes([0.01,0.01,0.98,0.98])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    #CENTER
    #ax.plot([0],[0],'k+',ms=10,zorder=100)

    #ORBIT
    MTOT=M1+M2
    f=np.linspace(0,2*pi,100)
    r=abin*(1-e**2)/(1+e*cos(f))
    x2=-M1/MTOT*r*cos(f)
    y2=-M1/MTOT*r*sin(f)
    x1=M2/MTOT*r*cos(f)
    y1=M2/MTOT*r*sin(f)
    ax.plot(x1,y1,'k-',linewidth=1,zorder=20)
    ax.plot(x2,y2,'k-',linewidth=1,zorder=20)
    C1=Circle((x1[0],y1[0]),rang/90,
              facecolor='k',alpha=1.0,linewidth=0,zorder=50)
    C2=Circle((x2[0],y2[0]),rang/90,
              facecolor='k',alpha=1.0,linewidth=0,zorder=50)
    ax.add_patch(C1)
    ax.add_patch(C2)

    #CRITICAL ORBIT
    aCR=Circle((0,0),acrit,facecolor='none',edgecolor='k',
                linewidth=2,linestyle='dashed',zorder=20)
    ax.add_patch(aCR)

    #INNER
    lini,aEi,louti=HZbin4(M2/M1,LZ1,LZ2,TZ1,abin,
                          crits=['runaway greenhouse','maximum greenhouse'])
    aHZi=(lini+louti)/2
    outHZ=Circle((0,0),louti,facecolor='g',alpha=0.3,linewidth=2)
    ax.add_patch(outHZ)
    inHZ=Circle((0,0),lini,facecolor='r',edgecolor='r',alpha=0.2,
                linewidth=2,zorder=10)
    ax.add_patch(inHZ)

    #OUTER
    lino,aEo,louto=HZbin4(M2/M1,LZ1,LZ2,TZ1,abin,
                       crits=['recent venus','early mars'])
    aHZo=(lino+louto)/2
    outHZ=Circle((0,0),louto,facecolor='g',alpha=0.3,linewidth=2)
    ax.add_patch(outHZ)
    inHZ=Circle((0,0),lino,facecolor='w',edgecolor='r',
                linewidth=2,zorder=10)
    ax.add_patch(inHZ)

    #TITLE
    ax.set_title(r"$M_1=%.3f$, $M_2=%.3f$, $a_{\rm bin}=%.3f$ AU, $e=%.3f$, $P_{\rm bin}=%.3f$ days"%(M1,M2,abin,e,Pbin),position=(0.5,0.95),fontsize=16)
    ax.text(0.5,0.02,r"$a_{\rm crit}=%.2f$ AU, $l_{\rm in,RV}$=%.2f AU, $l_{\rm in,RG}$=%.2f AU, $l_{\rm out,MG}$=%.2f AU, $l_{\rm out,EM}$=%.2f AU"%(acrit,lino,lini,louti,louto),transform=ax.transAxes,horizontalalignment='center',fontsize=14)

    ax.set_xlim((-rang,rang))
    ax.set_ylim((-rang,rang))

    plt.savefig(TMPDIR+"/HZ-%s.png"%suffix)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CHECK IF INTEGRATION IS REQUIRED
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not qintegration:
        fout.close()
        exit(0)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #INTEGRATION RANGE
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    dt=min(1E-3,min(tsync1,tsync2)/10)
    nmax=tau1/dt
    tau_vec=np.arange(tau0+dt,tau1,dt)
    ntau=len(tau_vec)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #MASSLOSS FIT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    suffix1="%.2f"%(M1)
    suffix2="%.2f"%(M2)
    ffit1=TMPDIR+"solution-%s.txt"%(suffix1)
    ffit2=TMPDIR+"solution-%s.txt"%(suffix2)

    if not fileexists(ffit1):
        Prot_vec=[]
        tvec=tau_vec[::ntau/50]
        ncomp=1
        data1=[]
        for tau in tvec:
            g,T,R,L=StellarGTRL(Z,M1,tau)
            prot=Prot(tau,Ms=M1,Rs=R)/DAY
            data1+=[[tau,prot]]
        data1=np.array(data1)
        def chiSquare(x):
            chisquare=0
            for p in data1:
                t=p[0]
                y=p[1]
                chisquare+=((theoProt(t,x)-y)/theoProt(t,x))**2
            np.savetxt(ffit1,x)
            return chisquare
        xfit1=minimize(chiSquare,[1,1.0,1.0]).x
        plt.figure()
        plt.plot(data1[:,0],data1[:,1],'bo')
        plt.plot(data1[:,0],theoProt(data1[:,0],xfit1),'b-')
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel(r"$\tau$")
        plt.ylabel(r"$P_{\rm rot}$")
        plt.title(r"$M_1$ = %.2f $M_{\rm sun}$"%M1)
        plt.savefig(TMPDIR+"/PeriodFit-%s.png"%suffix1)
    else:
        xfit1=np.loadtxt(ffit1)
        
    if not fileexists(ffit2):
        ncomp=2
        data2=[]
        for tau in tvec:
            g,T,R,L=StellarGTRL(Z,M2,tau)
            prot=Prot(tau,Ms=M2,Rs=R)/DAY
            data2+=[[tau,prot]]
        data2=np.array(data2)
        def chiSquare(x):
            chisquare=0
            for p in data2:
                t=p[0]
                y=p[1]
                chisquare+=((theoProt(t,x)-y)/theoProt(t,x))**2
            np.savetxt(ffit2,x)
            return chisquare
        xfit2=minimize(chiSquare,[1,1.0,1.0]).x
        plt.figure()
        plt.plot(data2[:,0],data2[:,1],'bo')
        plt.plot(data2[:,0],theoProt(data2[:,0],xfit2),'b-')
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel(r"$\tau$")
        plt.ylabel(r"$P_{\rm rot}$")
        plt.title(r"$M_1$ = %.2f $M_{\rm sun}$"%M2)
        plt.savefig(TMPDIR+"/PeriodFit-%s.png"%suffix2)
    else:
        xfit2=np.loadtxt(ffit2)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #TIDAL INTEGRATION
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    W1=W1o/DAY
    W2=W2o/DAY
    P1=2*pi/W1
    P2=2*pi/W2
    d="\t"*0
    print d,"Tidal integration:"
    if verbose:
        d="\t"*1
        print d,"Times: ",tau0,tau1
        print d,"Time step: %e Gyr (%e s)"%(dt,dt*GYR)
        print d,"Initial conditions: W: ",W1*DAY,W2*DAY
        print d,"Initial conditions: P: ",P1/DAY,P2/DAY
        if pause:raw_input()

    i=0
    iper=int(nmax/10)

    tvec=[]
    P1vec=[]
    P2vec=[]

    Prot1vec=[]
    Prot2vec=[]

    acc1_tid_vec=[]
    acc2_tid_vec=[]

    acc1_ML_vec=[]
    acc2_ML_vec=[]

    acc1_vec=[]
    acc2_vec=[]

    RXUVout_vec=[]
    RXUVcen_vec=[]
    RXUVin_vec=[]

    RSWout_vec=[]
    RSWcen_vec=[]
    RSWin_vec=[]

    intFXUVout=0
    intFXUVcen=0
    intFXUVin=0
    intFXUVout_sing=0
    intFXUVcen_sing=0
    intFXUVin_sing=0

    tau_rep=tau_vec[0]

    q1sync=False
    q2sync=False
    tvecX=[]
    for tau in tau_vec:

        #==============================
        #INSTANTANEOUS PROPERTIES
        #==============================
        g1,T1,R1,L1=StellarGTRL(Z,M1,tau)
        g2,T2,R2,L2=StellarGTRL(Z,M2,tau)

        if verbose:
            d="\t"*1
            print d,"Tau:",tau
            d="\t"*2
            print d,"Stellar radius: ",R1,R2
            print d,"Stellar luminosity: ",L1,L2
            if pause:raw_input()

        #==============================
        #TIDAL ACCELERATION
        #==============================
        if qtid:
            acc1_tid=tidalAcceleration(M1,R1,L1,M2,abin,e,nbin/DAY,W1)
            acc2_tid=tidalAcceleration(M2,R2,L2,M1,abin,e,nbin/DAY,W2)
        else:
            acc1_tid=acc2_tid=0

        acc1_tid_vec+=[acc1_tid]
        acc2_tid_vec+=[acc2_tid]

        if verbose:
            d="\t"*2
            print d,"Tidal acceleration:"
            d="\t"*3
            print d,"Main: ",acc1_tid
            print d,"Secondary: ",acc2_tid
            if pause:raw_input()
        
        #==============================
        #MASS-LOSS ACCELERATION
        #==============================
        #COMPUTE THE EFFECTIVE AGE
        if qML:
            tau_rot1=tfromProt(P1/DAY,xfit1)
            tau_rot2=tfromProt(P1/DAY,xfit1)
            dProtdt1=dtheoProt(tau_rot1,xfit1)*DAY/GYR
            dProtdt2=dtheoProt(tau_rot2,xfit2)*DAY/GYR
            acc1_ML=-2*np.pi/P1**2*dProtdt1
            acc2_ML=-2*np.pi/P2**2*dProtdt2
        else:
            acc1_ML=acc2_ML=0

        acc1_ML_vec+=[acc1_ML]
        acc2_ML_vec+=[acc2_ML]

        Prot1vec+=[Prot1]
        Prot2vec+=[Prot1]

        if verbose:
            d="\t"*2
            print d,"Mass-loss acceleration 1:"
            d="\t"*3
            print d,"Instantaneous rotation:",P1/DAY
            print d,"Rotational age:",tau_rot1
            print d,"Time step:",dt
            print d,"Period derivative:",dProtdt1
            print d,"Frequency derivative:",acc1_ML
            d="\t"*2
            print d,"Mass-loss acceleration 2:"
            d="\t"*3
            print d,"Instantaneous rotation:",P2/DAY
            print d,"Rotational age:",tau_rot1
            print d,"Time step: %e Gyr (%e s)"%(dt,dt*GYR)
            print d,"Period derivative:",dProtdt2
            print d,"Frequency derivative:",acc2_ML
            if pause:raw_input()

        #==============================
        #XUV & STELLAR WIND
        #==============================
        if not (i%200):
            #STELLAR XUV LUMINOSITY (INCLUDING TIDAL INTERACTION)
            LXUV1=starLXUV(L1,tau_rot1)
            LXUV2=starLXUV(L2,tau_rot2)
            FXUVout=(LXUV1+LXUV2)/(4*np.pi*(lout*AU*1E2)**2)/PEL
            FXUVcen=(LXUV1+LXUV2)/(4*np.pi*(aHZ*AU*1E2)**2)/PEL
            FXUVin=(LXUV1+LXUV2)/(4*np.pi*(lin*AU*1E2)**2)/PEL
            Pswout,Fswout=binaryWind(lout,tau_rot1,M1,R1,tau_rot2,M2,R2)
            Pswcen,Fswcen=binaryWind(aHZ,tau_rot1,M1,R1,tau_rot2,M2,R2)
            Pswin,Fswin=binaryWind(lin,tau_rot1,M1,R1,tau_rot2,M2,R2)

            #STELLAR XUV LUMINOSITY (NO TIDAL)
            LXUV1=starLXUV(L1,tau_rot1)
            LXUV2=starLXUV(L2,tau_rot2)
            FXUVout=(LXUV1+LXUV2)/(4*np.pi*(lout*AU*1E2)**2)/PEL
            FXUVcen=(LXUV1+LXUV2)/(4*np.pi*(aHZ*AU*1E2)**2)/PEL
            FXUVin=(LXUV1+LXUV2)/(4*np.pi*(lin*AU*1E2)**2)/PEL
            Pswout,Fswout=binaryWind(lout,tau_rot1,M1,R1,tau_rot2,M2,R2)
            Pswcen,Fswcen=binaryWind(aHZ,tau_rot1,M1,R1,tau_rot2,M2,R2)
            Pswin,Fswin=binaryWind(lin,tau_rot1,M1,R1,tau_rot2,M2,R2)
            
            #STELLAR XUV LUMINOSITY (SINGLE STAR)
            LXUV_sing=starLXUV(L1,tau)
            FXUVout_sing=(LXUV_sing)/(4*np.pi*(lout1*AU*1E2)**2)/PEL
            FXUVcen_sing=(LXUV_sing)/(4*np.pi*(aHZ1*AU*1E2)**2)/PEL
            FXUVin_sing=(LXUV_sing)/(4*np.pi*(lin1*AU*1E2)**2)/PEL
            Pswout_sing,Fswout_sing=binaryWind(lout1,tau,M1,R1,-1,-1,-1)
            Pswcen_sing,Fswcen_sing=binaryWind(aHZ1,tau,M1,R1,-1,-1,-1)
            Pswin_sing,Fswin_sing=binaryWind(lin1,tau,M1,R1,-1,-1,-1)

            #TIME VECTOR
            tvecX+=[tau]

            #RATIO
            RXUVout=FXUVout/FXUVout_sing
            RXUVcen=FXUVcen/FXUVcen_sing
            RXUVin=FXUVin/FXUVin_sing

            RFSWout=Fswout/Fswout_sing
            RFSWcen=Fswcen/Fswcen_sing
            RFSWin=Fswin/Fswin_sing

            RXUVout_vec+=[RXUVout]
            RXUVcen_vec+=[RXUVcen]
            RXUVin_vec+=[RXUVin]

            RSWout_vec+=[RFSWout]
            RSWcen_vec+=[RFSWcen]
            RSWin_vec+=[RFSWin]

            if verbose:
                d="\t"*2
                print d,"XUV Luminosity:"
                d="\t"*3
                print d,"Cmponent 1:",LXUV1
                print d,"Cmponent 2:",LXUV2
                print d,"Single Component 1:",LXUV_sing
                d="\t"*2
                print d,"XUV Flux:"
                d="\t"*3
                print d,"XUV at Earth-Distance: Binary = %e, Single = %e"%(FXUVcen,FXUVcen_sing)
                print d,"XUV at Mars-Distance: Binary = %e, Single = %e"%(FXUVout,FXUVout_sing)
                d="\t"*2
                print d,"Stellar wind flux:"
                d="\t"*3
                print d,"SW Flux at Earth-Distance: Binary = %e, Single = %e"%(Fswcen,Fswcen_sing)
                print d,"SW Flux at Mars-Distance: Binary = %e, Single = %e"%(Fswout,Fswout_sing)

            #==============================
            #INTEGRATING OUT XUV FLUX
            #==============================
            intFXUVout+=FXUVout*PELSI*dt
            intFXUVcen+=FXUVcen*PELSI*dt
            intFXUVin+=FXUVin*PELSI*dt
            intFXUVout_sing+=FXUVout_sing*PELSI*dt
            intFXUVcen_sing+=FXUVcen_sing*PELSI*dt
            intFXUVin_sing+=FXUVin_sing*PELSI*dt

        #==============================
        #TOTAL ACCELERATION
        #==============================
        acc1=acc1_tid+acc1_ML
        acc2=acc2_tid+acc2_ML

        if verbose:
            d="\t"*2
            print d,"Total acceleration:"
            d="\t"*3
            print d,"Main: ",acc1
            print d,"Secondary: ",acc2
            if pause:raw_input()
        
        acc1_vec+=[acc1]
        acc2_vec+=[acc2]

        dW1=acc1*(dt*GYR)
        dW2=acc2*(dt*GYR)

        if verbose:
            d="\t"*2
            print d,"Change in frequency:"
            d="\t"*3
            print d,"Main: ",dW1/W1
            print d,"Secondary: ",dW2/W2
            if pause:raw_input()
            
        W1+=dW1
        W2+=dW2

        P1=2*pi/W1
        P2=2*pi/W2

        tvec+=[tau]
        P1vec+=[P1/DAY]
        P2vec+=[P2/DAY]

        if verbose:
            d="\t"*2
            print d,"New period:"
            d="\t"*3
            print d,"Main: ",P1/DAY
            print d,"Secondary: ",P2/DAY
            if pause:raw_input()

        if not (i%iper):
            d="\t"*1
            print d,"Tau = %e"%tau
            d="\t"*2
            print d,"Tidal acceleration: Acc1 = %e, Acc2 = %e"%(acc1_tid,acc2_tid)
            print d,"Mass-loss acceleration: Acc1 = %e, Acc2 = %e"%(acc1_ML,acc2_ML)
            print d,"Total acceleration: Acc1 = %e, Acc2 = %e"%(acc1,acc2)
            print d,"Instantaneous periods: P1 = %.17e, P2 = %.17e"%(P1/DAY,P2/DAY)
            print d,"Last report:%e"%(tau-tau_rep)
            tau_rep=tau
        i+=1

    acc1_tid_vec=np.array(acc1_tid_vec)
    acc1_ML_vec=np.array(acc1_ML_vec)
    acc1_vec=np.array(acc1_vec)
    acc2_tid_vec=np.array(acc2_tid_vec)
    acc2_ML_vec=np.array(acc2_ML_vec)
    acc2_vec=np.array(acc2_vec)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT PERIOD
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure()
    plt.plot(tvec,np.array(P1vec),'b-',label='Primary')
    plt.plot(tvec,np.array(P2vec),'r-',label='Secondary')
    plt.plot(tvec,theoProt(tvec,xfit1),'b--',label='No tidal')
    plt.plot(tvec,theoProt(tvec,xfit2),'r--')

    #plt.xscale('log')
    plt.grid()
    plt.xlabel(r"$t$ (Gyr)")
    plt.ylabel(r"$P$ (day)")
    plt.axhline(Psync,linestyle='-',color='k')
    plt.axhline(Pbin/1.0,linestyle='-',color='c',label='1:1')
    plt.axhline(Pbin/1.5,linestyle='--',color='c',label='3:2')
    plt.axhline(Pbin/2.0,linestyle='-.',color='c',label='2:1')
    plt.legend(loc='best',prop=dict(size=10))
    plt.savefig(TMPDIR+"/PeriodEvolution-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT ACCELERATIONS
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure()
    plt.plot(tvec,abs(acc1_tid_vec),'b--',label='Tidal')
    plt.plot(tvec,abs(acc2_tid_vec),'r--')
    plt.plot(tvec,abs(acc1_ML_vec),'b-.',label='Mass')
    plt.plot(tvec,abs(acc2_ML_vec),'r-.')
    plt.plot(tvec,abs(acc1_vec),'b-',label='Total')
    plt.plot(tvec,abs(acc2_vec),'r-')

    plt.xscale('log')
    plt.yscale('log')
    plt.legend(loc='best',prop=dict(size=8))
    plt.xlabel(r"$t$ (Gyr)")
    plt.ylabel(r"$d\Omega/dt$ (rad/s)")
    plt.savefig(TMPDIR+"/AccelerationEvolution-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT XUV
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure()
    plt.plot(tvecX,RXUVout_vec,'b-',label='XUV @ Mars')
    plt.plot(tvecX,RXUVcen_vec,'g-',label='XUV @ Earth')
    plt.plot(tvecX,RXUVin_vec,'r-',label='XUV @ Venus')
    #plt.xscale('log')
    #plt.yscale('log')
    plt.ylim((0,2))
    plt.axhline(1,linestyle='--',color='k')
    plt.legend(loc='best',prop=dict(size=8))
    plt.xlabel(r"$t$ (Gyr)")
    plt.ylabel(r"$F_{\rm XUV,bin}/F_{\rm XUV,sing}$")
    plt.savefig(TMPDIR+"/FluxXUV-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT SW
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure()
    plt.plot(tvecX,RSWout_vec,'b-',label='XUV @ Mars')
    plt.plot(tvecX,RSWcen_vec,'g-',label='XUV @ Earth')
    plt.plot(tvecX,RSWin_vec,'r-',label='XUV @ Venus')
    #plt.xscale('log')
    #plt.yscale('log')
    plt.ylim((0,2))
    plt.axhline(1,linestyle='--',color='k')
    plt.legend(loc='best',prop=dict(size=8))
    plt.xlabel(r"$t$ (Gyr)")
    plt.ylabel(r"$F_{\rm SW,bin}/F_{\rm SW,sing}$")
    plt.savefig(TMPDIR+"/FluxSW-%s.png"%suffix)

############################################################
#ROUTINES
############################################################
solution=Run()
fout.close()
