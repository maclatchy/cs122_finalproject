import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

# Load base layers
zip_gdf = gpd.read_file("../data_files/chicago_zip_tracts.shp")
zip_gdf.zip = zip_gdf.zip.astype(int)
zip_gdf = zip_gdf.drop(['objectid'], axis=1)
zip_gdf = zip_gdf.dropna()

# Grocery stores
grocery = pd.read_csv('../data_files/grocery_stores.csv', usecols=[6, 10, 14, 15])
grocery.columns = grocery.columns.str.lower()
grocery.rename(columns = {'zip_code':'zip'}, inplace = True) 
geometry = [Point(xy) for xy in zip(grocery.longitude, grocery.latitude)]
grocery = gpd.GeoDataFrame(grocery, crs="EPSG:4326", geometry=geometry)
grocery = grocery.dropna()

# Health centers
health = pd.read_csv('../data_files/health_centers.csv', usecols=[1,4])
health.columns = health.columns.str.lower().str.strip()
health[['zip']] = health.address.str.extract(r'(\d{5})')
health[['lat']] = health.address.str.split('(').str.get(1).str.split(',').str.get(0)
health[['lon']] = health.address.str.split('(').str.get(1).str.split(',').str.get(1).str.strip(')')
health.drop(columns=['address'], inplace=True)
health.zip = health.zip.astype(int)
health.lat = health.lat.astype(float)
health.lon = health.lon.astype(float)
geometry = [Point(xy) for xy in zip(health.lon, health.lat)]
health = gpd.GeoDataFrame(health, crs="EPSG:4326", geometry=geometry)
health = health.dropna()
# Not in Chicago
health = health.drop([41])

# Libraries
library = pd.read_csv('../data_files/library.csv', usecols=[5,8])
library.columns = library.columns.str.lower().str.strip()
library[['lat', 'lon']] = library.location.str.split(expand=True)
library.lat = library.lat.str.strip('(').str.strip(',')
library.lon = library.lon.str.strip(')')
library.lat = library.lat.astype('float')
library.lon = library.lon.astype('float')
library.zip = library.zip.astype('int')
geometry = [Point(xy) for xy in zip(library.lon, library.lat)]
library = gpd.GeoDataFrame(library, crs="EPSG:4326", geometry=geometry)
library= library.dropna()

# Parks
parks = pd.read_csv('../data_files/new_parks.csv', usecols=[1,2,3])
parks.columns = parks.columns.str.lower().str.strip()
parks.rename(columns={'zipcode': 'zip', 'lattitude': 'lat',
                      'longitude': 'lon'}, inplace=True)
parks.lat = parks.lat.astype('float')
parks.lon = parks.lon.astype('float')
parks.zip = parks.zip.astype('int')
geometry = [Point(xy) for xy in zip(parks.lon, parks.lat)]
parks = gpd.GeoDataFrame(parks, crs="EPSG:4326", geometry=geometry)
parks.drop(columns=['lat', 'lon'], inplace=True)
# Wrong zip codes
parks = parks.drop([185, 372, 1451])
parks = parks.dropna()


# Schools
schools = pd.read_csv('../data_files/CPS.csv', usecols=[19, 67, 68])
schools.columns = schools.columns.str.lower().str.strip()
schools.rename(columns={'school_latitude': 'lat',
                        'school_longitude': 'lon'}, inplace=True)
schools.lat = schools.lat.astype('float')
schools.lon = schools.lon.astype('float')
schools.zip = schools.zip.astype('int')
geometry = [Point(xy) for xy in zip(schools.lon, schools.lat)]
schools.drop(columns=['lat', 'lon'], inplace=True)
schools = gpd.GeoDataFrame(schools, crs='EPSG:4326', geometry=geometry)
schools = schools.dropna()

# CTA rail stations
cta_rail = gpd.read_file('../data_files/CTA_RailStations.shp')
cta_rail_zip = pd.read_csv('../data_files/cta_railstation_zips.csv')
cta_rail = pd.concat([cta_rail, cta_rail_zip], axis=1)
cta_rail.columns = cta_rail.columns.str.lower().str.strip()
cta_rail.rename(columns={'zipcode': 'zip'}, inplace=True)
to_drop = ['station_id', 'longname', 'ada', 'pknrd', 'gtfs',
           'point_x', 'point_y', 'address']
cta_rail.drop(columns=to_drop, inplace=True)
cta_rail = cta_rail.to_crs('EPSG:4326')
cta_rail = cta_rail.dropna()

# CTA bus stops
cta_bus = gpd.read_file('../data_files/CTA_BusStops.shp')
cta_bus_zip = pd.read_csv('../data_files/cta_bus_zips.csv')
cta_bus = pd.concat([cta_bus, cta_bus_zip], axis=1)
cta_bus.columns = cta_bus.columns.str.lower().str.strip()
cta_bus.rename(columns={'zipcode': 'zip'}, inplace=True)
cta_bus = cta_bus.loc[cta_bus.city == 'CHICAGO']
to_drop = ['systemstop', 'objectid', 'street', 'cross_st', 'point_x',
           'point_y', 'owlroutes', 'city', 'status', 'public_nam', 'dir',
           'routesstpg', 'pos']
cta_bus.drop(columns=to_drop, inplace=True)
cta_bus = cta_bus.dropna()


def community_profile_map(zip_code):
    '''
    Input:
      zip (int): ZIP code

    Output:
      Map of zip code with locations
    '''
    ax = library.loc[library.zip == zip_code].plot(color='green', figsize=(20, 20))
    ax1 = health.loc[health.zip == zip_code].plot(ax=ax, color='red', figsize=(20, 20))
    ax2 = grocery.loc[grocery.zip == zip_code].plot(ax=ax1, color='blue', figsize=(20, 20))
    ax3 = parks.loc[parks.zip == zip_code].plot(ax=ax2, color='orange', figsize=(20, 20))
    ax4 = schools.loc[schools.zip == zip_code].plot(ax=ax3, color = 'yellow', figsize=(20, 20))
    #ax5 = cta_rail.loc[cta_rail.zip == zip_code].plot(ax=ax4, color = 'brown', figsize=(20, 20))
    final = zip_gdf.loc[zip_gdf.zip == zip_code].boundary.plot(ax=ax4, color= 'black', figsize=(20, 20))
    ctx.add_basemap(final, crs=zip_gdf.crs.to_string())
    plt.show()
    return

community_profile_map(60615)