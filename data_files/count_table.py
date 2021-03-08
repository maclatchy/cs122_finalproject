## Written by Emma Chancellor Dyer


import pandas as pd 
import numpy as np 
import requests
from bs4 import BeautifulSoup as bs4
import re
import geopandas as geopd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx 
import geocoder
import sodapy


# Find all Chicago zip codes
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

zips = get_chi_zips()

# Find health center zip codes
def get_hc_zips():
    '''
    Finds the zipcode inside the Address string
    of the health_centers dataset and creates a 
    new DataFrame containing just zipcodes as integers
    rather than strings. 
    Output:
    hc_zip_df (DataFrame): pandas DataFrame containing the zipcodes
    of each health center in the City of Chicago
    '''
    health_centers = pd.read_csv("health_centers.csv")
    hc_address = health_centers["Address"]
    hc_zips = []
    for _, address in hc_address.iteritems():
        first = re.search(r"\d+", address[-50:])
        if first:
            first = first.group(0)
            hc_zips.append(first)
    for i, z in enumerate(hc_zips):
        if z == "60060644":
            hc_zips[i] = "60644"
        if z == "10660616":
            hc_zips[i] = "60616"
        if z == "26":
            hc_zips[i] = "60626"
        if z == "118":
            hc_zips[i] = "60118"
    int_zips = []
    for z in hc_zips:
        z = int(z)
        int_zips.append(z)
    hc_zip_df = pd.DataFrame({"zipcode": int_zips})
    return hc_zip_df


# Find zip codes for CTA Rail stops
def create_ctarail_zip_df():
    '''
    Finds the lattitude and longitude of CTA rail stations
    using the MapQuest API. Processes addresses without
    postal codes to find lat/lon, then reverse geocodes
    the lat/lon to find the postal code. 
    
    Output:
    zip_df (DataFrame): pandas DataFrame containing 
    zipcode of rail stations in the the order that
    stations appear in  CTA_RailStations.shp 
    '''
    cta_rail = geopd.read_file("CTA_RailStations.shp")
    ad = cta_rail["ADDRESS"]
    ad = ad + " Chicago, IL"
    lat_lst = []
    lon_lst = []
    zip_lst = []
    for i in range(len(ad)):
        print("Get lat/lon:", i)
        g = geocoder.mapquest(ad.iloc[i], key = "mmcN5Afp3QejG7fOZ0ljDyhrneaqeazD")
        lat_lst.append(g.lat)
        lon_lst.append(g.lng)
    for i in range(len(lon_lst)):
        print("Get Address:", i)
        g = geocoder.mapquest([lat_lst[i], lon_lst[i]], method = 'reverse', key = "mmcN5Afp3QejG7fOZ0ljDyhrneaqeazD")
        postal = g.postal
        zip_lst.append(postal)
    zip_df = pd.DataFrame({"zipcode" : zip_lst})
    return zip_df


# Find zip codes for CTA bus stops
def create_ctabus_zip_df():
    '''
    Finds the zipcode for each CTA bus stop using the 
    lattitude and longitude values provided by the CTA_BusStops.shp.
    Uses the MapQuest API to reverse geocode the lat/lon coordinates
    and obtain the zipcode. 

    Note: This will take about 30+ minutes to run. There are 10,846
    CTA bus stops. 
    '''
    cta_bus = geopd.read_file("CTA_BusStops.shp")
    lat = cta_bus["POINT_Y"]
    lon = cta_bus["POINT_X"]
    bus_zip_lst = []
    for i in range(len(lat)):
        print("Finding Zipcode:", i)
        g = geocoder.mapquest([lat.iloc[i], lon.iloc[i]], method = 'reverse', key = "mmcN5Afp3QejG7fOZ0ljDyhrneaqeazD")
        postal = g.postal
        bus_zip_lst.append(postal)
    clean_bus_zips = []
    for z in bus_zip_lst:
        if z:
            z = z[:5]
            clean_bus_zips.append(z)
    zip_df = pd.DataFrame({"zipcode": clean_bus_zips})
    return zip_df

# Get crime data and find the zip code the crime was committed
def create_crime_zip_df():
    '''
    Get latitude and longitude from crime data with Chicago Data 
    Portal API and use MapQuest geocoder API to reverse geocode and
    find the zip code each crime was commited. 
    
    Output:
    zip_df (DataFrame): pandas DataFrame containing zipcodes for crimes committed in Chicago
    in 2015 to present (8 March 2021).
    '''
    crime_j = requests.get("https://data.cityofchicago.org/resource/ijzp-q8t2.json?$where=year > 2015")
    crime = crime_j.json()
    all_latlon_lst = []
    for c in crime:
        lat_lon = []
        for key, value in c.items():
            if key == "latitude":
                lat = value
                lat_lon.append(lat)
            if key == "longitude":
                lon = value
                lat_lon.append(lon)
        if len(lat_lon) == 2:
            all_latlon_lst.append(lat_lon)
    crime_zips = []
    for i in all_latlon_lst:
        print("Finding Crime Zipcode:", i)
        g = geocoder.mapquest([i[0], i[1]], method = 'reverse', key = "mmcN5Afp3QejG7fOZ0ljDyhrneaqeazD")
        z = g.postal
        z = z[:5]
        crime_zips.append(z)
    zip_df = pd.DataFrame({"zipcode": crime_zips})
    return zip_df


# ALL DATA FRAMES
grocery_stores = pd.read_csv("grocery_stores.csv") #zip_code col_name
parks = pd.read_csv("new_parks.csv") # zipcode col_name
libraries = pd.read_csv("library.csv") # ZIP col_name
health_centers = get_hc_zips() # zipcode col_name
rail_zips = pd.read_csv("cta_railstation_zips.csv") # zipcode col_name
bus_zips = pd.read_csv("cta_bus_zips.csv") # zipcode col_name
crime_zips = pd.read_csv("2015topresent_crime_zips.csv") # zipcode col_name


def get_counts():
    '''
    Takes pandas DataFrames containing the zip codes for the location of 
    every grocery store, park, library, health center, CTA train stop,
    CTA bus stop, and crime committed between 2015 and March 2021 and 
    produces a DataFrame with the counts of each variable in each zip code. 
    '''
    grocery_count_lst = []
    park_count_lst = []
    library_count_lst = []
    health_center_count_lst = []
    cta_rail_count_lst = []
    cta_bus_count_lst = []
    crime_count_lst = []
    zips = get_chi_zips()
    for z in zips:
        # Grocery Store Counts
        grocery_count = grocery_stores.query("zip_code == {}".format(z)).zip_code.count()
        grocery_count_lst.append(grocery_count)
        # Park Counts
        park_count = parks.query("zipcode == {}".format(z)).zipcode.count()
        park_count_lst.append(park_count)
        # Library Counts
        library_count = libraries.query("ZIP == {}".format(z)).ZIP.count()
        library_count_lst.append(library_count)
        # Health Center Counts
        health_center_count = health_centers.query("zipcode == {}".format(z)).zipcode.count()
        health_center_count_lst.append(health_center_count)
        # CTA Train Stop Counts
        cta_rail_count = rail_zips.query("zipcode == {}".format(z)).zipcode.count()
        cta_rail_count_lst.append(cta_rail_count)
        # CTA Bus Stop Counts
        cta_bus_count = bus_zips.query("zipcode == {}".format(z)).zipcode.count()
        cta_bus_count_lst.append(cta_bus_count)
        # Crime Counts
        crime_count = crime_zips.query("zipcode == {}".format(z)).zipcode.count()
        crime_count_lst.append(crime_count)
    count_df = pd.DataFrame({"zipcode": zips,
                            "grocery_stores": grocery_count_lst,
                            "parks": park_count_lst,
                            "libraries": library_count_lst,
                            "health_centers": health_center_count_lst,
                            "cta_train_stops": cta_rail_count_lst,
                            "cta_bus_stops": cta_bus_count_lst,
                            "crimes": crime_count_lst})
    return count_df