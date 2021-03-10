#%%
import pandas as pd
import numpy as np
import zip_recommendation
import math
'''
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
'''

#%%
# User interface
print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
      "\nWelcome to the Spike-Protein's final project!\n")
print("\nOur goal is to help you find the ideal Chicago zipcode for you"
      "\nto live!\n")
print("\nPlease input a whole number ranged [0, 5] for all prompts, with 0"
      "\nbeing the least important and 5 being the most important.\n"
      "\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

attribute_dict = {"grocery_stores":"Question: how important is proximity to grocery stores for you? \n",
                  "parks":"Question: how important is proximity to parks for you? \n",
                  "libraries":"Question: how important is proximity to public libraries for you? \n",
                  "health_centers":"Question: how important is proximity to health centers for you? \n",
                  "cta_train_stops":"Question: how important is proximity to CTA TRAIN stops for you? \n",
                  "cta_bus_stops":"Question: how important is proximity to CTA BUS stops for you? \n",
                  "crimes":"Question: how important is the local crime level to you? \n"}

preference_dict = dict()

def get_score(attribute):
    '''
    Takes user inputs and builds a socre dictionary

    Input:
      attribute (str): key in attribute dictionary
    '''
    question = attribute_dict[attribute]
    while True:
        data = input(question)
        try:
            data = int(data)
        except:
            print("\nYou did not enter a valid whole number.\n")
            continue
        if data > 5 or data < 0:
            print("\nThe number you entered was not in the range [0, 5].\n")
            continue
        else:
            preference_dict[('z_' + attribute)] = data
            break
    print('\nThank you!\n')
    return

# Get preferences and display zipcodes
for key in attribute_dict.keys():
    get_score(key)
sort_df = zip_recommendation.get_sorted_weights(preference_dict)
print("\nThese zip codes match your entries the best:")
print(sort_df.head(5))
print('')
'''
# zip conversion
life_exp = pd.read_csv('../data_files/il_life_expectancy.csv', usecols=[0,2,3,4])
life_exp.columns = life_exp.columns.str.lower().str.strip()
to_drop = life_exp.loc[life_exp.cnty2kx != 31]
life_exp.drop(to_drop.index, inplace=True)

zip_census_conv = pd.read_csv('../data_files/zip_census_convert.csv')
zip_census_conv.columns = zip_census_conv.columns.str.lower().str.strip()
zip_census_conv.drop(columns=['bus_ratio', 'oth_ratio', 'tot_ratio'], inplace=True)

income = pd.read_csv('../data_files/med_income.csv')
income.columns = income.columns.str.lower().str.strip()

tup_lst = list()
for index, row in income.iterrows():
    i = (zip_census_conv.loc[zip_census_conv.zip == row.zip_code])
    best = i.res_ratio.max()
    best_row = i.loc[i.res_ratio == best]
    zip_code = (best_row.zip.values).tolist()
    tract = (best_row.tract.values).tolist()
    if zip_code and tract:
        tup = zip_code[0], tract[0]
        tup_lst.append(tup)

zip_census_master = pd.DataFrame(tup_lst, columns=['zip', 'tract_id'])

schools = pd.read_csv('../data_files/CPS.csv', usecols=[19, 67, 68])

#missing zip codes in income but not census
missing_zip = [60680,60691,60664]
zips = list(map(int,income["zip_code"]))
columns = ["zip_code","med_inc","lif_ex","schools"]
tl = []
for z in zips:
    mi = income.loc[income["zip_code"] == z].values[0]
    if(math.isnan(mi[0])):
        mi = "NA"
    else:
        mi = int(mi[0])
    if(z in missing_zip):
        le = "NA"
    else:
        tract = zip_census_master.loc[zip_census_master["zip"] == z].values[0]
        tract = tract[1]
        if(life_exp.loc[life_exp["tract_id"] == tract].empty):
            le = "NA"
        else:
            le = life_exp.loc[life_exp["tract_id"] == tract].values[0]
            le = le[3]
    num_s = len(schools[schools["Zip"] == z])
    data = (z,mi,le,num_s)
    tl.append(data)
zip_information = pd.DataFrame(tl, columns=columns)
'''
