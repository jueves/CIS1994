# This script transforms original data from CIS poll 2080 to csv.
# The questionaire is structured in cards, and each card has several enumerated
# single character answers.
# Output file cis2080.csv has a header with the structure "T" + card number + "_" + question number

#############
# Variables #
#############
data_file_name = "DA2080"
real_num_responses = 17616
cells_per_card = {1:78, 2:79, 3:80, 4:78, 5:84} # Expected num of characters per
                                                # card in the poll.
           
#############                                                
# Functions #
#############
def clean_card(card, card_num):
      # Gets a card as a str and the expected number for this card.
      # Enforces expected length and checks format.
      # Then returns the updated card.
      
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


def get_header():
  header = ""
  for key, value in cells_per_card.items():
    card_header = ["T" + str(key) + "_" + str(i+1) for i in range(value)]
      
    if (key != 1):
      # Drop first 10 headers
      card_header = card_header[10:]
      header = header + ";"
      
    # Join in a single string
    card_header = ";".join(card_header)
      
    header = header + card_header
      
  return(header + "\n")


###################
# Data processing #
###################

with open(data_file_name, "r") as f:
  num_responses = sum(1 for line in f)/5

with open(data_file_name, "r") as input_file:
  if (num_responses != real_num_responses):
    raise Exception("Error in the number of responses. Expected {}, got {}".format(real_num_responses,
                                                                                   num_responses))
  # Limit responses for testing:
  #num_responses = 5
  
  with open("cis2080.csv", "a") as output_file:
    # Add header
    output_file.write(get_header())
    
    # Add body
    for i in range(int(num_responses)):
      full_line = ""
      for j in range(5):
        card = input_file.readline()[:-1]
        
        full_line = full_line + clean_card(card, j+1)
      
      full_line_csv = ";".join([*full_line]) + "\n"
      
      # Save as csv line
      output_file.write(full_line_csv)
