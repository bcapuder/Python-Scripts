# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 17:12:05 2014

@author: User
"""

import time
import requests
import pandas as pd
import numpy as np
newdict={}
r = requests.get('http://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key=LanrAm0zU4yN7QV64GIbp353VigkpOPWGbLY4nfo')
for station in r.json()['fuel_stations']:
    newdict[str(station['id'])]={'access_days_time': str(station['access_days_time']),'status_code':str(station['status_code']),'updated_at':str(station['updated_at']),'e85_blender_pump':str(station['e85_blender_pump']),'hy_status_link':str(station['hy_status_link']),'city':str(station['city']),'zip':str(station['zip']),'geocode_status':str(station['geocode_status']),'state':str(station['state']),'ev_network_web':str(station['ev_network_web']),'cards_accepted':str(station['cards_accepted']),'date_last_confirmed':str(station['date_last_confirmed']),'ev_dc_fast_num':str(station['ev_dc_fast_num']),'latitude':station['latitude'],'open_date':str(station['open_date']),'ng_psi':str(station['ng_psi']),'ev_other_evse':str(station['ev_other_evse']),'groups_with_access_code':str(station['groups_with_access_code']),'fuel_type_code':str(station['fuel_type_code']),'ev_level2_evse_num':str(station['ev_level2_evse_num']),'station_name':str(station['station_name']),'plusfour':str(station['plus4']),'expected_date':str(station['expected_date']),'owner_type_code':str(station['owner_type_code']),'ev_network':str(station['ev_network']),'longitude':station['longitude'],'ng_vehicle_class':str(station['ng_vehicle_class']),'ev_level1_evse_num':str(station['ev_level1_evse_num']),'ev_connector_types':str(station['ev_connector_types']),'station_phone':str(station['station_phone']),'street_address':str(station['street_address'])}
df=pd.DataFrame.from_dict(newdict,'index')
df.to_csv('C:\Users\User\Documents\Altfuel.csv')
