import numpy as np
import pandas as pd
import requests
import json
import csv
from bs4 import BeautifulSoup as bs4
import re


def get_my_data():
# Chicago Primary Care Health Centers
    
    hc_data = pd.read_csv("https://data.cityofchicago.org/resource/cjg8-dbka.csv")
    return print(hc_data)


def find_parks():
    park_page = requests.get("https://www.chicagoparkdistrict.com/parks-facilities/a-z")
    park_text = park_page.text
    soup = bs4(park_text, 'html.parser')
    park_name = soup.find_all("a", href=re.compile(r"^/parks-facilities/"))
    addr_dict = dict()
    park_address = soup.find_all("p", class_="address", translate="no")
    for addr in park_address:
        park_addr = []
        addr = addr.text
        addr_lst = addr.split()
        zip_code = addr_lst[-1]
        for word in addr_lst:
            if word != "Chicago," \
                and word != "IL":
                park_addr.append(word)
        address = " ".join(park_addr)
        print(address)
        if zip_code in addr_dict:
            addr_dict[zip_code] = addr_dict[zip_code].append(address)
        else:
            addr_dict[zip_code] = [address]
        #addr = " ".join(addr.split())
        
    

    print(addr_dict)
        
            
            

    found_park = False
    for park in park_name:
        a_tag = park["href"]
        if a_tag == "/parks-facilities/a-z":
            found_park = True
            continue
        if found_park:
            park_ref = park["href"]
            park_str = re.search(r"(?<=/parks\-facilities/).*[a-z0-9]", park_ref)
            park_str = park_str.group(0)
            park_str = park_str.replace("-", " ")
    
    return