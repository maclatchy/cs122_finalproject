#%%
import numpy as np
import pandas as pd
import requests
import json
import csv
from bs4 import BeautifulSoup as bs4
import re
import string
import csv
import time
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from shapely.geometry import Point
import contextily as ctx
#%%

def get_chi_zips():
    '''
    Produce a list of all zipcodes in the City of Chicago
    '''
    url = "http://www.ciclt.net/sn/clt/capitolimpact/gw_ziplist.aspx?ClientCode=capitolimpact&State=IL&StName=Illinois&StFIPS=17&CityKey=1714000"
    chicago_zips = requests.get(url)
    chicago_zip_txt = chicago_zips.text
    soup = bs4(chicago_zip_txt, "html.parser")
    zip_code_soup = soup.find_all("a", href = re.compile(r"^/sn/clt/capitolimpact/gw_zipdet"))
    all_chi_zips = []
    for zip_code in zip_code_soup:
        zip_code = zip_code.contents
        all_chi_zips.append(zip_code[0])
    return all_chi_zips

all_chi_zips = get_chi_zips()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"}
first_half_zips = all_chi_zips[0:34]
second_half_zips = all_chi_zips[34:69]
def get_csv_links(all_chi_zips):
    '''
    Get the links to download Redfin property listings
    as a .csv file for each Chicago zip code
    '''
    zip_base_url = "https://www.redfin.com/zipcode/"
    link_list = []
    csv_links =[]
    for zipcode in all_chi_zips:
        link = zip_base_url + str(zipcode)
        link_list.append(link)
    for i, link in enumerate(link_list):
        print(i)
        homes = requests.get(link, headers=headers)
        homes_txt = homes.text
        soup = bs4(homes_txt, "html.parser")
        home_soup = soup.find("a", id="download-and-save")
        if home_soup:
            csv_link = home_soup["href"]
            print(csv_link)
            csv_links.append(csv_link)
        time.sleep(10)
    return csv_links


link_df = pd.read_csv("redfin_links.csv")
def create_homelisting_tbl(link_df):
    '''
    Create a .csv file "all_listings.csv" that contains
    up to the top 300 Redfin property listings in each
    Chicago zip code
    '''
    all_listings = False
    for (colname, coldata) in link_df.iteritems():
        for i, link in enumerate(coldata):
            url = "https://www.redfin.com" + link
            f = requests.get(url, headers=headers).content
            csv_name = "redfin_" + str(i) + ".csv"
            csv_file = open(csv_name, "wb")
            csv_file.write(f)
            csv_file.close()
            df = pd.read_csv(csv_name)
            if all_listings:
                df.to_csv("all_listings.csv", mode = "a", index=False, header=False)
            else:
                df.to_csv("all_listings.csv", index=False)
                all_listings = True      
    return 

'''
# Cleaning redfin data
og_redfin = pd.read_csv("all_listings.csv")
redfin = pd.read_csv("all_listings.csv", usecols=[2, 3, 6, 7, 8, 
                                                  9, 10, 11, 25, 26])
redfin.columns = redfin.columns.str.lower()
redfin.rename(columns={'zip or postal code':'zip', 'property type':'p_type', 
                        'square feet':'sq_feet'}, inplace=True)
to_drop = redfin.loc[(redfin.p_type == 'Parking') | (redfin.p_type == 'Vacant Lot') | (redfin.p_type == 'Vacant Land')
                        | (redfin.address == "nan")]
redfin.drop(to_drop.index, inplace=True)
redfin.address = redfin.address.str.lower()
duplicates = redfin[redfin.duplicated()]
redfin.drop(duplicates.index, inplace=True)
redfin.address = redfin.address.str.title()
'''
#%%
class PropertyMatch:

    def __init__(self, zip_codes):
        self.zip_codes = zip_codes
        self.price_dict = {1:"least expensive", 2:"below average", 3:"average",
                        4:"more expensive", 5:"most expensive"}

    def property_matches(self, price, beds):
        '''
        Output a string list of the top two property matches
        in each top-match zipcode.
        
        Inputs:
        price (int): int. 1-5 representing relative housing cost
        among the houses in the top-match zip codes. 1-least expensive, 
        2-below average, 3-average, 4-expensive, 5-most expensive
        beds (int): number of desired beds, minimum 1 and maximum 5

        Outputs:
        string (str): string that has the property type, address, 
        zipcode, price, number of bathrooms, community location, and 
        square feet for each matched property
        '''
        top_matches = []
        sub_beds = self.all_property_matches(price, beds)
        price = self.price_dict[price]            
        for z in self.zip_codes:
            df = sub_beds.loc[sub_beds.zip == z]
            df = df.iloc[:2,[0,1,2,3,5,6,7]].copy()
            d = df.to_dict("index")
            top_matches.append(d)
        whole_s = ""
        string = ""
        n = 1
        for p in top_matches:
            s = ""
            for _, val in p.items():
                if whole_s != "":
                    whole_s = whole_s + "\n" 
                whole_s = str(n) + ". "
                for k, v in val.items():
                    s = str(k).title() + ": " + str(v) + ", " 
                    whole_s = whole_s + s
                whole_s = whole_s[:-2]
                string = string + whole_s + "\n" + "\n"
                n +=1
        if string == "":
            string = "No homes with {} bedroom(s) are within your price range.".format(beds)   
        return string 


    def all_property_matches(self, price, beds):
        '''
        Creates a pandas DataFrame with all property matches 
        given a person's price range and the number of beds desired

        Inputs:
        price (int): int. 1-5 representing relative housing cost
        among the houses in the top-match zip codes. 1-least expensive, 
        2-below average, 3-average, 4-expensive, 5-most expensive
        beds (int): number of desired beds, minimum 1 and maximum 5

        Outputs:
        sub_beds (DataFrame): pandas DataFrame containing 
        the property matches for the user's given inputs
        '''
        redfin = pd.read_csv("redfin_clean.csv")
        price = self.price_dict[price]
        sub = redfin[redfin["zip"].isin(self.zip_codes)].copy()
        sub = sub.loc[(sub.beds == beds)].copy()
        sub["quantile"] = pd.qcut(sub["price"], q = 5, precision = 0)
        bin_labels = ["most expensive", "expensive", "average", "below average", "least expensive"]
        sub['price_category'] = pd.qcut(sub['price'],
                              q=[0, .2, .4, .6, .8, 1],
                              labels=bin_labels)
        sub_price = sub.loc[sub.price_category == price].copy()
        sub_beds = sub_price.loc[sub.beds == beds]
        sub_beds = sub_beds.reset_index(drop=True)
        return sub_beds
    
    def get_prop_geom(self, price, beds):
        '''
        Creates a GeoDataFrame of the property matches
        that fall into the user's price range and meet the
        number of beds requirement. 

        Inputs:
        price (int): int. 1-5 representing relative housing cost
        among the houses in the top-match zip codes. 1-least expensive, 
        2-below average, 3-average, 4-expensive, 5-most expensive
        beds (int): number of desired beds, minimum 1 and maximum 5

        Outputs:
        properties (GeoDataFrame): contains the property matches 
        and a geometry column for each listing
        '''
        sub = self.all_property_matches(price, beds)
        geometry = [Point(xy) for xy in zip(sub["latitude"], sub["longitude"])]
        properties = gpd.GeoDataFrame(sub, crs = "EPSG:4326", geometry = geometry)
        properties = properties.dropna()
        return properties
'''
# Mapping Addresses (unfinished)
# ["address", "zip", "price", "baths", "location", "sq_feet"]
# Mapping
# Load base layers
props = PropertyMatch([60615, 60637])
sub = props.property_matches("hi")
zip_gdf = gpd.read_file("../data_files/chicago_zip_tracts.shp")
zip_gdf.zip = zip_gdf.zip.astype(int)
zip_gdf = zip_gdf.drop(['objectid'], axis=1)
zip_gdf = zip_gdf.dropna()
#crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(sub["latitude"], sub["longitude"])]
properties = gpd.GeoDataFrame(sub, crs = "EPSG:4326", geometry = geometry)
properties = properties.dropna()
ax = properties.loc[properties.zip == 60615].plot( color = "red", figsize = (20,20))
#ax = properties[properties["zip"].isin(self.zips)].plot(ax = ax, color = "red", figsize = (20,20))
#ax0 = zip_gdf.loc[zip_gdf.zip == 60615].geometry.boundary.plot(ax = ax, color = "black", figsize = (20,20))
ctx.add_basemap(ax, crs=zip_gdf.crs.to_string())
plt.show()
'''




# %%
