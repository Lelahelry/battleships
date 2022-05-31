import os
import time
import random
import functions as f
class ship:
    """
    Class which manages the shape and attributes of ships on the map.
    """
    def __init__(self, name: str, shape: list[tuple[bool, ...]]):
        """
        Ship initialization, needs a name and shape
        """
        self.name = name
        self.shape = shape
        self.sunk = False
        self.placed = False

    def __str__(self):
        """
        Returns string representation of the ship for text mode
        """
        lines = [" __"*len(self.shape[0])] + ["|" + "".join(["██|" if cell else "__|" for cell in row]) for row in self.shape]
        return "\n".join(lines)

    def clockwise_rotate(self):
        """
        Rotates ship list representation to the right
        """
        assert not self.placed, "Ship is anchored, cannot be rotated anymore!"

        self.shape = list(zip(*self.shape[::-1]))

    def anticlockwise_rotate(self):
        """
        Rotates ship list representation to the right.
        Redundant with clockwise_rotate if ships are linear but useful if they are not.
        """
        assert not self.placed, "Ship is anchored, cannot be rotated anymore!"
        
        self.shape = list(zip(*self.shape))[::-1]
    
    def place(self, positions: set[tuple[int, int]]):
        """
        Updates a ship as placed.
        """
        self.positions = {cellpos: True for cellpos in positions}
        self.placed = True

    def damage(self, xtar: int, ytar: int):
        """
        Handles shooting a ship and returns the associated cell state. S for sunk and H for hit
        """
        assert (ytar, xtar) in self.positions.keys(), "Position already hit."

        self.positions[(ytar, xtar)] = False
        if not (True in self.positions.values()):
            hit = 'S'
            self.sunk = True
        else:
            hit = 'H'
        
        return hit


class player:
    """
    This class represents a full battleships player, with the associated actions it can take and its own battlefield.
    """
    def __init__(self, name: str, gridsize: int, ships: list[ship], isAI: bool=False):
        """
        Simple player constructor.
        """
        self.name = name
        self.ships = ships
        self.isAI = isAI
        self.alive = True
        self.opponent = None
        self.map = [["WU"] * gridsize for _ in range(gridsize)] # All cells start out like this, W means water and U means unhit.
        self.hits = [None]
        self.graphical_parameters = None

    def set_opponent(self, opponent: 'player'):
        """
        Sets the player's opponent for upcoming game.
        """
        self.opponent = opponent
    
    def strmap(self, *, full: bool=False):
        """
        Returns string representation of the player's battlefield for text mode.
        Either full one for ship placement and endgame or hidden one which only shows known positions.
        """
        lines = ["  " + ''.join([f" {j:2}" for j in range(len(self.map[0]))])]
        if full:
            lines += [f"{i} |" + ''.join(["__|" if cell[:-1] == 'W' else "()|" if cell[-1] == 'M' else "##|" if cell[-1] == "H" else "░░|" if cell[-1] == "S" else "██|" for cell in row]) for i, row in enumerate(self.map)]
        else:
            lines += [f"{i} |" + ''.join(["__|" if cell[-1] == 'U' else "()|" if cell[-1] == 'M' else "##|" if cell[-1] == "H" else "░░|" for cell in row]) for i, row in enumerate(self.map)]
        
        return "\n".join(lines)
    
    def place_ship(self, xpos: int, ypos: int, ship: ship, occupied_positions: set[tuple[int, int]], *, verbose: bool=True):
        """
        Method which validates ship placement, returns set containing its positions if valid, else returns empty set.
        Is able to print warning messages or not, depending on where it is used.
        """
        ship_positions = {(ypos + i, xpos + j) for i, row in enumerate(ship.shape) for j, cell in enumerate(row) if cell}
        
        if not occupied_positions.isdisjoint(ship_positions):
            if verbose:
                os.system("clear||cls")
                print("\nCannot have ships overlapping, please try again.")
            return set()
        else:
            for ypos, xpos in ship_positions:
                if not (0 <= xpos < len(self.map[0]) and 0 <= ypos < len(self.map)):
                    if verbose:
                        os.system("clear||cls")
                        print("\nCannot place ship out of bounds, please try again.")
                    return set()
            
            return ship_positions
    
    def target_check(self, xtar: int, ytar: int, *, verbose: bool=True):
        """
        Method which validates given targets for upcoming shot.
        Is able to print warning messages or not, depending on where it is used.
        """
        if not (0 <= xtar < len(self.map[0])) or not (0 <= ytar < len(self.map)):
            if verbose:
                os.system("clear||cls")
                print("\nTarget is out of bounds, please try again.")
            return False
        elif self.map[ytar][xtar][-1] != 'U':
            if verbose:
                os.system("clear||cls")
                print("\nTarget has already been hit, please try again.")
            return False
        else:
            return True
    
    def setup(self, *, graphical: bool = False):
        """
        First big gameplay loop corresponding to setup phase.
        Handles the full determination of a player's battlefield, be it in text mode or graphical mode, AI player or real one.
        """
        if self.isAI: # AI player branch.
            print(f"{self.name} is setting up its battlefield.")
            occupied_positions = set() # Set of all occupied positions of the player's boats, starts empty.
            for idx, ship in enumerate(self.ships):
                rotate_choice = bool(random.randint(0, 1)) # Decision to rotate is randomly determined.
                if rotate_choice:
                    ship.clockwise_rotate()
                
                ship_positions = set() # Set of current ship placed positions, starts empty.
                while ship_positions == set():
                    if graphical:
                        pass
                    
                    # AI chooses a random spot to place its ship, which may or may not be valid
                    # It then tries to place its ship, and if it doesn't work it'll go through the same process again in the next loop iteration.
                    xanchor, yanchor = random.randint(0, len(self.map[0])), random.randint(0, len(self.map))
                    ship_positions = self.place_ship(xanchor, yanchor, ship, occupied_positions, verbose=False)
                
                # Updating the actual map with definitive positions of the ship.
                # The ID of the ship is associated with unhit status in the map cell.
                for ypos, xpos in ship_positions:
                    self.map[ypos][xpos] = str(idx) + 'U'
                
                # Finally, the ship object itself is updated.
                # As is the set of occupied positions that is filled with the positions of the recently placed ship.
                ship.place(ship_positions)
                occupied_positions.update(ship_positions)
            
            print(f"\n{self.name} has placed its ships!\n")
            time.sleep(1.5)
        else: # Real player branch
            occupied_positions = set() # Set of all occupied positions of the player's boats, starts empty.
            for idx, ship in enumerate(self.ships):
                ship_positions = set()  # Set of current ship placed positions, starts empty.
                while ship_positions == set():
                    if graphical:
                        xpos, ypos = f.get_graphical_pos(**self.graphical_parameters)
                        
                        
                        ship_positions = self.place_ship(xpos, ypos, ship, occupied_positions)
                    else:
                        print(f"\n{self.name}, here's your battlefield's in its current state:\n")
                        print(self.strmap(full=True))
                        print("\nYou're gonna place this ship:")
                        print(ship, "\n")
                        print("To rotate it to the right or left, press R/r or L/l, else enter the desired coordinates for its top-left corner.")
                        inp1 = input("Anchor horizontal position (or rotate command): ").lower()
                        if inp1 == 'r':
                            ship.clockwise_rotate()
                        elif inp1 == 'l':
                            ship.anticlockwise_rotate()
                        elif inp1.isdecimal():
                            inp2 =  input("Anchor vertical position: ").lower()
                            if inp2.isdecimal():
                                ship_positions = self.place_ship(int(inp1), int(inp2), ship, occupied_positions)
                            else:
                                os.system("clear||cls")
                                print("\nInvalid inputs, please try again.")
                        else:
                            os.system("clear||cls")
                            print("\nInvalid inputs, please try again.")
                
                # Updating the actual map with definitive positions of the ship.
                # The ID of the ship is associated with unhit status in the map cell.
                for ypos, xpos in ship_positions:
                    self.map[ypos][xpos] = str(idx) + 'U'
                
                # Finally, the ship object itself is updated.
                # As is the set of occupied positions that is filled with the positions of the recently placed ship.
                ship.place(ship_positions)
                occupied_positions.update(ship_positions)
                print(f"\n{self.name}'s ship, {ship.name} #{idx} has been successfully placed!")
            
            print(f"\n{self.name}, here's your full battlefield:\n")
            print(f"{self.strmap(full=True)}")
            time.sleep(3)
        
        os.system("clear||cls")

    def play(self, *, graphical: bool = False):
        """
        Main gameplay loop corresponding to the battle phase.
        Again, handles human, AI and graphical playing.
        """
        target_valid = False
        if self.isAI: # AI player branch
            while not target_valid:
                # Last hit being None means no hit has happened yet or the last one was inexploitable.
                if self.opponent.hits[-1] is None:
                    # in this case, simply shoot at random.
                    xtar, ytar = random.randint(0, len(self.map[0])), random.randint(0, len(self.map))
                    target_valid = self.opponent.target_check(xtar, ytar, verbose=False)
                # Use last hit to determine the next one
                else:
                    yprev, xprev = self.opponent.hits[-1]
                    # List 4 adjacent postions to last hit
                    possible_offsets = [(xprev - 1, yprev), (xprev + 1 , yprev), (xprev, yprev - 1), (xprev, yprev + 1)]
                    # Eliminate invalid ones
                    valid_offsets = [(xoff, yoff) for xoff, yoff in possible_offsets if self.opponent.target_check(xoff, yoff, verbose=False)]

                    # If no valid positions remain, then the last hit is useless, hence append None.
                    if valid_offsets == []:
                        self.opponent.hits.append(None)
                    else:
                        # If the last two hits are in line, then assign highest priority to the move continuing the line (if valid)
                        if not self.opponent.hits[-2] is None:
                            yprev2, xprev2 = self.opponent.hits[-2]
                            ydir, xdir = yprev - yprev2, xprev - xprev2

                            best_target = (xprev + xdir, yprev + ydir)
                            if best_target in valid_offsets:
                                valid_offsets.remove(best_target)
                                valid_offsets.insert(0, best_target)
                        
                        # If a considered target is surrounded by hits, then assign lowest priority to it.
                        for i, (xoff, yoff) in enumerate(valid_offsets):
                            surroundings = {(xoff - 1, yoff), (xoff + 1 , yoff), (xoff, yoff - 1), (xoff, yoff + 1)}

                            if surroundings.issubset(self.opponent.hits):
                                valid_offsets.append(valid_offsets.pop(i))
                        
                        # Finally, select first valid target because it has highest priority.
                        xtar, ytar = valid_offsets[0]
                        target_valid = True
        else: # Real player branch
            while not target_valid:
                if graphical:
                    pass
                else:
                    print(f"\n{self.name}, this is what you know about {self.opponent.name}'s battlefield:\n")
                    print(self.opponent.strmap())
                    print("\nPlease choose a cell to target.")
                    inp1 = input("Target horizontal position: ")
                    if inp1.isdecimal():
                        inp2 = input("Target vertical position: ")
                        if inp2.isdecimal():
                            xtar, ytar = int(inp1), int(inp2)
                            target_valid = self.opponent.target_check(xtar, ytar)
                        else:
                            os.system("clear||cls")
                            print("\nInvalid inputs, please try again.")
                    else:
                        os.system("clear||cls")
                        print("\nInvalid inputs, please try again.")
        
        self.opponent.get_shot(xtar, ytar)
        print(f"\nHere's {self.opponent.name}'s battlefield after this shot:\n")
        print(self.opponent.strmap())
        time.sleep(1.5)
        os.system("clear||cls")

    def get_shot(self, xtar: int, ytar: int):
        """
        Method which defines the action of being shot at by the other player.
        """
        assert self.map[ytar][xtar][-1] == 'U', f"Position ({ytar}, {xtar}) already hit." # Check that the target is unhit

        # If target is water, then shot is a miss.
        if self.map[ytar][xtar][:-1] == 'W':
            self.map[ytar][xtar] = self.map[ytar][xtar][:-1] + 'M'
            print(f"\nX: {xtar}, Y: {ytar} // MISS!")
        else:
            # Target is a boat, hence store id of the boat and type of hit.
            id = self.map[ytar][xtar][:-1]
            hit = self.ships[int(id)].damage(xtar, ytar)
            self.map[ytar][xtar] = id + hit

            # If boat is sunk, mark all its cells as sunk and check if player should still be alive.
            if hit == 'S':
                self.last_hit = None
                for ypos, xpos in self.ships[int(id)].positions.keys():
                    self.map[ypos][xpos] = self.map[ypos][xpos][:-1] + hit
                print(f"\nX: {xtar}, Y: {ytar} // SUNK!")

                self.alive = False
                i, n = 0, len(self.ships)
                while not self.alive and i < n:
                    if not self.ships[i].sunk:
                        self.alive = True
                    else: i += 1
            # Boat is simply hit, nothing fancy happens.
            else:
                self.hits.append((ytar, xtar))
                print(f"\nX: {xtar}, Y: {ytar} // HIT!")

class battle:
    """
    Class which represents an individual game of battleships and controls its flow.
    """
    def __init__(self, gridsize: int, possible_ships: dict[str, list[tuple[bool, ...]]], P1_name: str, P2_name: str, P1isAI: bool = False, P2isAI: bool = False):
        """
        Simple constructor for battle object.
        """
        self.gridzise = gridsize

        P1_ships = [ship(name, shape) for name, shape in possible_ships.items()]
        P2_ships = [ship(name, shape) for name, shape in possible_ships.items()]

        self.player1 = player(P1_name, gridsize, P1_ships, P1isAI)
        self.player2 = player(P2_name, gridsize, P2_ships, P2isAI)

        self.player1.set_opponent(self.player2)
        self.player2.set_opponent(self.player1)
    
    def start(self, *, graphical: bool = False, **graphical_parameters):
        """
        Overarching gameplay loop of a battleships game, executes all portions of it from start to finish
        """
        self.player1.graphical_parameters = graphical_parameters
        self.player2.graphical_parameters = graphical_parameters

        os.system("clear||cls")
        print("Let the game begin!\n")

        # Ship placement procedure, both players set up their battlefied one after the other.
        self.player1.setup(graphical=graphical)
        self.player2.setup(graphical=graphical)

        # Start of actual game
        # Loop stops when a winner is designated.
        winner = None
        while winner is None:
            self.player1.play(graphical=graphical)
            if not self.player2.alive: # If player 2 has died, then played 1 is the winner
                winner = self.player1
            else: # Else player 2 can play its round
                self.player2.play(graphical=graphical)
                if not self.player1.alive: # If player 1 has died, then played 2 is the winner
                    winner = self.player2
        
        print(f"\n{winner.name}, you won the game!")
        print("\nAfter the battle, your battlefield looks like this:\n")
        print(winner.strmap(full=True))
        print(f"\nAnd here's how {winner.opponent.name}'s battlefield ended up:\n")
        print(winner.opponent.strmap(full=True))
        print("\nThanks for playing our game!")