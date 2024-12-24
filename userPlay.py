import random

class Door:
    def __init__(self, number):
        self.number = number
        self.isOpen = False
        self.prize = None
        self.picked = None

class Monty:
    def reveal_goat(self, doors, user_choice):
        # Collect all doors with goats that are not chosen by the user and are not already open
        goat_doors = [door for door in doors if door.prize == 'Goat' and door.number != user_choice + 1 and not door.isOpen]
        
        # Randomly select a door from the available goat doors
        revealed_goat = random.choice(goat_doors)
        
        return revealed_goat.number
class Agent:
    def choose_door(self):
        return int(input("Choose a door (1, 2, or 3): ")) - 1

class Game:
    def __init__(self):
        self.doors = [Door(i+1) for i in range(3)]
        self.monty = Monty()
        self.agent = Agent()

    def initialize_game(self):
        # Randomly assign the car behind one door and goats behind the others
        prizes = ['Car', 'Goat', 'Goat']
        random.shuffle(prizes)
        for door, prize in zip(self.doors, prizes):
            door.prize = prize

    def play(self):
        print("Welcome to the Monty Hall game!")
        print("Behind one of these doors is a car, and behind the others are goats.")
        print("You get to choose one door, and then Monty will reveal one of the doors hiding a goat.")
        print("You'll then have the option to stick with your initial choice or switch to the other unopened door.")

        self.initialize_game()

        # User chooses a door
        user_choice = self.agent.choose_door()

        # Monty reveals a door hiding a goat
        revealed_goat_number = self.monty.reveal_goat(self.doors, user_choice)
        print(f"Monty reveals a goat behind door {revealed_goat_number}.")

        # User decides whether to stick with their initial choice or switch
        switch = input("Do you want to switch doors? (yes/no): ").lower().strip() == 'yes'

        if switch:
            # User switches to the unopened door
            for door in self.doors:
                if door.number != user_choice + 1 and door.number != revealed_goat_number:
                    user_choice = door.number - 1
                    break

        # Determine the outcome
        if self.doors[user_choice].prize == 'Car':
            print("Congratulations! You won the car!")
        else:
            print("Sorry, you got a goat.")

if __name__ == "__main__":
    game = Game()
    game.play()
