import game

# First, define game constants.
gridsize = 10
shapes = {"Carrier":    [(True,True,True,True,True)],
          "Battleship": [(True,True,True,True)],
          "Cruiser":    [(True,True,True)],
          "Submarine":  [(True,True,True)],
          "Destroyer":  [(True,True)]
          }

# Then, put default values for the parameters.
P1_name, P2_name = "AI 1", "AI 2"
P1isAI, P2isAI = None, None

# Prompt the users to choose the parameters of the game.
while P1isAI is None:
    inp = input("Is player 1 an AI? (Yes/Y/y or No/N/n) ").lower()
    if inp[0] == "y":
        P1isAI = True
    elif inp[0] == "n":
        P1isAI = False
        P1_name = input("What's player 1's name? ")
    else:
        print("\nInvalid inputs, please try again.")

while P2isAI is None:
    P2isAI = input("Is player 2 an AI?  (Yes/Y/y or No/N/n) ").lower()
    if inp[0] == "y":
        P2isAI = True
    elif inp[0] == "n":
        P2isAI = False
        P2_name = input("What's player 2's name? ")
    else:
        print("\nInvalid inputs, please try again.")

# Finally, create the game with the given parameters and start it.
bat = game.battle(gridsize, shapes, P1_name, P2_name, P1isAI, P2isAI)
bat.start()