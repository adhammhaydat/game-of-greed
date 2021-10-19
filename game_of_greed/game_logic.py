from collections import Counter
from random import gammavariate, randint
scores = {
    # rule 1
    (1, 1): 100,
    (1, 2): 200,
    (1, 3): 1000,
    (1, 4): 2000,
    (1, 5): 3000,
    (1, 6): 4000,
    # ________________
    # rule 2
    (2, 1): 0,
    (2, 2): 0,
    (2, 3): 200,
    (2, 4): 400,
    (2, 5): 600,
    (2, 6): 800,
    # ________________
    # rule 3
    (3, 1): 0,
    (3, 2): 0,
    (3, 3): 300,
    (3, 4): 600,
    (3, 5): 900,
    (3, 6): 1200,
    # ________________
    # rule 4
    (4, 1): 0,
    (4, 2): 0,
    (4, 3): 400,
    (4, 4): 800,
    (4, 5): 1200,
    (4, 6): 1600,
    # ________________
    # rule 5
    (5, 1): 50,
    (5, 2): 100,
    (5, 3): 500,
    (5, 4): 1000,
    (5, 5): 1500,
    (5, 6): 2000,
    # ________________
    # rule 6
    (6, 1): 0,
    (6, 2): 0,
    (6, 3): 600,
    (6, 4): 1200,
    (6, 5): 1800,
    (6, 6): 2400,
}
class GameLogic:
    """
    A class holding game logic related methods like calculating the score, and generating a random dice roll
    """
    @staticmethod
    def get_scorers(test_input):
        """
        For filtering a tuple of choices so that only the dice that evaluates to some value is kept

        Args:
            test_input (tuple): A tuple representing a kept dice roll

        Returns:
            tuple: The dice that evaluates to something 
        """
        return (filter(lambda x : x == 1 or x == 5,test_input))
    @staticmethod
    def roll_dice(num_dice):
        """
        Roll a dice a number of time based on the input

        Args:
            num_dice (Integer): The number of dice to roll

        Returns:
            tuple: A tuple representing the rolls of n dices
        """
        return tuple(randint(1, 6) for _ in range(0, num_dice))
    @staticmethod
    def calculate_score(dice):
        """
        Calculate a score given a dice roll

        Args:
            dice (tuple): a tuple representing a dice roll

        Returns:
            Integer: Score of dice roll
        """
        dice = Counter(dice)
        if len(dice) == 6:
            return 1500
        elif len(dice) == 3 and len(list(filter(lambda itm: itm[1] == 2, dice.items()))) == 3:
            return 1500
        else:
            total = 0
            for item, occ in dice.items():
                total += scores[(item, occ)]
            return total
    @staticmethod
    def validate_keepers(roll, keepers):
        """
        Check if player is cheating or if made a typo

        Args:
            roll (tuple): a tuple representing a dice roll
            keepers (tuple): A tuple representing dice that is kept

        Returns:
            Boolean: True if valid, false otherwise
        """
        temp = dict(Counter(roll))
        for itm in keepers:
            if itm not in temp.keys():
                return False
            temp[itm]-=1
            if temp[itm] < 0:
                return False
        return True
class Banker():
    """
    A class representing a place to hold shelved dice and banked dice
    """
    def __init__(self):
        """
        The constructor method, initialize the properties balance and shelved
        """
        self.balance = 0
        self.shelved = 0
    def shelf(self, point):
        """
        Add kept dice to shelf

        Args:
            point (integer): The value of kept dice
        """
        self.shelved = point
    def bank(self):
        """
        Bank or add to the balance of the player when banking

        Returns:
            integer : The balance of the player
        """
        self.balance = self.balance+self.shelved
        self.clear_shelf()
        return self.balance
    def clear_shelf(self):
        """
        Set the shelf to zero, reset
        """
        self.shelved = 0
    def add_to_shelf(self,val):
        """
        Add to the shelf the value passed which is based on the evaluation of kept dice

        Args:
            val (integer): The amount to be shelved
        """
        self.shelved += val
class Game():
    """
    A class representing the game itself, it holds the logic necessary for the game to function
    """
    def __init__(self):
        """
        The constructor method, initialize necessary properties
        """
        self.round = 1
        self.rolls = 6
        self.cheated = False
        self.str_dice = ''
        self.on = False
    def handle_start(self):
        """
        Handle starting the game

        Returns:
            Banker or None : A banker instance or None if the game wont't start
        """
        print("Welcome to Game of Greed\n(y)es to play or (n)o to decline")
        start = input('> ').lower()
        if start != 'n' and start != 'no':
            self.on = True
            return Banker()
        return
    def play(self, roller = GameLogic.roll_dice):
        """
        The method to call when you actually want to play

        Args:
            roller (function, optional): A function for generating a dice roll given an integer. Defaults to GameLogic.roll_dice.
        """
        banker = self.handle_start()
        while self.on:
            print(f'Starting round {self.round}')
            while True:
                if not self.cheated:
                    print(f"Rolling {self.rolls} dice...")
                dice = roller(self.rolls)
                self.str_dice = ' '.join(map(str, dice)) if not self.cheated else self.str_dice
                print(f'*** {self.str_dice.strip()} ***')
                # need to check if the last roll evaluates to nothing
                # ***************************************************
                if not GameLogic.calculate_score(dice):
                    print("****************************************\n**        Zilch!!! Round over         **\n****************************************")
                    print(f"You banked {0} points in round {self.round}")
                    print(f"Total score is {banker.balance} points")
                    self.round += 1
                    self.rolls = 6
                    break
                print('Enter dice to keep, or (q)uit:')
                prompt = input("> ").lower()
                if prompt == 'q' or prompt == 'quit':
                    print(
                        f"Thanks for playing. You earned {banker.balance} points")
                    return
                else:
                    shelf = [int(n) for n in prompt if n != ' ']
                    #print(shelf)
                    # if values shelved violate what is correct continue
                    current_dice = Counter(dice)
                    if not GameLogic.validate_keepers(current_dice, shelf):
                        print("Cheater!!! Or possibly made a typo...")
                        self.cheated = True
                        continue
                    banker.add_to_shelf(GameLogic.calculate_score(shelf))
                    print(
                        f"You have {banker.shelved} unbanked points and {len(dice) - len(shelf)} dice remaining")
                    print("(r)oll again, (b)ank your points or (q)uit:")
                    prompt = input("> ")
                    if prompt == "b":
                        self.rolls = len(dice) - len(shelf)
                        print(
                            f"You banked {banker.shelved} points in round {self.round}")
                        banker.bank()
                        print(f"Total score is {banker.balance} points")
                        self.round += 1
                        self.rolls = 6
                        break
                    elif prompt == 'r':
                        self.rolls = len(dice) - len(shelf)
                        if not self.rolls:
                            self.rolls = 6
                            continue
                        continue
                    elif prompt == 'q':
                        print(f"Thanks for playing. You earned {banker.balance} points")
        print('OK. Maybe another time')
if __name__ == "__main__":
    g = Game()
    g.play()