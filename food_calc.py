from datetime import date
from decimal import Decimal
import json
import os

paragraph = "===================================================="
path = os.path.dirname(os.path.realpath(__file__))
profiles_path = os.path.join(path, 'profiles')
food_path = os.path.join(path, 'foods')
food_groups = ["fruits", "vegetables", "grains", "proteins", "dairy", "beverages"]


#First action each time the program is booted up
def boot_up():
    global diet_snapshot
    #Makes sure that there is a profiles directory
    if not os.path.exists(profiles_path):
        os.makedirs(profiles_path)

    #Get all the profiles
    profiles = os.listdir(profiles_path)

    #If there are no profiles, then create one
    if len(profiles) == 0:
        diet_snapshot = None
        print("There are currently no profiles to load. We will create one for you!")
        print(paragraph)
        new_profile()
        main_menu()
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
            global user_path
            user_path = os.path.join(profiles_path, profiles[choice - 1])
            with open(user_path, 'r') as openfile:
                global user_prof
                user_prof = json.load(openfile)

            if len(user_prof["snapshots"]) == 0:
                diet_snapshot = None
            else:
                diet_snapshot = user_prof["snapshots"][0]

            #Close out the interaction
            print(paragraph)
            print("Welcome, " + user_prof["name"] + "!")
            print(paragraph)
            main_menu()       
        else:
            diet_snapshot = None
            new_profile()
            main_menu()     

#Main menu
def main_menu():
    print("Account: " + user_prof["name"])
    choice = input("1. Start new day\n2. Add food to current day\n3. Edit/Create Profile\n4. Data\n5. Exit\nYour input (1, 2, 3, 4, or 5): ")
    if (choice == "1"):
        print(paragraph)
        start_day()
    elif (choice == "2"):
        print(paragraph)
        food_menu()
    elif (choice == "3"):
        print(paragraph)
        profile_menu()
    elif (choice == "4"):
        print(paragraph)
        data_menu()

#Food Menu
def food_menu():
    choice = input("1. Create new food item\n2. Add existing food item\n3. Back\nYour input (1, 2, or 3): ")
    if (choice == "1"):
        print(paragraph)
        new_food()
    elif (choice == "2"):
        existing_food()
    else:
        print(paragraph)
        main_menu()

#Create or edit profile or go back to main menu
def profile_menu():
    choice = input("1. Create new profile\n2. Edit profile\n3. Back\nYour input (1, 2, or 3): ")
    if (choice == "1"):
        new_profile()
        profile_menu()
    elif (choice == "2"):
        edit_profile()
    else: 
        print(paragraph)
        main_menu()

#Data menu
def data_menu():
    choice = input("1. Snapshot Breakdown\n2. Foods consumed\n3. Back\nYour input (1, 2, or 3): ")
    if (choice == "1"):
        print(paragraph)
        snapshot_breakdown()
        data_menu()
    elif (choice == "2"):
        print(paragraph)
        food_breakdown()
    else:
        print(paragraph)
        main_menu()

#Start a new day
def start_day():
    create_diet_snapshot()
    main_menu()

#Make snapshot for current day
def create_diet_snapshot():
    #get list of snapshots from user
    days = user_prof["snapshots"]

    #check to see if a new snapshot is needed
    if (len(days) == 0) or ((not len(days) == 0) and (not days[0]["date"] == str(date.today()))):
        diet_structure = '{ "date" : "", "cal_count" : 0, "foods" : [], "protein" : 0, "carbs" : 0, "fat" : 0}'

        global diet_snapshot
        diet_snapshot = json.loads(diet_structure)
        diet_snapshot["date"] = str(date.today())
        diet_snapshot["cal_count"] = user_prof["cal_goal"]
        diet_snapshot["protein"] = user_prof["prot_goal"]
        diet_snapshot["carbs"] = user_prof["carb_goal"]
        diet_snapshot["fat"] = user_prof["fat_goal"]

        #update profile
        days.insert(0, diet_snapshot)
        with open(user_path, "w") as outfile:
            json.dump(user_prof, outfile)
        
        print("New snapshot for " + str(date.today()) + " created. Go ahead and add food to it!")
        print(paragraph)

    else:
        print("You already have a diet snapshot for today, please add food to it!.")
        print(paragraph)

#Create a new food file
def new_food():

    #Create path
    if not os.path.exists(food_path):
        os.makedirs(food_path)

    #Choose food group
    print("Select the food group of the new food item.")
    choice = input("1. Fruit\n2. Vegetable\n3. Grain\n4. Protein\n5. Dairy\n6. Beverage\n7. Back\nYour input (1, 2, 3, 4, 5, 7, or 7): ")
    print(paragraph)
    
    #Enter information
    if choice != "7":
        food_group_path = os.path.join(food_path, food_groups[int(choice) - 1])
        if not os.path.exists(food_group_path):
            os.makedirs(food_group_path)
        
        food_item = json.loads('{"name": "", "serving": 0, "cal": 0, "protein": 0, "carb": 0, "fat": 0}')
        print("Please enter the nutrition info as you see on the packet, or as you have calculated.")
        food_item["name"] = input("Please enter the name of this food item: ")

        serving = float(input("How many grams per serving: "))
        calories = float(input("How many calories per serving: "))
        protein = float(input("How much protein per serving (g): "))
        carbs = float(input("How many carbohydrates per serving (g): "))
        fat = float(input("How much fat per serving (g): "))

        #Divide each to be value per gram for future food entries
        food_item["serving"] = serving
        food_item["cal"] = calories / serving
        food_item["protein"] = protein / serving
        food_item["carb"] = carbs / serving
        food_item["fat"] = fat / serving

        #Create food json object
        food_item_path = os.path.join(food_group_path, food_item["name"].lower() + ".json")
        with open(food_item_path, "w") as outfile:
            json.dump(food_item, outfile)

        #Ask if they want to add it to their daily snapshot
        choice = input("Would you like to add this food to your snapshot? (y/n): ")
        print(paragraph)
        if choice.lower() == "y" or choice.lower() == "yes":  
            add_to_snapshot(food_item)
    else:
        food_menu()

#Add food that has already been added
def existing_food():

    #Create Path
    if not os.path.exists(food_path):
        os.makedirs(food_path)

    #Select food group
    print("Select the food group of the new food item.")
    choice = input("1. Fruit\n2. Vegetable\n3. Grain\n4. Protein\n5. Dairy\n6. Beverage\n7. Back\nYour input (1, 2, 3, 4, 5, 7, or 7): ")
    print(paragraph)

    #Make sure there are foods in the group
    if choice != "7":
        food_group_path = os.path.join(food_path, food_groups[int(choice) - 1])
        if not os.path.exists(food_group_path):
            print("There are currently no foods added to this group.\nPlease create a new food item.")
            print(paragraph)
            food_menu()
        else:
            food_names = os.listdir(food_group_path)
            if (len(food_names) == 0):
                print("There are currently no foods added to this group.\nPlease create a new food item.")
                print(paragraph)
                food_menu()
            else:
                #List out all the foods in the category
                count = 0
                for name in food_names:
                    count = count + 1
                    print(str(count) + ". " + name[:name.rfind(".")].title())
                
                count += 1
                print(str(count) + ". Back")

                choice = int(input("Please select the food you would like to add (1-" + str(count) + "): "))

                #Get the food item
                if not choice == count:
                    food_item_path = os.path.join(food_group_path, food_names[choice - 1])
                    food_item = None
                    with open(food_item_path, "r") as openfile:
                        food_item = json.load(openfile)
                    
                    add_to_snapshot(food_item)
                else:
                    existing_food()
    else:
        food_menu()

#Add food to the snapshot
def add_to_snapshot(food):

    global diet_snapshot

    #Check to make sure the current snapshot is the correct date
    if (diet_snapshot == None):
        print("It seems like you didn't start a new snapshot.")
        create_diet_snapshot()
        add_macros(food)
    elif (diet_snapshot["date"] != str(date.today())):
        print("The current snapshot does not match with todays date.")
        choice = input("Would you like to override this? (y/n): ")
        if choice.lower() == "y" or choice.lower() == "yes":
            add_macros(food)
        else:
            create_diet_snapshot()
            add_macros(food)
    else:
        add_macros(food)
    
#Add macros to current snapshot
def add_macros(food):
    #Get how many grams/servings were eaten then apply to the food characteristics
    choice = float(input("How much of this food in grams did you eat?\nOne serving is " + str(food["serving"]) + " gram(s).\nYour input (g): "))
    calories = round(food["cal"] * choice, 1)
    carbs = round(food["carb"] * choice, 1)
    protein = round(food["protein"] * choice, 1)
    fat = round(food["fat"] * choice, 1)

    #Create a serving object to store in the snapshot
    serving = json.loads('{"name": "", "cal": 0, "protein": 0, "carb": 0, "fat": 0}')
    serving["name"] = food["name"]
    serving["cal"] = calories
    serving["carb"] = carbs
    serving["fat"] = fat
    serving["protein"] = protein

    #Update macros for daily snapshot
    diet_snapshot["cal_count"] = int(diet_snapshot["cal_count"] - calories)
    diet_snapshot["protein"] = round(diet_snapshot["protein"] - protein, 1)
    diet_snapshot["carbs"] = round(diet_snapshot["carbs"] - carbs, 1)
    diet_snapshot["fat"] = round(diet_snapshot["fat"] - fat, 1)

    diet_snapshot["foods"].append(serving)

    user_prof["snapshots"][0] = diet_snapshot

    #Write update snapshot to file
    with open(user_path, "w") as outfile:
        json.dump(user_prof, outfile)

    print(paragraph)
    snapshot_breakdown()
    food_menu()
    
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
    global user_path
    user_path = os.path.join(profiles_path, profile["name"].lower() + ".json")
    with open(user_path, "w") as outfile:
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

#Edit the users profile
def edit_profile():

    #Give options on what the user can update
    attributes = ["cal_goal", "prot_goal", "carb_goal", "fat_goal"]
    print("Account: " + user_prof["name"])
    print("1. Calorie Goal: " + str(user_prof["cal_goal"]))
    print("2. Protein Goal: " + str(user_prof["prot_goal"]))
    print("3. Carbohydrate Goal: " + str(user_prof["carb_goal"]))
    print("4. Fat Goal: " + str(user_prof["fat_goal"]))
    print("5. Back")
    choice = int(input("Select the attribute you would like to change (1, 2, 3, or 4): "))

    if not choice == 5:
        #Get the desired value
        goal = choice
        choice = int(input("What should the new value be?: "))

        #Update profile and write to file
        user_prof[attributes[goal - 1]] = choice
        with open(user_path, "w") as outfile:
            json.dump(user_prof, outfile)
        print(paragraph)
        edit_profile()
    else:
        print(paragraph)
        profile_menu()

#BMR calculator
def bmr_calc(gender, height, weight, age):
    if (gender == "1"):
        return int(88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age))
    else:
        return int(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age))

#Display daily snapshot's values in their current state
def snapshot_breakdown():
    print("Here are the remaining macros you have leftover for today:")
    print("Leftover Calories: " + str(diet_snapshot["cal_count"]))
    print("Leftover Protein: " + str(diet_snapshot["protein"]))
    print("Leftover Carbohydrates: " + str(diet_snapshot["carbs"]))
    print("Leftover Fat: " + str(diet_snapshot["fat"]))
    print(paragraph)

#display the foods that have been consumed that day
def food_breakdown():
    consumed = diet_snapshot["foods"]
    cals = 0
    protein = 0
    carbs = 0
    fat = 0

    if not len(consumed) == 0:
        for food in consumed:
            print(str(food["name"]) + "| Cal: " + str(food["cal"]) + " | Protein: " + str(food["protein"]) + " | Carbs: " + str(food["carb"]) + " | Fat: " + str(food["fat"]))
            print()
            cals += food["cal"]
            protein += food["protein"]
            carbs += food["carb"]
            fat += food["fat"]

        print(paragraph)

        print("Total | Calories: " + str(cals) + " | Protein: " + str(protein) + " | Carbs: " + str(carbs) + " | Fat: " + str(fat))

        print(paragraph)
        data_menu()
    else:
        print("You haven't consumed any foods today, add them to your snapshot then come back!")
        data_menu()
        

#Run Script
print("Welcome to your daily diet tracker!")
print(paragraph)
boot_up()







    
    

