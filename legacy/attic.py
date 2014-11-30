loadIceGasGiantsGrid(DATA_DIR+"IceGasGiants/",verbose=True)
radiusFunction=lambda M,t:Giants['0'].Radius(M,t)
ts,lumflux_func=interpMatrix(env.lumflux)

Mgs=np.logspace(np.log10(0.05),np.log10(1.0),10)
Mgs=[1.0]
for Mg in Mgs:
    M=Mg*MJUP
    R=radiusFunction(Mg,env.tauini)*RJUP
    R=1.0*RJUP
    Ms=[M]
    i=1
    for t in ts[1:]:
        dt=(t-ts[i-1])*GYR
        FXUVp=lumflux_func[11](t)*PELSI
        rho=M/(4.0*PI/3*R**3)
        Mpdot=-3*FXUVp/(4*GCONST*rho)
        M+=Mpdot*dt
        if M<0:break
        Ms+=[M]
        i+=1
    print Ms.shape
    exit(0)
