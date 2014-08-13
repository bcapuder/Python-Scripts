# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 12:35:30 2014

@author: bcapuder


"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 15:23:32 2014

@author: User
"""
import time
import requests
import pandas as pd
import datetime
import numpy as np
import console



#initiate client
tiernum=2
f = open('C:\Users\User\Documents\RecentAnchor.txt','r')
anchor=f.readlines()[0]
f.close()
client = console.Client('bcapuder','cTJxzxX_SmZLHiuQn1zs')
now = datetime.datetime.now()
threshold=range(200,10000,200)
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
pagecounter=0
newdict={}
citydict={}
countydict={}
r = requests.get('http://reference.3taps.com/locations/?auth_token=2506e1aa51e77ceaee767fb5c56135e5&level=city')
for location in r.json()['locations']:
    citydict[str(location['code'])]=str(location['short_name'])
time.sleep(2)
r = requests.get('http://reference.3taps.com/locations/?auth_token=2506e1aa51e77ceaee767fb5c56135e5&level=county')
for location in r.json()['locations']:
    countydict[str(location['code'])]=str(location['short_name'])
time.sleep(2)
r=requests.get('http://polling.3taps.com/poll/?auth_token=2506e1aa51e77ceaee767fb5c56135e5')
f = open('C:\Users\User\Documents\RecentAnchor.txt','w')
f.write(r.json()['anchor'])
f.close()
r = requests.get('http://search.3taps.com/?auth_token=2506e1aa51e77ceaee767fb5c56135e5&rpp=100&location.country=USA&retvals=id,account_id,source,category,location,external_id,external_url,timestamp,timestamp_deleted,expires,language,price,currency,annotations,status,state,immortal,deleted&category_group=RRRR&anchor='+str(anchor)+'&page='+str(pagecounter))
for thresh in threshold:
    newdict={}
    while r.json()['next_page']>0 and pagecounter<thresh:
        time.sleep(2)
        r = requests.get('http://search.3taps.com/?auth_token=2506e1aa51e77ceaee767fb5c56135e5&rpp=100&location.country=USA&retvals=id,body,heading,account_id,source,category,location,external_id,external_url,timestamp,timestamp_deleted,expires,language,price,currency,annotations,status,state,immortal,deleted&category_group=RRRR&anchor='+str(anchor)+'&page='+str(pagecounter))
        for post in r.json()['postings']:
            outputdict={}
            if 'status' in post.keys():
                try:
                    outputdict['status']=str(post['status'])
                except:
                    outputdict['status']=''
            else:
                outputdict['status']=''
            if 'body' in post.keys():
                try:
                    outputdict['body']=str(post['body'])[0:500]
                except:
                    outputdict['body']=''
            else:        
                outputdict['body']=''
            if 'heading' in post.keys():
                try:
                    outputdict['heading']=str(post['heading'])[0:500]
                except:
                    outputdict['heading']=''
            else:
                outputdict['heading']=''
            if 'category' in post.keys():
                outputdict['category']=str(post['category'])
            else:
                outputdict['category']=''
            if 'annotations' in post.keys():
                if 'phone' in post['annotations'].keys():
                    outputdict['phone']=str(post['annotations']['phone'])
                else:
                    outputdict['phone']=''
                if 'bedrooms' in post['annotations'].keys():
                    outputdict['bedrooms']=str(post['annotations']['bedrooms'])
                else:
                    outputdict['bedrooms']=''
                if 'bathrooms' in post['annotations'].keys():
                    outputdict['bathrooms']=str(post['annotations']['bathrooms'])
                else:
                    outputdict['bathrooms']=''
                if 'rent' in post['annotations'].keys():
                    outputdict['rent']=str(post['annotations']['rent'])
                else:
                    outputdict['rent']=''
                if 'original_posting_date' in post['annotations'].keys():
                    outputdict['original_posting_date']=str(post['annotations']['original_posting_date'])
                else:
                    outputdict['original_posting_date']=''
                if 'available' in post['annotations'].keys():
                    outputdict['available']=str(post['annotations']['available'])
                else:
                    outputdict['available']=''
                if 'apartment' in post['annotations'].keys():
                    outputdict['apartment']=str(post['annotations']['apartment'])
                else:
                    outputdict['apartment']=''
                if 'source_subloc' in post['annotations'].keys():
                    outputdict['source_subloc']=str(post['annotations']['source_subloc'])
                else:
                    outputdict['source_subloc']=''
                if 'source_account' in post['annotations'].keys():
                    outputdict['source_account']=str(post['annotations']['source_account'])
                else:
                    outputdict['source_account']=''
                if 'source_continent' in post['annotations'].keys():
                    outputdict['source_continent']=str(post['annotations']['source_continent'])
                else:
                    outputdict['source_continent']=''
                if 'sqft' in post['annotations'].keys():
                    try:
                        outputdict['sqft']=int(float(str(post['annotations']['sqft'])))
                    except:
                        outputdict['sqft']=''
                else:
                    outputdict['sqft']=''
                if 'source_cat' in post['annotations'].keys():
                    outputdict['source_cat']=str(post['annotations']['source_cat'])
                else:
                    outputdict['source_cat']=''
                if 'source_neighborhood' in post['annotations'].keys():
                    try:
                        outputdict['source_neighborhood']=str(post['annotations']['source_neighborhood'])
                    except:
                        outputdict['source_neighborhood']=''
                else:
                    outputdict['source_neighborhood']=''
                if 'source_state' in post['annotations'].keys():
                    outputdict['source_state']=str(post['annotations']['source_state'])
                else:
                    outputdict['source_state']=''
                if 'source_map_yahoo' in post['annotations'].keys():
                    outputdict['source_map_yahoo']=str(post['annotations']['source_map_yahoo'])
                else:
                    outputdict['source_map_yahoo']=''
                if 'source_loc' in post['annotations'].keys():
                    outputdict['source_loc']=str(post['annotations']['source_loc'])
                else:
                    outputdict['source_loc']=''
                if 'cats' in post['annotations'].keys():
                    outputdict['cats']=str(post['annotations']['cats'])
                else:
                    outputdict['cats']=''
                if 'latlong_source' in post['annotations'].keys():
                    outputdict['latlong_source']=str(post['annotations']['latlong_source'])
                else:
                    outputdict['latlong_source']=''
                if 'dogs' in post['annotations'].keys():
                    outputdict['dogs']=str(post['annotations']['dogs'])
                else:
                    outputdict['dogs']=''
                if 'source_map_google' in post['annotations'].keys():
                    outputdict['source_map_google']=str(post['annotations']['source_map_google'])
                else:
                    outputdict['source_map_google']=''
                if 'source_subcat' in post['annotations'].keys():
                    outputdict['source_subcat']=str(post['annotations']['source_subcat'])
                else:
                    outputdict['source_subcat']=''
                if 'source_heading' in post['annotations'].keys():
                    outputdict['source_heading']=str(post['annotations']['source_heading'])
                else:
                    outputdict['source_heading']=''
                if 'w_d_in_unit' in post['annotations'].keys():
                    outputdict['w_d_in_unit']=str(post['annotations']['w_d_in_unit'])[0:499]
                else:
                    outputdict['w_d_in_unit']=''
                if 'off_street_parking' in post['annotations'].keys():
                    outputdict['off_street_parking']=str(post['annotations']['off_street_parking'])
                else:
                    outputdict['off_street_parking']=''
                if 'townhouse' in post['annotations'].keys():
                    outputdict['townhouse']=str(post['annotations']['townhouse'])
                else:
                    outputdict['townhouse']=''
                if 'wheelchair_accessible' in post['annotations'].keys():
                    outputdict['wheelchair_accessible']=str(post['annotations']['wheelchair_accessible'])
                else:
                    outputdict['wheelchair_accessible']=''
                if 'year' in post['annotations'].keys():
                    outputdict['year']=str(post['annotations']['year'])
                else:
                    outputdict['year']=''
                if 'duplex' in post['annotations'].keys():
                    outputdict['duplex']=str(post['annotations']['duplex'])
                else:
                    outputdict['duplex']=''
                if 'sale_dates' in post['annotations'].keys():
                    outputdict['sale_dates']=str(post['annotations']['sale_dates'])
                else:
                    outputdict['sale_dates']=''
                if 'house' in post['annotations'].keys():
                    outputdict['house']=str(post['annotations']['house'])
                else:
                    outputdict['house']=''
                if 'attached_garage' in post['annotations'].keys():
                    outputdict['attached_garage']=str(post['annotations']['attached_garage'])
                else:
                    outputdict['attached_garage']=''
                if 'furnished' in post['annotations'].keys():
                    outputdict['furnished']=str(post['annotations']['furnished'])
                else:
                    outputdict['furnished']=''
                if 'no_smoking' in post['annotations'].keys():
                    outputdict['no_smoking']=str(post['annotations']['no_smoking'])
                else:
                    outputdict['no_smoking']=''
                if 'street_parking' in post['annotations'].keys():
                    outputdict['street_parking']=str(post['annotations']['street_parking'])
                else:
                    outputdict['street_parking']=''
                if 'cottage_cabin' in post['annotations'].keys():
                    outputdict['cottage_cabin']=str(post['annotations']['cottage_cabin'])
                else:
                    outputdict['cottage_cabin']=''
                if 'detached_garage' in post['annotations'].keys():
                    outputdict['detached_garage']=str(post['annotations']['detached_garage'])
                else:
                    outputdict['detached_garage']=''
                if 'w_d_hookups' in post['annotations'].keys():
                    outputdict['w_d_hookups']=str(post['annotations']['w_d_hookups'])
                else:
                    outputdict['w_d_hookups']=''
                if 'land' in post['annotations'].keys():
                    outputdict['land']=str(post['annotations']['land'])
                else:
                    outputdict['land']=''
                if 'laundry_on_site' in post['annotations'].keys():
                    outputdict['laundry_on_site']=str(post['annotations']['laundry_on_site'])
                else:
                    outputdict['laundry_on_site']=''
                if 'condo' in post['annotations'].keys():
                    outputdict['condo']=str(post['annotations']['condo'])
                else:
                    outputdict['condo']=''
                if 'private_bath' in post['annotations'].keys():
                    outputdict['private_bath']=str(post['annotations']['private_bath'])
                else:
                    outputdict['private_bath']=''
                if 'private_room' in post['annotations'].keys():
                    outputdict['private_room']=str(post['annotations']['private_room'])
                else:
                    outputdict['private_room']=''
                if 'no_private_bath' in post['annotations'].keys():
                    outputdict['no_private_bath']=str(post['annotations']['no_private_bath'])
                else:
                    outputdict['no_private_bath']=''
                if 'carport' in post['annotations'].keys():
                    outputdict['carport']=str(post['annotations']['carport'])
                else:
                    outputdict['carport']=''
                if 'manufactured' in post['annotations'].keys():
                    outputdict['manufactured']=str(post['annotations']['manufactured'])
                else:
                    outputdict['manufactured']=''
                if 'loft' in post['annotations'].keys():
                    outputdict['loft']=str(post['annotations']['loft'])
                else:
                    outputdict['loft']=''
                if 'in_law' in post['annotations'].keys():
                    outputdict['in_law']=str(post['annotations']['in_law'])
                else:
                    outputdict['in_law']=''
                if 'flat' in post['annotations'].keys():
                    outputdict['flat']=str(post['annotations']['flat'])
                else:
                    outputdict['flat']=''
                if 'assisted_living' in post['annotations'].keys():
                    outputdict['assisted_living']=str(post['annotations']['assisted_living'])
                else:
                    outputdict['assisted_living']=''
            if 'deleted' in post.keys():
                outputdict['deleted']=str(post['deleted'])
            else:
                outputdict['deleted']=''
            if 'timestamp' in post.keys():
                outputdict['timestamp']=str(post['timestamp'])
            else:
                outputdict['timestamp']=''
            if 'price' in post.keys():
                outputdict['price']=post['price']
            else:
                outputdict['price']=''
            if 'expires' in post.keys():
                outputdict['expires']=str(post['expires'])
            else:
                outputdict['expires']=''
            if 'immortal' in post.keys():
                outputdict['immortal']=str(post['immortal'])
            else:
                outputdict['immortal']=''
            if 'source' in post.keys():
                outputdict['source']=str(post['source'])
            else:
                outputdict['source']=''
            if 'state' in post.keys():
                outputdict['state']=str(post['state'])
            else:
                outputdict['state']=''
            if 'location' in post.keys():
                if 'city' in post['location'].keys():
                    outputdict['city']=citydict[str(post['location']['city'])]
                else:
                    outputdict['city']=''
                if 'geolocation_status' in post['location'].keys():
                    outputdict['geolocation_status']=str(post['location']['geolocation_status'])
                else:
                    outputdict['geolocation_status']=''
                if 'zipcode' in post['location'].keys(): 
                    outputdict['zipcode']=str(post['location']['zipcode']).strip('USA-')
                else:
                    outputdict['zipcode']=''
                if 'long' in post['location'].keys():
                    outputdict['long']=post['location']['long']
                else:
                    outputdict['long']=''
                if 'county' in post['location'].keys(): 
                    outputdict['county']=countydict[str(post['location']['county'])]
                else:
                    outputdict['county']=''
                if 'state' in post['location'].keys(): 
                    outputdict['state']=str(post['location']['state']).strip('USA-')
                else:
                    outputdict['state']=''
                if 'lat' in post['location'].keys(): 
                    outputdict['lat']=post['location']['lat']
                else:
                    outputdict['lat']=''
                if 'formatted_address' in post['location'].keys(): 
                    outputdict['formatted_address']=str(post['location']['formatted_address'])
                else:
                    outputdict['formatted_address']=''
                if 'accuracy' in post['location'].keys(): 
                    outputdict['accuracy']=post['location']['accuracy']
                else:
                    outputdict['accuracy']=''
            if 'external_id' in post.keys():
                outputdict['external_id']=str(post['external_id'])
            else:
                outputdict['external_id']=''
            if 'external_url' in post.keys():
                outputdict['external_url']=str(post['external_url'])
            else:
                outputdict['external_url']=''
            if 'language' in post.keys():
                outputdict['language']=str(post['language'])
            else:
                outputdict['language']=''
            if 'currency' in post.keys():
                outputdict['currency']=str(post['currency'])
            else:
                outputdict['currency']=''
            newdict[str(post['id'])]=outputdict
        print str(pagecounter)
        pagecounter+=1
    print 'dataframe part'
    empty = np.empty((len(newdict),74))
    empty[:]=np.NAN
    df = pd.DataFrame(empty,columns=['intid','status','body','heading','category','phone','bedrooms','bathrooms','rent','original_posting_date','available','apartment','source_subloc','source_account','source_continent','sqft','source_cat','source_neighborhood','source_state','source_map_yahoo','source_loc','cats','latlong_source','dogs','source_map_google','source_subcat','source_heading','w_d_in_unit','off_street_parking','townhouse','wheelchair_accessible','year','duplex','sale_dates','house','attached_garage','furnished','no_smoking','street_parking','cottage_cabin','detached_garage','w_d_hookups','land','laundry_on_site','condo','private_bath','private_room','no_private_bath','carport','manufactured','loft','in_law','flat','assisted_living','deleted','timestamp','price','expires','immortal','source','state','city','geolocation_status','zipcode','long','county','lat','formatted_address','accuracy','external_id','external_url','language','currency','created_at'])
    df.intid=newdict.keys()
    for i in range(0,len(newdict)):
        df.status[i]=newdict[df.intid[i]]['status'].decode('ascii','ignore')
        df.body[i]=newdict[df.intid[i]]['body'].decode('ascii','ignore')
        df.heading[i]=newdict[df.intid[i]]['heading'].decode('ascii','ignore')
        df.category[i]=newdict[df.intid[i]]['category'].decode('ascii','ignore')
        df.phone[i]=newdict[df.intid[i]]['phone'].decode('ascii','ignore')
        df.bedrooms[i]=newdict[df.intid[i]]['bedrooms'].decode('ascii','ignore')
        df.bathrooms[i]=newdict[df.intid[i]]['bathrooms'].decode('ascii','ignore')
        df.rent[i]=newdict[df.intid[i]]['rent'] if type(newdict[df.intid[i]]['rent'])==float else ''
        df.original_posting_date[i]=newdict[df.intid[i]]['original_posting_date'].decode('ascii','ignore')
        df.available[i]=newdict[df.intid[i]]['available'].decode('ascii','ignore')
        df.apartment[i]=newdict[df.intid[i]]['apartment'].decode('ascii','ignore')
        df.source_subloc[i]=newdict[df.intid[i]]['source_subloc'].decode('ascii','ignore')
        df.source_account[i]=newdict[df.intid[i]]['source_account'].decode('ascii','ignore')
        df.source_continent[i]=newdict[df.intid[i]]['source_continent'].decode('ascii','ignore')
        if type(newdict[df.intid[i]]['sqft'])==int or type(newdict[df.intid[i]]['sqft'])==float :
            df.sqft[i]=int(newdict[df.intid[i]]['sqft'])
        else:
            df.sqft[i]=''
        df.source_cat[i]=newdict[df.intid[i]]['source_cat'].decode('ascii','ignore')
        df.source_neighborhood[i]=newdict[df.intid[i]]['source_neighborhood'].decode('ascii','ignore')
        df.source_state[i]=newdict[df.intid[i]]['source_state'].decode('ascii','ignore')
        df.source_map_yahoo[i]=''
        df.source_loc[i]=newdict[df.intid[i]]['source_loc'].decode('ascii','ignore')
        df.cats[i]=newdict[df.intid[i]]['cats'].decode('ascii','ignore')
        df.latlong_source[i]=newdict[df.intid[i]]['latlong_source']
        df.dogs[i]=newdict[df.intid[i]]['dogs']
        df.source_map_google[i]=''
        df.source_subcat[i]=newdict[df.intid[i]]['source_subcat'].decode('ascii','ignore')
        df.source_heading[i]=newdict[df.intid[i]]['source_heading'].decode('ascii','ignore')
        df.w_d_in_unit[i]=newdict[df.intid[i]]['w_d_in_unit'].decode('ascii','ignore')
        df.off_street_parking[i]=newdict[df.intid[i]]['off_street_parking'].decode('ascii','ignore')
        df.townhouse[i]=newdict[df.intid[i]]['townhouse'].decode('ascii','ignore')
        df.wheelchair_accessible[i]=newdict[df.intid[i]]['wheelchair_accessible'].decode('ascii','ignore')
        df.year[i]=newdict[df.intid[i]]['year'].decode('ascii','ignore')
        df.duplex[i]=newdict[df.intid[i]]['duplex'].decode('ascii','ignore')
        df.sale_dates[i]=newdict[df.intid[i]]['sale_dates'].decode('ascii','ignore')
        df.house[i]=newdict[df.intid[i]]['house'].decode('ascii','ignore')
        df.attached_garage[i]=newdict[df.intid[i]]['attached_garage'].decode('ascii','ignore')
        df.furnished[i]=newdict[df.intid[i]]['furnished'].decode('ascii','ignore')
        df.no_smoking[i]=newdict[df.intid[i]]['no_smoking'].decode('ascii','ignore')
        df.street_parking[i]=newdict[df.intid[i]]['street_parking'].decode('ascii','ignore')
        df.cottage_cabin[i]=newdict[df.intid[i]]['cottage_cabin'].decode('ascii','ignore')
        df.detached_garage[i]=newdict[df.intid[i]]['detached_garage'].decode('ascii','ignore')
        df.w_d_hookups[i]=newdict[df.intid[i]]['w_d_hookups'].decode('ascii','ignore')
        df.land[i]=newdict[df.intid[i]]['land'].decode('ascii','ignore')
        df.laundry_on_site[i]=newdict[df.intid[i]]['laundry_on_site'].decode('ascii','ignore')
        df.condo[i]=newdict[df.intid[i]]['condo'].decode('ascii','ignore')
        df.private_bath[i]=newdict[df.intid[i]]['private_bath'].decode('ascii','ignore')
        df.private_room[i]=newdict[df.intid[i]]['private_room'].decode('ascii','ignore')
        df.no_private_bath[i]=newdict[df.intid[i]]['no_private_bath'].decode('ascii','ignore')
        df.carport[i]=newdict[df.intid[i]]['carport'].decode('ascii','ignore')
        df.manufactured[i]=newdict[df.intid[i]]['manufactured'].decode('ascii','ignore')
        df.loft[i]=newdict[df.intid[i]]['loft'].decode('ascii','ignore')
        df.in_law[i]=newdict[df.intid[i]]['in_law'].decode('ascii','ignore')
        df.flat[i]=newdict[df.intid[i]]['flat'].decode('ascii','ignore')
        df.assisted_living[i]=newdict[df.intid[i]]['assisted_living'].decode('ascii','ignore')
        df.deleted[i]=newdict[df.intid[i]]['deleted'].decode('ascii','ignore')
        df.timestamp[i]=newdict[df.intid[i]]['timestamp']
        df.price[i]=newdict[df.intid[i]]['price']
        df.expires[i]=newdict[df.intid[i]]['expires'].decode('ascii','ignore')
        df.immortal[i]=newdict[df.intid[i]]['immortal'].decode('ascii','ignore')
        df.source[i]=newdict[df.intid[i]]['source'].decode('ascii','ignore')
        df.state[i]=newdict[df.intid[i]]['state'].decode('ascii','ignore')
        df.city[i]=newdict[df.intid[i]]['city'].decode('ascii','ignore')
        df.geolocation_status[i]=newdict[df.intid[i]]['geolocation_status'].decode('ascii','ignore')
        df.zipcode[i]=newdict[df.intid[i]]['zipcode'].decode('ascii','ignore')
        df.long[i]=newdict[df.intid[i]]['long']
        df.county[i]=newdict[df.intid[i]]['county'].decode('ascii','ignore')
        df.lat[i]=newdict[df.intid[i]]['lat']
        df.formatted_address[i]=newdict[df.intid[i]]['formatted_address'].decode('ascii','ignore')
        df.accuracy[i]=newdict[df.intid[i]]['accuracy']
        df.external_id[i]=int(newdict[df.intid[i]]['external_id'])
        df.external_url[i]=newdict[df.intid[i]]['external_url']
        df.language[i]=newdict[df.intid[i]]['language']
        df.currency[i]=newdict[df.intid[i]]['currency']
        df.created_at[i]=createdstr
    filename='C:\Users\User\Documents\ThreeTapsTier'+str(tiernum)+'Thresh'+str(thresh)+hourstr+'.csv'   
    df.to_csv(filename,index=False)
    print 'shove'
    #import csv, most fields aren't necessary--558 is though; represents credential id
    if newdict<>{}:
        client.csv_import(filename,'redshift-dr','house','threetaps','','','',558,'',name='3taps import',compression='none')
                                    
