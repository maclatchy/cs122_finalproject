import pandas as pd
import numpy as np

user_weights = {"z_grocery_stores":2,"z_parks":3,"z_libraries":1,"z_health_centers":1,"z_cta_train_stops":5,"z_cta_bus_stops":0,"z_crimes":0}
df = pd.read_csv("../data_files/z_score_counts.csv")

def weighting(zipcode):
    #given a particular zip code calculate score from user weights
    keys = list(user_weights.keys())
    score = 0
    for i in range(len(keys)):
        score += zipcode[i+8]*user_weights.get(keys[i])
    return score
#multiply z_crimes by -1 because high z_score on crimes means more than average
user_weights["z_crimes"] *= -1

zips = []
scores = []
for index, row in df.iterrows():
    value = weighting(row)
    scores.append(value)
    zips.append(int(row[0]))

df = pd.DataFrame()
df["zipcode"] = zips
df["score"] = scores

sort_df = df.sort_values(["score"], ascending=[False])
sort_df.reset_index(drop=True, inplace=True)
print("These zip codes match your entry the best:")
print(sort_df.head(5))