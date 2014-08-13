# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 17:49:40 2014

@author: User
"""

import time
import requests
import pandas as pd
import datetime
import numpy as np
import console

#initiate client
client = console.Client('bcapuder','cTJxzxX_SmZLHiuQn1zs')
now = datetime.datetime.now()
#makes created_at string for job
if now.month < 10:
    monthstr="0"+str(now.month)
else:
    monthstr=str(now.month)
if now.day < 10:
    daystr="0"+str(now.day)
else:
    daystr=str(now.day)
if now.hour < 10:
    hourstr="0"+str(now.hour)
else:
    hourstr=str(now.hour)
if now.minute < 10:
    minutestr="0"+str(now.minute)
else:
    minutestr=str(now.minute)
if now.second < 10:
    secondstr="0"+str(now.second)
else:
    secondstr=str(now.second)
createdstr = str(now.year)+"-"+monthstr+"-"+daystr+" "+hourstr+":"+minutestr+":"+secondstr
newdict={}
keepGoing = True
pageCounter = 0
while keepGoing:
    time.sleep(2)
    r = requests.get("http://www.fema.gov/api/open/v1/DisasterDeclarationsSummaries?$skip="+str(pageCounter)+"&$filter=declarationDate ge '2000-01-01T00:00:00.000z'")
    if len(r.json()['DisasterDeclarationsSummaries'])==0:
        keepGoing = False
    for disaster in r.json()['DisasterDeclarationsSummaries']:
        outputdict={}
        outputdict['title']=str(disaster['title'])
        outputdict['disasternum']=str(disaster['disasterNumber'])
        outputdict['incidentend']=str(disaster['incidentEndDate'][0:10])
        outputdict['incidentbeg']=str(disaster['incidentBeginDate'][0:10])
        outputdict['ihpro']=str(disaster['ihProgramDeclared'])
        outputdict['county']=str(disaster['declaredCountyArea'])
        outputdict['state']=str(disaster['state'])
        outputdict['type']=str(disaster['incidentType'])
        outputdict['disas']=str(disaster['disasterType'])
        outputdict['hmpro']=str(disaster['hmProgramDeclared'])
        outputdict['iapro']=str(disaster['iaProgramDeclared'])
        outputdict['decdate']=str(disaster['declarationDate'][0:10])
        newdict[str(disaster['_id'])]=outputdict
    pageCounter +=100 
empty = np.empty((len(newdict),14))
empty[:]=np.NAN
df = pd.DataFrame(empty,columns=['key','state','county','type','title','disasternum','incidentbeg','incidentend','ihpro','hmpro','iapro','decdate','disas','created_at'])
#sets key column = keys from newdict
df.key=newdict.keys()
"""
for loop simply sets column of df = corresponding value in newdict
a couple use join syntax since charges and notes typically come in lists
"""
for i in range(len(newdict)):
    df.state[i]=newdict[df.key[i]]['state']
    df.county[i]=newdict[df.key[i]]['county']
    df.type[i]=newdict[df.key[i]]['type']
    df.title[i]=newdict[df.key[i]]['title']
    df.disasternum[i]=newdict[df.key[i]]['disasternum']
    df.incidentbeg[i]=newdict[df.key[i]]['incidentbeg']
    df.incidentend[i]=newdict[df.key[i]]['incidentend']
    df.ihpro[i]=newdict[df.key[i]]['ihpro'].upper()
    df.hmpro[i]=newdict[df.key[i]]['hmpro'].upper()
    df.iapro[i]=newdict[df.key[i]]['iapro'].upper()
    df.decdate[i]=newdict[df.key[i]]['decdate']
    df.disas[i]=newdict[df.key[i]]['disas']
    df.created_at[i]=createdstr
#save df to csv
filename = 'C:\Users\User\Documents\FEMAScrape'+str(now.month)+str(now.day)+str(now.hour)+'.csv'    
df.to_csv(filename,index=False)
client.csv_import(filename,'redshift-dr','dre','femascrape','','','',558,'',name='fema import',compression='none')
