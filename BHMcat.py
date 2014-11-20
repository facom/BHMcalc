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
   python %s <cat_dir> [<recalculate>] [<sort_field>] [<sort_order>] [<filter>]

   <cat_dir>: location of the catalogue

   <recalculate>: 1/0.  Recalculate derivative properties.

   <sort_field>: field to sort with.

   <sort_order>: order of sort, 1: reverse, 0: normal

   <filter>: Filter.  Ex. binary_Pbin > 0.  Python syntax.

"""%argv[0]

catdir,recalculate,sortfield,sortorder,catfilter=\
    readArgs(argv,
             ["str","int","str","int","str"],
             [".","1","BHMCatS","0","binary_Pbin>0"],
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
    sfields,sfieldstyp,sfieldstxt,systems=\
        readCatalogue("BHM/data/BHMcat/BHMcat-Systems.csv",3)

    pfields,pfieldstyp,pfieldstxt,planets=\
        readCatalogue("BHM/data/BHMcat/BHMcat-Planets.csv",3)

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
        #ADD PLANETS DATA FIELD
        #========================================
        splanets=system["Planets"].split(";")
        if '-' in splanets:
            #DEFAULT PLANET
            system["PlanetsData"]=[planets["BHMCatP0000"]]
        else:
            system["PlanetsData"]=[]
            for splanet in splanets:
                if splanet=='':break
                #print "Adding %s to %s..."%(splanet,system["BHMCatS"])
                system["PlanetsData"]+=[planets[splanet]]
            #print system["PlanetsData"]
            
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
    systems["PlanetFields"]=pfields
    systems["PlanetFieldsType"]=pfieldstyp
    systems["PlanetFieldsText"]=pfieldstxt
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
pfields=systems["PlanetFields"]
pfieldstyp=systems["PlanetFieldsType"]
pfieldstext=systems["PlanetFieldsText"]

del(systems["Fields"],systems["FieldsType"],systems["FieldsText"],
    systems["PlanetFields"],systems["PlanetFieldsType"],systems["PlanetFieldsText"])

#############################################################
#CREATING HTML TABLE
#############################################################
table=""
#////////////////////////////////////////
#TABLE HEADER
#////////////////////////////////////////
table+="""
<html>
<head>
  <link rel="stylesheet" type="text/css" href="BHM.css">
</head>
<body>
<table>
"""
table+="<tr class='header'>"
#SYSTEM
for key in sfields[:-2]:
    text=sfieldstext[key]
    if "_" in text:
        text=text.replace("_","<sub>")
        text=text+"</sub>"
    if ",err" in text:
        text=text.replace(",err","")
        text="&Delta;"+text
    if "\\" in text:
        text=re.sub(r"\\(\w+)",r"&\1;",text)
    table+="<td class='field_cat' style='width:1px;white-space:nowrap'>%s</td>"%text
#PLANET
for key in pfields[6:-1]:
    text=pfieldstext[key]
    if "_" in text:
        text=text.replace("_","<sub>")
        text=text+"</sub>"
    if ",err" in text:
        text=text.replace(",err","")
        text="&Delta;"+text
    if "\\" in text:
        text=re.sub(r"\\(\w+)",r"&\1;",text)
    table+="<td class='field_cat' style='width:1px;white-space:nowrap'>%s</td>"%text
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
        if ((i%2)==0):clase="row_light"
        else:clase="row_dark";
        row=""
        row+="<tr class='%s'>"%clase
        qstring="LOADCONFIG&"
        for key in sfields[:-1]:
            if key=="Planets":
                for pkey in pfields[6:-1]:
                    ptipo=pfieldstyp[pkey]
                    pvalue=planet[pkey]
                    exec("%s=%s('%s')"%(pkey,ptipo,pvalue))
                    qstring+="%s=%s&"%(pkey,pvalue)
                    pvalue=adjustValue(pkey,pvalue,ptipo)
                    row+="<td class='field_cat' style='width:1px;white-space:nowrap'>%s</td>"%(pvalue)
                    if i==0:fk.write("%s\n"%pkey)
            else:
                if i==0:fk.write("%s\n"%key)
                tipo=sfieldstyp[key]
                value=system[key]
                exec("%s=%s('%s')"%(key,tipo,value))
                qstring+="%s=%s&"%(key,value)
                value=adjustValue(key,value,tipo)
                row+="<td class='field_cat' style='width:1px;white-space:nowrap'>%s</td>"%(value)
                
        valueADS=system["binary_ADS"]+";"+planet["planet_ADS"] 
        valueADS=adjustValue("ADS",valueADS,"str")
        row+="<td class='field_cat' style='width:1px;white-space:nowrap'>%s</td>"%(valueADS)
        row+="</tr>\n"
        exec("row=row.replace('%s','<a href=%s?%s target=_parent>%s</a>')"%(system["BHMCatS"],
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
ft=open("%s/BHMcat.html"%catdir,"w")
ft.write(table)
ft.close()
print "Number of objects after filter: ",i
