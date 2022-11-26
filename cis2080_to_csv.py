import pandas as pd

real_num_responses = 17616

# Expeced num of characters per card in the poll.
cells_per_card = {1:78, 2:79, 3:80, 4:78, 5:84} # For card 5, exclude anything over 84
                                                # as there aren't proper labels.


def get_card(card, card_num):
      # Gets a card as a str and the expected number for this card.
      # Enforces expected length and checks format.
      # Then returns the updated card.
      
      # Enforce min length
      extra_spaces = cells_per_card[j+1] - len(card)
      card = card + " "*extra_spaces

      # Enforce max length
      card = card[:cells_per_card[j+1]]
      
      # Check format
      if (card[:12] != " "*10 + str(card_num)):
        raise Exception("Format error, expected card {}, got line: {}").format(card_num, card))
      
      # Remove first spaces and card number
      card = card[11:]
      
      return(card)


with open("DA2080", "r") as f:
  num_responses = sum(1 for line in f)/5

with open("DA2080", "r") as f:
  if (num_responses != real_num_responses):
    raise Exception("Error in the number of responses. Expected {}, got {}".format(real_num_responses,
                                                                                   num_responses))

  # Limit responses for testing:
  num_responses = 1
  
  for i in range(num_responses):
    full_line = ""
    for j in range(5):
      card = f.readline()[:-1]
      
      full_line = full_line + get_card(card, j+1)
    
    # Hay que guardar en algun lado esta full_line
    


  

print(cards)

