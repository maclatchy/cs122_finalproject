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
#census_gdf = gpd.read_file("../data_files/census_tract_boundaries.shp")
#neighbor_gdf = gpd.read_file("../data_files/Neighborhoods_2012b.shp")

# Grocery stores
grocery = pd.read_csv("../data_files/grocery_stores.csv", usecols=[6, 14, 15])
grocery.columns = grocery.columns.str.lower()
grocery.rename(columns={'zip_code': 'zip'}, inplace=True)
geometry = [Point(xy) for xy in zip(grocery.longitude, grocery.latitude)]
grocery = gpd.GeoDataFrame(grocery, crs="EPSG:4326", geometry=geometry)

# Health centers
health = gpd.read_file('../data_files/health_centers.csv')
health.columns = health.columns.str.lower().str.strip()
health[['zip']] = health.address.str.extract(r'(\d{5})')
health[['lat']] = health.address.str.split(
    '(').str.get(1).str.split(',').str.get(0)
health[['lon']] = health.address.str.split(
    '(').str.get(1).str.split(',').str.get(1).str.strip(')')
to_drop = ['facility', 'address', 'phone',
           'fqhc, look-alike, or neither; special notes']
health.drop(columns=to_drop, inplace=True)
health.zip = health.zip.astype(int)
health.lat = health.lat.astype(float)
health.lon = health.lon.astype(float)
health.geometry = [Point(xy) for xy in zip(health.lon, health.lat)]
health.crs = 'EPSG:4326'
# Not in Chicago
health = health.drop([41])

# Libraries
library = gpd.read_file('../data_files/library.csv')
library.columns = library.columns.str.lower().str.strip()
library[['lat', 'lon']] = library.location.str.split(expand=True)
library.lat = library.lat.str.strip('(').str.strip(',')
library.lon = library.lon.str.strip(')')
to_drop = ['hours of operation', 'phone', 'website',
           'location', 'city', 'state', 'name']
library.drop(columns=to_drop, inplace=True)
library.lat = library.lat.astype('float')
library.lon = library.lon.astype('float')
library.zip = library.zip.astype('int')
library.geometry = [Point(xy) for xy in zip(library.lon, library.lat)]
library.crs = 'EPSG:4326'

# Parks
parks = gpd.read_file('../data_files/new_parks.csv')
parks.columns = parks.columns.str.lower().str.strip()
parks.rename(columns={'zipcode': 'zip', 'lattitude': 'lat',
                      'longitude': 'lon'}, inplace=True)
parks.lat = parks.lat.astype('float')
parks.lon = parks.lon.astype('float')
parks.zip = parks.zip.astype('int')
parks.geometry = [Point(xy) for xy in zip(parks.lon, parks.lat)]
parks.crs = 'EPSG:4326'
# Wrong zip codes
parks = parks.drop([1451, 372])

# Schools
schools = pd.read_csv('../data_files/CPS.csv', usecols=[16, 19, 67, 68])
schools.columns = schools.columns.str.lower().str.strip()
schools.rename(columns={'school_latitude': 'lat',
                        'school_longitude': 'lon'}, inplace=True)
schools.lat = schools.lat.astype('float')
schools.lon = schools.lon.astype('float')
schools.zip = schools.zip.astype('int')
geometry = [Point(xy) for xy in zip(schools.lon, schools.lat)]
schools = gpd.GeoDataFrame(schools, crs='EPSG:4326', geometry=geometry)

# CTA rail stations
cta_rail = gpd.read_file('../data_files/CTA_RailStations.shp')
cta_rail_zip = pd.read_csv('../data_files/cta_railstation_zips.csv')
cta_rail = pd.concat([cta_rail, cta_rail_zip], axis=1)
cta_rail.columns = cta_rail.columns.str.lower().str.strip()
cta_rail.rename(columns={'zipcode': 'zip'}, inplace=True)
to_drop = ['station_id', 'longname', 'ada', 'pknrd', 'gtfs',
           'point_x', 'point_y']
cta_rail.drop(columns=to_drop, inplace=True)
cta_rail = cta_rail.to_crs('EPSG:4326')
cta_rail

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
cta_bus


def community_profile_map(zip_code):
    '''
    Input:
      zip (int): ZIP code

    Output:
      Map of zip code with library locations
    '''
    ax0 = library.loc[library.zip==zip_code].plot(color='green',
                                                  figsize=(10, 10))
    ax1 = health.loc[health.zip==zip_code].plot(ax=ax0,
                                                color='red',
                                                figsize=(10, 10))
    ax2 = grocery.loc[grocery.zip==zip_code].plot(ax=ax1,
                                                  color='blue',
                                                  figsize=(10, 10))
    ax3 = parks.loc[parks.zip==zip_code].plot(ax=ax2,
                                              color='blue',
                                              figsize=(10, 10))
    ax4 = schools.loc[schools.zip==zip_code].plot(ax=ax3,
                                                  color='yellow',
                                                  figsize=(10, 10))
    final_ax = zip_gdf.loc[zip_gdf.zip==zip_code].boundary.plot(ax=ax4,
                                                                color='black',
                                                                figsize=(10, 10))
    ctx.add_basemap(final_ax, crs=zip_gdf.crs.to_string())
    return

community_profile_map(60615)