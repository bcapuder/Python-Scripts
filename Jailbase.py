# -*- coding: utf-8 -*-

"""
Created on Mon Jul 14 11:54:30 2014
bcapuder
python script for scraping jailbase.com through its api
"""
import time
import requests
import pandas as pd
import numpy as np
import console
import datetime
#define function scrapejailbase so that it can be called by other scripts
def jailbasescrape ():
    #a dataframe is opened with the most recent jailbase_id for each source
    df = pd.read_csv("C:\Users\User\Documents\Mostrecentsourcejailbase.csv")
    oldrecent = df.set_index('source_id').to_dict()
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
    #this dict stores the sources
    sources = {}
    #this dict stores the info to be pushed to jekyll
    newdict={}
    #this keeps track of which source script is on
    count=0
    #this is the api for grabbing the sources jailbase pulls from and stores these in sources
    r = requests.get('http://www.jailbase.com/api/1/sources/')
    for element in r.json()['records']:
        sources[str(element['source_id'])]={'name':element['name'],'state':element['state']}
    #a dataframe is created to store new most recent jailbase_ids for each source
    df2 = pd.DataFrame(np.zeros((len(sources),5)),columns=['source_id','most_recent_id','name','state','county'])
    #the api for recent is implemented by looping through each source, resetting pageCounter to keep track of what page its on for each source
    for i in sources:
        pageCounter = 1
        time.sleep(1)
        #this is an initial call to the api to see if its empty and check next_page
        r = requests.get('http://www.jailbase.com/api/1/recent/?source_id='+i+'&page='+str(pageCounter))
        
        #keepGoing serves as a break when jailbase_id is found in the df with most recent jailbase_id or if source is empty
        keepGoing = True
        if r.json()['records']==[]:
            #this is a check for empty source
            keepGoing = False        
        """
        This is the main loop--it goes through each page until it finds next_page = 0 or it finds the most recent id for the source.
        pageCounter increments at bottom of loop to point api at next page for the source
        Sources have a total of 10 pages--never more and sometimes less
        """
        while r.json()['next_page']>0 and keepGoing:
            print str(pageCounter)
            time.sleep(2)
            r = requests.get('http://www.jailbase.com/api/1/recent/?source_id='+i+'&page='+str(pageCounter))
            """
            Each page has 10 records so this portion loops through each record and assembles outputdict
            outputdict is a dictionary of values i.e. gender,race,etc for each record
            each record's outputdict is then paired with its jailbase_id in a dictionary (newdict)
            """
            for element in r.json()['records']:
                #if id is in list of most recent, while loop exits
                if any(df.most_recent_id == str(element['id'])):
                    keepGoing=False
                #detailstring stores values for each prospective detail found in record since this varies by source
                detailstring = ['','','','','','','','','','']
                #these are properties that every record has
                outputdict={}   
                outputdict['name']=element['name']
                outputdict['charges']=element['charges']
                outputdict['mugshot']=element['mugshot']
                outputdict['more_info_url']=element['more_info_url']
                outputdict['book_date']=element['book_date']
                """
                this for loop goes through each element in details and replaces the blank string
                in detailstring when the characteristic is found
                """            
                for thing in element['details']:
                    if 'Gender' in thing:
                        detailstring[0]=str(thing[1])
                    if 'Race' in thing:
                        detailstring[1]=str(thing[1])
                    if 'Height' in thing:
                        #these chars are replaced since they have the potential to disrupt strings
                        detailstring[2]=str(thing[1]).replace("'"," ft").replace('"',' in')
                    if 'Weight' in thing:
                        #these chars are replaced since they have the potential to disrupt strings
                        #height ends up in weight sometimes
                        detailstring[3]=str(thing[1]).replace("'"," ft").replace('"',' in')
                    if 'Eyes' in thing:
                        detailstring[4]=str(thing[1])
                    if 'Hair' in thing:
                        detailstring[5]=str(thing[1])    
                    if 'Facility' in thing:
                        detailstring[6]=str(thing[1])        
                    if 'Notes' in thing:
                        #some sources put age in notes so this checks that and puts age in the right spot if necessary
                        if 'Age:' in str(thing[1]):
                            detailstring[9]=str(thing[1]).replace('Age:','').strip()
                        else:
                            detailstring[7]=str(thing[1])
                    if 'Ref #' in thing:
                        detailstring[8]=str(thing[1])
                    if 'Age (at arrest)' in thing:
                        detailstring[9]=str(thing[1])
                #this is the record for loop and so the outputdict is assembled, whether characteristic is was found or not
                outputdict['gender']=detailstring[0]
                outputdict['race']=detailstring[1]
                outputdict['height']=detailstring[2]
                outputdict['weight']=detailstring[3]
                outputdict['eyes']=detailstring[4]
                outputdict['hair']=detailstring[5]
                outputdict['facility']=detailstring[6]
                outputdict['notes']=detailstring[7]
                outputdict['refnum']=detailstring[8]
                outputdict['age']=detailstring[9]
                newdict[str(element['id'])] = outputdict
            #end of while loop, increments to next page
            pageCounter+=1
        df2.source_id[count]=i
        time.sleep(1)
        r = requests.get('http://www.jailbase.com/api/1/recent/?source_id='+i+'&page=0')
        if r.json()['records']<>[]:
            #writes new most recent source_id to second dataframe
            df2.most_recent_id[count]=r.json()['records'][0]['id']
        print "done with "+i
        count+=1
    #this updates df2 to see if oldrecent had a valid that this does not as well as inserts name,state,and county
    for i in range(len(df2)):
        if df2.most_recent_id[i] == 0 and df2.most_recent_id[i] in oldrecent['most_recent_id']:
            df2.most_recent_id[i]=oldrecent['most_recent_id'][df2.source_id[i]]
        df2.name[i]=sources[df2.source_id[i]]['name']
        df2.state[i]=sources[df2.source_id[i]]['state']
        if ' County' in df2.name[i]:
            df2.county[i]=df2.name[i].split(' County')[0]
    #overwrites old source lookup csv
    df2.to_csv("C:\Users\User\Documents\Mostrecentsourcejailbase.csv",index=False)
    #if there was a new source added, this adds the new source to jailbaselookup
    if len(df2) != len(df):
        newsources=[]
        for i in range(0,len(df2)):
            if any(df.source_id != df2.source_id[i]):
                newsources.append([df2.source_id[i],sources[df2.source_id[i]]['name'],sources[df2.source_id[i]]['state'],''])
            newsources.append(['','','',''])
            df3=pd.DataFrame(newsources)
            df3=df3[0:len(df3)]
            filename2="C:\Users\User\Documents\Lookup"+str(now.month)+str(now.day)+str(now.hour)+".csv"
            df3.to_csv(filename2,index=False)
            client.csv_import(filename2,'redshift-dr','jekyll','jailbaselookup','','','',558,'',name='jailbase import',compression='none')
    newsources=df2.set_index('source_id').to_dict()
    """
    Done with scrape, now puts newdict into dataframe
    first initiate empty dataframe, then fill with elements from newdict
    """
    #uses empty to inititate df3 as full of NaNs
    empty = np.empty((len(newdict),19))
    empty[:]=np.NAN
    df4 = pd.DataFrame(empty,columns=['key','state','county','age','bookdate','charges','eyes','facility','gender','hair','height','moreinfourl','mugshot','name','notes','race','refnum','weight','created_at'])
    #sets key column = keys from newdict
    df4.key=newdict.keys()
    
    """
    for loop simply sets column of df4 = corresponding value in newdict
    a couple use join syntax since charges and notes typically come in lists
    """
    for i in range(len(newdict)):
        df4.state[i]=newsources['state'][df4.key[i].split('/')[1]]
        if newsources['county'][df4.key[i].split('/')[1]]<>0:
            df4.county[i]=str(newsources['county'][df4.key[i].split('/')[1]]).upper()
        df4.age[i]=newdict[df4.key[i]]['age']
        df4.bookdate[i]=newdict[df4.key[i]]['book_date']
        df4.charges[i]=" ".join([str(x) for x in (";".join([str(x) for x in newdict[df4.key[i]]['charges']])).split('\xb0')])
        if len(df4.charges[i])>1000:
            df4.charges[i]=df4.charges[i][0:999]
        df4.eyes[i]=newdict[df4.key[i]]['eyes']
        df4.facility[i]=newdict[df4.key[i]]['facility']
        df4.gender[i]=newdict[df4.key[i]]['gender']
        df4.hair[i]=newdict[df4.key[i]]['hair']
        df4.height[i]=newdict[df4.key[i]]['height']
        df4.moreinfourl[i]=newdict[df4.key[i]]['more_info_url']
        df4.mugshot[i]=newdict[df4.key[i]]['mugshot']
        df4.name[i]=newdict[df4.key[i]]['name']
        df4.notes[i]=newdict[df4.key[i]]['notes']
        df4.race[i]=newdict[df4.key[i]]['race']
        df4.refnum[i]=newdict[df4.key[i]]['refnum']
        df4.weight[i]=newdict[df4.key[i]]['weight']
        df4.created_at[i]=createdstr
    #save df4 to csv
    filename = 'C:\Users\User\Documents\JailbaseOutPut'+str(now.month)+str(now.day)+str(now.hour)+'.csv'    
    df4.to_csv(filename,index=False)
    #import csv, most fields aren't necessary--558 is though; represents credential id
    client.csv_import(filename,'redshift-dr','jekyll','jailbase','','','',558,'',name='jailbase import',compression='none')
    print createdstr
jailbasescrape()
