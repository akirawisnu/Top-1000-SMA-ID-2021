# -*- coding: utf-8 -*-
"""
Created on Thu May 27 09:42:20 2021
@author: Akirawisnu
"""

import pandas as pd
import os

loc = '' # fill with your folder location for saving data
os.chdir(loc)

tps_data=[]

for i in range(1,11):
    print(i)
    link ='https://top-1000-sekolah.ltmpt.ac.id/?page={}&per-page=100'.format(i)

    df0 = pd.read_html(link)[0]
    df1 = pd.read_html(link)[1]
    
    # clean the unnecessary header / column names
    df0.columns = df0.columns.get_level_values(0)
    df1.columns = df1.columns.get_level_values(0)
    
    # merge data
    df = pd.merge(df0, df1, on=['NPSN'], how="inner")
    # drop all with suffix _x as they are duplicates
    df = df[df.columns.drop(list(df.filter(regex='_x')))]
    # rename the suffix _y to no suffix
    df.columns = df.columns.str.replace(r'_y$', '')
    del df['#'] # drop this unnecessary column / variables
    
    # append them into each TPS dataframe
    tps_data.append(df)
    
tps_data = pd.concat(tps_data) # concat the appended dataframes into readable table

# clean from noises
tps_data['Sekolah'] = tps_data['Sekolah'].str.replace(' More..', '')

# export to favorite tools, Stata
tps_data = tps_data.fillna('')
tps_data = tps_data.astype(str)

# get clean string
kolom = ["Rerata", "Tertinggi", "Terendah", "Std. Deviasi"]
for i in kolom:
    print("{}".format(i))
    tps_data[i] = tps_data[i].str[:3] + '.' + tps_data[i].str[3:]

tps_data.to_stata(f'{loc}/top-1000-sekolah.ltmpt.V1.dta', version=119, write_index=False)
    
    