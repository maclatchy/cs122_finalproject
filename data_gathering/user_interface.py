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

while True:
    school = input("How important is proximity to schools for you? \n")
    try:
        school = int(school)
    except:
        print("\nYou did not enter a valid whole number.")
        continue
    if school > 5 or school < 0:
        print(error_value)
        continue
    else:
        preference_dict['school'] = school
        break
print('\nThank you!\n')
print(preference_dict)

