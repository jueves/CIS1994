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
# Set NAs
def set_NAs(var_dict):
  for key, value in var_dict.items():
    data[key] = data[key].replace(value, pd.NA)
    
set_NAs({
  "drink_loc1": [0, 9],
  "drink_loc2": [0, 9],
  "political_espectrum": 98,
  "occupation": 98,
  "socioeconomic_condition": 12,
  "sex": 9,
  "sector": 9,
  "status": 9
})


def get_numeric_keys(dictionary):
  # Gets a dictionary with string keys and returns
  # a similar dictionary with integer keys.
  new_dic = {}
  for key, value in dictionary.items():
    new_dic[int(key)] = value
  return(new_dic)

# Assign labels
for key, value in var_names.items():
  if (value["description"] != "incomplete" and "values" in value.keys()):
    numeric_dic = get_numeric_keys(value['values'])
    data[value['name']] = data[value['name']].map(numeric_dic)
    if (isinstance(list(value["values"].values())[0], str)):
      # Apply categorical
      print(value["name"])

