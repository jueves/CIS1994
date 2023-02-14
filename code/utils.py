import pickle
import json

''''
These functions are not needed for the project to work, but
utilities to make coding and data exploration more eficient.
'''

pickle_filename = "../data/preprocessed_data.pickle"

# Import labels
with open("../metadata/descriptive_var_names.json") as f:
  var_names = json.load(f)


# Functions
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

def save_my_data(data):
  # Save data and var_names as a pickle object
  pickling_on = open(pickle_filename, "wb")
  pickle.dump((data), pickling_on)
  pickling_on.close()


def load_my_data(subdata=False):
  # Load preprocessed Pandas datadrame
  pickle_off = open(pickle_filename, "rb")
  data = pickle.load(pickle_off)
  pickle_off.close()

  if subdata:
    selected_vars = []
    for value in var_names.values():
        if (value["description"] != "incomplete"):
            selected_vars.append(value["name"])

    data = data[selected_vars].drop(columns=["day", "month", "year"])


  return(data)

