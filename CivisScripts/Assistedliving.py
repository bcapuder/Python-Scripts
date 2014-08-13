# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 17:37:04 2014

@author: User
"""

from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

webpage = urlopen("http://www.assistedlivingfacilities.org/directory/")
progress = 0
stateList = []
cityList = []
homesList = []
addressList = []
citystzipList = []
phoneList = []
soup = BeautifulSoup(webpage)
tableSoup = soup.find('table',{'align':'center'})
links = tableSoup.findAll('a')
print len(links)
for link in links:
    if 'wy' not in str(link):
        stateList.append(link['href'])

for state in stateList:
    webpage = urlopen("http://www.assistedlivingfacilities.org"+state)
    soup = BeautifulSoup(webpage)
    tableSoup = soup.findAll('table',{'align':'center'})
    links = tableSoup[1].findAll('a')
    for link in links:
        cityList.append(link['href'])
for city in cityList:
    print progress
    webpage = urlopen("http://www.assistedlivingfacilities.org"+city)
    soup = BeautifulSoup(webpage)
    tableSoup = soup.find('table',{'class':'lined'})
    tr = tableSoup.findAll('tr')
    for element in tr:
        td = element.findAll('td')
        if len(td) == 4 and td[0].text<>'Name' and td[0].text not in homesList:
            homesList.append(td[0].text)
            counter = 0
            for string in str(td[1]).split('<br/>'):
                if counter == 0:
                    addressList.append(string.replace('<td>','').replace('</td>',''))
                if counter == 1:
                    citystzipList.append(string.replace('<td>','').replace('</td>',''))
                counter +=1
            phoneList.append(td[2].text.split(':')[2].strip())
np.zeros((len(homesList),6))
df = pd.DataFrame(np.zeros((len(homesList),6)),columns=['Home','Address1','City','State','Zip','Phone'])
for i in range(len(homesList)):
    df.Home[i]=homesList[i]
    df.Address1[i]=addressList[i]
    df.City[i]=citystzipList[i].split(',')[0]
    if ',' in citystzipList[i]:
        df.State[i]=citystzipList[i].split(',')[1].strip().split(' ')[0]
        if ' ' in citystzipList[i].split(',')[1].strip():
            df.Zip[i]=citystzipList[i].split(',')[1].strip().split(' ')[1]
    df.Phone[i]=phoneList[i]
df.to_csv("C:\Users\User\Documents\Assistedlivinglist.csv")
