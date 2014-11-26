"""
;-----------------------------------------------------------------------------
    PRO BOREAS,Mstar,Rstar,Lstar,Protday,FeH, $
               Rossby,fstar,Mdot,Mdot_hot,Mdot_cold,MATR
;-----------------------------------------------------------------------------
;
; boreas.pro:  Stand-alone IDL procedure to compute the mass loss rate of
;  a cool, late-type star using the models of Cranmer & Saar (2011).
;
; Inputs (all scalars):
;
; Mstar:  mass of star (in units of solar mass)
; Rstar:  radius of star (in units of solar mass)
; Lstar:  bolometric luminosity of star (in units of solar mass)
; Protday:  rotation period of star (in days)
; FeH:  metallicity (log of iron/hydrogen abundance ratio, in solar units)
;
; Outputs: (all scalars):
;
; Rossby:  dimensionless Rossby number for this star
; fstar:  dimensionless filling factor of open flux tubes at photosphere
; Mdot:  mass loss rate (in units of solar masses per year)
; Mdot_hot:  mass loss rate from just hot coronal (gas pressure) model
; Mdot_cold:  mass loss rate from just cold (wave pressure) model
; MATR:  hot wind's Alfvenic Mach number at the transition region
;
;-----------------------------------------------------------------------------
# Adapted and Optimized for Python by Jorge I. Zuluaga (University of Antioquia)
# Optimized code is ~10% faster than the transliterated version.
"""
from numpy import *
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt

#################################################################################
#PHOTOSPHERIC MASS DENSITY INTERPOLANT
#################################################################################
NTEFFS=19
C0fit = interp1d(linspace(2500.0,7000.0,NTEFFS),
                 [-9.0329342,-8.8057005,-8.6187019,-8.5343736,-8.5792239,
                   -8.6915425,-8.8033701,-8.8791533,-8.9288180,-8.9604793,
                   -8.9954977,-9.0593624,-9.1566287,-9.2743908,-9.4120161,
                   -9.5781877,-9.7290674,-9.8972636,-10.1])
C1fit = interp1d(linspace(2500.0,7000.0,NTEFFS),
                 [0.78081830,0.68284416,0.60471646,0.56629124,0.57113263,
                  0.59584083,0.61352883,0.61218030,0.59646729,0.57949132,
                  0.56963417,0.57219919,0.58595944,0.60671743,0.63103575,
                  0.65574884,0.67753323,0.69808401,0.72])

def rhoPhoto(Teff,logg):
    global C0fit,C1fit
    C0now = C0fit(Teff)
    C1now = C1fit(Teff)
    rhophoto = 10.**(C0now + C1now*logg)
    return rhophoto
                 
def pyBoreas(Mstar,Rstar,Lstar,Protday,FeH):
    """
    Returns
    Rossby,fstar,Mdot,Mdot_hot,Mdot_cold,MATR
    """
    global C0fit,C1fit

    #################################################################################
    #KEY PARAMETERS
    #################################################################################
    alphaturb  = 0.5
    heightfac  = 0.5
    theta      = 0.333
    ffloor     = 1.0e-4
    ellperpSUN = 3.0e7
    niter      = 50

    #################################################################################
    #CONSTANTS
    #################################################################################
    Gconst  = 6.6732e-08
    xMsun   = 1.989e+33
    xRsun   = 6.96e+10
    xLsun   = 3.826e+33
    boltzK  = 1.380622e-16
    xmHyd   = 1.67333e-24
    stefan  = 5.66961e-5
    xMdotyr = 6.30276e+25
    TeffSUN    = 5770.2
    ProtdaySUN = 25.3
    gravSUN    = Gconst*xMsun/xRsun/xRsun
    
    #################################################################################
    #BASIC STELLAR PARAMETERS IN CGS
    #################################################################################
    xMcgs  = Mstar * xMsun
    xRcgs  = Rstar * xRsun
    xLcgs  = Lstar * xLsun
    Teff   = (xLcgs/4./pi/xRcgs/xRcgs/stefan)**0.25
    grav   = Gconst*xMcgs/xRcgs/xRcgs
    logg   = log10(grav)
    ZoZsun = 10.**(FeH)
    Vesc2  = 2.*Gconst*xMcgs/xRcgs
    Vesc   = (Vesc2)**0.5

    #################################################################################
    #INPUT VALIDATION
    #################################################################################
    icrazy = 0
    if ((Teff < 1500.) or (Teff > 12000.)):icrazy = 1
    if ((logg < -4.0) or (logg > 7.0)):icrazy = 1
    if ((Lstar < 1.e-4) or (Lstar > 1.e6)):icrazy = 1
    if ((Mstar < 0.001) or (Mstar > 100.)):icrazy = 1
    if ((FeH < -5.0) or (FeH > 2.0)):icrazy = 1

    if (icrazy != 0):
        print ' '
        print ' Input parameters seem to be out of bounds! '
        print ' '
        return

    #################################################################################
    #ESTIMATE ROSSBY NUMBER AND OPEN-FLUX FILLING FACTOR
    #################################################################################
    tauc    = 314.241*exp(-Teff/1952.5)*exp(-(Teff/6250.)**18.)+0.002
    taucSUN = 314.241*exp(-TeffSUN/1952.5)*exp(-(TeffSUN/6250.)**18.)+0.002

    gratio = gravSUN/grav
    if (gratio > 1.):tauc = tauc * (gratio**0.18)

    Rossby    = Protday / tauc
    RossbySUN = ProtdaySUN / taucSUN
    Ronorm    = Rossby/RossbySUN
    fstar     = 0.5 / (1. + (Ronorm/0.16)**2.6)**1.3

    if (fstar < ffloor):fstar = ffloor

    #################################################################################
    #COMPUTE PHOTOSPHERIC MASS DENSITY
    #################################################################################
    #print Teff,logg
    C0now = C0fit(Teff)
    C1now = C1fit(Teff)
    rhophoto = 10.**(C0now + C1now*logg)

    #################################################################################
    #PHOTOSPHERIC EQUATION OF STATE (FIT TO OPAL MODELS)
    #################################################################################
    xmuavg = 1.75 + 0.5*tanh((3500.-Teff)/600.)
    gadia  = 5./3.

    #################################################################################
    #MAGNETIC FIELD, AND SCALE HEIGHT
    #################################################################################
    Pphoto = rhophoto*boltzK*Teff/(xmuavg*xmHyd)
    Bequi  = (8.*pi*Pphoto)**0.5
    Bphoto = 1.13*Bequi

    cs2    = gadia*boltzK*Teff/(xmuavg*xmHyd)
    Hphoto = cs2 / (gadia*grav)

    xmuavgSUN = 1.75 + 0.5*tanh((3500.-TeffSUN)/600.)
    cs2SUN    = gadia*boltzK*TeffSUN/(xmuavgSUN*xmHyd)
    HphotoSUN = cs2SUN / (gadia*gravSUN)

    #################################################################################
    #SURFACE FLUX OF ALFVEN WAVES
    #################################################################################
    """
    Estimate surface flux of Alfven waves using a parameterized fit to the
    Musielak et al. (2002a) kink-mode flux models
    """
    alpha_MU02 = 6.774 + 0.5057*logg
    T0_MU02    = 5624. + 600.2*logg
    F0_MU02    = exp(22.468 - 0.0871*logg)

    FluxAphoto = F0_MU02 * ((Teff/T0_MU02)**alpha_MU02) \
        * exp(-(Teff/T0_MU02)**25.)
    if (FluxAphoto < 1.e-10):FluxAphoto = 1.e-10
    
    #################################################################################
    #SET UP MHD TURBULENCE PARAMETERS AT THE PHOTOSPHERE
    #################################################################################
    Valfphoto    = Bphoto / (4.*pi*rhophoto)**0.5
    vperpPHOT    = (FluxAphoto/rhophoto/Valfphoto)**0.5
    ellperpphoto = ellperpSUN * (Hphoto/HphotoSUN)
    
    Qphoto       = alphaturb*rhophoto*(vperpPHOT**3)/ellperpphoto
    
    #################################################################################
    #EXTRAPOLATE MHD TURBULENCE PARAMETERS UP TO THE TRANSITION REGION (TR)
    #################################################################################
    fTR  = fstar**theta
    BTR  = Bphoto * (fstar/fTR)
    uinf = Vesc
    
    TTR       = 2.0e5
    Lammax    = 7.4e-23 + 4.2e-22*(ZoZsun**1.13)
    LammaxSUN = 7.4e-23 + 4.2e-22
    
    #################################################################################
    #SELF-CONSISTENT SOLUTION FOR DENSITY AND HEATING RATE
    #################################################################################
    """
    Iterate to find self-consistent solution for density and heating rate
    at the TR, assuming that the non-WKB reflection at the TR is imperfect.
    The reflection coefficient is given by an approximate version of the
    low-frequency Cranmer (2010) limit.
    """
    ReflCoef = 0.5
    for iter in range(1,niter+1):
        quench  = ReflCoef*(1.+ReflCoef)/(1.+ReflCoef**2)**1.5 * (2.)**0.5
        sqbrac  = quench*Qphoto*xmHyd*xmHyd/(rhophoto**0.25)/Lammax
        rhoTR   = (sqbrac**(4./7.)) * (fstar**(2.*(1.-theta)/7.))
        QTR     = Qphoto*quench*((rhoTR/rhophoto)**0.25)*(BTR/Bphoto)**0.5
        ValfTR  = BTR / (4.*pi*rhoTR)**0.5
        PTR     = 2.0*rhoTR*boltzK*TTR/xmHyd
        ReflCoefnew = abs((ValfTR-uinf)/(ValfTR+uinf))
        ReflCoef    = (ReflCoefnew*ReflCoef)**0.5

    #################################################################################
    #CAP HEATING FLUX 
    #################################################################################
    """
    Does the heating-related energy flux at the TR exceed the flux in
    "passive propagation" of the Alfven waves?  If so, cap it!
    """
    FluxTR0  = heightfac*QTR*xRcgs
    FluxA_TR = FluxAphoto * fstar/fTR
    if (FluxTR0 > FluxA_TR):FluxTR0 = FluxA_TR

    #################################################################################
    #MASS-LOSS RATE FOR HOT CORONAL WIND
    #################################################################################
    """
    Estimate the mass loss rate for a hot coronal wind, using the
    Hansteen et al. (1995) energy balance approximation.
    """
    velfacTR = 1.4e6 * (Lammax/LammaxSUN)**0.5
    FcondTR  = PTR * velfacTR
    fraccond = FcondTR / FluxTR0
    fccmax   = 0.9
    if (fraccond > fccmax):fraccond = fccmax
    FluxTR   = FluxTR0 * (1.-fraccond)

    AreaTR      = fTR * (4.*pi*xRcgs*xRcgs)
    Mdotcgs_hot = AreaTR*FluxTR/ ((Vesc2+uinf*uinf)/2.)
    Mdot_hot    = Mdotcgs_hot / xMdotyr

    uTR_hot = Mdotcgs_hot / (rhoTR*AreaTR)
    MATR    = uTR_hot / ValfTR

    #################################################################################
    #WIND PARAMETERS FIRST ESTIMATION
    #################################################################################
    """
    for the Holzer et al. (1983) cold wave-driven wind, first estimate the
    radius, speed, and magnetic field at the wave-modified critical point.
    """
    enn   = 2.0       #; B \propto r^{-enn} at crit point
    beta  = 0.5*enn
    eee36 = (3./7./beta + 4./7.) / (1. + (vperpPHOT/Vesc)**2)

    rcrit = 1.75*eee36 * xRcgs
    ucrit = (Gconst*xMcgs/enn/rcrit)**0.5

    Bcrit = Bphoto * ((xRcgs/rcrit)**2) * fstar

    #################################################################################
    #DENSITY AND WAVE AMPLITUDE
    #################################################################################
    """
    At the critical point, iterate on the definition of u_crit and the
    condition of wave action conservation to get density and wave amplitude.
    """
    Areaphoto    = fstar * (4.*pi*xRcgs*xRcgs)
    Areacrit     = 4.*pi*rcrit*rcrit
    action_photo = rhophoto*(vperpPHOT**2)*Valfphoto*Areaphoto

    vperpcrit = 2.*ucrit
    rhocrit   = 4.*pi*(action_photo/((vperpcrit**2)*Bcrit*Areacrit))**2

    for iter in range(1,niter+1):
        Valfcrit  = Bcrit / (4.*pi*rhocrit)**0.5
        MAcrit    = ucrit / Valfcrit
        macfac    = (1. + 3.*MAcrit)/(1. + MAcrit)
        vperpcrit = 2.*ucrit / (macfac)**0.5
        rhocrit   = action_photo / \
            ((vperpcrit**2)*Valfcrit*Areacrit*(1.+MAcrit)**2)

    Mdotcgs_cold = rhocrit*ucrit*Areacrit
    Mdot_cold    = Mdotcgs_cold / xMdotyr

    #################################################################################
    #ESTIMATE THE ACTUAL MASS LOSS FROM BOTH HOT AND COLD PROCESSES.
    #################################################################################
    Mdot = Mdot_cold + (Mdot_hot*exp(-4.*MATR**2))

    return tauc,fstar,Bequi,Bphoto,BTR,Rossby,Mdot,Mdot_hot,Mdot_cold,MATR

if __name__=="__main__":
    Rossby,fstar,Mdot,Mdot_hot,Mdot_cold,MATR=pyBoreas(1.0,1.0,1.0,25.4,0.0)
    print Rossby,fstar,Mdot,Mdot_hot,Mdot_cold,MATR
    
    Teffs=linspace(2500,6000,60)
    Teffs2=linspace(6000,7000,10)

    fig=plt.figure()
    plt.plot(Teffs,C0fit(Teffs),'b+-')
    plt.plot(Teffs2,C0fit(Teffs2),'r+-')
    plt.xlim((2500,8000))
    plt.ylim((-11.0,-8.4))
    plt.grid()
    fig.savefig("tests/C0fit.png")

    fig=plt.figure()
    plt.plot(Teffs,C1fit(Teffs),'b+-')
    plt.plot(Teffs2,C1fit(Teffs2),'r+-')
    plt.xlim((2500,8000))
    plt.grid()
    fig.savefig("tests/C1fit.png")

    fig=plt.figure()
    logg=4.35
    plt.plot(Teffs,rhoPhoto(Teffs,logg),'b+-')
    plt.plot(Teffs2,rhoPhoto(Teffs2,logg),'r+-')
    plt.xlim((2500,8000))
    plt.yscale("log")
    plt.grid()
    fig.savefig("tests/C-rhophoto.png")

