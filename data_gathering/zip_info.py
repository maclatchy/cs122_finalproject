#%%
import pandas as pd
import numpy as np
import zip_recommendation
import math

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
#%%
