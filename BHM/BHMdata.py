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
# Data manipulation routines
###################################################
from BHM import *

###################################################
#PACKAGES
###################################################
import csv
import pickle

###################################################
#CONFIGURATION
###################################################

###################################################
#MACROS
###################################################

###################################################
#GLOBALS
###################################################

###################################################
#ROUTINES
###################################################
def dms(string):
    #ASSUME SPACES AS SEPARATORS
    parts=string.split()
    #ASSUME ":"
    if(len(parts)==1):
        parts=string.split(":")
    #NONE OF THE ABOVE THE ANGLE IS NOT IN SEX.
    if(len(parts)==1):
        parts=[float(string),0,0]
    d=float(parts[0])+float(parts[1])/60.0+float(parts[2])/3600;
    return d

def readCatalogue(file,idcol=0,pritype='priority'):
    """
    Read catalogue from a csv file with the following structure:
    - Line 1: Fields.
    - Line 2: Types.  Available: int, float, str, dms (degree, minutes, seconds).
    - Line 3: Text.  Text version of field names (LaTeX format).

    Delimited by ,
    """
    csvfile=open(file,"rb")
    content=csv.reader(csvfile,delimiter=',')
    
    objects=dict()
    classes=dict()
    
    data=dict()
    i=0
    for row in content:
        if '#' in row[0]:continue
        i+=1
        #########################################
        #FIELDS
        #########################################
        if i==1:
            row=array(row)
            j=0
            fields=[]
            for field in row:
                fields+=[field]
                j+=1
            ncols=j

        #########################################
        #FIELD TYPES
        #########################################
        elif i==2:
            row=array(row)
            fieldstyp=dict()
            j=0
            for tipo in row:
                fieldstyp[fields[j]]=tipo
                j+=1
                
        #########################################
        #FIELD TEXT
        #########################################
        elif i==3:
            row=array(row)
            fieldstxt=dict()
            j=0
            for text in row:
                fieldstxt[fields[j]]=text
                j+=1

        #########################################
        #PRIORITY
        #########################################
        elif i==4:
            row=array(row)
            fieldspri=dict()
            j=0
            for pri in row:
                if pritype=="priority":
                    fieldspri[fields[j]]=int(pri)
                else:
                    tipo=fieldstyp[fields[j]]
                    pri=pri.replace(",",".")
                    exec("fieldspri[fields[j]]=%s(pri)"%tipo)
                j+=1

        #########################################
        #TABLE
        #########################################
        else:
            rid=row[idcol]
            obj=dict()
            j=0
            for value in row:
                tipo=fieldstyp[fields[j]]
                if tipo=="float" or tipo=="dms":value=value.replace(",",".")
                exec "obj[fields[j]]=%s(value.strip())"%tipo in locals(),globals()
                j+=1
            data[rid]=obj

    return fields,fieldstyp,fieldstxt,fieldspri,data

def sortCatalogue(catalogue,key,reverse=False):
    ids=sorted(catalogue,key=lambda k:catalogue[k][key],reverse=reverse)
    scatalogue=[]
    for cid in ids:
        scatalogue+=[catalogue[cid]]
    return scatalogue

def notMissing(value):
    if value!=-1 and value!=-2 and value!="-":return 1
    else:return 0

def linkADS(adstring):
    link="http://adsabs.harvard.edu/abs/"+adstring
    return link

def adjustValue(key,value,tipo):
    if value==-1:value="-"
    elif value==-2:value="N/A"
    else:
        if tipo=="float" or tipo=="dms":value="%+.5f"%value
        if "ADS" in key and value!='-':
            refs=value.split(";")
            value=""
            j=1
            for ref in refs[:-1]:
                ref=ref.strip()
                if '-' in ref or ref=='':continue
                #print "Ref j:",ref
                value+="<a href="+linkADS(ref)+" target=_blank>Ref %d</a>,"%j
                j+=1
            value=value.strip(",")
    return value

def loadResults(resdir,verbose=False):
    results=dict2obj(dict())

    for obj in OBJECTS_ALL:
        if verbose:print "Reading object %s..."%obj
        try:
            exec("results.%s=loadConf(resdir+'%s.conf')+loadConf(resdir+'%s.data')"%(obj,obj,obj))
        except:
            results.star2=results.star1
    
    return results
