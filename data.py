import pandas as pd
import numpy as np
import geopandas as gpd

# CDC life expectancy by zip code
IL_le_data = pd.read_csv("IL_A.csv")
IL_le_data.rename(columns = {'STATE2KX':'State ID', 'CNTY2KX':'County ID', 
                             'TRACT2KX':'Tract ID', 'e(0)':'LE', 
                             'se(e(0))':'SE'}, inplace = True) 
print(IL_le_data.shape)

# Health centers from Chicago data portal
hc_cdp_data = pd.read_csv('https://data.cityofchicago.org/resource/cjg8-dbka.csv')
hc_cdp_data = hc_cdp_data.reset_index()
hc_cdp_data.rename(columns = {'index':'Index'}, inplace = True) 
print(hc_cdp_data.shape)

# Life expectancy race/ethnicity Chicago data portal
le_cdp_data = pd.read_csv('https://data.cityofchicago.org/resource/3qdj-cqb8.csv')
le_cdp_data = le_cdp_data.reset_index()
le_cdp_data.rename(columns = {'index':'Index'}, inplace = True) 
print(le_cdp_data.shape)

# Library locations Chicago data portal
lib_cdp_data = pd.read_csv('https://data.cityofchicago.org/resource/x8fc-8rcq.csv')
print(lib_cdp_data.shape)

# Neighborhood boundaries
neighbor_bound = gpd.read_file('Neighborhoods_2012/Neighborhoods_2012b.shp')
print(neighbor_bound.shape)

# Census tract boundaries
census_bound = gpd.read_file('Boundaries - Census Tracts - 2010/'
                             'geo_export_b422834f-4172-488f-901e-9cc00aa9cf19.shp')
print(census_bound.shape)

# Zip code boundaries
zip_bound = gpd.read_file('Boundaries - ZIP codes/'
                          'geo_export_0c65adac-cb98-462f-b7b5-f5b6f8a590eb.shp')
print(zip_bound.shape)