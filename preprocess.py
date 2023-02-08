import pandas as pd
import json
import pickle

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

def get_metadata():
  '''
  Returns an indexed list of all variables with complete
  metadata and asks to choose an item.
  
  Once the item is selected, it returns full metadata for
  that variable.
  '''
  var_descriptor = dict() # Index - Metadata dictionary
  names_list = "" # Indexed list of variables
  index = 0
  for key, value in var_names.items():
    if (value["description"] != "incomplete"):
      index = index + 1
      names_list = names_list + "\n" + str(index) + " - " + key + " " + value["name"]
      var_descriptor[index] = var_names[key]
  
  print(names_list + "\n")
  var_number = int(input("Introduce the index of the variable to expand: "))

  if (var_number in var_descriptor.keys()):
    print("\n" + json.dumps(var_descriptor[var_number], indent=4, ensure_ascii=False))
  else:
    print("Introduce a valid index number.")

# Rename selected variables
new_names = []
for code in data.columns:
  if (code in var_names.keys() and var_names[code]["description"] != "incomplete"):
    new_names.append(var_names[code]["name"])
  else:
    new_names.append(code)

data.columns = new_names

# Set NAs
def set_NAs(var_dict):
  for key, value in var_dict.items():
    data[key] = data[key].replace(value, pd.NA)
    
set_NAs({
  "cigarettes": 0,
  "cigars": 0,
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
      is_ordered = value["ordered"] == "True"
      data[value['name']] = pd.Categorical(data[value["name"]],
                                           categories=list(value["values"].values()),
                                           ordered=is_ordered).remove_unused_categories()


# Save data and get_metadata() as a pickle object
pickling_on = open("preprocessed_objs.pickle", "wb")
pickle.dump((data, var_names, get_metadata), pickling_on)
pickling_on.close()
