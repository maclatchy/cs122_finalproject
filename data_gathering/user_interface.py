# User interface

print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
      "\nWelcome to the Spike-Protein's final project!\n")
print("\nOur goal is to help you find the ideal Chicago neighborhood for you"
      "\nto live!\n")
print("\nPlease input a whole number ranged [0, 5] for all prompts, with 0"
      "\nbeing the least important and 5 being the most important.\n"
      "\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

preference_dict = dict()

error_value = "\nPlease input a whole number ranged [0, 5]\n"

attribute_dict = {"grocery_stores":"How important is proximity to grocery stores for you? \n",
                  "parks":"How important is proximity to parks for you? \n",
                  "libraries":"How important is proximity to public libraries for you? \n",
                  "health_centers":"How important is proximity to health centers for you? \n",
                  "cta_train_stops":"How important is proximity to CTA TRAIN stops for you? \n",
                  "cta_bus_stops":"How important is proximity to CTA BUS stops for you? \n",
                  "crimes":"How important is the crime level for you? \n"}


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
            print(error_value)
            continue
        else:
            preference_dict[('z_' + attribute)] = data
            break
    print('\nThank you!\n')
    return

# Get preferences
get_score('grocery_stores')
get_score('parks')
get_score('libraries')
get_score('health_centers')
get_score('cta_train_stops')
get_score('cta_bus_stops')
get_score('crimes')

print(preference_dict)

