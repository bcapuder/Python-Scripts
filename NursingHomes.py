# -*- coding: utf-8 -*-
"""
Created on Wed Jul 09 14:09:35 2014

@author: bcapuder

This script takes in a csv of nursing homes where data was messy and formatted where
each home was allotted one line for name, one for address1, one for citystzip
and one for phone, this script flattens the csv for reading into redshift
"""

import pandas as pd
import numpy as np
#open nursing home csv
df = pd.read_csv("C:\Users\User\Documents\Nursinghomes.csv")
#initialize dataframe
df2 = pd.DataFrame(np.zeros((15642,6)),columns=['Home','Address1','City','State','Zip','Phone'])
#counter keeps track of df2's current row
counter=0
for i in range(len(df)):
    #first row of 4, saves name to df2    
    if i%4 == 0:
        df2.Home[counter]=df.Data[i]
    #second row of 4, saves address1 to df2
    elif i%4 == 1:
        df2.Address1[counter]=df.Data[i]
    #third row of 4, saves and parses city,state,zip if there
    elif i%4 == 2:
        df2.City[counter]=df.Data[i].split(',')[0]
        if ',' in df.Data[i]:
            df2.State[counter]=df.Data[i].split(',')[1].strip().split(' ')[0]
            if ' ' in df.Data[i].split(',')[1]:
                df2.Zip[counter]=df.Data[i].split(',')[1].strip().split(' ')[1]
    #final row of 4, saves phone and increments df2 row
    else:
        df2.Phone[counter]=df.Data[i]
        counter+=1
#saves to csv
df2.to_csv("C:\Users\User\Documents\NursingHomeList.csv")
