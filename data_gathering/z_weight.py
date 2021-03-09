import pandas as pd
import numpy as np

df = pd.read_csv("counts.csv")
#not including zip code cause that is identifier column --> not getting z-score from it
z_columns = ["grocery_stores","parks","libraries","health_centers","cta_train_stops","cta_bus_stops","crimes"]
    
for col in z_columns:
    new_col_name = "z_" + col
    z_scores = []
    col_list = df[col]
    mu = col_list.mean()
    std = col_list.std()
    print("here")
    for entry in col_list:
        z = (entry-mu)/std
        z_scores.append(z)
    df[new_col_name] = z_scores
df.drop(df.columns[8],axis=1,inplace=True)
print(df.head(5))
df.to_csv(r'C:\Users\mattludwig\Desktop\z_score_counts.csv', index = False, header=True)