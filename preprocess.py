import pandas as pd
import json

data = pd.read_csv("cis2080.csv")

with open('multicolumns.json') as f:
  multicolumns_dic = json.load(f)

def merge_cols(data, columns, card_num):
  # To be developed
  # Get first T{card_num} column index and work on that.
  return(data)

for card_num, value in multicolumns_dic["cards"].items():
  for key, columns in value.items():
    data = merge_cols(data, columns, card_num)
    print("Card number:", card_num,
          "\nColumns:", columns)
