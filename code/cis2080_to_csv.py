# This script transforms original data from CIS poll 2080 to csv.
# The questionaire is structured in cards, and each card has several enumerated single character answers.
# Output file cis2080.csv has a header with the structure "T" + card number + "_" + question number

import pandas as pd
import json

#############
# Variables #
#############
data_file_name = "../data/DA2080"
csv_file_name = "../data/cis2080.csv"
multicolumns_file_name = '../metadata/multicolumns.json'
real_num_responses = 17616
cells_per_card = {1:78, 2:79, 3:80, 4:78, 5:84} # Expected num of characters per
                                                # card in the poll.
           
#############                                                
# Functions #
#############
def clean_card(card, card_num):
      """
      Gets a card as a str and the expected int number for this card.
      Enforces expected length and checks format.
      Returns the updated card.
      """
      
      # Enforce min length
      extra_spaces = cells_per_card[card_num] - len(card)
      card = card + " "*extra_spaces

      # Enforce max length
      card = card[:cells_per_card[card_num]]
      
      # Check format
      if (card[10] != str(card_num)):
        raise Exception("Format error, expected card {}, got line: {}".format(card_num, card))
      
      # Remove first spaces and card number
      if (card_num != 1):
        card = "T" + card[11:] # Add "T" as a card start mark for debuging
      
      return(card)


def get_header(cells_per_card):
  """
  Returns a list of column names.
  Each column label includes the card and the original column number as showed
  in the questionaire.
  """
  
  header = list()
  for key, value in cells_per_card.items():
    card_header = ["T" + str(key) + "_" + str(i+1).zfill(2) for i in range(value)]
      
    if (key != 1):
      # Drop first 10 headers
      card_header = card_header[10:]
      
    header = header + card_header
      
  return(header)


def merge_cols(data, col_nums, card_num):
  new_col_name = "T" + str(card_num) + "_" + str(col_nums[0]).zfill(2) + "-" + str(col_nums[-1]).zfill(2)
  old_col_names = ["T" + str(card_num) + "_" + str(x).zfill(2) for x in col_nums]

  data[new_col_name] = data[old_col_names].agg(''.join, axis=1)
  data = data.drop(columns=old_col_names)
  return(data)


###################
# Data processing #
###################

with open(data_file_name, "r") as f:
  num_responses = sum(1 for line in f)/5

with open(data_file_name, "r") as input_file:
  if (num_responses != real_num_responses):
    raise Exception("Error in the number of responses. Expected {}, got {}".format(real_num_responses,
                                                                                   num_responses))
  # Read data as a nested list
  data_list = list()
  for i in range(int(num_responses)):
    full_line = ""
    for j in range(5):
      card = input_file.readline()[:-1]
      
      full_line = full_line + clean_card(card, j+1)
    
    data_list.append([*full_line])
    
data = pd.DataFrame(data_list, columns=get_header(cells_per_card))

with open(multicolumns_file_name) as f:
  multicolumns_dic = json.load(f)

for card_num, value in multicolumns_dic.items():
  for key, col_nums in value.items():
    data = merge_cols(data, col_nums, card_num)

# Rearrange columns by name
data = data.reindex(sorted(data.columns), axis=1)

data.to_csv(csv_file_name, sep=";", index=False)
