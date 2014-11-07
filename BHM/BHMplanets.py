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
# Planetary Evolution Routines
###################################################
from BHM import *
from BHM.BHMnum import *
from BHM.BHMastro import *

###################################################
#LIMITATIONS
###################################################
"""
Since this module works with a planetary grid there are some
limitations in mass and composition:

Planetary mass: M (mass in Earth masses), Mg (Mass in Jupiter Masses)

   1.0 < M < 7.0
   0.05 < M < 11.3

Core mass fraction: CMF (Earth = 0.34)

   0.1 < CMF < 0.8

Hydrogen/Helium fraction: f_H/He (Jupiter = 0.97)

   0.0 < f_H/He < 1.0
"""

###################################################
#PACKAGES
###################################################

###################################################
#CONFIGURATION
###################################################
DIRPLGIRD=DATA_DIR+"SolidPlanets/MobileLids"

###################################################
#MACROS
###################################################

###################################################
#GLOBALS
###################################################
#SOLID PLANET MODELS
MPS=[]
MODELS=[]
CMFS=[]
IMFS=[]

#THERMAL EVOLUTION MODEL FIELDS
IT=0
IQCONV=1
IRIC=2
IRSTAR=3
IQC=4
IQM=5
IQR=6
ITCMB=7
ITL=8
ITUP=9
IRIFLAG=10
"""
STRUC FIELDS:
0:ur, 1:r, 2:mr, 3:rho, 4:P, 5:g, 6:phi, 7:T, 8:composition

TEVOL FIELDS:
0:t, 1:Qconv[W], 2:Ri[Rp], 3:R*[Rp], 4:Qc[W], 5:Qm[W], 6:Qr[W], 7:Tcmb[K], 
8:Tl[K], 9:Tup[K], 10:RiFlag, 11:Bs[T]
"""

#GAS-ICE GIANTS
Giants=dict()
CS=['S','0','10','25','50','100']
Gtimes=[0.001,0.0032,0.01,0.0316,0.1,0.3126,
        1.0,3.1623,10.0]
GMemin=1E100*np.ones_like(Gtimes)
GMemax=0*np.ones_like(Gtimes)
GMjmin=1E100*np.ones_like(Gtimes)
GMjmax=0*np.ones_like(Gtimes)
GRjmin=1E100*np.ones_like(Gtimes)
GRjmax=0*np.ones_like(Gtimes)
GMsmin=1E100
GMsmax=0

###################################################
#ROUTINES
###################################################

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#GAS-ICE GIANTS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def t2i(t):
    for i in xrange(0,len(Gtimes)):
        if Gtimes[i]==t:
            return i
    return 0

def MultiBisect(func,ref,a,b,n,verbose=False):
    """
    Multi Bisection Algorithm
    """
    def fsw(x):
        return func(x)-ref
    dx=(b-a)/n
    ms=[]
    for x in np.arange(a,b,dx):
        x1=max(x,a)
        x2=min(x+dx,b)
        m=Bisect(fsw,x1,x2)
        if m>0:ms+=[m]
    return ms

def loadIceGasGiantsGrid(dirplgrid,verbose=False):
    global GMemin,GMemax,GMjmin,GMjmax,GMsmax,GRjmin,GRjmax,GRsmax,Gtimes
    if verbose:PRINTOUT("Loading Ice-Gas Giants Grid")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #READING SOLID DATA
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    data=np.loadtxt(dirplgrid+"SOLID-MC_10_100.dat")
    GMsmax=data[:,0].max()*MEARTH/MJUP
    GRsmax=data[:,1].max()
    Giants['S']=dict2obj(dict())
    Giants['S'].time=[]
    for i in xrange(0,len(Gtimes)):
        Giants['S'].time+=[dict()]
        Ms=data[:,0]*MEARTH/MJUP
        Rs=data[:,1]
        Giants['S'].time[i]['Mj2Rj']=interp1d(Ms,Rs,kind='linear')
        Giants['S'].time[i]['Mjmin']=Ms.min()
        Giants['S'].time[i]['Mjmax']=Ms.max()
        Giants['S'].time[i]['Rjmin']=Rs.min()
        Giants['S'].time[i]['Rjmax']=Rs.max()
        Giants['S'].time[i]=dict2obj(Giants['S'].time[i])

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #READING GAS DATA
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for C in CS[1:]:
        data=np.loadtxt(dirplgrid+"GIANTS-MC_%s-A_1AU.dat"%C)
        if verbose:PRINTOUT("Reading data for core mass %s..."%C)
        ndata=data.shape[0]
        qchange=0
        Meold=0
        GiantsMatrix=[]
        giant=[]
        for i in xrange(0,ndata):
            row=data[i]
            Me=row[0]
            if Me<Meold:
                nmass=len(giant)
                GiantsMatrix+=[np.array(giant)]
                giant=[]
            giant+=[row]
            Meold=Me
        GiantsMatrix+=[np.array(giant)]
        ntimes=len(GiantsMatrix)
        Giants[C]=dict2obj(dict(data=np.array(GiantsMatrix)))
        Giants[C].time=[]
        Rbis=[]

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #CREATING INTERPOLATING FUNCTIONS AT EACH TIME
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        for i in xrange(0,ntimes):
            Giants[C].time+=[dict()]
            matrix=Giants[C].data[i]
            nmass=matrix.shape[0]

            Giants[C].time[i]['time']=Gtimes[i]
            Giants[C].time[i]['nmass']=nmass
            
            addMs=np.array([])
            addRs=np.array([])
            if float(C)>0:
                addMs=np.array([float(C)*MEARTH/MJUP])
                addRs=np.array([Giants['S'].time[0].Mj2Rj(float(C)*MEARTH/MJUP)])
            Mss=np.concatenate((addMs,matrix[:,0]))
            Rss=np.concatenate((addRs,matrix[:,2]))
            
            Memin=Mss.min()
            Giants[C].time[i]['Memin']=Memin
            GMemin[i]=min(GMemin[i],Memin)
            Memax=Mss.max()
            Giants[C].time[i]['Memax']=Memax
            GMemax[i]=max(GMemax[i],Memax)

            Me2Rj=interp1d(Mss,Rss,kind='slinear')
            Giants[C].time[i]['Me2Rj']=Me2Rj

            addMs=np.array([])
            addRs=np.array([])
            if float(C)>0:
                addMs=np.array([float(C)*MEARTH/MJUP])
                addRs=np.array([Giants['S'].time[0].Mj2Rj(float(C)*MEARTH/MJUP)])
            Mss=np.concatenate((addMs,matrix[:,1]))
            Rss=np.concatenate((addRs,matrix[:,2]))

            Mjmin=Mss.min()
            Giants[C].time[i]['Mjmin']=Mjmin
            GMjmin[i]=min(GMjmin[i],Mjmin)
            Mjmax=Mss.max()
            Giants[C].time[i]['Mjmax']=Mjmax
            GMjmax[i]=max(GMjmax[i],Mjmax)

            Mj2Rj=interp1d(Mss,Rss,kind='slinear')
            Giants[C].time[i]['Mj2Rj']=Mj2Rj

            Rjmin=Rss.min()
            Giants[C].time[i]['Rjmin']=Rjmin
            GRjmin[i]=min(GRjmin[i],Rjmin)
            Rjmax=Rss.max()
            Giants[C].time[i]['Rjmax']=Rjmax
            GRjmax[i]=max(GRjmax[i],Rjmax)

            Tini=matrix[0,4]
            Giants[C].time[i]['Tini']=Tini
            
            Giants[C].time[i]=dict2obj(Giants[C].time[i])

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CREATING INTERPOLATING FUNCTIONS FOR QINT AND TINT SOLID
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i in xrange(0,len(Gtimes)):
        Tint=[]
        Qint=[]
        Ms=[]
        for C in CS[2:]:
            Mj=float(C)*MEARTH/MJUP
            Ms+=[Mj]
            Tini=Giants[C].time[i].Tini
            Tint+=[Tini]
            Rj=Giants['S'].time[i].Mj2Rj(Mj)
            Q=4*np.pi*(Rj*RJUP)**2*SIGMA*(Tini**4)
            Qint+=[Q]
        Giants['S'].time[i].Qint=interp1d(Ms,Qint,kind='slinear')
        Giants['S'].time[i].Tint=interp1d(Ms,Tint,kind='slinear')

    Giants['S'].Radius=lambda Mp,t:Giants['S'].time[0].Mj2Rj(Mp)
    Giants['S'].Qinterior=lambda Mp,t:Giants['S'].time[0].Qint(Mp)
    Giants['S'].Tinterior=lambda Mp,t:Giants['S'].time[0].Tint(Mp)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CREATING INTERPOLATING FUNCTIONS FOR QINT AND TINT GAS
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for C in CS[1:]:
        for i in xrange(0,len(Gtimes)):
            matrix=Giants[C].data[i]

            addMs=np.array([])
            addTs=np.array([])
            if float(C)>0:
                addMs=np.array([float(C)*MEARTH/MJUP])
                addTs=np.array([Giants['S'].time[i].Tint(float(C)*MEARTH/MJUP)])
            Mss=np.concatenate((addMs,matrix[:,1]))
            Tss=np.concatenate((addTs,matrix[:,4]))
            Tint=interp1d(Mss,Tss,kind='slinear')
            Giants[C].time[i].Tint=Tint

            addMs=np.array([])
            addQs=np.array([])
            if float(C)>0:
                addMs=np.array([float(C)*MEARTH/MJUP])
                addQs=np.array([Giants['S'].time[i].Qint(float(C)*MEARTH/MJUP)])
            Mss=np.concatenate((addMs,matrix[:,1]))
            Qss=np.concatenate((addTs,matrix[:,5]/1E7))
            Qint=interp1d(Mss,Qss,kind='slinear')
            Giants[C].time[i].Qint=Qint

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #CREATING INTERPOLATION FUNCTION FOR TIME AND MASS
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Gtimes=np.array(Gtimes)
    nGtimes=Gtimes.shape[0]
    def Property(COMP,Mp,t,prop):
        #print COMP,Mp,t,prop
        id=np.arange(0,nGtimes)
        its=id[Gtimes==t]
        if len(its):
            it=its[0]
            try:
                p=eval("Giants[COMP].time[it].%s(Mp)"%prop)
            except:
                p=-1
        else:
            lages=id[Gtimes<=t]
            gages=id[Gtimes>t]
            iless=lages[-1]
            igreat=gages[0]
            t1=Gtimes[iless]
            t2=Gtimes[igreat]
            try:
                p1=eval("Giants[COMP].time[iless].%s(Mp)"%prop)
                p2=eval("Giants[COMP].time[igreat].%s(Mp)"%prop)
                logp=np.log10(p1)+(np.log10(p2)-np.log10(p1))/(np.log10(t2)-np.log10(t1))*(np.log10(t)-np.log10(t1))
                p=10**logp
            except:
                p=-1
            
        return p
        
    Giants['0'].Radius=lambda Mp,t:Property('0',Mp,t,'Mj2Rj')
    Giants['0'].Qinterior=lambda Mp,t:Property('0',Mp,t,'Qint')
    Giants['0'].Tinterior=lambda Mp,t:Property('0',Mp,t,'Tint')
    
    Giants['10'].Radius=lambda Mp,t:Property('10',Mp,t,'Mj2Rj')
    Giants['10'].Qinterior=lambda Mp,t:Property('10',Mp,t,'Qint')
    Giants['10'].Tinterior=lambda Mp,t:Property('10',Mp,t,'Tint')

    Giants['25'].Radius=lambda Mp,t:Property('25',Mp,t,'Mj2Rj')
    Giants['25'].Qinterior=lambda Mp,t:Property('25',Mp,t,'Qint')
    Giants['25'].Tinterior=lambda Mp,t:Property('25',Mp,t,'Tint')

    Giants['50'].Radius=lambda Mp,t:Property('50',Mp,t,'Mj2Rj')
    Giants['50'].Qinterior=lambda Mp,t:Property('50',Mp,t,'Qint')
    Giants['50'].Tinterior=lambda Mp,t:Property('50',Mp,t,'Tint')

    Giants['100'].Radius=lambda Mp,t:Property('100',Mp,t,'Mj2Rj')
    Giants['100'].Qinterior=lambda Mp,t:Property('100',Mp,t,'Qint')
    Giants['100'].Tinterior=lambda Mp,t:Property('100',Mp,t,'Tint')

    
    """
    Examples:
    C='100'
    print Giants[C].Radius(0.5,0.7)
    print Giants[C].Tinterior(0.5,0.7)
    print Giants[C].Qinterior(0.5,0.7)
    exit(0)

    Mj=10*MEARTH/MJUP
    print Giants['100'].time[6].Tint(2.0)
    print Mj,Giants['S'].time[0].Qint(Mj)/QINTJUP
    
    print Giants['10'].time[6].Rjini
    print Giants['0'].time[0].time
    print Giants['0'].time[0].nmass
    print Giants['0'].time[0].Mjmin
    print Giants['0'].time[0].Rjmin,Giants['0'].time[0].Rjmax
    print Giants['0'].time[0].Mj2Rj(0.3)

    Mjmin=Giants['10'].time[0].Mjmin
    Mjmax=Giants['10'].time[0].Mjmax
    print Mjmin,Mjmax
    Mj2Rj=Giants['10'].time[0].Mj2Rj
    print MultiBisect(Mj2Rj,2.0,Mjmin,Mjmax,100)
    """

def M2R(Mj,it=0,COMPS=CS,verbose=False,units='jupiter',unpack=4):
    
    if units=='earth':
        factor=MEARTH/MJUP
    else:
        factor=1

    Mjmin=GMjmin[it]
    Mjmax=GMjmax[it]
    Mj=Mj*factor

    Rsup=0
    Rinf=1E100
    qenclose=0
    for C in COMPS:
        Mjmin=Giants[C].time[it].Mjmin
        Mjmax=Giants[C].time[it].Mjmax
        if verbose:print "Testing %s: Ms = (%e,%e)"%(C,Mjmin,Mjmax)
        if Mj>Mjmin and Mj<Mjmax:
            qenclose=1
            R=Giants[C].time[it].Mj2Rj(Mj)
            if R>Rsup:
                Rsup=R
                Csup=C
            if R<Rinf:
                Rinf=R
                Cinf=C
        else:
            if verbose:print "%e MJ no enclosed by %s"%(Mj,C)
            pass
            
    if not qenclose:
        if verbose:print "Mass %e MJ out of range [%e,%e] MJ"%(Mj,Mjmin,Mjmax)
        if unpack==4:return -1,-1,-1,-1
        else:return -1,-1
    else:
        if unpack==4:return Rinf,Cinf,Rsup,Csup
        else:return Rinf,Rsup

def PlanetIceGasProperties(Mp,tau,fHHe=1.0,verbose=False,tolM=1E-2):
    if tau>10:tau=10

    stimes=Gtimes<=tau
    it=t2i(Gtimes[stimes][-1])
    if fHHe==1.0:
        C='0'
        Mpmin=Giants[C].time[it].Mjmin
        Mpmax=Giants[C].time[it].Mjmax
        if Mp<Mpmin or Mp>Mpmax:
            if verbose:print "Mass %e is out of range (%e,%e)"%(Mp,Mpmin,Mpmax)
            return -1,-1,-1
        else:
            return Giants[C].Radius(Mp,tau),Giants[C].Tinterior(Mp,tau),Giants[C].Qinterior(Mp,tau)
    elif fHHe==0.0:
        C='S'
        Mpmin=Giants[C].time[it].Mjmin
        Mpmax=Giants[C].time[it].Mjmax
        if Mp<Mpmin or Mp>Mpmax:
            if verbose:print "Mass %e is out of range (%e,%e)"%(Mp,Mpmin,Mpmax)
            return -1
        else:
            return Giants[C].Radius(Mp,tau),0,0
    else:
        Ms=[]
        Rs=[]
        Ts=[]
        Qs=[]
        for C in CS[2:]:
            Mc=float(C)*MEARTH/MJUP
            if verbose:print "Testing C = %s ME, Mc = %e MJ"%(C,Mc)
            Mpmin=Giants[C].time[it].Mjmin
            Mpmax=Giants[C].time[it].Mjmax
            if verbose:print "\tExtreme masses: %e - %e"%(Mpmin,Mpmax)
            Mpvec=np.logspace(np.log10(Mpmin),np.log10(Mpmax),50)
            qold=0
            f1=0
            for M in Mpvec[::-1]:
                M=round(M,3)
                f2=1-Mc/M
                if verbose:print "\t\tTesting M = %e, f = %e against fHHe = %e"%(M,f2,fHHe)
                if f2<fHHe and qold:
                    M2=M
                    R2=Giants[C].Radius(M,tau)
                    T2=Giants[C].Tinterior(M,tau)
                    Q2=Giants[C].Qinterior(M,tau)
                    M=(M2-M1)/(f2-f1)*(fHHe-f1)+M1
                    R=(R2-R1)/(f2-f1)*(fHHe-f1)+R1
                    T=(T2-T1)/(f2-f1)*(fHHe-f1)+T1
                    Q=(Q2-Q1)/(f2-f1)*(fHHe-f1)+Q1
                    if verbose:
                        print "\tM = %e"%M
                        print "\tf1 = %e, R1 = %e, T1 = %e, Q1 = %e"%(f1,R1,T1,Q1)
                        print "\tf2 = %e, R2 = %e, T2 = %e, Q2 = %e"%(f2,R2,T2,Q2)
                        print "\tf = %e, R = %e, T = %e, Q = %e"%(fHHe,R,T,Q)
                    break
                f1=f2
                M1=M
                R1=Giants[C].Radius(M,tau)
                T1=Giants[C].Tinterior(M,tau)
                Q1=Giants[C].Qinterior(M,tau)
                if verbose:print "\tM1 = %e, f1 = %e, R1 = %e, T1 = %e, Q1 = %e, tau = %e"%(M1,f1,R1,T1,Q1,tau)
                qold=1
            Ms+=[M]
            Rs+=[R]
            Ts+=[T]
            Qs+=[Q]

    dM=-1
    if Mp<Ms[0]:
        dM=abs(Mp-Ms[0])/Ms[0]
        Rref=Rs[0]
        Tref=Ts[0]
        Qref=Qs[0]
    if Mp>Ms[-1]:
        dM=abs(Mp-Ms[-1])/Ms[-1]
        Rref=Rs[-1]
        Tref=Ts[-1]
        Qref=Qs[-1]
    if verbose:print "dM = %e, Ms = "%dM,Ms
    if dM>tolM:
        if verbose:print "Mass %e is out of range (%e,%e)"%(Mp,Ms[0],Ms[-1])
        if Mp>0.3:
            Mc=10*MEARTH/MJUP
            f1=1-Mc/Mp
            R1=Giants['10'].Radius(Mp,tau)
            T1=Giants['10'].Tinterior(Mp,tau)
            Q1=Giants['10'].Qinterior(Mp,tau)
            f2=1.0
            R2=Giants['0'].Radius(Mp,tau)
            T2=Giants['0'].Tinterior(Mp,tau)
            Q2=Giants['0'].Qinterior(Mp,tau)
            if verbose:
                d="\t"
                print d,"Interpolating beyond Mc = 10"
                print d,"Fraction at Mc = 10, f = %e against fHHe = %e"%(f1,fHHe)
                print d,"Data at Mc = 10: R = %e, T = %e, Q = %e"%(R1,T1,Q1)
                print d,"Data at Mc = 0: R = %e, T = %e, Q = %e"%(R2,T2,Q2)
            R=(R2-R1)/(f2-f1)*(fHHe-f1)+R1
            T=(T2-T1)/(f2-f1)*(fHHe-f1)+T1
            Q=(Q2-Q1)/(f2-f1)*(fHHe-f1)+Q1
            return R,T,Q
        else:
            return -1,-1,-1
    elif dM>0:
        if verbose:print "Returning extreme values: Rs = %e, Ts = %e, Qs = %e"%(Rref,Tref,Qref)
        return Rref,Tref,Qref

    radiusMpf=interp1d(Ms,Rs,kind='slinear')
    temperatureMpf=interp1d(Ms,Ts,kind='slinear')
    heatMpf=interp1d(Ms,Qs,kind='slinear')
    
    try:
        Rp=radiusMpf(Mp)
        Tint=temperatureMpf(Mp)
        Qint=heatMpf(Mp)
    except:
        Rp=-1
        Tint=-1
        Qint=-1
    
    return Rp,Tint,Qint

"""
EXAMPLES:

core='0'
t=3.1623
i=t2i(t)
planet=Giants[core].time[i]
Mpmin=planet.Mjmin
Mpmax=planet.Mjmax
Rpmin=planet.Rjmin
Rpmax=planet.Rjmax
print Mpmin,Mpmax,Rpmin,Rpmax

Mp=0.5
Rp=planet.Mj2Rj(Mp)
Tint=planet.Tint(Mp)
Qint=planet.Qint(Mp)
print Mp,Rp,Tint,Qint

core='10'
planet=Giants[core]

Mp=0.5
t=8.5
Rp=planet.Radius(Mp,t)
Tint=planet.Tinterior(Mp,t)
Qint=planet.Qinterior(Mp,t)
print t,Mp,Rp,Tint,Qint

Mp=0.5
Rp=M2R(Mp)
print Rp

t=3.1623
i=t2i(t)
Mp=1.0
Rp=M2R(Mp,it=i,COMPS=['10','25'])
print t,Mp,Rp

Mp=1.0
t=0.1
fHHe=1.0
Rp,Tint,Qint=PlanetProperties(Mp,t,fHHe)
print Rp,Tint,Qint

"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#SOLID PLANETS
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def loadSolidPlanetsGrid(dirplgrid,verbose=False):
    """
    LOAD PLANETARY GRID PROPERTIES:
    Masses (MPS), Core mass fractions (CMFS), Ice mass fractions (IMFS)
    """
    global MODELS,CMFS,IMFS,MPS
    if verbose:PRINTOUT("Loading Solid Planet Grid")
    list=System("cd %s;ls -d CMF*"%dirplgrid,out=True)
    MODELS+=list.split()
    cmfs=[]
    imfs=[]
    for model in MODELS:
        cmf,imf=model.split('-')
        cmfs+=[float(cmf[4:])]
        imfs+=[float(imf[4:])]
    if verbose:PRINTOUT("%d models load..."%len(MODELS))
    CMFS+=np.unique(np.array(cmfs)).tolist()
    IMFS+=np.unique(np.array(imfs)).tolist()
    list=System("cd %s/%s;ls -d *STRUC*"%(dirplgrid,MODELS[0]),out=True)
    files=list.split()
    Mps=[]
    for file in files:
        parts=file.split('-')
        Mps+=[float(parts[0][1:])]
    MPS+=np.unique(np.array(Mps)).tolist()

    CMFS=np.array(CMFS)
    IMFS=np.array(IMFS)
    MPS=np.array(MPS)

    del((list,cmfs,imfs,Mps))

def loadPlanetCell(Mp=1.0,CMF=0.32,IMF=0.00,dirplgrid="",verbose=True):
    """
LOAD PLANETARY CELL AROUND A MASS AND COMPOSITION.

A planetary grid sample a 3D space: MP, CMF, IMF.  Grid is sampled in
discrete values of this space.  If you provide a point in this space
you will have 8 neighbors:

    ML < MP < MU

    for ML and MU:

              IMFL

       CMFL   POINT   CMFU

              IMFU


Get a cell object:

   model : dictionary having values of the corners (Mp,CMF,IMF)

   sig : signature of the cell.  Array with the values of CMF:IMF:Mp
         at the corners of the cell

   cmfs : range of cmf enclosing data point

   imfs : range of imf enclosing data point 

   mps : range of masses enclosing data point 

   struct : Matrix of structure data - model x points x fields
            0:ur, 1:r, 2:mr, 3:rho, 4:P, 5:g, 6:phi, 7:T, 8:composition
   
   tevol : Matrix of thermal evolution data - model x points x fields
           0:t, 1:Qconv[W], 2:Ri[Rp], 3:R*[Rp], 4:Qc[W], 5:Qm[W], 6:Qr[W], 7:Tcmb[K], 
           8:Tl[K], 9:Tup[K], 10:RiFlag, 11:Bs[T]

Usage:

   cell=loadPlanetCell(Mp=2.9,CMF=0.28,IMF=0.15,verbose=False)
   print cell.sig
   print cell.model.Mp
   print cell.struct.shape
   print cell.struct[0] #The structure of the planet having properties cell.sig[0]

   """
    #GLOBALS
    global CMFS,IMFS,MPS

    #ARRAYS
    PGSTRUC=[]
    PGTEVOL=[]
    PGFULL=[]
    PGVAL=[]

    #CMF
    cond=abs(CMFS-CMF)<1E-5
    if np.size(CMFS[cond])>0:
        lcmf=ucmf=CMF
        if verbose:print "Point in the Grid."
    else:
        lcmfs=CMFS[CMFS<=CMF]
        ucmfs=CMFS[CMFS>=CMF]
        lcmf=lcmfs[-1]
        ucmf=ucmfs[0]
    if verbose:print "LCMF,UCMF:",lcmf,ucmf

    #IMF
    cond=abs(IMFS-IMF)<1E-5
    if np.size(IMFS[cond])>0:
        limf=uimf=IMF
        if verbose:print "Point in the Grid."
    else:
        limfs=IMFS[IMFS<=IMF]
        uimfs=IMFS[IMFS>=IMF]
        limf=limfs[-1]
        uimf=uimfs[0]
    if verbose:print "LIMF,UIMF:",limf,uimf

    #LCMF,LIMF
    mps=[]
    for c in ['l','u']:
        for i in ['l','u']:
            cmd="'CMF_%.2f-IMF_%.2f'"
            cmd+="%%(%scmf,%simf)"%(c,i)
            model=eval(cmd)
            cmd="'%.2f:%.2f'"
            cmd+="%%(%scmf,%simf)"%(c,i)
            modelsig=eval(cmd)
            if verbose:print "Reading model:%s"%model
            list=System("cd %s/%s;ls *STRUC*"%(dirplgrid,model),out=True)
            if 'No' in list:continue
            files=list.split()
            Mps=[]
            for file in files:
                parts=file.split('-')
                Mps+=[float(parts[0][1:])]
            Mps=np.array(Mps)
            Mps.sort()
            lcmps=Mps[Mps<=Mp]
            ucmps=Mps[Mps>=Mp]
            lcmp=lcmps[-1];ucmp=ucmps[0]
            mps+=[lcmp,ucmp]
            if verbose:print "UCMP,LCMP:",ucmp,lcmp
            file="%s/%s/M%.2f-STRUC.dat"%(dirplgrid,model,lcmp)
            strl=np.loadtxt(file)
            file="%s/%s/M%.2f-STRUC.dat"%(dirplgrid,model,ucmp)
            stru=np.loadtxt(file)
            PGSTRUC+=[strl,stru]
            file="%s/%s/M%.2f-TEVOL.dat"%(dirplgrid,model,lcmp)
            tevl=np.loadtxt(file)
            file="%s/%s/M%.2f-TEVOL.dat"%(dirplgrid,model,ucmp)
            tevu=np.loadtxt(file)
            PGTEVOL+=[tevl,tevu]
            PGFULL+=[(strl,tevl),(stru,tevu)]
            PGVAL+=["%s:%s"%(modelsig,lcmp),"%s:%s"%(modelsig,ucmp)]

    if np.size(np.unique(PGVAL))==1:
        PGVAL=np.unique(PGVAL)
        nsig=1
    else:
        nsig=np.size(PGVAL)/2
        if nsig<4:
            #IF IT'S A 3 POINT INTERPOLATION CHECK THAT IT IS IN HALF-CELL
            dC=CMF-lcmf
            rdC=ucmf-CMF
            dI=IMF-limf
            ratIC=dI/rdC
            if dI/rdC-1>=1E-5:1/0

    cell=dict2obj(dict(
            model=dict2obj(dict(Mp=Mp,CMF=CMF,IMF=IMF)),
            nsig=nsig,
            sig=np.array(PGVAL),
            cmfs=[lcmf,ucmf],
            imfs=[limf,uimf],
            mps=mps,
            struct=PGSTRUC,
            tevol=PGTEVOL,
            full=PGFULL,
            ))

    return cell

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#STRUCTURE BULK PROPERTIES
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
"""
STRUC FIELDS:
0:ur, 1:r, 2:mr, 3:rho, 4:P, 5:g, 6:phi, 7:T, 8:composition

TEVOL FIELDS:
0:t, 1:Qconv[W], 2:Ri[Rp], 3:R*[Rp], 4:Qc[W], 5:Qm[W], 6:Qr[W], 7:Tcmb[K], 
8:Tl[K], 9:Tup[K], 10:RiFlag, 11:Bs[T]
"""
def getRadius(struc,**args):
    R=struc[-1,1]
    return R

def getCentralPressure(struc,**args):
    P=struc[0,4]
    return P

def getCentralDensity(struc,**args):
    rho=struc[0,3]
    return rho

def getSurfaceGravitationalField(struc,**args):
    g=struc[-1,5]
    return g

def getCoreDensity(struc,**args):
    core=struc[:,8]==0
    rhocs=struc[core,3]
    return rhocs[-3]

def getCoreRadius(struc,**args):
    core=struc[:,8]==0
    Rs=struc[core,1]
    return Rs[-1]

def getCoreGravitationalField(struc,**args):
    core=struc[:,8]==0
    gs=struc[core,5]
    g=gs.mean()
    return g

def getMantleAverageDensity(struc,**args):
    mantle=struc[:,8]==1
    rhocs=struc[mantle[3:-3],3]
    return rhocs.mean()

def getMantleThick(struc,**args):
    mantle=struc[:,8]==1
    Rs=struc[mantle,0]
    return Rs[-1]-Rs[0]

def getMantleGravitationalField(struc,**args):
    mantle=struc[:,8]==1
    gs=struc[mantle,5]
    g=gs.mean()
    return g

def getIceThick(struc,**args):
    ice=struc[:,8]==2
    Rs=struc[ice,0]
    if np.size(Rs)==0:return 0
    else:return Rs[-1]-Rs[0]

def getIcePressure(struc,**args):
    mantle=struc[:,8]==1
    Ps=struc[mantle,4]
    return Ps[-1]

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#THERMAL BULK PROPERTIES
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def getInitialTCMB(tevol,**args):
    try:TCMB=tevol[1,7]
    except:TCMB=tevol[7]
    return TCMB

def getInitialDeltaTCMB(tevol,**args):
    try:DeltaT=tevol[1,7]-tevol[1,8]
    except:DeltaT=tevol[7]-tevol[8]
    return DeltaT

def getTimeInnerCore(tevol,**args):
    try:tdyn=tevol[-1,0]
    except:tdyn=1E8
    try:
        Riflag=tevol[:,10]==0
        ts=tevol[Riflag,0]
        tic=ts[-1]
    except:
        tic=tevol[0]
    return tic/tdyn

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#DYNAMO BULK PROPERTIES
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def getDynamoLifetime(tevol,**args):
    try:tau=tevol[-1,0]
    except IndexError:tau=1E8
    return tau

def getAbsoluteMaximumDipoleMoment(tevol,
                           R=1,M=1,
                           Rc=0.5,rhoc=1E4,P=1,
                           sigma=sigma_E,kappa=kappa_E):
    try:
        Qconvs=tevol[1:,1]
        Rics=tevol[1:,2]
    except:
        if tevol[1]<0:return 0
        Qconvs=np.array([tevol[1]])
        Rics=np.array([tevol[2]])

    Mdips=scaledDipoleMoment(R*REARTH,
                             M*MEARTH,
                             P*DAY,
                             Qconvs,
                             Rc*R*REARTH,
                             rhoc,
                             Rics*R*REARTH,
                             sigma,kappa)
    return max(Mdips)

def getTimeMaximumDipoleMoment(tevol,
                           R=1,M=1,
                           Rc=0.5,rhoc=1E4,P=1,
                           sigma=sigma_E,kappa=kappa_E):
    try:
        ts=tevol[1:,0]
        Qconvs=tevol[1:,1]
        Rics=tevol[1:,2]
    except:
        if tevol[1]<0:return 0
        Qconvs=np.array([tevol[1]])
        Rics=np.array([tevol[2]])

    Mdips=scaledDipoleMoment(R*REARTH,
                             M*MEARTH,
                             P*DAY,
                             Qconvs,
                             Rc*R*REARTH,
                             rhoc,
                             Rics*R*REARTH,
                             sigma,kappa)
    return ts[Mdips.argmax()]

def getTemporalMaximumDipoleMoment(tevol,
                                   t=0,
                                   R=1,M=1,
                                   Rc=0.5,rhoc=1E4,P=1,
                                   sigma=sigma_E,kappa=kappa_E):
    try:
        cond=tevol[:,0]<=t*GIGA
        Qconvs=tevol[cond,1]
        Rics=tevol[cond,2]
    except:
        if tevol[1]<0:return 0
        Qconvs=np.array([tevol[1]])
        Rics=np.array([tevol[2]])

    Mdips=scaledDipoleMoment(R*REARTH,
                             M*MEARTH,
                             P*DAY,
                             Qconvs,
                             Rc*R*REARTH,
                             rhoc,
                             Rics*R*REARTH,
                             sigma,kappa)
    return max(Mdips)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#THERMAL EVOLVING PROPERTIES
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def interpFunc(tevol,col):
    try:
        ts=tevol[:,0]/GIGA
        ps=tevol[:,col]
        func=interp1d(ts,ps,kind='slinear')
    except:
        func=lambda t:tevol[col]
    return func

def getSurfaceHeat(tevol,t=0.0):
    Qfunc=interpFunc(tevol,5)
    try:Q=Qfunc(t)
    except:Q=0
    return Q

def getInnerCoreRadius(tevol,t=0.0):
    Ric=interpFunc(tevol,2)
    try:R=Ric(t)
    except:R=0
    return R

def getConvectiveHeat(tevol,t=0.0):
    Qconv=interpFunc(tevol,1)
    try:Qc=Qconv(t)
    except:Qc=0
    return Qc

def planetProperty(cell,prop,data='struct',verbose=False,**args):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #NO INTERPOLATION
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if cell.nsig==1:
        #VALUE
        R=eval("get%s(cell.%s[0],**args)"%(prop,data))
        return R

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #INTERPOLATION WITH 3 POINTS
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if cell.nsig<4:
        R=0
        dcmf=cell.model.CMF-cell.cmfs[0]
        dimf=cell.model.IMF-cell.imfs[0]
        cmfr=cell.model.CMF+dimf
        imfr=cell.model.IMF+dcmf
        
        #INFERIOR MASS
        R1=eval("get%s(cell.%s[0],**args)"%(prop,data))
        if verbose:print "R1=",R1
        R2=eval("get%s(cell.%s[4],**args)"%(prop,data))
        if verbose:print "R2=",R2
        RC=(R2-R1)/(cell.cmfs[1]-cell.cmfs[0])*(cmfr-cell.cmfs[0])+R1
        if verbose:print "RC=",RC
        R2=eval("get%s(cell.%s[2],**args)"%(prop,data))
        if verbose:print "R2=",R2
        RI=(R2-R1)/(cell.imfs[1]-cell.imfs[0])*(imfr-cell.imfs[0])+R1
        if verbose:print "RI=",RI

        dRIC=RI-RC
        if verbose:print "dRIC = ",dRIC

        dIC=np.sqrt((cmfr-cell.cmfs[0])**2+(imfr-cell.imfs[0])**2)
        dmIC=np.sqrt((cell.model.CMF-cell.cmfs[0])**2+(imfr-cell.model.IMF)**2)
        DIC=dIC-dmIC

        if verbose:print "dIC,dmIC,DIC=",dIC,dmIC,DIC

        dRf=DIC*(dRIC/dIC)
        Rml=RC+dRf
        if verbose:print "dRf,Rml=",dRf,Rml

        if cell.mps[0]==cell.mps[1]:return Rml

        #SUPERIOR MASS
        R1=eval("get%s(cell.%s[1],**args)"%(prop,data))
        if verbose:print "R1=",R1
        R2=eval("get%s(cell.%s[5],**args)"%(prop,data))
        if verbose:print "R2=",R2
        RC=(R2-R1)/(cell.cmfs[1]-cell.cmfs[0])*(cmfr-cell.cmfs[0])+R1
        if verbose:print "RC=",RC
        R2=eval("get%s(cell.%s[3],**args)"%(prop,data))
        if verbose:print "R2=",R2
        RI=(R2-R1)/(cell.imfs[1]-cell.imfs[0])*(imfr-cell.imfs[0])+R1
        if verbose:print "RI=",RI

        dRIC=RI-RC
        if verbose:print "dRIC = ",dRIC

        dIC=np.sqrt((cmfr-cell.cmfs[0])**2+(imfr-cell.imfs[0])**2)
        dmIC=np.sqrt((cell.model.CMF-cell.cmfs[0])**2+(imfr-cell.model.IMF)**2)
        DIC=dIC-dmIC

        if verbose:print "dIC,dmIC,DIC=",dIC,dmIC,DIC

        dRf=DIC*(dRIC/dIC)
        Rmu=RC+dRf
        if verbose:print "dRf,Rmu=",dRf,Rmu

        R=(Rmu-Rml)/(cell.mps[1]-cell.mps[0])*(cell.model.Mp-cell.mps[0])+Rml

        if verbose:print "Final R:",R
        
        return R

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #INTERPOLATION WITH 4 POINTS
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    Rs=[]
    ir=0

    #GET CORNER RADIUS
    for i in xrange(0,8,2):
        try:
            R1=eval("get%s(cell.%s[i],**args)"%(prop,data))
        except NameError:
            print "Property '%s' not recognized."%prop
            exit(1)
        R2=eval("get%s(cell.%s[i+1],**args)"%(prop,data))
        if cell.mps[i+1]==cell.mps[i]:
            Rs+=[R2]
        else:
            Rs+=[(R2-R1)/(cell.mps[i+1]-cell.mps[i])*(cell.model.Mp-cell.mps[i])+R1]
        if verbose:print "Property:",R1,R2,Rs[ir]
        ir+=1

    #INTERPOLATE BETWEEN IMF
    if cell.imfs[1]==cell.imfs[0]:
        Rlcmf=Rs[0]
        Rucmf=Rs[2]
    else:
        Rlcmf=(Rs[1]-Rs[0])/(cell.imfs[1]-cell.imfs[0])*(cell.model.IMF-cell.imfs[0])+Rs[0]
        Rucmf=(Rs[3]-Rs[2])/(cell.imfs[1]-cell.imfs[0])*(cell.model.IMF-cell.imfs[0])+Rs[2]

    #INTERPOLATE BETWEEN CMF
    if cell.cmfs[1]==cell.cmfs[0]:
        R=Rlcmf
    else:
        R=(Rucmf-Rlcmf)/(cell.cmfs[1]-cell.cmfs[0])*(cell.model.CMF-cell.cmfs[0])+Rlcmf

    return R

PG_Property=planetProperty

def PlanetSolidProperties(cmf,mmf,Mp=1.0,properties=['Radius'],data='struct',verbose=False,test=False):
    imf=1-(cmf+mmf)
    if verbose:print "Retrieving information for: (IMF = %.2f, CMF = %.2f, MMF = %.2f)"%(imf,cmf,mmf)
    Ps=np.ones(np.size(properties))
    if imf<0 or cmf<0.1 or mmf<0.1:
        sig=[]
        Ps*=0
    else:
        if test:
            if verbose:print "Mp=%.2f, CMF=%.2f, MMF=%.2f, IMF=%.2f"%(Mp,cmf,mmf,imf)
            planetcell=loadPlanetCell(Mp=Mp,CMF=cmf,IMF=imf)
            Rp=planetProperty(planetcell,'Radius',data='struct')
            if verbose:print "Cell signature:",planetcell.sig
        try:
            planetcell=loadPlanetCell(Mp=Mp,CMF=cmf,IMF=imf,verbose=False)
            sig=planetcell.sig
            Ps=[planetProperty(planetcell,property,data=data) for property in properties]
        except:
            sig=[]
            Ps*=0
    return sig,Ps

"""
Examples of use of previous routines:

Rp=PG_Property(cell,'Radius',verbose=True)
print Rp
del(cell)
"""

###################################################
#GIANT PLANETS SIMPLIFIED INTERIOR STRUCTURE
###################################################
def funcRho(x):
    f=(1/np.pi*np.sin(np.pi*x)-x*np.cos(np.pi*x))/x**3
    return f

def giantStructure(Mp,Rp):
    """
    See Griessmeier PhD Thesis
    """
    #CORE RADIUS SCALING
    Rc=RCJUP*Mp**0.75*Rp**-0.96/(Rp*RJUP) # Rp
    if Rc>1:Rc=1.0
    
    #INNER CORE
    Ric=Rc/2

    #CORE DENSITY
    rhom=(Mp*MJUP)/(4*np.pi/3*(Rp*RJUP)**3)
    rhoc=rhom*funcRho(Rc)
    
    #THERMAL AND ELECTRICAL CONDUCTIVITY
    if Rp<0.6:
        #ICE GIANT
        sigma=0.03*6E5
        kappa=1E-6
    else:
        #GAS GIANT
        sigma=0.1*6E5
        kappa=1E-6
    
    return Rc,Ric,rhom,rhoc,sigma,kappa

###################################################
#SCALING DIPOLE MOMENTS
###################################################
def DipoleMoment(B,R):
    """
    Dipolar magnetic moment

    Parameters:
    B: magnetic field strength (T)
    R: Radius (m)

    Return:
    M: A m^2
    """
    M=4*np.pi*R**3*B/(np.sqrt(2)*MU0)
    return M

def softStepFunction(x,f,g,a,b):
    """
    Soft-step function given by:

    f + (g-f) / { exp[(x-b)/a] + 1 }

    Maximum value: g
    Minimum value: f

    Return:
    s: Value of the step
    ds: Delta x
    """
    s=f+(g-f)/(np.exp((x-b)/a)+1)
    dx=b+5*a
    return s,dx

def funcScalecmul(Rolm):
    """
    Christensen 2010
    """
    f=0.6;g=1.0; #Limit values
    a=0.005;b=0.1; #Soft factors
    cmuldip,dc=softStepFunction(Rolm,f,g,a,b)
    return cmuldip

def funcScalebdip(fdip,abf=2.5,bbf=1.1):
    #bdip = abf*fdip **(-bbf)
    bdip=abf*fdip**(-bbf)
    return bdip

def funcScalefdip(Rolm,f=fdip_f_E,g=fdip_g_E,a=fdip_a_E,b=fdip_b_E):
    """
    Fraction of core rms field represented by CMB dipolar component

    Bdip = Brms / bdip_min

    Average envelope: f=0.35,g=1.0,a=0.009,b=0.09

    """
    #fdip is fitted by a soft-step function:
    #fdip(Roml) = f + (g-f) / { exp[(Rolm-b)/a] + 1 }
    fdip,df=softStepFunction(Rolm,f,g,a,b)
    bdip=funcScalebdip(fdip)
    return fdip,bdip

def scaledDipoleMoment(Rp,Mp,P,Qconv,Rc,rhoc,Ric,
                       sigma,kappa,
                       verbose=False,indent="\t"):

    #BASIC CHECKS
    try:
        if Qconv<0:return 0
    except ValueError:
        cond=Qconv<0
        Qconv[cond]=0

    #DERIVED CORE PROPERTIES
    Chi=Ric/Rc
    D=Rc*(1-Chi)
    V=Rc**3*(1-Chi**3)

    #CORE PROPERTIES
    if verbose:
        print indent,"Core properties:"
        print indent+"\tRp = %e RJ"%(Rp/RJUP)
        print indent+"\tMp = %e MJ"%(Mp/MJUP)
        print indent+"\tRic = %e m"%Ric
        print indent+"\tRc = %e Rp"%(Rc/Rp)
        print indent+"\tChi = %e"%Chi
        print indent+"\tQconv = %e W"%Qconv
        print indent+"\trhoc = %e kg/m^3"%rhoc
        print indent+"\tD = %e"%D
        print indent+"\tV = %e"%V

    #SCALING RELATIONSHIPS
    Rolm=Rosl_E*CROLM*\
          (Qconv/QconvE)**(1./2)*(P/DAY)**(7./6)/\
          ((rhoc/rhoc_E)**(1./6)*(Rc/Rc_E)**(11./6)*
           (1-Chi)**(1./3)*(1-Chi**3)**(1./2)*\
           ((sigma/sigma_E)/(kappa/kappa_E))**(1./5))

    Brms=0.24*np.sqrt(MU0)*rhoc**(1./6)*\
        (D/V)**(1./3)*Qconv**(1./3)

    cmul=funcScalecmul(Rolm)
    fdip,bdip=funcScalefdip(Rolm)
    Bcdip=Brms/bdip
    Bs=Bcdip*(Rc/Rp)**3.0
    Ms=DipoleMoment(Bs,Rp)

    #MAGNETIC FIELD PROPERTIES
    if verbose:
        print indent+"Magnetic field properties:"
        print indent+"\tRolm = %e"%Rolm
        print indent+"\tBrms = %e"%Brms
        print indent+"\tCmul = %e"%cmul
        print indent+"\tfdip = %e"%fdip
        print indent+"\tbdip = %e"%bdip
        print indent+"\tBs = %e"%Bs
        print indent+"\tMs = %e"%(Ms/MDIPE)

    return Ms

def planetaryDipoleMoment(planet):
    Mdip=scaledDipoleMoment(planet.R*REARTH,
                            planet.M*MEARTH,
                            planet.Prot*DAY,
                            planet.Qconv,
                            planet.Rc*planet.R*REARTH,
                            planet.rhoc,
                            planet.Ric*planet.R*REARTH,
                            planet.sigma,planet.kappa)
    return Mdip
                            
