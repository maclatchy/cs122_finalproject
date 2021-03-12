import pandas as pd
import numpy as np
import zip_recommendation
import redfin
import math
import mapping

# little introduction :)
intro = ["Welcome to our Neighborhood matcher! \U0001F60A\U0001F3D9\n"
         " [ press enter to continue ]\n"]
intro.append("I'm sure you're excited to meet your perfect neighborhood"
             " in Chicago,")
intro.append("but first let's get to know each other a little bit better.")
intro.append("have a drink \U0001F377\U0001F378\U0001F9C3")     
intro.append("and rank the following questions using the numbers from 1(low)-"
             "5(high)")
    
for line in intro:
    print(line)
    input()

error_value = ("Sorry, I didn't catch that. Did you say '1', '2', '3', '4'"
               " or '5'?")

attribute_dict = {"grocery_stores":("Question: how important is proximity to" 
                                    " grocery stores for you? \U0001F34E" 
                                    " \U0001F96C \U0001F35E \n"),
                  "parks":("Question:(how important is proximity to parks for" 
                           " you? \U0001F343 \U0001F31E \U0001F3C3 \n"),
                  "libraries":("Question: how important is proximity to public"
                               " libraries for you? \U0001F4DA \U0001F453" 
                               " \U0001F3E0 \n"),
                  "health_centers":("Question: how important is proximity to" 
                                    " health centers for you? \U0001F9D1" 
                                    " \U0001F9E1 \U0001F3E5 \n"),
                  "cta_train_stops":("Question: how important is proximity to"
                                     " CTA TRAIN stops for you? \U0001F687" 
                                     " \U0001F68D \U0001F698 \n"),
                  "cta_bus_stops":("Question: how important is proximity to CTA"
                                   " BUS stops for you? \U0001F687 \U0001F68D"
                                   " \U0001F698 \n"),
                  "crimes":("Question: how important is the local crime level to"
                            " you? \U0001F303 \U0001F977 \U0001F4B0 \n")}

property_attribute_dict = {"price":("Question: what price range do you desire"
                                    " (1=least expensive, 5=most expensive)"),
                            "beds":"Question: how many beds do you want (1-5)"}
preference_dict = dict()

def get_score(attribute):
    '''
    Takes user inputs and builds a score dictionary
    Input:
      attribute (str): key in attribute dictionary
    '''
    question = attribute_dict[attribute]
    while True:
        data = input(question)
        try:
            data = int(data)
        except:
            print("\n" + error_value + "\n")
            continue
        if data > 5 or data < 0:
            print("\n" + error_value + "\n")
            continue
        else:
            preference_dict[('z_' + attribute)] = data
            break
    print('\nThank you!\n')
    return

def get_property_score(p_attribute):
    '''
    Same as get_score but not connected to z-score dataframe
    '''
    question = property_attribute_dict[p_attribute]
    while True:
        d = input(question)
        try:
            d = int(d)
        except:
            print("\n" + error_value + "\n")
            continue
        if d > 5 or d < 0:
            print("\n" + error_value + "\n")
            continue
        else:
            print('\nThank you!\n') 
            return d   

# Get preferences and display zipcodes
for key in attribute_dict.keys():
    get_score(key)
sort_df = zip_recommendation.get_sorted_weights(preference_dict)
print("\nThese zip codes match your entries the best:")
print(sort_df.head(5))
print('')

#get top 5 zipcodes then make class object for proerty return
property_zips = sort_df["zipcode"].tolist()[:5]
p_object = redfin.PropertyMatch(property_zips)
price = get_property_score("price")
beds = get_property_score("beds")
print("Here are available properties from the recommended neighborhoods: \n")
print(p_object.property_matches(price,beds))

#Give information for any requested Chicago zipcode
stats_df = pd.read_csv('../data_gathering/zip_stats.csv')
available_zips = stats_df["zip_code"].tolist()
while True:
    zip_inquiry = input("Please enter a Chicago zip code for more information:")
    try:
        zip_inquiry = int(zip_inquiry)
    except:
        print("\n Sorry. Could you re-enter a numeric zip code")
    if zip_inquiry in available_zips:
        print(stats_df.loc[stats_df["zip_code"] == zip_inquiry])
        break
    else:
        print("\n We didn't recognize that as a Chicago zip code")
        continue

while True:
    response = input('\nWould you like to see a map of {}' 
                     ' [y or n]?\n'.format(str(zip_inquiry)))
    if 'y' == response.lower():
        zip_inquiry = int(zip_inquiry)
        params = ['all']
        mapping.community_profile_map(zip_inquiry, params)
        while True:
            new_response = input('\nWould you like to see specific amenities'
                                 ' [y or n]?\n')
            if 'y' == new_response.lower() or 'n' == new_response.lower():
                break
            else:
                print('\nPlease respond with [y or n].\n')
        break
    elif 'n' == response.lower():
        new_response = None
        break
    else:
        print('\nPlease respond with [y or n]\n')

param_s = set()
p_dict = {1:'grocery', 
          2:'health',
          3:'parks', 
          4:'schools', 
          5:'cta_rail', 
          6:'library'}

res = 0
fail = 0
flag = None
while True:
    if response == 'n':
        break
    if new_response == 'n':
        break
    if not flag:
        while True:
            if res == 'n':
                break
            if fail == 'fail':
                break
            print('\nPlease input one number corresponding to the amenity you would' 
                ' like to see.\n')
            print("\nPlease type 'done' when you don't want to see any additional"
                " amenities.\n")
            num = input('\n1=grocery, 2=health, 3=parks, 4=schools, 5=cta_rail,'
                        ' 6=library\n')
            if num.lower() == 'done':
                mapping.community_profile_map(zip_inquiry, list(param_s))
                while param_s:
                    param_s.pop()
                break 
            try:
                num = int(num)
            except:
                continue
            if num < 0 or num > 6:
                print('\nPlease enter a number between 1 and 6.\n')
                continue
            else:
                param_s.add(p_dict[num])
                continue
    res = input('\nWould you like to see a different zipcode [y or n]?\n')
    if res.lower() == 'y':
        print('\nYour property zipcodes:', property_zips)
        new_zip = input('\nPlease input one of your property zipcodes.\n')
        try:
            zip_inquiry = int(new_zip)
        except:
            print('\nPlease enter a valid zipcode.\n')
            fail = 'fail'
            continue
        if int(new_zip) in property_zips:
            fail = None
            flag = False
            continue
        else:
            print('\nPlease enter a Chicago zipcode in your property list.\n')
            flag = True
            continue
    elif res.lower() == 'n':
        break
    else:
        print('\nplease enter y or n.\n')
        continue

while True:
    response = input("\nWould you like to download a complete list of"
                     " properties that match your criteria [y or n]?\n")
    if 'y' == response.lower():
        stats = pd.read_csv("zip_stats.csv")
        stats = stats.rename(columns={"zip_code":"zip"})
        properties = p_object.all_property_matches(price, beds)
        final = pd.merge(properties, stats, left_on="zip", right_on="zip")
        final.to_csv("property_results.csv", index = False)
        print("Thank you for using our service to find a new home in Chicago!")
        break
    elif 'n' == response.lower():
        print("Thank you for using our service to find a new home in Chicago!")
        break
    else:
        print('Please respond with [y or n]\n')