from datetime import date
import json
import os

paragraph = "===================================================="
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profiles')

#First action each time the program is booted up
def boot_up():
    #Makes sure that there is a profiles directory
    if not os.path.exists(path):
        os.makedirs(path)

    #Get all the profiles
    profiles = os.listdir(path)

    #If there are no profiles, then create one
    if len(profiles) == 0:
        print("There are currently no profiles to load. We will create one for you!")
        print(paragraph)
        new_profile()
    else: 
        count = 0
        for profile in profiles:
            count = count + 1
            print(str(count) + ". " + profile[:profile.rfind(".")].title())
        
        count += 1
        print(str(count) + ". Create new profile")

        #Select one of the profiles
        choice = int(input("Please select the profile you would like to load (1-" + str(count) + "): "))

        if not choice == count:
            #Load the path
            global profile_path
            profile_path = os.path.join(path, profiles[choice - 1])
            with open(profile_path, 'r') as openfile:
                global user_prof
                user_prof = json.load(openfile)

            #Close out the interaction
            print(paragraph)
            print("Welcome, " + user_prof["name"] + "!")
            print(paragraph)
            main_menu()       
        else:
            new_profile()
        

#Main menu
def main_menu():
    print("Account: " + user_prof["name"])
    choice = 0
    choice = input("1. Start new day\n2. Add food to current day\n3. Edit/Create Profile\n4. Exit\nYour input (1, 2, 3, or 4): ")
    if (choice == "1"):
        print(paragraph)
        start_day()
    elif (choice == "2"):
        #do nothing
        print("Your momma")
    elif (choice == "3"):
        print(paragraph)
        profile_menu()

#Start a new day
def start_day():
    days = user_prof["snapshots"]

    if (len(days) == 0) or ((not len(days) == 0) and (not days[0]["date"] == str(date.today()))):
        diet_structure = '{ "date" : "", "cal_count" : 0, "foods" : [], "protein" : 0, "carbs" : 0, "fat" : 0}'
        global diet_snapshot
        diet_snapshot = json.loads(diet_structure)
        diet_snapshot["date"] = str(date.today())

        days.insert(0, diet_snapshot)
        with open(profile_path, "w") as outfile:
            json.dump(user_prof, outfile)
        
        print("New snapshot for " + str(date.today()) + " created. Go ahead and add food to it!")
        main_menu()

    else:
        print("You already have a diet snapshot for today, please add food to it!.")
        print(paragraph)
        main_menu()

#BMR calculator
def bmr_calc(gender, height, weight, age):
    if (gender == "1"):
        return int(88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age))
    else:
        return int(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age))
    
#Create a new profile
def new_profile():
    #Creating profile json
    profile_structure = '{"name" : "", "cal_goal" : 0, "prot_goal" : 0, "carb_goal" : 0, "fat_goal" : 0, "snapshots" : []}'
    profile = json.loads(profile_structure)

    #Ask Info
    profile["name"] = input("Write your name: ")
    gender = input("Input 1 if you are male and 2 if you are female: ")
    height = int(input("Please input your height in feet: ")) * 12
    height = height + int(input("Please input the remaining inches left in your height: "))
    weight = int(input("Please input your weight in pounds: "))
    age = int(input("Please input your age in years: "))

    #Calculate BMR
    height = height * 2.54
    weight = weight * 0.453592
    profile["cal_goal"] = bmr_calc(gender, height, weight, age)

    #Incorporate macro calculations
    profile["prot_goal"] = int(profile["cal_goal"] * .4 / 4)
    profile["fat_goal"] = int(profile["cal_goal"] * .15 / 9)
    profile["carb_goal"] = int(profile["cal_goal"] * .45 / 4)
    
    #Write to json file
    global profile_path
    profile_path = os.path.join(path, profile["name"].lower() + ".json")
    with open(profile_path, "w") as outfile:
        json.dump(profile, outfile)
    
    global user_prof
    user_prof = profile

    #Close out the Interaction
    print(paragraph)
    print("Successfully created your profile! It is currently logged in!")
    print("Calorie Goal: " + str(profile["cal_goal"]))
    print("Protein Goal: " + str(profile["prot_goal"]))
    print("Carbohydrate Goal: " + str(profile["carb_goal"]))
    print("Fat Goal: " + str(profile["fat_goal"]))
    print(paragraph)
    profile_menu()


#Create or edit profile or go back to main menu
def profile_menu():
    choice = input("1. Create new profile\n2. Edit profile\n3. Back\nYour input (1, 2, or 3): ")
    if (choice == "1"):
        new_profile()
    elif (choice == "2"):
        print("nothing")
    else: 
        print(paragraph)
        main_menu()



#Run Script
print("Welcome to your daily diet tracker!")
print(paragraph)
boot_up()







    
    

