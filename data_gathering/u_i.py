#%%
import pandas as pd
import numpy as np
import zip_recommendation
import math
#import geopandas as gpd
#import matplotlib.pyplot as plt
#from shapely.geometry import Point
#import contextily as ctx

# little introduction :)
intro = ["Welcome to our Neighborhood matcher! \U0001F60A\U0001F3D9\n [ press enter to continue ]\n"]
intro.append("I'm sure you're excited to meet your perfect neighborhood in Chicago,")
intro.append("but first let's get to know each other a little bit better.")
intro.append("have a drink \U0001F377\U0001F378\U0001F9C3")     
intro.append("and rank the following questions using the numbers from 1(low)-5(high)")
    
for line in intro:
    print(line)
    input()

error_value = "Sorry, I didn't catch that. Did you say '1', '2', '3', '4' or '5'?"

attribute_dict = {"grocery_stores":"Question: how important is proximity to grocery stores for you? \U0001F34E \U0001F96C \U0001F35E \n",
                  "parks":"Question: how important is proximity to parks for you? \U0001F343 \U0001F31E \U0001F3C3 \n",
                  "libraries":"Question: how important is proximity to public libraries for you? \U0001F4DA \U0001F453 \U0001F3E0 \n",
                  "health_centers":"Question: how important is proximity to health centers for you? \U0001F9D1 \U0001F9E1 \U0001F3E5 \n",
                  "cta_train_stops":"Question: how important is proximity to CTA TRAIN stops for you? \U0001F687 \U0001F68D \U0001F698 \n",
                  "cta_bus_stops":"Question: how important is proximity to CTA BUS stops for you? \U0001F687 \U0001F68D \U0001F698 \n",
                  "crimes":"Question: how important is the local crime level to you? \U0001F303 \U0001F977 \U0001F4B0 \n"}

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
            print("\n" + error_value + "\n")
            continue
        if data > 5 or data < 0:
            print("\n" + error_value + "\n")
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
#get top 5 zipcodes then make class object for proerty return
property_zips = sort_df["zipcode"].tolist()[:5]

#Give information for any requested Chicago zipcode
stats_df = pd.read_csv('../data_gathering/zip_stats.csv')
available_zips = stats_df["zip_code"].tolist()
while True:
    zip_inquiry = input("Please enter a Chicago zip code for more information:")
    try:
        zip_inquiry = int(zip_inquiry)
    except:
        print("\n Sorry. Could you re-enter a numeric zip code")
    if zip_inquiry in available_zips:
        print(stats_df.loc[stats_df["zip_code"] == zip_inquiry])
        break
    else:
        print("\n We didn't recognize that as a Chicago zip code")
        continue
#%%
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