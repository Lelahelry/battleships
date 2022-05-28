import game

# Game setup
gridsize = 10
shapes = {"Carrier":    [(True,True,True,True,True)],
          "Battleship": [(True,True,True,True)],
          "Cruiser":    [(True,True,True)],
          "Submarine":  [(True,True,True)],
          "Destroyer":  [(True,True)]
          }

P1_name, P2_name = "AI 1", "AI 2"
P1isAI, P2isAI = "", ""

while isinstance(P1isAI, str):
    P1isAI = input("Is player 1 an AI? (Yes/Y/y or No/N/n) ").lower()
    if P1isAI[0] == "y":
        P1isAI = True
    elif P1isAI[0] == "n":
        P1isAI = False
        P1_name = input("What's player 1's name? ")
    else:
        print("\nInvalid inputs, please try again.")

while isinstance(P2isAI, str):
    P2isAI = input("Is player 2 an AI?  (Yes/Y/y or No/N/n) ").lower()
    if P2isAI[0] == "y":
        P2isAI = True
    elif P2isAI[0] == "n":
        P2isAI = False
        P2_name = input("What's player 2's name? ")
    else:
        print("\nInvalid inputs, please try again.")


bat = game.battle(gridsize, shapes, P1_name, P2_name, P1isAI, P2isAI)
bat.start()