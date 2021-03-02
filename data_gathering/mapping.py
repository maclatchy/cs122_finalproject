import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx

# Load base layers
zip_gdf = gpd.read_file("/data_files/chicago_zip_tracts.shp")
zip_gdf.zip = zip_gdf.zip.astype(int)
census_gdf = gpd.read_file("/data_files/census_tract_boundaries.shp")
neighbor_gdf = gpd.read_file("/data_files/Neighborhoods_2012b.shp")

# Load and clean park data
parks = gpd.read_file("/data_files/new_parks.csv")
parks.rename(columns = {'zipcode':'zip', 'lattitude':'lat', 'longitude':'lon'}, inplace = True) 
parks.lat = parks.lat.astype('float')
parks.lon = parks.lon.astype('float')
parks.zip = parks.zip.astype('int')
geometry = [Point(xy) for xy in zip(parks.lon, parks.lat)]
parks.geometry = geometry

# Load and clean grocery data
grocery = pd.read_csv("/data_files/grocery_stores.csv")
grocery.columns = grocery.columns.str.lower()
grocery.rename(columns = {'zip code':'zip'}, inplace = True) 
geometry = [Point(xy) for xy in zip(grocery.longitude, grocery.latitude)]
grocery = grocery.drop(['longitude', 'latitude'], axis=1)
grocery_gdf = gpd.GeoDataFrame(grocery, crs="EPSG:4326", geometry=geometry)

# Load and clean health center data
health = pd.read_csv('data_files/health_centers.csv')
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
libraries = pd.read_csv("/data_files/library.csv")
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

def community_profile_map(zip_code):
  '''
  Input:
    zip (int): ZIP code

  Output:
    Map of zip code with library locations
  '''
  # Point layer of libraries
  ax0 = lib_gdf.loc[lib_gdf.zip == zip_code].plot(color='green', zorder=2, figsize=(10, 10))
  # Point layer of health centers
  ax1 = health_gdf.loc[health_gdf.zip == zip_code].plot(ax=ax0, color='red', zorder=1, figsize=(10, 10))
  # Point layer of grocery stores
  ax2 = grocery_gdf.loc[grocery_gdf.zip == zip_code].plot(ax=ax1, color='blue', zorder=1, figsize=(10, 10))
  # Point layer for park location
  ax3 = parks.loc[parks.zip == zip_code].plot(ax=ax2, color='blue', zorder=1, figsize=(10, 10))
  # Polygon layer of zip codes
  final_ax = zip_gdf.loc[zip_gdf.zip == zip_code].boundary.plot(ax=ax3, color= 'black', zorder=1, figsize=(10, 10))
  # Streetview basemap
  ctx.add_basemap(final_ax, crs=zip_gdf.crs.to_string())
  return 

community_profile_map(60615)

