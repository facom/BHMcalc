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
# Catalogue loader
###################################################
from BHM import *
from BHM.BHMdata import *
from BHM.BHMstars import *
from BHM.BHMplanets import *
from BHM.BHMnum import *

###################################################
#CLI ARGUMENTS
###################################################
Usage=\
"""
Usage:
   python %s <cat_dir> [<recalculate>] [<sort_field>] [<sort_order>] 
                       [<display_level>] [<filter>] [<catalogue_id>]

   <cat_dir>: location of the catalogue

   <recalculate>: 1/0.  Recalculate derivative properties.

   <sort_field>: field to sort with.

   <sort_order>: order of sort, 1: reverse, 0: normal

   <display_level>: Level of details in catalogue

   <filter>: Filter.  Ex. binary_Pbin > 0.  Python syntax.

   <catalogue_id>: Unique ID.

"""%argv[0]

catdir,recalculate,sortfield,sortorder,displaylevel,catfilter,catid=\
    readArgs(argv,
             ["str","int","str","int","int","str","str"],
             [".","1","BHMCatS","0","1","binary_Pbin>0",""],
             Usage=Usage)

###################################################
#CATALOGUE LOCATION
###################################################
#GET THE LAST STYLE SHEET
System("cp web/BHM.css %s"%catdir)

#PICKLE FILE
fpickle="BHM/data/BHMcat/BHMcat.pickle"

if recalculate:
    ###################################################
    #LOAD CATALOGUES: SYSTEMS AND PLANETS
    ###################################################
    PRINTOUT("Loading catalogues...")
    sfields,sfieldstyp,sfieldstxt,sfieldspri,systems=\
        readCatalogue("BHM/data/BHMcat/BHMcat-Systems.csv",3)

    pfields,pfieldstyp,pfieldstxt,pfieldspri,planets=\
        readCatalogue("BHM/data/BHMcat/BHMcat-Planets.csv",3)

    cfields,cfieldstyp,cfieldstxt,cfieldsdef,smodels=\
        readCatalogue("BHM/data/BHMcat/BHMcat-ModelSystem.csv",0,pritype="default")

    cfields,cfieldstyp,cfieldstxt,cfieldsdef,pmodels=\
        readCatalogue("BHM/data/BHMcat/BHMcat-ModelPlanet.csv",0,pritype="default")

    #############################################################
    #CALCULATE DERIVARIVE MISSING PROPERTIES
    #############################################################
    PRINTOUT("Calculating missing/derivative properties of systems...")

    #////////////////////////////////////////
    #SYSTEMS
    #////////////////////////////////////////
    for system in sortCatalogue(systems,"BHMCatS"):
        #========================================
        #METAL FRACTION
        #========================================
        if notMissing(system["binary_FeHobs"]):
            #print "Calculating Zobs for %s..."%system["BHMCatS"]
            system["binary_Zobs"]=ZfromFHe(system["binary_FeHobs"])[0]
        if notMissing(system["binary_FeHfit"]):
            #print "Calculating Zobs for %s..."%system["BHMCatS"]
            system["binary_Zfit"]=ZfromFHe(system["binary_FeHfit"])[0]
    
        #========================================
        #DISTANCES
        #========================================
        if not notMissing(system["binary_d"]):
            if notMissing(system["binary_V"]):
                if notMissing(system["star1_R"]) and notMissing(system["star2_R"]) and \
                        notMissing(system["star1_T"]) and notMissing(system["star2_T"]):
                    #print "Calculating d for %s (%s %s)..."%(system["BHMCatS"],system["SourceCat"],system["SourceID"])
                    L=starLuminosity(system["star1_R"],system["star1_T"])+\
                        starLuminosity(system["star2_R"],system["star2_T"])
                    BCV=bolometricCorrection(system["star1_T"])
                    system["binary_dmod"]=starDistance(L,system["binary_V"],BCV)
                    #print system["binary_d"],system["binary_dmod"]

        #========================================
        #ROTATIONAL PERIOD
        #========================================
        if (not notMissing(system["star1_Protv"])) \
                and notMissing(system["star1_vsini"]) and notMissing(system["star1_R"]):
            if not notMissing(system["binary_ibin"]):system["binary_ibin"]=90.0
            system["star1_Protv"]=starProt(system["star1_vsini"],system["binary_ibin"],system["star1_R"])
            if notMissing(system["star1_vsinierr"]):
                system["star1_Protverr"]=system["star1_Protv"]*system["star1_vsinierr"]/system["star1_vsini"]

        if (not notMissing(system["star2_Protv"])) \
                and notMissing(system["star2_vsini"]) and notMissing(system["star2_R"]):
            if not notMissing(system["binary_ibin"]):system["binary_ibin"]=90.0
            system["star2_Protv"]=starProt(system["star2_vsini"],system["binary_ibin"],system["star2_R"])
            if notMissing(system["star2_vsinierr"]):
                system["star2_Protverr"]=system["star2_Protv"]*system["star2_vsinierr"]/system["star2_vsini"]

        #========================================
        #ADD MODEL PARAMETERS
        #========================================
        smodel=smodels[system["BHMCatS"]]

        #========================================
        #ADD PLANETS DATA FIELD
        #========================================
        splanets=system["Planets"].split(";")
        system["PlanetsModel"]=dict()
        if '-' in splanets:
            #DEFAULT PLANET
            defplanet="BHMCatP0000"
            pmodel=dict()
            pmodel.update(smodel)
            system["PlanetsData"]=[planets[defplanet]]
            pmodel.update(pmodels[defplanet])
            system["PlanetsModel"][defplanet]=pmodel
        else:
            system["PlanetsData"]=[]
            for splanet in splanets:
                if splanet=='':break
                pmodel=dict()
                pmodel.update(smodel)
                system["PlanetsData"]+=[planets[splanet]]
                pmodel.update(pmodels[splanet])
                system["PlanetsModel"][splanet]=pmodel

    #////////////////////////////////////////
    #PLANETS
    #////////////////////////////////////////
    PRINTOUT("Calculating missing/derivative properties of planets...")

    for planet in sortCatalogue(planets,"BHMCatS"):
        #========================================
        #MASS IN EARTH MASSES
        #========================================
        #print "Checking planet %s (%s)..."%(planet["BHMCatP"],planet["PlanetID"])
        if notMissing(planet["planet_M"]):
            if planet["planet_M"]<1:
                planet["planet_M"]*=MJUP/MEARTH
                planet["planet_Merr"]*=MJUP/MEARTH
                #print TAB,"Corrected mass = %e +/- %e"%(planet["planet_M"],planet["planet_Merr"])
            
        #========================================
        #RADIUS IN EARTH RADIUS
        #========================================
        if notMissing(planet["planet_R"]):
            if planet["planet_R"]<1:
                planet["planet_R"]*=RJUP/REARTH
                planet["planet_Rerr"]*=RJUP/REARTH
                #print TAB,"Corrected radius = %e +/- %e"%(planet["planet_R"],planet["planet_Rerr"])

    systems["Fields"]=sfields
    systems["FieldsType"]=sfieldstyp
    systems["FieldsText"]=sfieldstxt
    systems["FieldsPriority"]=sfieldspri
    systems["PlanetFields"]=pfields
    systems["PlanetFieldsType"]=pfieldstyp
    systems["PlanetFieldsText"]=pfieldstxt
    systems["PlanetFieldsPriority"]=pfieldspri
    fl=open(fpickle,'w')
    pickle.dump(systems,fl)
    fl.close()
else:
    fl=open(fpickle,'r')
    systems=pickle.load(fl)
    fl.close()

sfields=systems["Fields"]
sfieldstyp=systems["FieldsType"]
sfieldstext=systems["FieldsText"]
sfieldspri=systems["FieldsPriority"]
pfields=systems["PlanetFields"]
pfieldstyp=systems["PlanetFieldsType"]
pfieldstext=systems["PlanetFieldsText"]
pfieldspri=systems["PlanetFieldsPriority"]

del(systems["Fields"],systems["FieldsType"],
    systems["FieldsText"],systems["FieldsPriority"],
    systems["PlanetFields"],systems["PlanetFieldsType"],
    systems["PlanetFieldsText"],systems["PlanetFieldsPriority"])

#############################################################
#CREATING HTML TABLE
#############################################################
#DISPLAY LEVEL
prilevel=[0]
for level in xrange(1,5):
    if level<=displaylevel:
        pri='block'
    else:pri='none'
    prilevel+=[pri]

table=""
#////////////////////////////////////////
#TABLE HEADER
#////////////////////////////////////////
table+="""
<html>
<head>
  <link rel="stylesheet" type="text/css" href="BHM.css">
  <style>
    td.pri1{display:block;}
    td.pri2{display:%s;}
    td.pri3{display:%s;}
    td.pri4{display:%s;}
    td.pri100{display:none;}
  </style>
</head>
<body>
<table>
"""%(prilevel[2],prilevel[3],prilevel[4])

table+="<tr class='header'>"
#SYSTEM
for key in sfields[:-3]:
    text=sfieldstext[key]
    prior=sfieldspri[key]
    if "_" in text:
        text=text.replace("_","<sub>")
        text=text+"</sub>"
    if ",err" in text:
        text=text.replace(",err","")
        text="&Delta;"+text
    if "\\" in text:
        text=re.sub(r"\\(\w+)",r"&\1;",text)
    table+="<td class='field_cat pri%s' style='width:1px;white-space:nowrap'>%s</td>"%(prior,text)
#PLANET
for key in pfields[6:-1]:
    text=pfieldstext[key]
    prior=pfieldspri[key]
    if "_" in text:
        text=text.replace("_","<sub>")
        text=text+"</sub>"
    if ",err" in text:
        text=text.replace(",err","")
        text="&Delta;"+text
    if "\\" in text:
        text=re.sub(r"\\(\w+)",r"&\1;",text)
    table+="<td class='field_cat pri%s' style='width:1px;white-space:nowrap'>%s</td>"%(prior,text)
table+="<td class='field_cat' style='width:1px;white-space:nowrap'>References</td>"
table+="</tr>\n"

#////////////////////////////////////////
#TABLE
#////////////////////////////////////////
i=0
PRINTOUT("Generating table sorting by field '%s'..."%sortfield)
fk=open("%s/BHMcat.keys"%catdir,"w")
for system in sortCatalogue(systems,sortfield,reverse=sortorder):
    for planet in system["PlanetsData"]:
        planetcat=planet["BHMCatP"]
        if ((i%2)==0):clase="row_light"
        else:clase="row_dark";
        row=""
        row+="<tr class='%s'>"%clase
        qstring="LOADCONFIG&"
        for key in sfields[:-2]:
            if key=="Planets":
                for pkey in pfields[6:-1]:
                    ptipo=pfieldstyp[pkey]
                    pvalue=planet[pkey]
                    pprior=pfieldspri[pkey]
                    exec("%s=%s('%s')"%(pkey,ptipo,pvalue))
                    qstring+="%s=%s&"%(pkey,pvalue)
                    pvalue=adjustValue(pkey,pvalue,ptipo)
                    row+="<td class='field_cat pri%s' style='width:1px;white-space:nowrap'>%s</td>"%(pprior,pvalue)                    
                    if i==0:fk.write("%s\n"%pkey)
            else:
                if i==0:fk.write("%s\n"%key)
                tipo=sfieldstyp[key]
                value=system[key]
                prior=sfieldspri[key]
                exec("%s=%s('%s')"%(key,tipo,value))
                #if 'str_' in key:value="'%s'"%value
                qstring+="%s=%s&"%(key,value)
                value=adjustValue(key,value,tipo)
                row+="<td class='field_cat pri%s' style='width:1px;white-space:nowrap'>%s</td>"%(prior,value)
               
        for key in system["PlanetsModel"][planetcat].keys():
            value=system["PlanetsModel"][planetcat][key]
            qstring+="%s=%s&"%(key,value)

        valueADS=system["binary_ADS"]+";"+planet["planet_ADS"] 
        valueADS=adjustValue("ADS",valueADS,"str")
        row+="<td class='field_cat' style='width:1px;white-space:nowrap'>%s</td>"%(valueADS)
        row+="</tr>\n"
        exec("row=row.replace(\"%s\",\"<a href=\\\"%s?%s\\\" target=_parent>%s</a>\")"%(system["BHMCatS"],
                                                                                        WEB_DIR,
                                                                                        qstring,
                                                                                        system["BHMCatS"]))
        exec("cond=%s"%catfilter)
        if cond:
            table+=row
            i+=1

fk.close()
table+="</table>"
table+="<p>Number of objects: <b>%d</b></p>"%i
table+="</body></html>"
ft=open("%s/BHMcat%s.html"%(catdir,catid),"w")
ft.write(table)
ft.close()
print "Catalogue written into: %s/BHMcat%s.html"%(catdir,catid)
print "Number of objects after filter: ",i
