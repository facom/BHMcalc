   <ZSVEC> (string): Vector of metallicities in theoretical isochrones
   grid.  Available values: ZSVEC_full (fine grid), ZSVEC_coarse
   (coarse grid), ZSVEC_siblings (near solar metallicities).

logrho_func,Teff_func,logR_func,logL_func=\
    evoFunctions(evodata)

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ts=np.linspace(0.7,TAGE,100)
vs=[];ns=[]
Ms=1.4
for t in ts:
    v,n=vnGreissmeier(1.0,t,Ms,Ms**0.25)
    vs+=[v];ns+=[n]
ns=array(ns)
vs=array(vs)
Ps=ns*vs**2/(NSUN*VSUN**2)
ax.plot(ts,Ps)
ax.set_yscale("log")
ax.grid(which='both')
fig.savefig("tmp/vn.png")

Ms=1.5
Rs=Ms**0.25
print Prot(TAGE,Ms=Ms,Rs=Rs)/DAY

exit(0)

    t=max(TAU_MIN,star.taumax/50)
    star.acc=tidalAcceleration(star.M,star.Rfunc(t),
                               star.Lfunc(t),star.MoI,
                               stars[NEXT(i,2)].M,
                               binary.abin,binary.ebin,
                               binary.nbin/DAY,star.W/DAY,
                               verbose=False)
    star.tsync=-(star.W/DAY)/star.acc/GYR
    
    #INTERRUPT IF TWINS
    if qnotwins:break
    i+=1

print star.tsync
