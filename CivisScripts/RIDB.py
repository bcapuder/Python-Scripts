# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 10:19:46 2014

@author: User
"""
from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import ast
import requests
import xml.etree.ElementTree as ET

newdict={}
r=requests.get("http://ridb.recreation.gov/webservices/RIDBServiceNG.cfc?method=getAllFacilityAddresses")
tree=ET.fromstring(r.content)
for child in tree:
    outputlist=['','','','','','','','','']
    for kid in child:
        if "Address1" in str(kid.tag) and kid.text<>None:
            outputlist[0]=kid.text
        if "Address2" in str(kid.tag) and kid.text<>None:
            outputlist[1]=kid.text
        if "Address3" in str(kid.tag) and kid.text<>None:
            outputlist[2]=kid.text
        if "City" in str(kid.tag) and kid.text<>None:
            outputlist[3]=kid.text
        if "AddressStateCode" in str(kid.tag) and kid.text<>None:
            outputlist[4]=kid.text
        if "PostalCode" in str(kid.tag) and kid.text<>None:
            outputlist[5]=kid.text
        if "FacilityID" in str(kid.tag) and kid.text<>None:
            outputlist[6]=kid.text
        if "FacilityAddressType" in str(kid.tag) and kid.text<>None:
            outputlist[7]=kid.text
        if "AddressID" in str(kid.tag) and kid.text<>None:
            outputlist[8]=kid.text
    if outputlist[8]<>'':
        newdict[outputlist[8]]={"address1":outputlist[0],"address2":outputlist[1],"address3":outputlist[2],"city":outputlist[3],"state":outputlist[4],"zip5":outputlist[5],"facility_id":outputlist[6],"facility_type":outputlist[7]}
r=requests.get('http://ridb.recreation.gov/webservices/RIDBServiceNG.cfc?method=getAllRecAreaAddresses')
tree=ET.fromstring(r.content)
for child in tree:
    for kid in child:
        outputlist=['','','','','','','','','']
        if "Address1" in str(kid.tag) and kid.text<>None:
            outputlist[0]=kid.text
        if "Address2" in str(kid.tag) and kid.text<>None:
            outputlist[1]=kid.text
        if "Address3" in str(kid.tag) and kid.text<>None:
            outputlist[2]=kid.text
        if "City" in str(kid.tag) and kid.text<>None:
            outputlist[3]=kid.text
        if "AddressStateCode" in str(kid.tag) and kid.text<>None:
            outputlist[4]=kid.text
        if "PostalCode" in str(kid.tag) and kid.text<>None:
            outputlist[5]=kid.text
        if "FacilityID" in str(kid.tag) and kid.text<>None:
            outputlist[6]=kid.text
        if "FacilityAddressType" in str(kid.tag) and kid.text<>None:
            outputlist[7]=kid.text
        if "AddressID" in str(kid.tag) and kid.text<>None:
            outputlist[8]=kid.text
    if outputlist[8]<>'':
        newdict[outputlist[8]]={"address1":outputlist[0],"address2":outputlist[1],"address3":outputlist[2],"city":outputlist[3],"state":outputlist[4],"zip5":outputlist[5],"facility_id":outputlist[6],"facility_type":outputlist[7]}
df=pd.DataFrame.from_dict(newdict,'index')
