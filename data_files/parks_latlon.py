
import geocoder
import pandas as pd
'''
Get the lattitude and longitude of Chicago parks using the 
MapQuest API (with Emma's API key)
'''
parks = pd.read_csv("all_parks.csv")
address = parks["address"]
zip_code = parks["zipcode"]
lat_lst = []
lon_lst = []
len(parks)

for i in range(len(parks)):
    print(i)
    full_address = address.iloc[i] + ", " + str(zip_code[i])
    g = geocoder.mapquest(full_address, key = "mmcN5Afp3QejG7fOZ0ljDyhrneaqeazD")
    lat_lst.append(g.lat)
    lon_lst.append(g.lng)


