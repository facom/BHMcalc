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
# Numerical routines
###################################################
from BHM import *

###################################################
#PACKAGES
###################################################
from scipy.interpolate import interp1d #as interpol
from scipy.integrate import quad as integrate,odeint
from scipy.misc import derivative
from scipy.linalg import norm
from scipy.optimize import newton,brentq 
try:
    from scipy.optimize import minimize
except:
    from scipy.optimize import fmin
    def minimize(f,xo,**args):
        s=dict()
        s['x']=fmin(f,xo,disp=False)
        return dict2obj(s)

###################################################
#ROUTINES
###################################################
"""
def interp1d(Xs,Ys,kind='slinear'):
    f=interpol(Xs,Ys,kind=kind,bounds_error=False,fill_value=0.0)
    return f
"""

def scaleProp(m,alpha,beta):
    """
    Scaling function
    """
    return alpha*m**beta

def interpArray(t,r,kind='slinear'):
    x=interp1d(t,r[:,0],kind=kind)
    y=interp1d(t,r[:,1],kind=kind)
    rfunc=lambda t:array([x(t),y(t)])
    return rfunc

def statsArray(array):
    mean=array.mean()
    minn=array.min()
    maxx=array.max()
    rang=maxx-minn
    stdv=array.std()
    return mean,minn,maxx,rang,stdv

def disconSignal(t,s,tausys=12,iper=3,dimax=20):
    ds=np.log10(s[1::])-np.log10(s[:-1:])
    ds=np.append([0],ds)
    imax=-1
    epsmax=0
    dsold=ds[-1]
    for i in np.arange(10,len(ds))[::-iper]:
        eps=2*abs(ds[i]-dsold)/(ds[i]+dsold)
        if eps>epsmax:
            imax=i
            epsmax=eps
        #print t[i],eps,epsmax
        dsold=ds[i]
        if abs(imax-i)>dimax and epsmax>0:
            #print "Break 1"
            break
        if t[i]<tausys/2:
            imax=-1
            #print "Break 2"
            break
    scont=s[imax]
    return t[imax]

def interpMatrix(data):
    x=data[:,0]
    ncols=data.shape[1]
    yfunc=[None]
    for j in xrange(1,ncols):
        y=data[:,j]
        yfunc+=[interp1d(x,y,kind='slinear')]
    return x,yfunc

def chopArray(array,xini,xend):
    cond1=array>xini
    cond2=array<xend
    narray=np.concatenate(([xini],array[cond1*cond2],[xend]))
    return narray

def minmeanmaxArrays(arrays):
    mins=[];maxs=[];means=[]
    for array in arrays:
        mins+=[min(array)]
        means+=[np.mean(array)]
        maxs+=[max(array)]
    return min(mins),np.mean(means),max(maxs)

XQUAD5=np.array([0,
                 1./3*(5-2*(10./7)**0.5)**0.5,
                 1./3*(5+2*(10./7)**0.5)**0.5,
                 ])

WQUAD5=np.array([128./225,
                 +(322+13*70**0.5)/900.,
                 +(322+13*70**0.5)/900.,
                 (322-13*70**0.5)/900.,
                 +(322-13*70**0.5)/900.
                 ])

def integrateArray(xs,ys,a,b):
    """
    Gaussian Quadrature with 5 points
    """
    xi=[]
    xi+=[(b-a)/2*XQUAD5[0]+(a+b)/2]
    xi+=[(b-a)/2*XQUAD5[1]+(a+b)/2]
    xi+=[-(b-a)/2*XQUAD5[1]+(a+b)/2]
    xi+=[(b-a)/2*XQUAD5[2]+(a+b)/2]
    xi+=[-(b-a)/2*XQUAD5[2]+(a+b)/2]
    yi=np.array(np.interp(xi,xs,ys))
    integral=(WQUAD5*yi).sum()*(b-a)/2
    return integral

def rectangleArray(xs,ys,i):
    """
    Rectangle Rule Integrating from xs[0] to xs[i]
    """
    integral=(ys[1:i+1]*(xs[1:i+1]-xs[:i])).sum()
    return integral

def trapezoidalArray(xs,ys,i):
    """
    Simpson Rule Integrating from xs[0] to xs[i]
    """
    integral=((ys[1:i+1]+ys[:i])*(xs[1:i+1]-xs[:i])/2).sum()
    return integral

def signalInverseFourier(t,ft,N,T,maxk=8):
    serie=ft[0]
    for k in xrange(1,maxk):
        w=2*PI*k/T
        serie+=2*ft[k]*np.exp(1j*w*t)
    serie=serie/N
    return serie

def softArrayFourier(ts,s,maxk=8):
    N=len(ts)
    ft=np.fft.fft(s,N)
    T=ts[-1]
    ss=[signalInverseFourier(t,ft,N,T,maxk=maxk) for t in ts]
    return ss

def softArraySG(y,frac=5,nP=7,deriv=0, rate=1):
    r"""

    Source:
    http://wiki.scipy.org/Cookbook/SavitzkyGolay

    See also:
    http://en.wikipedia.org/wiki/Savitzky%E2%80%93Golay_filter

    Comment on derivative scale (Jorge Zuluaga):

    Since values for t (independent variable) is not provided the
    scale of the derivatives should be adjusted accordingly.  For that
    purpose the only thing you need to do is multiply derivatives by
    the length of the vector and divide by the independent variable range.

    Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    leny=len(y)
    window_size=int((1.0*leny)/frac)
    if window_size%2==0:window_size-=1
    order=nP

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
    
def bracketValue(value,vector):
    dv=value-vector
    iv=np.abs(dv).argsort()
    
    if value<vector[0]:return (vector[0],)*3+((value-vector[0])/value,)
    if value>vector[-1]:return (vector[-1],)*3+((value-vector[-1])/value,)

    vcl=vector[iv[0]]
    v1=vector[iv[1]]
    s1=dv[iv[1]]
    v2=vector[-1]
    for i in xrange(2,len(vector)):
        if dv[iv[i]]*s1<0:
            v2=vector[iv[i]]
            break
    vlw=min(v1,v2)
    vup=max(v1,v2)
    
    match=(value-vcl)/value
    return vlw,vcl,vup,match

