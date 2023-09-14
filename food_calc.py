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
    choice = input("1. Start new day\n2. Add food to current day\n3. Edit/Create Profile\n4. Today's Snapshot Breakdown\n5. Exit\nYour input (1, 2, 3, 4, or 5): ")
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
        snapshot_breakdown()
        main_menu()

def new_food():
    if not os.path.exists(food_path):
        os.makedirs(food_path)

    print("Select the food group of the new food item.")
    choice = input("1. Fruit\n2. Vegetable\n3. Grain\n4. Protein\n5. Dairy\n6. Beverage\n7. Back\nYour input (1, 2, 3, 4, 5, 7, or 7): ")
    print(paragraph)
    
    if choice != "7":
        food_group_path = os.path.join(food_path, food_groups[int(choice) - 1])
        if not os.path.exists(food_group_path):
            os.makedirs(food_group_path)
        
        food_item = json.loads('{"name": "", "cal": 0, "protein": 0, "carb": 0, "fat": 0}')
        print("Please enter the nutrition info as you see on the packet, or as you have calculated.")
        food_item["name"] = input("Please enter the name of this food item: ")

        weight = float(input("How many grams per serving: "))
        calories = float(input("How many calories per serving: "))
        protein = float(input("How much protein per serving (g): "))
        carbs = float(input("How many carbohydrates per serving (g): "))
        fat = float(input("How much fat per serving (g): "))

        food_item["cal"] = calories / weight
        food_item["protein"] = protein / weight
        food_item["carb"] = carbs / weight
        food_item["fat"] = fat / weight

        food_item_path = os.path.join(food_group_path, food_item["name"].lower() + ".json")
        with open(food_item_path, "w") as outfile:
            json.dump(food_item, outfile)

        choice = input("Would you like to add this food to your snapshot? (y/n): ")
        print(paragraph)
        if choice.lower() == "y" or choice.lower() == "yes":  
            add_to_snapshot(food_item)
    else:
        food_menu()

def add_to_snapshot(food):
    global diet_snapshot
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
    

def add_macros(food):
    choice = float(input("How much of this food in grams did you eat?\nYour input (g): "))
    calories = round(food["cal"] * choice, 1)
    carbs = round(food["carb"] * choice, 1)
    protein = round(food["protein"] * choice, 1)
    fat = round(food["fat"] * choice, 1)

    serving = json.loads('{"name": "", "cal": 0, "protein": 0, "carb": 0, "fat": 0}')
    serving["name"] = food["name"]
    serving["cal"] = calories
    serving["carb"] = carbs
    serving["fat"] = fat
    serving["protein"] = protein

    diet_snapshot["cal_count"] = int(diet_snapshot["cal_count"] - calories)
    diet_snapshot["protein"] = diet_snapshot["protein"] - protein
    diet_snapshot["carbs"] = diet_snapshot["carbs"] - carbs
    diet_snapshot["fat"] = diet_snapshot["fat"] - fat

    diet_snapshot["foods"].append(serving)

    user_prof["snapshots"][0] = diet_snapshot

    with open(user_path, "w") as outfile:
        json.dump(user_prof, outfile)

    print(paragraph)
    snapshot_breakdown()
    food_menu()

def snapshot_breakdown():
    print("Here are the remaining macros you have leftover for today:")
    print("Leftover Calories: " + str(diet_snapshot["cal_count"]))
    print("Leftover Protein: " + str(diet_snapshot["protein"]))
    print("Leftover Carbohydrates: " + str(diet_snapshot["carbs"]))
    print("Leftover Fat: " + str(diet_snapshot["fat"]))
    print(paragraph)

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

def existing_food():
    if not os.path.exists(food_path):
        os.makedirs(food_path)

    print("Select the food group of the new food item.")
    choice = input("1. Fruit\n2. Vegetable\n3. Grain\n4. Protein\n5. Dairy\n6. Beverage\n7. Back\nYour input (1, 2, 3, 4, 5, 7, or 7): ")
    print(paragraph)

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
                count = 0
                for name in food_names:
                    count = count + 1
                    print(str(count) + ". " + name[:name.rfind(".")].title())
                
                count += 1
                print(str(count) + ". Back")

                choice = int(input("Please select the food you would like to add (1-" + str(count) + "): "))

                if not choice == count:
                    food_item_path = os.path.join(food_group_path, food_names[choice - 1])
                    food_item = None
                    with open(food_item_path, "r") as openfile:
                        food_item = json.load(openfile)
                    
                    add_to_snapshot(food_item)
                else:
                    existing_food()





#Start a new day
def start_day():
    create_diet_snapshot()
    main_menu()

def create_diet_snapshot():
    days = user_prof["snapshots"]

    if (len(days) == 0) or ((not len(days) == 0) and (not days[0]["date"] == str(date.today()))):
        diet_structure = '{ "date" : "", "cal_count" : 0, "foods" : [], "protein" : 0, "carbs" : 0, "fat" : 0}'
        global diet_snapshot
        diet_snapshot = json.loads(diet_structure)
        diet_snapshot["date"] = str(date.today())
        diet_snapshot["cal_count"] = user_prof["cal_goal"]
        diet_snapshot["protein"] = user_prof["prot_goal"]
        diet_snapshot["carbs"] = user_prof["carb_goal"]
        diet_snapshot["fat"] = user_prof["fat_goal"]

        days.insert(0, diet_snapshot)
        with open(user_path, "w") as outfile:
            json.dump(user_prof, outfile)
        
        print("New snapshot for " + str(date.today()) + " created. Go ahead and add food to it!")
        print(paragraph)

    else:
        print("You already have a diet snapshot for today, please add food to it!.")
        print(paragraph)


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


#Create or edit profile or go back to main menu
def profile_menu():
    choice = input("1. Create new profile\n2. Edit profile\n3. Back\nYour input (1, 2, or 3): ")
    if (choice == "1"):
        new_profile()
        profile_menu()
    elif (choice == "2"):
        print("nothing")
    else: 
        print(paragraph)
        main_menu()



#Run Script
print("Welcome to your daily diet tracker!")
print(paragraph)
boot_up()







    
    

