import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

# Load base layers
zip_gdf = gpd.read_file("/data_file/chicago_zip_tracts.shp")
zip_gdf.zip = zip_gdf.zip.astype(int)
census_gdf = gpd.read_file("/data_file/census_tract_boundaries.shp")
neighbor_gdf = gpd.read_file("/data_files/Neighborhoods_2012b.shp")


# Load and clean grocery data
grocery = pd.read_csv("/Users/seanmaclatchy/Desktop/CS122/project/grocery_stores.csv")
grocery.columns = grocery.columns.str.lower()
grocery.rename(columns = {'zip code':'zip'}, inplace = True) 
geometry = [Point(xy) for xy in zip(grocery.longitude, grocery.latitude)]
grocery = grocery.drop(['longitude', 'latitude'], axis=1)
grocery_gdf = gpd.GeoDataFrame(grocery, crs="EPSG:4326", geometry=geometry)

# Load and clean health center data
health = pd.read_csv('https://data.cityofchicago.org/resource/cjg8-dbka.csv')
health = health.reset_index()
health[['zip']] = health.location_1.str.extract(r'(\d{5})')
health.zip = health.zip.astype(int)
health[['lat']] = health.location_1.str.split('(').str.get(1).str.split(',').str.get(0)
health.lat = health.lat.astype(float)
health[['lon']] = health.location_1.str.split('(').str.get(1).str.split(',').str.get(1).str.strip(')')
health.lon = health.lon.astype(float)
geometry = [Point(xy) for xy in zip(health.lon, health.lat)]
health = health.drop(['lon', 'lat'], axis=1)
health_gdf = gpd.GeoDataFrame(health, crs="EPSG:4326", geometry=geometry)

# Load and clean library data
libraries = pd.read_csv("/Users/seanmaclatchy/Desktop/CS122/project/library.csv")
libraries.columns= libraries.columns.str.lower()
libraries[['lat', 'lon']] = libraries.location.str.split(expand=True)
libraries.lat = libraries.lat.str.strip('(').str.strip(',')
libraries.lon = libraries.lon.str.strip(')')
libraries.lat = libraries.lat.astype('float')
libraries.lon = libraries.lon.astype('float')
libraries.zip = libraries.zip.astype('int')
geometry = [Point(xy) for xy in zip(libraries.lon, libraries.lat)]
libraries = libraries.drop(['lon', 'lat'], axis=1)
lib_gdf = gpd.GeoDataFrame(libraries, crs="EPSG:4326", geometry=geometry)

# Get zip and points function
def get_zip_lib(zip_code):
    '''
    Input:
      zip (int): ZIP code

    Output:
      Map of zip code with library locations
    '''
    fig, ax = plt.subplots(figsize=(10, 10))
    lib_gdf.loc[lib_gdf.zip == zip_code].plot(ax=ax, color='red')
    zip_gdf.loc[zip_gdf.zip == zip_code].geometry.boundary.plot(ax=ax, color='black')
    health_gdf.loc[health_gdf.zip == zip_code].plot(ax=ax, color='blue')
    grocery_gdf.loc[grocery_gdf.zip == zip_code].plot(ax=ax, color='green')
    plt.show()
    return

get_zip_lib(60615)

