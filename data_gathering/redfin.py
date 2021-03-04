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

