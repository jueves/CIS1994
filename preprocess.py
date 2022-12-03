import pandas as pd
import json

data = pd.read_csv("cis2080.csv", sep=";", na_values=[" ", " "*2, "-8", "99"], decimal=",")

# Add UBE
# Standard Drinks, also known as Unidades de Bebida Estándar (UBE)
drink_type_vars = ["T1_"+str(x) for x in range(67, 79, 2)] + \
                 ["T2_"+str(x) for x in range(12, 80, 2)]
drink_amount_vars = ["T1_"+str(x) for x in range(68, 79, 2)] + \
                  ["T2_"+str(x) for x in range(13, 80, 2)]

def get_ube(row):
  def get_ube_per_drinktype(drink):
    if (pd.isna(drink)):
      ube = 0
    elif (int(drink) in [1, 2, 6]):
      ube = 1
    elif (int(drink) in [3, 4, 5, 7, 8]):
      ube = 2
    else:
      ube = 0
    return(ube)
  
  def get_drink_amount(raw_amount):
    if (pd.isna(raw_amount)):
      amount = 0
    else:
      amount = int(raw_amount)
    
    return(amount)

  drink_types = [get_ube_per_drinktype(x) for x in row[drink_type_vars]]
  drink_amounts = [get_drink_amount(x) for x in row[drink_amount_vars]]
  ube = sum([drink_types[i] * drink_amounts[i] for i in range(len(drink_types))])
  return(ube)
  

data["UBE"] = data.apply(get_ube, axis=1)

# List complete variables
with open("descriptive_var_names.json") as f:
  var_names = json.load(f)

def get_names():
  for key, value in var_names.items():
    if (value["description"] != "incomplete"):
      print(key + " " + value["name"])# + "\n" + value["description"] + "\n")

# Rename selected variables
new_names = []
for code in data.columns:
  if (code in var_names.keys() and var_names[code]["description"] != "incomplete"):
    new_names.append(var_names[code]["name"])
  else:
    new_names.append(code)

data.columns = new_names

# Set data types
# Income
for key, value in var_names["T5_44-45"]["values"].items():
  if (value == "NA"):
    value = pd.NA
    
  data.income = data.income.replace(float(key), value)

# # Drink location
# data.drink_loc1 = data.drink_loc1.replace([0, 9], pd.NA)
# data.drink_loc2 = data.drink_loc2.replace([0, 9], pd.NA)
# 
# # Occupation
# # 98 = not enough information
# data.occupation = data.occupation.replace(98, pd.NA)
# 
# # Socioeconomic condition
# data.socioeconomic_condition = data.socioeconomic_condition.replace(12, pd.NA)
# 
# # Sex
# data.sex = data.sex.replace(9, pd.NA)

# Sector

# Set NAs
def set_NAs(var_dict):
  for key, value in var_dict.items():
    data[key] = data[key].replace(value, pd.NA)
    
set_NAs({
  "drink_loc1": [0, 9],
  "drink_loc2": [0, 9],
  "occupation": 98,
  "socioeconomic_condition": 12,
  "sex": 9,
  "sector": 9,
  "status": 9
})
