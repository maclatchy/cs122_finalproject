import numpy as np
import pandas as pd
import requests
import json
import csv
from bs4 import BeautifulSoup as bs4
import re
import string
import csv


def find_parks():
    '''
    Finds the address of all park facilities and creates a list of 
    dictionaries that contain the park address and the park zip code. 
    Addresses are non-repeating; parks that have multiple facilities at
    the same address are only recorded as one address. 
    '''
    page_num = ""
    all_park_facil = []
    for n in range(201):
        print(n)
        url = "https://www.chicagoparkdistrict.com/parks-facilities/a-z" + page_num
        park_page = requests.get(url)
        park_text = park_page.text
        soup = bs4(park_text, 'html.parser')
        park_address = soup.find_all("p", class_="address", translate="no")
        added_addrs = set()
        all_addrs = []
        all_zip = []
        for addr in park_address:
            park_addr = []
            addr = addr.text
            addr_lst = addr.split()
            if len(addr_lst) == 0:
                continue
            zip_code = addr_lst[-1]
            addr_lst = addr_lst[:-3]
            for word in addr_lst:
                park_addr.append(word)
            address = " ".join(park_addr)
            address = address.replace(".", "")
            all_addrs.append(address)
            all_zip.append(zip_code)   
        for i, addr in enumerate(all_addrs):
            if addr not in added_addrs:
                park_dict = dict()
                park_dict["address"] = addr
                park_dict["zipcode"] = all_zip[i]
                all_park_facil.append(park_dict)
                added_addrs.add(addr)
        page_num = "?page=" + str(n)
    return all_park_facil


'''
    with open("all_parks.csv", "w", newline="") as csv_file:
        cols = ["address", "zipcode"] 
        writer = csv.DictWriter(csv_file, fieldnames=cols)
        writer.writeheader()
        writer.writerows(p)
'''


def find_parks_nested():
    '''
    Creates a list of dictionaries of park addresses (key) and all the
    corresponding facilities at a given address (value). 
    '''
    page_num = ""
    all_park_facil = dict()
    check_dict_addresses = set()
    for n in range(200):
        print(n)
        url = "https://www.chicagoparkdistrict.com/parks-facilities/a-z" + page_num
        park_page = requests.get(url)
        park_text = park_page.text
        soup = bs4(park_text, 'html.parser')
        park_address = soup.find_all("p", class_="address", translate="no")
        soup = bs4(park_text, 'html.parser')
        park_name_soup = soup.find_all("a", href=re.compile(r"^/parks-facilities/"))
        found_park = False
        park_names = []
        for park in park_name_soup:
            a_tag = park["href"]
            if a_tag == "/parks-facilities/a-z":
                found_park = True
                continue
            if found_park:
                park_ref = park["href"]
                park_str = re.search(r"(?<=/parks\-facilities/).*[a-z0-9]", park_ref)
                park_str = park_str.group(0)
                park_str = park_str.replace("-", " ")
                park_str = string.capwords(park_str)
                park_names.append(park_str)
        print("Park Names:", park_names)
        for addr in park_address:
            park_addr = []
            addr = addr.text
            addr_lst = addr.split()
            if len(addr_lst) > 0:
                zip_code = addr_lst[-1]
                addr_lst = addr_lst[:-1]
            for word in addr_lst:
                if word != "Chicago," \
                    and word != "IL":
                    park_addr.append(word)
            address = " ".join(park_addr)
            address = address.replace(".", "")
            park_name = park_names[0]
            if address not in check_dict_addresses:
                park_dict = dict()
                park_dict["name"] = [park_name]
                park_dict["address"] = address
                if zip_code in all_park_facil:
                    current_park_lst = all_park_facil[zip_code]
                    current_park_lst.append(park_dict)
                    all_park_facil[zip_code] = current_park_lst
                else:
                    all_park_facil[zip_code] = [park_dict]
            else:
                if zip_code in all_park_facil:
                    zip_dic = all_park_facil[zip_code][0]
                    name_lst = zip_dic["name"]
                    name_lst.append(park_name)
                    zip_dic["name"] = name_lst
            check_dict_addresses.add(address)
            park_names = park_names[1:]
        page_num = "?page=" + str(n)
    return all_park_facil
