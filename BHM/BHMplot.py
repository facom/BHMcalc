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
# BHM plot module.  
# Plotting packages and routines.
###################################################
from BHM import *

###################################################
#PACKAGES
###################################################
from matplotlib import use
use('Agg')
from matplotlib import colors,ticker,patches,pylab as plt
from matplotlib.pyplot import cm
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import offset_copy

###################################################
#ROUTINES
###################################################
def logTickLabels(ax,perini,perfin,nperper,
                  frm='%.1f',axis='y',notation='normal',fontsize=8):
    """
    Generate the tick labels of a logarithmic scale axis

    Usage:
       logTickLabels(ax,
                     initial_period,final_period,
                     (num_labels_period1,num_labels_period 2,...),
                     axis='[x|y]',
                     frm='%format',
                     notatiom='scientific|normal')
    """
    i=0
    nper=perfin-perini
    yl=[]
    yt=[]
    npref=nperper[0]
    for ip in range(0,nper):
        try:npe=nperper[ip]
        except:npe=npref
        perl=perini+ip
        perh=perini+ip+1
        yval=np.linspace(10**perl,10**perh,10)
        imax=len(yval)
        ini=0
        if ip>0:ini=1
        for i in range(ini,imax):
            if i!=0 and i!=imax-1:
                if i%npe==0:
                    inum=i+1
                    if notation is 'sci':
                        yl+=[r"%d"%inum]
                    else:
                        yl+=[frm%yval[i]]
                else:
                    yl+=[""]
            else:
                ex=np.log10(yval[i])
                if notation is 'sci':
                    yl+=[r"10$^{%d}$"%ex]
                else:
                    yl+=[frm%yval[i]]
            yt+=[yval[i]]
            
    #print yt,yl
    if axis is 'y':
        ax.set_yticks(yt)
        ax.set_yticklabels(yl,fontsize=fontsize)
    else:
        ax.set_xticks(yt)
        ax.set_xticklabels(yl,fontsize=fontsize)

def plotFigure(plotdir,plotname,plotcmd,watermarkpos="outer"):
    #COMPLETE PLOTTING COMMAND
    plotcmd="""\
from BHM import *
from BHM.BHMplot import *
from numpy import array
%s
saveFig('%s%s.png',watermarkpos="%s")
"""%(plotcmd,plotdir,plotname,watermarkpos)
    #PLOT SCRIPT
    plotscr=plotdir+"%s.py"%plotname
    #SAVE PLOT SCRIPT
    fp=open(plotscr,"w")
    fp.write(plotcmd)
    fp.close()
    #EXECUTE COMMANDS
    exec(plotcmd)

def saveFig(filename,watermark="BHMcalc",watermarkpos="outer",dxw=0.01,dyw=0.01,va='top'):
    """
    Save figure with the respective data
    """
    ax=plt.gca()

    #SAVE WATERMARK
    if watermarkpos=='inner':
        xw=1-dxw
        yw=1-dyw
        ha='right'
    if watermarkpos=='outer':
        xw=1+dxw
        yw=1+dyw
        ha='left'

    ax.text(xw,yw,watermark,
            horizontalalignment=ha,
            verticalalignment=va,
            rotation=90,color='b',alpha=0.3,fontsize=12,
            transform=ax.transAxes)

    plt.savefig(filename)
    
    #SAVE DATA
    fdata=open(filename+".txt","w")
    fdata.write("Plot: %s\n"%filename)
    i=0
    for line in ax.lines:
        i+=1
        label=line.get_label()
        fdata.write("\nLine %d: %s\n"%(i,label))
        x=line.get_data()[0]
        y=line.get_data()[1]
        ndata=len(x)
        fdata.write("\n")
        for n in xrange(ndata):
            fdata.write("\t%25.17e\t%25.17e\n"%(x[n],y[n]))
    fdata.close()

def offSet(dx,dy):
    fig=plt.gcf()
    ax=fig.gca()
    toff=offset_copy(ax.transData,fig=fig,
                     x=dx,y=dy,units='dots')
    return toff
