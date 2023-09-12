from datetime import date
import json
structure = '{ "date" : "", "cal_goal" : 2380, "cal_count" : 0, "foods" : [], "protein" : 0, "carbs" : 0, "fat" : 0}'
diet_snapshot = None


def start_day():
    diet_snapshot = json.loads(structure)
    diet_snapshot["date"] = date.today()
    print(diet_snapshot["date"])
    print(diet_snapshot)

choice = 0
print("Welcome to your daily diet tracker!\nPlease type the number from the following menu of the action you wish to perform!\n")

choice = input("1. Start new day\n2. Add food to current day\n3. Edit/Create Profile\n4. Exit\nYour input (1, 2, 3, or 4): ")
if (choice == "1"):
    start_day()







    
    

