from BHM.isochrones import *
from BHM.plot import *
from BHM.BHM import *
from BHM.catalogue import *
from numpy import *

"""
Usage:

  python BHMcalc.py Z M1 M2 e Pbin TAU Mp ap tau1 qintegration sessid zsvec qchz EARLYWIND FeH ep incrit outcrit conf_name qsaved

Where:

  Z: System metallicity
  M1: Primary mass
  M2: Secondary mass
  e: Binary eccentricity
  Pbin: Binary period
  TAU: Sampling time
  Mp: Test planetary mass
  ap: Test planet semimajor axis
  tau1: Total time of integration
  qintegration: Calculate integrated quantities
  sessid: Session ID
  zsvec: Set of isochrones (ZSVEC_full, ZSVEC_solar, ZSVEC_coarse, ZSVEC_siblings)
  qchz: Calculate continuous habitable zone?
  EARLYWIND: Early wind (trend, constant)
  FeH: Metallicity in dex
  ep: Test planet eccentricity
  incrit: Criterium for inner edge ('recent venus', 'moist greenhouse', 'runaway greenhouse')
  outcrit: Criterium for outer edge ('maximum greenhouse', 'early mars')
  conf_name: Name of configuration
  qsaved: Use saved configuration

Example:

  BHMcalc.py 0 1 0.5 0 10 1 1 1.5 2 1 bqurr72q961bn3767ltm5pkir1 ZSVEC_siblings 0 trend 0 0.5 'recent venus' 'early mars' 'niche1' 0

"""

############################################################
#CONFIGURATION
############################################################
TMPDIR="tmp/"
ALPHA=0.3 #Entrapment Factor (Zendejas et al., 2010) 
MUATM=44.0 #MEAN 

#PHOTON DENSITY ON EARTH
#PHOTOSYNTHETIC PHOTON FLUX ON EARTH (400-700 nm)
#400-1400
PPFD_EARTH=3.83647334928e+21 #photons s^-1 m^-2
#400-1100
#PPFD_EARTH=3.03998869273e+21 #photons s^-1 m^-2
#400-700
#PPFD_EARTH=1.37945308352e+21 #photons s^-1 m^-2
#TOTAL PHOTON FLUX ON EARTH 
PFD_EARTH=6.34586512763e+21 #photons s^-1 m^-2
#TOTAL INSOLATION ON EARTH
SOLAR_CONSTANT=1367.9046529 #W m^-2

LINES=['']*100
LABEL_SIZE=16
LEGEND_SIZE=12
TICS_SIZE=12

############################################################
#INPUT PARAMETERS
############################################################
#NUMBER OF PARAMETERS
NPARAM=19
argvstr=""
for i in xrange(1,NPARAM+1):
    if i==11 or i==19:continue
    argvstr+="%s"%argv[i]

#INPUT MD5 STRING
MD5IN=md5str(argvstr)

#READ PARAMETERS
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
qchz=int(argv[13])
EARLYWIND=argv[14]
FeH=float(argv[15])
ep=float(argv[16])
incrit=argv[17]
outcrit=argv[18]
confname=argv[19]
qsaved=int(argv[20])

if qintegration:qchz=1
if Z==0:
    Z,dZ=ZfromFHe(FeH)

MD5.update("%.4f%.4f%.4f%.4f%.4f%.4f%s%s%s"%(Z,FeH,M1,M2,Pbin,e,incrit,outcrit,zsvec))
signature_HZ=MD5.hexdigest()

suffix="%.2f%.2f%.3f%.2f-%s"%(M1,M2,e,Pbin,sessid)
fout=open(TMPDIR+"output-%s.log"%sessid,"w")
print>>fout,"%s"%MD5IN

SAVEDIR="%s/conf-%s/"%(TMPDIR,MD5IN)
if not path.isdir(SAVEDIR):
    System("mkdir -p %s;sleep 0.5"%SAVEDIR)
    fl=open(SAVEDIR+"configuration","w")
    for arg in argv:
        fl.write(arg+"\n")
    fl.write("%s\n"%argvstr);
    fl.close()

if qsaved:
    if ((not fileexists(SAVEDIR+"tauvec")) and qchz) or ((not fileexists(SAVEDIR+"tvec")) and qintegration):
        print "Error: you have requested preconfigured results at '%s' that does not exist."%SAVEDIR
        qsaved=0

############################################################
#PLANET PROPERTIES
############################################################
#RADIUS
Rp=Mp**0.25
gp=GCONST*(Mp*MEARTH)/(Rp*Rp_E)**2

#CROSS SECTIONAL AREA
Ap=2*PI*(Rp*Rp_E)**2 #m^2

#ATMOSPHERIC MASS
Pp=1.0*BAR
Matm=4*PI*Pp*(Rp*Rp_E)**2/gp

#ATMOSPHERIC NUMBER OF MOLECULES
muatm=44 #CO_2 Rich atmosphere
muatm=29 #N_2 Rich atmosphere
Natm=Matm/(muatm*MP)

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
    global tau1,ap,Mp,e

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CONSTANT PROPERTIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #VERBOSITY
    verbose=False
    #verbose=True
    pause=False
    #pause=True

    #ISOCHRONE LIMITS
    tau0=0.01
    tauM=12.5
    
    #INITIAL PERIOD OF ROTATION ABOVE DISRUPTION
    PFAC=2
    
    #HZ ZONE AGE
    tauHZ=TAU

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #COMPONENT STARS PROPERTIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #MAIN COMPONENT
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    g1,T1,R1,L1=StellarGTRL(Z,M1,TAU)
    if g1*T1*R1*L1<0:print>>fout,"ERROR: Bad Metallicity"
    Rmin1,Rmax1=minmaxRadius(Z,M1,tmax=TAU)
    Pmax1=maxPeriod(M1,R1)
    Pini1=10*Pmax1
    Prot1=Prot(TAU,Ms=M1,Rs=R1)/DAY
    g1i,T1i,R1i,L1i=StellarGTRL(Z,M1,tau0)
    Pini1=PFAC*Prot(tau0,Ms=M1,Rs=R1i)/DAY
    W1o=2*pi/Pini1

    print>>fout,g1,T1,R1,L1,Rmin1,Rmax1,Pini1,Prot1

    gZ1,TZ1,RZ1,LZ1=StellarGTRL(Z,M1,tauHZ)
    lin1,aE1,lout1=HZ2013(LZ1,TZ1,lin=incrit,lout=outcrit)
    aHZ1=(lin1+lout1)/2

    print>>fout,lin1,aE1,aHZ1,lout1

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #SECONDARY COMPONENT
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    g2,T2,R2,L2=StellarGTRL(Z,M2,TAU)
    if g2*T2*R2*L2<0:print>>fout,"ERROR: Bad Metallicity"
    Rmin2,Rmax2=minmaxRadius(Z,M2,tmax=TAU)
    Pmax2=maxPeriod(M2,R2)
    Pini2=10*Pmax2
    Prot2=Prot(TAU,Ms=M2,Rs=R2)/DAY
    g2i,T2i,R2i,L2i=StellarGTRL(Z,M2,tau0)
    Pini2=PFAC*Prot(tau0,Ms=M2,Rs=R2i)/DAY
    W2o=2*pi/Pini2

    print>>fout,g2,T2,R2,L2,Rmin2,Rmax2,Pini2,Prot2

    gZ2,TZ2,RZ2,LZ2=StellarGTRL(Z,M2,tauHZ)
    lin2,aE2,lout2=HZ2013(LZ2,TZ2,lin=incrit,lout=outcrit)
    aHZ2=(lin2+lout2)/2

    print>>fout,lin2,aE2,aHZ2,lout2

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #BINARY PROPERTIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    nbin=2*np.pi/Pbin
    abin=aKepler(Pbin,M1,M2)
    mu=M2/(M1+M2)
    acrit=aCritical(mu,abin,e)

    nsync=nSync(e)
    Psync=Pbin/nsync
    Wsync=nbin*nsync

    print>>fout,abin,acrit,nsync,Psync

    lin,aE,lout=HZbin4(M2/M1,LZ1,LZ2,TZ1,abin,crits=[incrit,outcrit])
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

    print "Test planet:"
    print d,"ap = %f AU"%ap
    print d,"ep = %f"%ep

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
    print d,"HZ = ",lin2,aE2,aHZ2,lout2
    print
    titlebin=r"$M_1=%.3f$, $M_2=%.3f$, $a_{\rm bin}=%.3f$ AU, $e_{\rm bin}=%.3f$, $P_{\rm bin}=%.3f$ days"%(M1,M2,abin,e,Pbin)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #ESTIMATED SYNC. TIME
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #NOTE: TO CONVER W TO SI YOU SHOULD DIVIDE BY DAYS
    g1i,T1i,R1i,L1i=StellarGTRL(Z,M1,0.1)
    acc1=tidalAcceleration(M1,R1i,L1i,M2,abin,e,nbin/DAY,W1o/DAY,verbose=verbose)
    tsync1=-(W1o/DAY)/acc1/GYR
    
    g2i,T2i,R2i,L2i=StellarGTRL(Z,M2,0.1)
    acc2=tidalAcceleration(M2,R2i,L2i,M1,abin,e,nbin/DAY,W2o/DAY,verbose=verbose)
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
    print>>fout,Z

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #PLOT HABITABLE ZONE AND BINARY ORBIT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    rang=1.2*lout
    fig=plt.figure(figsize=(8,8))
    ifig=0
    ax=fig.add_axes([0.01,0.01,0.98,0.98])
    #ax=fig.add_axes([0.1,0.1,0.8,0.8])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

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

    #SINGLE STAR
    inHZs=Circle((0,0),lin1,facecolor='none',linestyle='dotted',color='b',linewidth=2,zorder=60)
    ax.add_patch(inHZs)

    #OUTER
    lino,aEo,louto=HZbin4(M2/M1,LZ1,LZ2,TZ1,abin,
                       crits=['recent venus','early mars'])
    aHZo=(lino+louto)/2
    outHZ=Circle((0,0),louto,facecolor='g',alpha=0.3,linewidth=2)
    ax.add_patch(outHZ)
    outHZ=Circle((0,0),lino,facecolor='w',edgecolor='r',
                linewidth=2,zorder=10)
    ax.add_patch(outHZ)

    #TITLE
    ax.set_title(titlebin,position=(0.5,0.95),fontsize=16)
    ax.text(0.5,0.02,r"$a_{\rm crit}=%.2f$ AU, $l_{\rm in,RV}$=%.2f AU, $l_{\rm in,RG}$=%.2f AU, $l_{\rm out,MG}$=%.2f AU, $l_{\rm out,EM}$=%.2f AU"%(acrit,lino,lini,louti,louto),transform=ax.transAxes,horizontalalignment='center',fontsize=14)
    
    rang=3
    ax.set_xlim((-rang,rang))
    ax.set_ylim((-rang,rang))

    saveFig(TMPDIR+"/HZ-%s.png"%suffix,watermarkpos='inner')

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #HABITABLE ZONE WITH TEST PLANET
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    rang=max(1.2*ap*(1+ep),1.2*lout)
    fig=plt.figure(figsize=(8,8));ifig=0
    ax=fig.add_axes([0.01,0.01,0.98,0.98])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    #STELLAR PROPERTIES
    ax.plot(x1,y1,'k-',linewidth=1,zorder=20)
    ax.plot(x2,y2,'k-',linewidth=1,zorder=20)
    C1=Circle((x1[0],y1[0]),rang/90,
              facecolor='k',alpha=1.0,linewidth=0,zorder=50)
    C2=Circle((x2[0],y2[0]),rang/90,
              facecolor='k',alpha=1.0,linewidth=0,zorder=50)
    ax.add_patch(C1)
    ax.add_patch(C2)
    aCR=Circle((0,0),acrit,facecolor='none',edgecolor='k',
                linewidth=2,linestyle='dashed',zorder=20)
    ax.add_patch(aCR)

    #HZ
    outHZ=Circle((0,0),louti,facecolor='g',alpha=0.3,linewidth=2)
    ax.add_patch(outHZ)
    inHZ=Circle((0,0),lini,facecolor='r',edgecolor='r',alpha=0.2,
                linewidth=2,zorder=10)
    ax.add_patch(inHZ)
    outHZ=Circle((0,0),louto,facecolor='g',alpha=0.3,linewidth=2)
    ax.add_patch(outHZ)
    outHZ=Circle((0,0),lino,facecolor='w',edgecolor='r',
                linewidth=2,zorder=10)
    ax.add_patch(outHZ)

    #PLANETARY PROPERTIES
    r=ap*(1-ep**2)/(1+ep*cos(f))
    x=r*cos(f)
    y=r*sin(f)
    ax.plot(x,y,'k-',linewidth=2,zorder=100)

    ax.set_title(titlebin,position=(0.5,0.95),fontsize=16)
    ax.text(0.5,0.92,"Test planet: $a_p = %.2f$ AU, $e_p = %.3f$"%(ap,ep),
            horizontalalignment='center',transform=ax.transAxes,
            fontsize=14)
    ax.text(0.5,0.02,r"$a_{\rm crit}=%.2f$ AU, $l_{\rm in,RV}$=%.2f AU, $l_{\rm in,RG}$=%.2f AU, $l_{\rm out,MG}$=%.2f AU, $l_{\rm out,EM}$=%.2f AU"%(acrit,lino,lini,louti,louto),transform=ax.transAxes,horizontalalignment='center',fontsize=14)
    ax.set_xlim((-rang,rang))
    ax.set_ylim((-rang,rang))
    saveFig(TMPDIR+"/HZ+planet-%s.png"%suffix,watermarkpos='inner')

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CHECK IF CONTINUOUS HABITABLE ZONE 
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not qchz:
        fout.close()
        exit(0)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #FIND OPTIMUM POINT INSIDE HABITABLE ZONE
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    d=0*"\t"
    print d,"Calculating the continuous Habitable Zone..."
    if not qsaved:
        d=1*"\t"
        print d,"From scratch..."
        tauvec=np.linspace(0.1,tauM,200)
        lins=[]
        louts=[]
        slins=[]
        slouts=[]
        i=0
        for tau in tauvec:
            g1e,T1e,R1e,L1e=StellarGTRL(Z,M1,tau)
            g2e,T2e,R2e,L2e=StellarGTRL(Z,M2,tau)
            try:
                lin1e,aE1e,lout1e=HZ2013(L1e,T1e,lin=incrit,lout=outcrit)
            except:
                break
            line,aEe,loute=HZbin4(M2/M1,L1e,L2e,T1e,abin,crits=[incrit,outcrit])
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
 
        #FIND BINARY CONTINUOUS HABITABLE ZONE
        """
        nlins=len(lins)
        dlins=[]
        for i in xrange(10,nlins):
            dlins+=[np.log10(lins[i])-np.log10(lins[i-3])]
        dlins=np.array(dlins)
        """
        #"""
        dlins=np.log10(lins[1::])-np.log10(lins[:-1:])
        dlins=np.append([0],dlins)
        #print np.log10(lins[1::])[-10:-1],dlins[-10:-1]
        #exit(0)
        #"""
        imax=-1
        dimax=20
        epsmax=0
        dlinold=dlins[-1]
        for i in arange(10,len(dlins))[::-3]:
            eps=2*abs(dlins[i]-dlinold)/(dlins[i]+dlinold)
            #print tauvec[i],dlins[i],dlinold,eps,epsmax,imax,i
            if eps>epsmax:
                imax=i
                epsmax=eps
            dlinold=dlins[i]
            if abs(imax-i)>dimax and epsmax>0:break
            if tauvec[i]<tausys/2:break
        lincont=lins[imax]
        loutcont=min(louts)
        #print lincont,loutcont
        #exit(0)

        #FIND SINGLE PRIMARY CONTINUOUS HABITABLE ZONE
        dslins=np.log10(slins[1::])-np.log10(slins[:-1:])
        dslins=np.append([0],dslins)
        imax=-1
        epsmax=0
        dlinold=dslins[-1]
        for i in arange(10,len(dslins))[::-3]:
            eps=2*abs(dslins[i]-dlinold)/(dslins[i]+dlinold)
            #print tauvec[i],dslins[i],dlinold,eps,epsmax
            if eps>epsmax:
                imax=i
                epsmax=eps
            dlinold=dslins[i]
            if abs(imax-i)>dimax and epsmax>0:break
            if tauvec[i]<tausys/2:break
        slincont=slins[imax]
        sloutcont=min(slouts)
         
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #STELLAR ORBIT
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #PERIOD OF THE PLANET
        MTbin=M1+M2
        Ppin=PKepler(lincont,MTbin,Mp*MEARTH/MSUN)
        Ppout=PKepler(loutcont,MTbin,Mp*MEARTH/MSUN)
        Ppp=max(Ppin,Ppout)
        epp=0.0
    
        #TIME
        torbs=linspace(0,1.5*Ppp,500)

        #INTEGRATE POSITIONS
        r1s=[]
        r2s=[]
        rpins=[]
        rpouts=[]
        rp1ins=[]
        rp2ins=[]
        rp1outs=[]
        rp2outs=[]
        for t in torbs:
            #MEAN ANOMALY
            Mbin=2*np.pi/Pbin*t
            Mp=2*np.pi/Ppp*t
            
            #ECCENTRIC AND TRUE ANOMALY
            Ebin=eccentricAnomaly(Mbin,e)
            fbin=2*arctan(np.sqrt((1+e)/(1-e))*tan(Ebin/2))
            Ep=eccentricAnomaly(Mp,epp)
            fp=2*arctan(np.sqrt((1+epp)/(1-epp))*tan(Ep/2))
            
            #RADIO-VECTOR BINARY COMPONENTS
            rbin=abin*(1-e*cos(Ebin))
            rred=array([rbin*cos(fbin),rbin*sin(fbin)])
            r1=M2/MTbin*rred
            r2=-M1/MTbin*rred
            r1s+=[r1]
            r2s+=[r2]

            #INNER EDGE
            rprad=lincont*(1-epp*cos(Ep))
            rp=array([rprad*cos(fp),rprad*sin(fp)])
            rpins+=[rp]
            rp1=r1-rp;rp1ins+=[rp1]
            rp2=r2-rp;rp2ins+=[rp2]

            #OUTER EDGE
            rprad=loutcont*(1-epp*cos(Ep))
            rp=array([rprad*cos(fp),rprad*sin(fp)])
            rpins+=[rp]
            rp1=r1-rp;rp1outs+=[rp1]
            rp2=r2-rp;rp2outs+=[rp2]

        r1s=np.array(r1s)
        r2s=np.array(r2s)
        rpins=np.array(rpins)
        rp1ins=np.array(rp1ins)
        rp2ins=np.array(rp2ins)
        rpouts=np.array(rpouts)
        rp1outs=np.array(rp1outs)
        rp2outs=np.array(rp2outs)
        
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #PHOTON FLUX DENSITY
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        npoint=len(torbs)
        lamb0=1.0*NANO
        lambinf=1E6*NANO
        lamb1=400.0*NANO
        lamb2=700.0*NANO
        lamb2=1100.0*NANO
        lamb2=1400.0*NANO
        
        fin1s=[]
        fout1s=[]
        fin2s=[]
        fout2s=[]
        
        pin1s=[]
        pout1s=[]
        pin2s=[]
        pout2s=[]
        
        flins=[]
        flouts=[]
        pins=[]
        pouts=[]
        
        for i in xrange(npoint):
            #DISTANCE
            r1in=norm(rp1ins[i])
            r2in=norm(rp2ins[i])
            r1out=norm(rp1outs[i])
            r2out=norm(rp2outs[i])
            
            #INSOLATION
            fluxin1=planckPower(lamb0,lambinf,T1)*(R1*RSUN/(r1in*AU))**2
            fin1s+=[fluxin1]
            fluxout1=planckPower(lamb0,lambinf,T1)*(R1*RSUN/(r1out*AU))**2
            fout1s+=[fluxout1]

            fluxin2=planckPower(lamb0,lambinf,T2)*(R2*RSUN/(r2in*AU))**2
            fin2s+=[fluxin2]
            fluxout2=planckPower(lamb0,lambinf,T2)*(R2*RSUN/(r2out*AU))**2
            fout2s+=[fluxout2]

            #PHOTON FLUX
            ppfdin1=planckPhotons(lamb1,lamb2,T1)*(R1*RSUN/(r1in*AU))**2
            pin1s+=[ppfdin1]
            ppfdout1=planckPhotons(lamb1,lamb2,T1)*(R1*RSUN/(r1out*AU))**2
            pout1s+=[ppfdout1]

            ppfdin2=planckPhotons(lamb1,lamb2,T2)*(R2*RSUN/(r2in*AU))**2
            pin2s+=[ppfdin2]
            ppfdout2=planckPhotons(lamb1,lamb2,T2)*(R2*RSUN/(r2out*AU))**2
            pout2s+=[ppfdout2]

            #TOTAL
            flin=fluxin1+fluxin2
            flout=fluxout1+fluxout2
            pin=ppfdin1+ppfdin2
            pout=ppfdout1+ppfdout2

            flins+=[flin]
            flouts+=[flout]
            pins+=[pin]
            pouts+=[pout]

        fin1s=array(fin1s)
        fout1s=array(fout1s)
        fin2s=array(fin2s)
        fout2s=array(fout2s)
        pin1s=array(pin1s)
        pout1s=array(pout1s)
        pin2s=array(pin2s)
        pout2s=array(pout2s)

        flins=array(flins)
        flouts=array(flouts)
        pins=array(pins)
        pouts=array(pouts)
        
        #SAVING STELLAR ORBIT
        savetxt(SAVEDIR+"torbs",torbs)
        savetxt(SAVEDIR+"r1s",r1s)
        savetxt(SAVEDIR+"r2s",r2s)
        savetxt(SAVEDIR+"rpins",rpins)
        savetxt(SAVEDIR+"rp1ins",rp1ins)
        savetxt(SAVEDIR+"rp2ins",rp2ins)
        savetxt(SAVEDIR+"rpouts",rpouts)
        savetxt(SAVEDIR+"rp1outs",rp1outs)
        savetxt(SAVEDIR+"rp2outs",rp2outs)
        savetxt(SAVEDIR+"stellar-orbits",[MTbin,Ppin,Ppout,lamb1,lamb2])
        
        #SAVING PHOTON FLUX
        savetxt(SAVEDIR+"fin1s",fin1s)
        savetxt(SAVEDIR+"fout1s",fout1s)
        savetxt(SAVEDIR+"fin2s",fin2s)
        savetxt(SAVEDIR+"fout2s",fout2s)
        savetxt(SAVEDIR+"pin1s",pin1s)
        savetxt(SAVEDIR+"pout1s",pout1s)
        savetxt(SAVEDIR+"pin2s",pin2s)
        savetxt(SAVEDIR+"pout2s",pout2s)

        savetxt(SAVEDIR+"flins",flins)
        savetxt(SAVEDIR+"flouts",flouts)
        savetxt(SAVEDIR+"pins",pins)
        savetxt(SAVEDIR+"pouts",pouts)

        #SAVING
        savetxt(SAVEDIR+"tauvec",tauvec)
        savetxt(SAVEDIR+"lins",lins)
        savetxt(SAVEDIR+"louts",louts)
        savetxt(SAVEDIR+"slins",slins)
        savetxt(SAVEDIR+"slouts",slouts)
        savetxt(SAVEDIR+"chz",[tausys,lincont,loutcont,slincont,sloutcont])
    else:
        d=1*"\t"
        print d,"Loading from a saved state..."
        tauvec=loadtxt(SAVEDIR+"tauvec")
        lins=loadtxt(SAVEDIR+"lins")
        louts=loadtxt(SAVEDIR+"louts")
        slins=loadtxt(SAVEDIR+"slins")
        slouts=loadtxt(SAVEDIR+"slouts")
        tausys,lincont,loutcont,slincont,sloutcont=loadtxt(SAVEDIR+"chz")

        #SAVING STELLAR ORBIT
        torbs=loadtxt(SAVEDIR+"torbs")
        r1s=loadtxt(SAVEDIR+"r1s")
        r2s=loadtxt(SAVEDIR+"r2s")
        rpins=loadtxt(SAVEDIR+"rpins")
        rp1ins=loadtxt(SAVEDIR+"rp1ins")
        rp2ins=loadtxt(SAVEDIR+"rp2ins")
        rpouts=loadtxt(SAVEDIR+"rpouts")
        rp1outs=loadtxt(SAVEDIR+"rp1outs")
        rp2outs=loadtxt(SAVEDIR+"rp2outs")
        
        #SAVING PHOTON FLUX
        fin1s=loadtxt(SAVEDIR+"fin1s")
        fout1s=loadtxt(SAVEDIR+"fout1s")
        fin2s=loadtxt(SAVEDIR+"fin2s")
        fout2s=loadtxt(SAVEDIR+"fout2s")
        pin1s=loadtxt(SAVEDIR+"pin1s")
        pout1s=loadtxt(SAVEDIR+"pout1s")
        pin2s=loadtxt(SAVEDIR+"pin2s")
        pout2s=loadtxt(SAVEDIR+"pout2s")

        flins=loadtxt(SAVEDIR+"flins")
        flouts=loadtxt(SAVEDIR+"flouts")
        pins=loadtxt(SAVEDIR+"pins")
        pouts=loadtxt(SAVEDIR+"pouts")

        MTbin,Ppin,Ppout,lamb1,lamb2=loadtxt(SAVEDIR+"stellar-orbits")

    if lincont<acrit:
        print "Inner edge of CHZ (%.3f) is inside critical distance (%.3f).  Changed."%(lincont,acrit)
        lincont=acrit
    print "Continuous Binary HZ: ",lincont,loutcont
    print "Continuous Single Primary HZ: ",slincont,sloutcont

    #PLOT HABITABLE ZONE
    fig=plt.figure();ifig=0

    plt.axhline(loutcont,color='k',linewidth=1)
    plt.axhline(lincont,color='k',linewidth=1)
    plt.plot([],[],'k-',linewidth=3)
    plt.axhspan(lincont,loutcont,color='k',alpha=0.3)
    plt.text(tauvec[-1]/2,0.98*loutcont+0*(lincont+loutcont)/2,'Circumbinary CHZ',
             horizontalalignment='center',verticalalignment='top',fontsize=18)

    """"
    plt.axhline(sloutcont,color='k',linewidth=1)
    plt.axhline(slincont,color='k',linewidth=1)
    plt.plot([],[],'k-',linewidth=3)
    plt.axhspan(slincont,sloutcont,color='k',alpha=0.3)
    plt.text(tauvec[-1]/2,1.02*slincont+0*(slincont+sloutcont)/2,'Single Primary CHZ',
             horizontalalignment='center',verticalalignment='bottom',fontsize=18)
    #"""

    plt.text(1.05*tauvec[0],0.98*loutcont,'%.2f AU'%loutcont,
             horizontalalignment='left',
             verticalalignment='top',
             fontsize=12)

    plt.text(1.05*tauvec[0],1.02*lincont,'%.2f AU'%lincont,
             horizontalalignment='left',
             verticalalignment='bottom',
             fontsize=12)

    plt.xlabel(r"$\tau$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$a$ (AU)",fontsize=LABEL_SIZE)

    plt.fill_between(tauvec,lins,louts,color='g',alpha=0.3)
    plt.plot(tauvec,lins,'r-',linewidth=2,label=incrit)
    plt.plot(tauvec,louts,'b-',linewidth=2,label=outcrit)
    plt.plot(tauvec,slins,'k--',linewidth=2)
    plt.plot(tauvec,slouts,'k--',linewidth=2)
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.plot([],[],'k--',linewidth=3,label='Single primary HZ limits')

    plt.yscale('log')
    logTickLabels(plt.gca(),-1,2,(1,),frm='%.1f',axis='y',notation='normal',fontsize=12)

    plt.ylim((min(slins),max(louts)))
    #plt.ylim((0.5,3.5))
    plt.xlim((tauvec[0],tauvec[-1]))

    plt.legend(loc='upper left',prop={'size':LEGEND_SIZE})
    plt.title(titlebin,position=(0.5,1.02),fontsize=16)
    saveFig(TMPDIR+"/HZevol-%s.png"%suffix)
    
    print>>fout,tausys,lincont,loutcont,slincont,sloutcont

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #PLOT STELLAR ORBIT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    fig=plt.figure(figsize=(8,8))
    """
    plt.plot(r1s[:,0],r1s[:,1])
    plt.plot(r2s[:,0],r2s[:,1])
    plt.plot(rps[:,0],rps[:,1])
    """
    orange="#FACC2E"
    plt.plot(rp1ins[:,0],rp1ins[:,1],'-',color=orange,label='Component 1')
    plt.plot(rp2ins[:,0],rp2ins[:,1],'r-',label='Component 2')
    plt.plot(rp1outs[:,0],rp1outs[:,1],'-',color=orange,linewidth=2)
    plt.plot(rp2outs[:,0],rp2outs[:,1],'r-',linewidth=2)
    plt.plot([0],[0],'ko',markersize=10)
    plt.text(0,lincont,"Inner CHZ",horizontalalignment='center',bbox=dict(facecolor='w',edgecolor='none'),fontsize=12)
    plt.text(0,loutcont,"Outer CHZ",horizontalalignment='center',bbox=dict(facecolor='w',edgecolor='none'),fontsize=12)
    rmax=loutcont
    plt.xlim((-1.5*rmax,1.5*rmax))
    plt.ylim((-1.5*rmax,1.5*rmax))
    plt.xlabel('x (AU)',fontsize=LABEL_SIZE)
    plt.ylabel('y (AU)',fontsize=LABEL_SIZE)
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.legend(loc='best',prop=dict(size=LEGEND_SIZE))
    plt.grid()
    saveFig(TMPDIR+"/StellarOrbits-%s.png"%suffix)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #PLOT PHOTON FLUX DENSITY
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    fig=plt.figure(figsize=(8,8))
    """
    plt.plot(torbs,fin1s/SOLAR_CONSTANT,'b-',label='Component 1, inner CHZ')
    plt.plot(torbs,fin2s/SOLAR_CONSTANT,'r-',label='Component 2, inner CHZ')
    plt.plot(torbs,fout1s/SOLAR_CONSTANT,'b:',label='Component 1, outer CHZ')
    plt.plot(torbs,fout2s/SOLAR_CONSTANT,'r:',label='Component 2, outer CHZ')

    plt.plot(torbs,pin1s/PPFD_EARTH,'b-',linewidth=2)
    plt.plot(torbs,pin2s/PPFD_EARTH,'r-',linewidth=2)
    plt.plot(torbs,pout1s/PPFD_EARTH,'b:',linewidth=2)
    plt.plot(torbs,pout2s/PPFD_EARTH,'r:',linewidth=2)
    """

    plt.plot(torbs,pins/PPFD_EARTH,'r-',linewidth=2,label='PPFD Inner CHZ')
    plt.plot(torbs,pouts/PPFD_EARTH,'b-',linewidth=2,label='PPFD Outer CHZ')
    plt.plot(torbs,flins/SOLAR_CONSTANT,'k-',linewidth=2,label='Insolation',zorder=-10)
    plt.plot(torbs,flouts/SOLAR_CONSTANT,'k-',linewidth=2,zorder=-10)

    plt.axhline(1.0,color='k',linewidth=2)
    plt.xlabel('t (days)',fontsize=LABEL_SIZE)
    plt.ylabel('Insolation, PPFD (PEL)',fontsize=LABEL_SIZE)
    plt.xlim((0,Ppout))
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.legend(loc='lower right',prop=dict(size=LEGEND_SIZE))
    #plt.grid()
    saveFig(TMPDIR+"/InsolationPhotonDensity-%s.png"%suffix)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CHECK IF INTEGRATION IS REQUESTED
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if not qintegration:
        fout.close()
        exit(0)

    if tau1>tausys:
        print "Requested total time %f is larger than system lifetime %f.  We have adjusted it"%(tau1,tausys)
        tau1=tausys

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #EARTH PROPERTIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    earthFXUV=loadtxt("BHM/data/earth-FXUV.dat")
    earthFSW=loadtxt("BHM/data/earth-FSW.dat")
    earthintFXUV=loadtxt("BHM/data/earth-intFXUV.dat")
    earthintFSW=loadtxt("BHM/data/earth-intFSW.dat")
    earthML=loadtxt("BHM/data/earth-ML.dat")

    cond=earthFXUV[:,0]<tau1
    earthFXUV=earthFXUV[cond,:]
    earthFSW=earthFSW[cond,:]
    earthintFXUV=earthintFXUV[cond,:]
    earthintFSW=earthintFSW[cond,:]

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #INTEGRATION RANGE
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    dt=min(1E-3,min(abs(tsync1),abs(tsync2))/10)
    nmax=tau1/dt
    tau_vec=np.arange(tau0+dt,tau1,dt)
    ntau=len(tau_vec)

    rate_Flux_integrate=50
    Dt=dt*rate_Flux_integrate*GYR
    tvec=tau_vec[::ntau/50]
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #STELLAR MASSLOSS FIT
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    suffix1="%.2f"%(M1)
    suffix2="%.2f"%(M2)
    ffit1=TMPDIR+"solution-%s.txt"%(suffix1)
    ffit2=TMPDIR+"solution-%s.txt"%(suffix2)

    if not fileexists(ffit1):
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
        plt.figure();ifig=0
        plt.plot(data1[:,0],data1[:,1],'bo')
        plt.plot(data1[:,0],theoProt(data1[:,0],xfit1),'b-')
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel(r"$\tau$")
        plt.ylabel(r"$P_{\rm rot}$")
        plt.title(r"$M_1$ = %.2f $M_{\rm sun}$"%M1)
        saveFig(TMPDIR+"/PeriodFit-%s.png"%suffix1)
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
        plt.figure();ifig=0
        plt.plot(data2[:,0],data2[:,1],'bo')
        plt.plot(data2[:,0],theoProt(data2[:,0],xfit2),'b-')
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel(r"$\tau$")
        plt.ylabel(r"$P_{\rm rot}$")
        plt.title(r"$M_1$ = %.2f $M_{\rm sun}$"%M2)
        saveFig(TMPDIR+"/PeriodFit-%s.png"%suffix2)
    else:
        xfit2=np.loadtxt(ffit2)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #TIDAL INTEGRATION
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    W1=W1o/DAY
    W2=W2o/DAY
    P1=2*pi/W1
    P2=2*pi/W2

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

    FXUVopt_vec=[]
    FXUVp_vec=[]
    FXUVin_vec=[]
    ntFXUVopt_vec=[]
    ntFXUVp_vec=[]
    ntFXUVin_vec=[]
    sFXUVopt_vec=[]
    sFXUVp_vec=[]
    sFXUVin_vec=[]

    FSWopt_vec=[]
    FSWp_vec=[]
    FSWin_vec=[]
    ntFSWopt_vec=[]
    ntFSWp_vec=[]
    ntFSWin_vec=[]
    sFSWopt_vec=[]
    sFSWp_vec=[]
    sFSWin_vec=[]

    tau_rep=tau_vec[0]
    q1sync=False
    q2sync=False
    tvecX=[]
    
    d="\t"*0
    print d,"Tidal integration:"
    if verbose:
        d="\t"*1
        print d,"Times: ",tau0,tau1
        print d,"Time step: %e Gyr (%e s)"%(dt,dt*GYR)
        print d,"Initial conditions: W: ",W1*DAY,W2*DAY
        print d,"Initial conditions: P: ",P1/DAY,P2/DAY
    if not qsaved:
        d="\t"*1
        print d,"Computing from scratch..."
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
                
            #==============================
            #TIDAL ACCELERATION
            #==============================
            acc1_tid=tidalAcceleration(M1,R1,L1,M2,abin,e,nbin/DAY,W1)
            acc2_tid=tidalAcceleration(M2,R2,L2,M1,abin,e,nbin/DAY,W2)

            acc1_tid_vec+=[acc1_tid]
            acc2_tid_vec+=[acc2_tid]
            
            if verbose:
                d="\t"*2
                print d,"Tidal acceleration:"
                d="\t"*3
                print d,"Main: ",acc1_tid
                print d,"Secondary: ",acc2_tid
        
            #==============================
            #MASS-LOSS ACCELERATION
            #==============================
            #COMPUTE THE EFFECTIVE AGE
            tau_rot1=tfromProt(P1/DAY,xfit1)
            tau_rot2=tfromProt(P2/DAY,xfit2)
            dProtdt1=dtheoProt(tau_rot1,xfit1)*DAY/GYR
            dProtdt2=dtheoProt(tau_rot2,xfit2)*DAY/GYR
            acc1_ML=-2*np.pi/P1**2*dProtdt1
            acc2_ML=-2*np.pi/P2**2*dProtdt2

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

             #==============================
             #XUV & STELLAR WIND
             #==============================
            if not (i%rate_Flux_integrate):
                #TIME VECTOR
                tvecX+=[tau]

                #FLUXES (INCLUDING TIDAL INTERACTION)
                LXUV1=starLXUV(L1,tau_rot1)
                LXUV2=starLXUV(L2,tau_rot2)
                FXUVopt=(LXUV1+LXUV2)/(4*np.pi*(loutcont*AU*1E2)**2)/PEL
                FXUVp=(LXUV1+LXUV2)/(4*np.pi*(ap*AU*1E2)**2)/PEL
                FXUVin=(LXUV1+LXUV2)/(4*np.pi*(lincont*AU*1E2)**2)/PEL
                Pswopt,FSWopt=binaryWind(loutcont,tau_rot1,M1,R1,tau_rot2,M2,R2,early=EARLYWIND)
                Pswp,FSWp=binaryWind(ap,tau_rot1,M1,R1,tau_rot2,M2,R2,early=EARLYWIND)
                Pswin,FSWin=binaryWind(lincont,tau_rot1,M1,R1,tau_rot2,M2,R2,early=EARLYWIND)

                #FLUXES (NO TIDAL INTERACTION)
                ntLXUV1=starLXUV(L1,tau)
                ntLXUV2=starLXUV(L2,tau)
                ntFXUVopt=(ntLXUV1+ntLXUV2)/(4*np.pi*(loutcont*AU*1E2)**2)/PEL
                ntFXUVp=(ntLXUV1+ntLXUV2)/(4*np.pi*(ap*AU*1E2)**2)/PEL
                ntFXUVin=(ntLXUV1+ntLXUV2)/(4*np.pi*(lincont*AU*1E2)**2)/PEL
                ntPswopt,ntFSWopt=binaryWind(loutcont,tau,M1,R1,tau,M2,R2,early=EARLYWIND)
                ntPswp,ntFSWp=binaryWind(ap,tau,M1,R1,tau,M2,R2,early=EARLYWIND)
                ntPswin,ntFSWin=binaryWind(lincont,tau,M1,R1,tau,M2,R2,early=EARLYWIND)

                #FLUXES (SINGLE STAR)
                sLXUV=starLXUV(L1,tau)
                sFXUVopt=(sLXUV)/(4*np.pi*(sloutcont*AU*1E2)**2)/PEL
                sFXUVp=(sLXUV)/(4*np.pi*(ap*AU*1E2)**2)/PEL
                sFXUVin=(sLXUV)/(4*np.pi*(slincont*AU*1E2)**2)/PEL
                sPswopt,sFSWopt=binaryWind(sloutcont,tau,M1,R1,-1,-1,-1,early=EARLYWIND)
                sPswp,sFSWp=binaryWind(ap,tau,M1,R1,-1,-1,-1,early=EARLYWIND)
                sPswin,sFSWin=binaryWind(slincont,tau,M1,R1,-1,-1,-1,early=EARLYWIND)

                #VECTORS
                FXUVopt_vec+=[FXUVopt]
                FXUVp_vec+=[FXUVp]
                FXUVin_vec+=[FXUVin]
                ntFXUVopt_vec+=[ntFXUVopt]
                ntFXUVp_vec+=[ntFXUVp]
                ntFXUVin_vec+=[ntFXUVin]
                sFXUVopt_vec+=[sFXUVopt]
                sFXUVp_vec+=[sFXUVp]
                sFXUVin_vec+=[sFXUVin]
                
                FSWopt_vec+=[FSWopt]
                FSWp_vec+=[FSWp]
                FSWin_vec+=[FSWin]
                ntFSWopt_vec+=[ntFSWopt]
                ntFSWp_vec+=[ntFSWp]
                ntFSWin_vec+=[ntFSWin]
                sFSWopt_vec+=[sFSWopt]
                sFSWp_vec+=[sFSWp]
                sFSWin_vec+=[sFSWin]
            
                if verbose:
                    d="\t"*2
                    print d,"XUV Luminosity:"
                    d="\t"*3
                    print d,"Cmponent 1:",LXUV1
                    print d,"Cmponent 2:",LXUV2
                    print d,"Cmponent 1 (no tidal):",ntLXUV1
                    print d,"Cmponent 2 (no tidal):",ntLXUV2
                    print d,"Single Component 1:",sLXUV
                    d="\t"*2
                    print d,"XUV Flux:"
                    d="\t"*3
                    print d,"XUV at Inner CHZ: Binary = %e, Single = %e"%(FXUVopt,sFXUVopt)
                    d="\t"*2
                    print d,"Stellar wind flux:"
                    d="\t"*3
                    print d,"SW Flux at Optimal Distance: Binary = %e, Single = %e"%(FSWopt,sFSWopt)
                    
                if pause:raw_input()

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
        
        FXUVopt_vec=np.array(FXUVopt_vec)
        FXUVp_vec=np.array(FXUVp_vec)
        FXUVin_vec=np.array(FXUVin_vec)
        ntFXUVopt_vec=np.array(ntFXUVopt_vec)
        ntFXUVp_vec=np.array(ntFXUVp_vec)
        ntFXUVin_vec=np.array(ntFXUVin_vec)
        sFXUVopt_vec=np.array(sFXUVopt_vec)
        sFXUVp_vec=np.array(sFXUVp_vec)
        sFXUVin_vec=np.array(sFXUVin_vec)
        
        FSWopt_vec=np.array(FSWopt_vec)
        FSWp_vec=np.array(FSWp_vec)
        FSWin_vec=np.array(FSWin_vec)
        ntFSWopt_vec=np.array(ntFSWopt_vec)
        ntFSWp_vec=np.array(ntFSWp_vec)
        ntFSWin_vec=np.array(ntFSWin_vec)
        sFSWopt_vec=np.array(sFSWopt_vec)
        sFSWp_vec=np.array(sFSWp_vec)
        sFSWin_vec=np.array(sFSWin_vec)

        savetxt(SAVEDIR+"tvec",tvec)
        savetxt(SAVEDIR+"P1vec",P1vec)
        savetxt(SAVEDIR+"P2vec",P2vec)
        savetxt(SAVEDIR+"acc1_tid_vec",acc1_tid_vec)
        savetxt(SAVEDIR+"acc2_tid_vec",acc2_tid_vec)
        savetxt(SAVEDIR+"acc1_ML_vec",acc1_ML_vec)
        savetxt(SAVEDIR+"acc2_ML_vec",acc2_ML_vec)
        savetxt(SAVEDIR+"acc1_vec",acc1_vec)
        savetxt(SAVEDIR+"acc2_vec",acc2_vec)
        savetxt(SAVEDIR+"tvecX",tvecX)
        savetxt(SAVEDIR+"FXUVopt_vec",FXUVopt_vec)
        savetxt(SAVEDIR+"FXUVp_vec",FXUVp_vec)
        savetxt(SAVEDIR+"FXUVin_vec",FXUVin_vec)
        savetxt(SAVEDIR+"ntFXUVopt_vec",ntFXUVopt_vec)
        savetxt(SAVEDIR+"ntFXUVp_vec",ntFXUVp_vec)
        savetxt(SAVEDIR+"ntFXUVin_vec",ntFXUVin_vec)
        savetxt(SAVEDIR+"sFXUVopt_vec",sFXUVopt_vec)
        savetxt(SAVEDIR+"sFXUVp_vec",sFXUVp_vec)
        savetxt(SAVEDIR+"sFXUVin_vec",sFXUVin_vec)
        savetxt(SAVEDIR+"FSWopt_vec",FSWopt_vec)
        savetxt(SAVEDIR+"FSWp_vec",FSWp_vec)
        savetxt(SAVEDIR+"FSWin_vec",FSWin_vec)
        savetxt(SAVEDIR+"ntFSWopt_vec",ntFSWopt_vec)
        savetxt(SAVEDIR+"ntFSWp_vec",ntFSWp_vec)
        savetxt(SAVEDIR+"ntFSWin_vec",ntFSWin_vec)
        savetxt(SAVEDIR+"sFSWopt_vec",sFSWopt_vec)
        savetxt(SAVEDIR+"sFSWp_vec",sFSWp_vec)
        savetxt(SAVEDIR+"sFSWin_vec",sFSWin_vec)
    else:
        d="\t"*1
        print d,"Loading from files..."
        tvec=loadtxt(SAVEDIR+"tvec")
        P1vec=loadtxt(SAVEDIR+"P1vec")
        P2vec=loadtxt(SAVEDIR+"P2vec")
        acc1_tid_vec=loadtxt(SAVEDIR+"acc1_tid_vec")
        acc2_tid_vec=loadtxt(SAVEDIR+"acc2_tid_vec")
        acc1_ML_vec=loadtxt(SAVEDIR+"acc1_ML_vec")
        acc2_ML_vec=loadtxt(SAVEDIR+"acc2_ML_vec")
        acc1_vec=loadtxt(SAVEDIR+"acc1_vec")
        acc2_vec=loadtxt(SAVEDIR+"acc2_vec")
        tvecX=loadtxt(SAVEDIR+"tvecX")
        FXUVopt_vec=loadtxt(SAVEDIR+"FXUVopt_vec")
        FXUVp_vec=loadtxt(SAVEDIR+"FXUVp_vec")
        FXUVin_vec=loadtxt(SAVEDIR+"FXUVin_vec")
        ntFXUVopt_vec=loadtxt(SAVEDIR+"ntFXUVopt_vec")
        ntFXUVp_vec=loadtxt(SAVEDIR+"ntFXUVp_vec")
        ntFXUVin_vec=loadtxt(SAVEDIR+"ntFXUVin_vec")
        sFXUVopt_vec=loadtxt(SAVEDIR+"sFXUVopt_vec")
        sFXUVp_vec=loadtxt(SAVEDIR+"sFXUVp_vec")
        sFXUVin_vec=loadtxt(SAVEDIR+"sFXUVin_vec")
        FSWopt_vec=loadtxt(SAVEDIR+"FSWopt_vec")
        FSWp_vec=loadtxt(SAVEDIR+"FSWp_vec")
        FSWin_vec=loadtxt(SAVEDIR+"FSWin_vec")
        ntFSWopt_vec=loadtxt(SAVEDIR+"ntFSWopt_vec")
        ntFSWp_vec=loadtxt(SAVEDIR+"ntFSWp_vec")
        ntFSWin_vec=loadtxt(SAVEDIR+"ntFSWin_vec")
        sFSWopt_vec=loadtxt(SAVEDIR+"sFSWopt_vec")
        sFSWp_vec=loadtxt(SAVEDIR+"sFSWp_vec")
        sFSWin_vec=loadtxt(SAVEDIR+"sFSWin_vec")
    
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT XUV (PEL)
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure();ifig=0
    plt.plot(tvecX,FXUVopt_vec,'b-',label='XUV BHM @ Outer CHZ')
    #plt.plot(tvecX,FXUVp_vec,'k-',linewidth=2,label=r'XUV BHM @ $a = %.2f\,\rm{AU}$'%ap)
    plt.plot(tvecX,FXUVin_vec,'r-',label='XUV w. BHM @ Inner CHZ')
    plt.plot(tvecX,ntFXUVopt_vec,'b--',label='XUV no BHM @ Outer CHZ')
    #plt.plot(tvecX,ntFXUVp_vec,'k--',linewidth=2)
    plt.plot(tvecX,ntFXUVin_vec,'r--',label='XUV no BHM @ Inner CHZ',linewidth=2)
    plt.plot(tvecX,sFXUVopt_vec,'b:',label='Single primary @ Outer CHZ',linewidth=1)
    plt.plot(tvecX,sFXUVin_vec,'r:',label='Single primary @ Inner CHZ',linewidth=1)
    #plt.plot(tvecX,sFXUVp_vec,'k-',linewidth=2,label='Earth')
    plt.plot(earthFXUV[:,0],earthFXUV[:,1],'k-',linewidth=2,label='Earth')
    #plt.plot([],[],'k--',label='No BHM')
    #plt.plot([],[],'k:',label='Single-primary')
    #plt.plot([],[],'k-.',label='Single-primary on planet')
    #plt.xscale('log')
    plt.yscale('log')
    logTickLabels(plt.gca(),-3,3,(3,),frm='%.1f',axis='y',notation='normal',fontsize=12)
    ymin=min(min(FXUVopt_vec),min(FXUVin_vec),min(FXUVp_vec),min(sFXUVopt_vec),min(sFXUVin_vec))
    ymax=max(max(FXUVopt_vec),max(FXUVin_vec),max(FXUVp_vec),max(sFXUVopt_vec),max(sFXUVin_vec))
    plt.ylim((ymin,ymax))
    #plt.axhline(1,linestyle='--',color='k')
    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$F_{\rm XUV} ({\rm PEL})$",fontsize=LABEL_SIZE)
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.legend(loc='best',prop=dict(size=LEGEND_SIZE))
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/FluxXUV-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT XUV (RATIOS)
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure();ifig=0
    plt.plot(tvecX,FXUVopt_vec/ntFXUVopt_vec,'k-',label='BHM/no BHM')
    plt.plot(tvecX,FXUVopt_vec/sFXUVopt_vec,'k--',label='BHM/Single')
    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$F_{\rm XUV,bin}/F_{\rm XUV,ref}$",fontsize=LABEL_SIZE)
    ymin,ymax=plt.ylim()
    plt.axhspan(0.0,1.0,color='g',alpha=0.2)
    plt.axhspan(1.0,max(1.0,ymax),color='r',alpha=0.2)
    plt.ylim((0.0,max(1.0,ymax)))
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.legend(loc='best',prop=dict(size=LEGEND_SIZE))
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/RatiosFluxXUV-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT SW (SWPEL)
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    SWPEL=NSUN*VSUN
    plt.figure();ifig=0
    plt.plot(tvecX,FSWopt_vec/SWPEL,'b-',label='SW BHM @ Outer CHZ')
    #plt.plot(tvecX,FSWp_vec/SWPEL,'k-',linewidth=2,label=r'SW w. BHM @ $a = %.2f\,\rm{AU}$'%ap)
    plt.plot(tvecX,FSWin_vec/SWPEL,'r-',label='SW BHM @ Inner CHZ')
    plt.plot(tvecX,ntFSWopt_vec/SWPEL,'b--',label='SW no BHM @ Outer CHZ')
    #plt.plot(tvecX,ntFSWp_vec/SWPEL,'k--',linewidth=2)
    plt.plot(tvecX,ntFSWin_vec/SWPEL,'r--',label='SW no BHM @ Inner CHZ',linewidth=2)
    plt.plot(tvecX,sFSWopt_vec/SWPEL,'b:',label='Single primary @ Outer CHZ',linewidth=1)
    plt.plot(tvecX,sFSWin_vec/SWPEL,'r:',label='Single primary @ Inner CHZ',linewidth=1)
    plt.plot(earthFSW[:,0],earthFSW[:,1],'k-',linewidth=2,label='Earth')
    #plt.plot([],[],'k--',label='No BHM')
    #plt.plot([],[],'k:',label='Single-primary')
    #plt.plot([],[],'k-.',label='Single-primary on planet')
    #plt.xscale('log')
    plt.yscale('log')
    logTickLabels(plt.gca(),-3,3,(3,),frm='%.1f',axis='y',notation='normal',fontsize=TICS_SIZE)
    plt.xticks(fontsize=TICS_SIZE)
    ymin=min(min(FSWopt_vec),min(FSWin_vec),min(FSWp_vec),min(sFSWopt_vec),min(sFSWin_vec))
    ymax=max(max(FSWopt_vec),max(FSWin_vec),max(FSWp_vec),max(sFSWopt_vec),max(sFSWin_vec))
    ymax=1000*SWPEL
    plt.ylim((ymin/SWPEL,ymax/SWPEL))
    #plt.axhline(1,linestyle='--',color='k')
    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$F_{\rm SW} ({\rm SW.PEL})$",fontsize=LABEL_SIZE)
    plt.legend(loc='best',prop=dict(size=LEGEND_SIZE))
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/FluxSW-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT SW (RATIOS)
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure();ifig=0
    plt.plot(tvecX,FSWopt_vec/ntFSWopt_vec,'k-',label='BHM/no BHM')
    plt.plot(tvecX,FSWopt_vec/sFSWopt_vec,'k--',label='BHM/Single')
    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$F_{\rm SW,bin}/F_{\rm SW,ref}$",fontsize=LABEL_SIZE)
    ymin,ymax=plt.ylim()
    plt.axhspan(0.0,1.0,color='g',alpha=0.2)
    plt.axhspan(1.0,max(1.0,ymax),color='r',alpha=0.2)
    plt.ylim((0.0,max(1.0,ymax)))
    plt.legend(loc='best',prop=dict(size=LEGEND_SIZE))
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/RatiosFluxSW-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #INTEGRATE XUV FLUX
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    nX=len(tvecX)
    plt.figure();ifig=0
    intFXUVopt=np.array([FXUVopt_vec[:i].sum() for i in xrange(nX)])*Dt
    intFXUVin=np.array([FXUVin_vec[:i].sum() for i in xrange(nX)])*Dt
    intFXUVp=np.array([FXUVp_vec[:i].sum() for i in xrange(nX)])*Dt
    intntFXUVopt=np.array([ntFXUVopt_vec[:i].sum() for i in xrange(nX)])*Dt
    intntFXUVin=np.array([ntFXUVin_vec[:i].sum() for i in xrange(nX)])*Dt
    intntFXUVp=np.array([ntFXUVp_vec[:i].sum() for i in xrange(nX)])*Dt
    intsFXUVopt=np.array([sFXUVopt_vec[:i].sum() for i in xrange(nX)])*Dt
    intsFXUVp=np.array([sFXUVp_vec[:i].sum() for i in xrange(nX)])*Dt
    intsFXUVin=np.array([sFXUVin_vec[:i].sum() for i in xrange(nX)])*Dt
    logFXUV=int(np.log10(max(intFXUVopt)))
    FXUVscale=10**logFXUV

    plt.plot(tvecX,intFXUVopt/FXUVscale,'b-',label='Integrated XUV BHM @ Outer CHZ')
    plt.plot(tvecX,intFXUVin/FXUVscale,'r-',label='Integrated XUV BHM @ Inner CHZ')
    #plt.plot(tvecX,intFXUVp/FXUVscale,'k-',linewidth=2,label=r'Integrated XUV @ $a = %.2f\,\rm{AU}$'%ap)
    plt.plot(tvecX,intntFXUVopt/FXUVscale,'b--',label='Integrated XUV no BHM @ Outer CHZ')
    plt.plot(tvecX,intntFXUVin/FXUVscale,'r--',label='Integrated XUV no BHM @ Inner CHZ')
    plt.plot(tvecX,intsFXUVopt/FXUVscale,'b:',label='Integrated XUV single primary @ Outer CHZ')
    plt.plot(tvecX,intsFXUVin/FXUVscale,'r:',label='Integrated XUV single primary @ Inner CHZ')
    plt.plot(earthintFXUV[:,0],earthintFXUV[:,1],'k-',linewidth=2,label=r'Earth')

    #plt.plot([],[],'k--',label='No BHM')
    #plt.plot([],[],'k:',label='Single-primary')
    #plt.plot([],[],'k-.',label='Single-primary on planet')

    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$\int_0^{t} F_{\rm XUV}(t)\,dt$ ($\times 10^{%d}\,{\rm J/cm}^2$)"%logFXUV,fontsize=LABEL_SIZE)
    plt.legend(loc='lower right',prop=dict(size=10))
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/IntFXUV-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #INTEGRATED SW FLUX
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    nX=len(tvecX)
    plt.figure();ifig=0
    intFSWopt=np.array([FSWopt_vec[:i].sum() for i in xrange(nX)])*Dt
    intFSWin=np.array([FSWin_vec[:i].sum() for i in xrange(nX)])*Dt
    intFSWp=np.array([FSWp_vec[:i].sum() for i in xrange(nX)])*Dt
    intntFSWopt=np.array([ntFSWopt_vec[:i].sum() for i in xrange(nX)])*Dt
    intntFSWin=np.array([ntFSWin_vec[:i].sum() for i in xrange(nX)])*Dt
    intntFSWp=np.array([ntFSWp_vec[:i].sum() for i in xrange(nX)])*Dt
    intsFSWopt=np.array([sFSWopt_vec[:i].sum() for i in xrange(nX)])*Dt
    intsFSWp=np.array([sFSWp_vec[:i].sum() for i in xrange(nX)])*Dt
    intsFSWin=np.array([sFSWin_vec[:i].sum() for i in xrange(nX)])*Dt
    logFSW=int(np.log10(max(intFSWopt)))
    FSWscale=10**logFSW

    plt.plot(tvecX,intFSWopt/FSWscale,'b-',label='Integrated SW BHM @ Outer')
    plt.plot(tvecX,intFSWin/FSWscale,'r-',label='Integrated SW BHM @ Inner CHZ')
    #plt.plot(tvecX,intFSWp/FSWscale,'k-',linewidth=2,label=r'Integrated SW @ $a = %.2f\,\rm{AU}$'%ap)
    plt.plot(tvecX,intntFSWopt/FSWscale,'b--',label='Integrated SW no BHM @ Outer CHZ')
    plt.plot(tvecX,intntFSWin/FSWscale,'r--',label='Integrated SW BHM @ Inner CHZ')
    plt.plot(tvecX,intsFSWopt/FSWscale,'b:',label='Integrated SW single primary @ Outer CHZ')
    plt.plot(tvecX,intsFSWin/FSWscale,'r:',label='Integrated SW single primary @ Inner CHZ')
    plt.plot(earthintFSW[:,0],earthintFSW[:,1],'k-',linewidth=2,label=r'Earth')
    #plt.plot([],[],'k--',label='No BHM')
    #plt.plot([],[],'k:',label='Single-primary')
    #plt.plot([],[],'k-.',label='Single-primary on planet')

    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$\int_0^{t} n_{\rm SW}\,v_{\rm SW}\,dt$ ($\times 10^{%d}\,{\rm ions/m}^2$)"%logFSW,
               fontsize=LABEL_SIZE)
    plt.legend(loc='lower right',prop=dict(size=10))
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/IntFSW-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #MASS-LOSS AT INNER CHZ VS. PLANET.MASS
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure();ifig=0
    
    Mpvec=linspace(0.1,10.0,100)
    Pl=[]
    ntPl=[]
    sPl=[]
    sPlp=[]
    for Mp in Mpvec:

        #PLANETARY PROPERTIES
        Rp=Mp**0.25
        gp=GCONST*(Mp*MEARTH)/(Rp*Rp_E)**2
        Ap=2*PI*(Rp*Rp_E)**2 #m^2

        #ACCUMULATED FLUX AT INNER CHZ
        MLfac=intFSWin[-1]
        ntMLfac=intntFSWin[-1]
        sMLfac=intsFSWin[-1]
        sMLfacp=intsFSWp[-1]

        #MASS LOSS
        Ml=ALPHA*MLfac*Ap*MUATM*MP
        Pl+=[Ml*gp/(2*Ap)/1E5]

        ntMl=ALPHA*ntMLfac*Ap*MUATM*MP
        ntPl+=[ntMl*gp/(2*Ap)/1E5]

        sMl=ALPHA*sMLfac*Ap*MUATM*MP
        sPl+=[sMl*gp/(2*Ap)/1E5]

        sMlp=ALPHA*sMLfacp*Ap*MUATM*MP
        sPlp+=[sMlp*gp/(2*Ap)/1E5]

    plt.plot(Mpvec,Pl,'k-',label='Mass loss BHM')
    plt.plot(Mpvec,ntPl,'k--',label='Mass loss no BHM')
    plt.plot(Mpvec,sPl,'k:',label='Mass loss single-primary')
    plt.plot(earthML[:,0],earthML[:,1],'k-',linewidth=2,label='Single solar-mass, $a = 1$ AU')

    plt.xlabel("$M_p/M_\oplus$",fontsize=LABEL_SIZE)
    plt.ylabel(r"$P_{\rm loss}\,({\rm bars})$",fontsize=LABEL_SIZE)
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.legend(loc='upper left',prop=dict(size=LEGEND_SIZE))
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/MassLoss-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT PERIOD
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure();ifig=0
    plt.plot(tvec,np.array(P1vec),'b-',label='Primary')
    plt.plot(tvec,np.array(P2vec),'r-',label='Secondary')
    plt.plot(tvec,theoProt(tvec,xfit1),'b--',label='Primary (no tidal)')
    plt.plot(tvec,theoProt(tvec,xfit2),'r--',label='Secondary (no tidal)')
    #plt.grid()
    plt.xlabel(r"$t$ (Gyr)",fontsize=LABEL_SIZE)
    plt.ylabel(r"$P$ (day)",fontsize=LABEL_SIZE)
    plt.axhline(Psync,linestyle='-',color='k')
    plt.axhline(Pbin/1.0,linestyle='-',color='c',linewidth=2,label='1:1 Resonance')
    plt.axhline(Pbin/1.5,linestyle='--',color='c',linewidth=2,label='3:2 Resonance')
    plt.axhline(Pbin/2.0,linestyle='-.',color='c',linewidth=2,label='2:1 Resonance')
    plt.xticks(fontsize=TICS_SIZE)
    plt.yticks(fontsize=TICS_SIZE)
    plt.legend(loc='best',prop=dict(size=LEGEND_SIZE))
    plt.title(titlebin,position=(0.5,1.04))
    saveFig(TMPDIR+"/PeriodEvolution-%s.png"%suffix)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #PLOT ACCELERATIONS
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    plt.figure();ifig=0
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
    plt.title(titlebin,position=(0.5,1.02))
    saveFig(TMPDIR+"/AccelerationEvolution-%s.png"%suffix)

############################################################
#ROUTINES
############################################################
solution=Run()
fout.close()
