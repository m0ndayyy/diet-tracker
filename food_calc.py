from datetime import date
import json
import os
diet_structure = '{ "date" : "", "cal_count" : 0, "foods" : [], "protein" : 0, "carbs" : 0, "fat" : 0}'
diet_snapshot = None

def main_menu():
    choice = 0
    choice = input("1. Start new day\n2. Add food to current day\n3. Edit/Create Profile\n4. Exit\nYour input (1, 2, 3, or 4): ")
    if (choice == "1"):
        print("====================================================")
        start_day()
    elif (choice == "2"):
        #do nothing
        print("Your momma")
    elif (choice == "3"):
        print("====================================================")
        profile_menu()


def start_day():
    diet_snapshot = json.loads(diet_structure)
    diet_snapshot["date"] = date.today()
    print(diet_snapshot["date"])
    print(diet_snapshot)

def bmr_calc(gender, height, weight, age):
    if (gender == "1"):
        return int(88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age))
    else:
        return int(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age))

def new_profile():
    profile_structure = '{"name" : "", "cal_goal" : 0, "prot_goal" : 0, "carb_goal" : 0, "fat_goal" : 0, "snapshots" : []}'
    profile = json.loads(profile_structure)
    profile["name"] = input("Write your name: ")

    gender = input("Input 1 if you are male and 2 if you are female: ")
    height = int(input("Please input your height in feet: ")) * 12
    height = height + int(input("Please input the remaining inches left in your height: "))
    weight = int(input("Please input your weight in pounds: "))
    age = int(input("Please input your age in years: "))

    height = height * 2.54
    weight = weight * 0.453592

    profile["cal_goal"] = bmr_calc(gender, height, weight, age)

    profile["prot_goal"] = int(profile["cal_goal"] * .4 / 4)
    profile["fat_goal"] = int(profile["cal_goal"] * .15 / 9)
    profile["carb_goal"] = int(profile["cal_goal"] * .45 / 4)
    

    filepath = os.path.join('./profiles', profile["name"].lower() + ".json")
    if not os.path.exists('./profiles'):
        os.makedirs('./profiles')
    with open(filepath, "w") as outfile:
        json.dump(profile, outfile)
    print("Successfully created your profile!")
    print("====================================================")
    print("Calorie Goal: " + str(profile["cal_goal"]))
    print("Protein Goal: " + str(profile["prot_goal"]))
    print("Carbohydrate Goal: " + str(profile["carb_goal"]))
    print("Fat Goal: " + str(profile["fat_goal"]))
    print("====================================================")
    profile_menu()



def profile_menu():
    choice = input("1. Create new profile\n2. Edit profile\n3. Back\nYour input (1, 2, or 3): ")
    if (choice == "1"):
        new_profile()
    elif (choice == "2"):
        print("nothing")
    else: 
        print("====================================================")
        main_menu()

print("Welcome to your daily diet tracker!\nPlease type the number from the following menu of the action you wish to perform!\n")
main_menu()







    
    

