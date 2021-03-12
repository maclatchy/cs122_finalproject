### cs122_finalproject

# **Moving to Chicago and Don't Know Where to Live?**

## **Project Description**
Well, look no further! Our program allows users to rank on a 1-5 scale (1 not important -  5 very important) their preferences on number of nearby grocery stores, parks, health centers, CTA train stops, CTA bus stops, and the level of crime they are looking for in a neighborhood. After answering their neighborhood preferences, they will receive a list of the top five zip codes that match their community preferences. The user can learn more about a particular zip code: median income, number of schools, and life expectancy. From here the user will be able to find properties for sale in their matched community. The user will input the number of bedrooms they are looking for in a property as well as the relative price range the would like on a scale of 1-5, 1 being least expensive and 5 being most expensive. After inputting this information, the user will recieve the top two property matches in each of the five matched zip codes. The user will then be able to better visualize their potential community by choosing to view a map of a selected zip code that shows the location of user-selected community ammenities. Finally, the user will be able to download a .csv file with all of the properties that match their preferences. 

## **Preference Ranking System**
Our ranking system uses weighted averages based on the relative frequency of ammenities or occurence of crime in each zip code to calculate scores for each zip code. A user's preferences are used to calculate an overall preference scores for each zip code. The user will receive an outpul with the top five zip codes corresponding to the highest calculated overall preference scores. 

## **Project Goal**
This project helps individuals moving to Chicago find potential neighborhoods and properties for sale based on individual preferences. Rather than blindly searching for properties on a property listing site, this program offers a more directed search by taking into consideration characteristics of a given zip code and the user's preferences. The user can also easily visualize the various resources available in a community by plotting a given zip code and immediately being able to view the libraries, grocery stores, health centers, train stops, schools, and parks that are in a given zip code. Lastly, users will be able to download all matches to their search in a .csv format so they can readily refer back to potential properties that have been found based on their preferences. 

## **Table of Contents**
### Functions and Programs
* [u_i.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/u_i.py)
    * The main user interface file that can be called in the terminal to start up the program
* [mapping.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/mapping.py)
    * Contains mapping functionality functions and creation of GeoPandas DataFrames
* [z_weight.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/z_weight.py)
    * Function for creating z-scores for each zip code and adding it to our table with the counts of each community factor per zip code
* [zip_recommendation.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/zip_recommendation.py)
    * Function that gathers top recommended zip codes based on the user's input and the weighted z-scores for each zip code
* [redfin.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/redfin.py)
    * Gets the top 300 property listings in every Chicago zip code from Redfin.com and cleans results
    * Creates the PropertyMatch class that has methods to produce a DataFrame of match results, a string that can be printed and lists the top two property matches from each matched zip code, and creates a GeoDataFrame with properties

## Data Scraping and Cleaning
* [count_table.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_files/count_table.py)
    Creates a table with the counts of the number of libraries, grocery stores, CTA bus stops, CTA train stops, parks, health centers, crimes (from 2015 to present) in each zip code.
* [parks_scrape.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/parks_scrape.py)
    * Finds the address and zip code for all park facilities in Chicago
* [shape_files.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/shape_files.py)
    * Loads shape files for mapping from the Chicago Data Portal and previsouly downloaded files in the repository
* [zip_info.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_gathering/zip_info.py)
    * Creates a table with life expectancy, number of schools, and median income for each zip code
* [parks_latlon.py](https://github.com/emmachancellor/cs122_finalproject/blob/main/data_files/parks_latlon.py)
    * Finds the lattitude and longitude of Chicago parks


