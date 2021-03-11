'''
Taking User's Inputs

Patricia Zito
'''

# little introduction :)
intro = ["Welcome to our Neighborhood matcher! \U0001F60A\U0001F3D9\n [ press enter to continue ]\n"]
intro.append("I'm sure you're excited to meet your perfect neighborhood in Chicago,")
intro.append("but first let's get to know each other a little bit better.")
intro.append("have a drink \U0001F377\U0001F378\U0001F9C3")     
intro.append("and rank the following questions using the numbers from 1(low)-5(high)")
    
for line in intro:
    print(line)
    input()


# questions 
print("So, how do you feel about books? Do you like having libraries by your house? ", "\U0001F4DA", "\U0001F453", "\U0001F3E0", "\n")
print("1- nope, I'm actually allergic to reading, 5- libraries near me are a plus")
lib_rank = input()
lib_rank = is_range(lib_rank)

print("I see. What about parks? Do you like those? ", "\U0001F343", "\U0001F31E", "\U0001F3C3", "\n")
print("1-  I actually don't mind them, 5- yess")
park_rank = input()
park_rank = is_range(park_rank)

print("Awesome, same. Groceries stores?", "\U0001F34E", "\U0001F96C", "\U0001F25E", "\n")
print("1- I don't care, 5- very important!")
groc_rank = input()
groc_rank = is_range(groc_rank)

print("uh huh. alrighty. What about health facilities? ", "\U0001F9D1", "\U000F2764" "\U0001F3E5", "\n")
print("1- nope, don't care, 5- yes!")
health_rank = input()
health_rank = is_range(health_rank)

print("okay, okay. And... schools?" "\U0001F9D2","\U0001F6B8", "\U0001F3EB", "\n")
print("1- nah, I don't need schools around me, 5- yep, schools would be good")
school_rank = input()
school_rank = is_range(school_rank)

print("And will you be taking buses or subways often?", "\U0001F687", "\U0001F68D", "\U0001F698", "\n")
print("1- I have a car so..., to 5- Yesss, CTA, brrr")
cta_rank = input()
cta_rank = is_range(cta_rank)

print("Okay, we're almost finished, I promise\n")
print("How important is the safety of the neighborhood?", "\U0001F303", "\U0001F977", "\U0001F4B0" "\n")
print("1- I could live in Gotham city, to 5- no crimes please!")
safe_rank = input()
safe_rank = is_range(safe_rank)

print("Okie Dokie. Last question! What is our rent budget($) ?")
cost = input()

print("Alright, thank you so much!")


def is_range(rank):
    '''
    Certifies that the number given is within 1-5.

    Inputs: 
        rank: (str) to be evaluated
    '''

    if int(rank) >= 1 and int(rank) <= 5:
        return rank
    else: 
        print("Sorry, I didn't catch that. Did you say '1', '2', '3', '4' or '5'?")
        rank = input()
        return is_range(rank)
