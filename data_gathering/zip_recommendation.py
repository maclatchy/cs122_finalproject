import pandas as pd
import numpy as np

df = pd.read_csv("../data_files/z_score_counts.csv")

def weighting(zipcode, user_weights):
    '''
    Get score for each category and zip code given user input and z scores
    '''
    keys = list(user_weights.keys())
    score = 0
    for i in range(len(keys)):
        score += zipcode[i+8]*user_weights.get(keys[i])
    return score


def get_sorted_weights(user_weights):
    '''
    Create a new dataframe of score by zipcode for ranking purposes
    '''
    #multiply z_crimes by -1 because high z_score on crimes means more than average
    user_weights["z_crimes"] *= -1
    zips = []
    scores = []
    for index, row in df.iterrows():
        value = weighting(row, user_weights)
        scores.append(value)
        zips.append(int(row[0]))
    new_df = pd.DataFrame()
    new_df["zipcode"] = zips
    new_df["score"] = scores
    sort_df = new_df.sort_values(["score"], ascending=[False])
    sort_df.reset_index(drop=True, inplace=True)
    return sort_df

#sort_df = get_sorted_weights(user_weights)
#print("These zip codes match your entry the best:")
#print(sort_df.head(5))