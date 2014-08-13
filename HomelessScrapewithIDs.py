# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 14:26:14 2014

@author: bcapuder

This script takes in a csv with a list of ids and their respective urls and
iterates through each one and grabs the phone number, name and city,state,zip
info from their respective webpages and stores the info in a csv
"""

from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
#read in csv with urls,ids
df = pd.read_csv("C:\Users\User\Documents\citieshomelessforpy.csv")
#initialize outputdict
outputDict = {}
#loop through dataframe
for i in range(len(df)):
    #open url
    webpage = urlopen(df.URL[i]).read()
    #create beautiful soup from webpage
    soup = BeautifulSoup(webpage)
    #find phone number by finding element with tag span and itemprop=telephone
    phoneSoup = soup.find('span', {'itemprop' : 'telephone'})
    #find name by finding element with tag span and itemprop=name
    nameSoup = soup.find('span',{'itemprop':'name'})
    #find location by finding element with tag span and itemprop=location
    locationSoup = soup.find('span',{'itemprop':'location'})
    #save info into outputdict indexed by id from df
    outputDict[str(df.ID[i])]={'name':str(nameSoup).replace('<span itemprop="name">','').replace('</span>',''), 'phone':str(phoneSoup).replace('<span itemprop="telephone">','').replace('</span>',''),'location':(str(soup)[str(soup).find('location">')+10:str(soup).find('<br/',str(soup).find('location">'))]).replace('</span>','')}
#create dataframe from the dictionary
df2=pd.DataFrame.from_dict(outputDict,'index')
#save to csv
df2.to_csv('C:\Users\User\Documents\Homelessinfo.csv')
