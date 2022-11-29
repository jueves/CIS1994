import pandas as pd
import json

data = pd.read_csv("cis2080.csv", sep=";", na_values=" ", decimal=",")

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

# Income

