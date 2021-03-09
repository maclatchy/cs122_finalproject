import zip_recommendation

# User interface
print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
      "\nWelcome to the Spike-Protein's final project!\n")
print("\nOur goal is to help you find the ideal Chicago zipcode for you"
      "\nto live!\n")
print("\nPlease input a whole number ranged [0, 5] for all prompts, with 0"
      "\nbeing the least important and 5 being the most important.\n"
      "\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

preference_dict = dict()

attribute_dict = {"grocery_stores":"Question: how important is proximity to grocery stores for you? \n",
                  "parks":"Question: how important is proximity to parks for you? \n",
                  "libraries":"Question: how important is proximity to public libraries for you? \n",
                  "health_centers":"Question: how important is proximity to health centers for you? \n",
                  "cta_train_stops":"Question: how important is proximity to CTA TRAIN stops for you? \n",
                  "cta_bus_stops":"Question: how important is proximity to CTA BUS stops for you? \n",
                  "crimes":"Question: how important is the crime level for you? \n"}


def get_score(attribute):
    question = attribute_dict[attribute]
    while True:
        data = input(question)
        try:
            data = int(data)
        except:
            print("\nYou did not enter a valid whole number.\n")
            continue
        if data > 5 or data < 0:
            print("\nThe number you entered was not in the range [0, 5].\n")
            continue
        else:
            preference_dict[('z_' + attribute)] = data
            break
    print('\nThank you!\n')
    return

# Get preferences
for key in attribute_dict.keys():
    get_score(key)

sort_df = zip_recommendation.get_sorted_weights(preference_dict)
print("\nThese zip codes match your entries the best:\n")
print(sort_df.head(5))
print('')

