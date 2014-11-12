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


            ft=(tn-ti)
            h=max(h,hmin)
            if ft<h:
                qlast=True
                h=ft
            else:
                qlast=False
            if verbose:
                print "="*30
                print "Step ti = %.17e"%ti
                print "Away from tn = %.17e"%ft
                print "Advancing h = %.17e"%h
                print "Function value: W = %.17e"%star.W
                print "="*30
            deltaW=1
            nimp=0
            while deltaW>Wtol and nimp<=maximp and (h>=hmin or qlast):
                i=0
                if verbose:
                    print "Initial timestep: %.17e"%h
                    print "Initial Function: %.17e"%star.W
                
                #EULER ZERO ORDER
                acc=totalAcceleration(t,star,stars[NEXT(i,2)],binary,
                                      verbose=False)
                if verbose:
                    print "Acceleration: %.17e"%acc
                    print "Time step: %.17e s"%(h*GYR)
                dW0=acc*(h*GYR)
                W0=star.W+dW0
                if verbose:
                    print "Zero order: %.17e"%W0
                if W0<0:
                    h/=2
                    continue

                #EULER FIRST HALF STEP
                dW12=acc*(h*GYR)/2
                W12=star.W+dW12
                if verbose:
                    print "First half: %.17e"%W12
                    print "Acceleration: %.17e"%acc
                
                #EULER SECOND HALF
                star.W=W12
                acc=totalAcceleration(t+h/2,star,stars[NEXT(i,2)],binary,
                                      verbose=False)
                dW1=acc*(h*GYR)/2
                W1=star.W+dW1
                if verbose:
                    print "Second half: %.17e"%W1
                    print "Acceleration: %.17e"%acc
                
                #DIFFERENCE
                deltaW=2*abs(W1-W0)/(W1+W0)
                if verbose:print "Uncertainty: %.17e"%deltaW
                
                #NEW STEP
                h=0.9*h*1E-6/deltaW
                if verbose:
                    print "New timestep: %.17e"%h
                    print "Minimum timestep: %.17e"%hmin
                    print "Condition1:",deltaW>Wtol
                    print "Condition2:",nimp<=maximp
                    print "Condition3:",(h>=hmin or qlast)
                    raw_input()

                maximp+=1

            star.W=W1+(W1-W0)
            ti+=h
            """
            See Wikipedia/Adaptive_stepsize
            """
            if verbose:
                print "Updated time step: h = %.17e"%h
                print "Function value: %.17e"%star.W
                raw_input()

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])

ax.plot(ts,star1.Ps.array/DAY,'b-')
Prots=theoProt(ts,star1.protfit)*DAY
ax.plot(ts,Prots/DAY,'b--')

ax.plot(ts,star2.Ps.array/DAY,'r-')
Prots=theoProt(ts,star2.protfit)*DAY
ax.plot(ts,Prots/DAY,'r--')

ax.axhline(binary.Pbin)
fig.savefig("tmp/prot-evol.png")

#==============================
#VERIFY ROTATIONAL FIT
#==============================
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
ax.plot(ts,prots,label='Model')
ax.plot(ts,theoProt(ts,prot_fit),label='Fit')
ax.axvline(tau_ms,color='k',linestyle='--',label='Turn over')
ax.axvline(star.tau,color='k',label='Stellar Age')
ax.set_ylabel("Period (days)")
ax.set_ylabel("$\tau$ (Gyr)")
ax.set_xlim((0,min(12,tau_max)))
ax.legend(loc='best')
fig.savefig(star_dir+"prot.png")
fig.savefig("tmp/prot.png")


star1=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")
star2=\
loadConf("%s"+"star.conf")+\
loadConf("%s"+"star.data")

#"""
ts,lumflux=interpMatrix(env.lumflux)
i=n-1
t=ts[i]
j=9
func=lumflux[j]
print "Time:",t
print "Integration:",integrate(func,env.tauini,t,epsrel=1E-3)
print "Approximation:",ints[j-9][i]

ls=env.lumflux[:,9]
ints=integrateArray(ts,ls,env.tauini,t)
print "Approximation 2:",ints
exit(0)
#"""

'#star1 input[name=star1.FeH]'
