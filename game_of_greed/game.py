from collections import Counter
# pytest and bot
from game_of_greed.game_logic import GameLogic
from game_of_greed.banker import Banker

# run
#from game_logic import GameLogic
#from banker import Banker

class Quit(Exception):
    """
    A custom exception, just for navigation purposes

    Args:
        Exception (Class): Exception
    """
    pass

class Game():
    """
    A class holding the logic necessary for the game to function
    """

    def __init__(self):
        """
        The constructor method
        """
        self.round = 1
        self.rolls = 6
        self.dice = ()
        self.dice_str = ''
        self.banked = False
        self.quit = False

    def _outer_round(self, roller, banker):
        """
        A function for handling the part concerned with starting new rounds.

        Args:
            roller (function): The function that takes a number and returns a tuple of random dices.
            banker (Banker): For handling banking and shelving of points
        """
        print(f"Starting round {self.round}")
        self._inner_round(roller, banker)
            

    def _inner_round(self, roller, banker):
        """
        For handling the inner part of a round, all cases that might happen in a round

        Args:
            roller (function): The function that takes a number and returns a tuple of random dices.
            banker (Banker): For handling banking and shelving of points
        """
        self.dice = roller(self.rolls)
        self.dice_str = ' '.join(map(str, self.dice))
        print(f"Rolling {self.rolls} dice...")
        self._handle_cheating(roller, banker)


                
    def _handle_cheating(self, roller, banker):
        """
        A nested part of a round that handles the alternative path when the user cheats or makes a typo

        Args:
            roller (function): The function that takes a number and returns a tuple of random dices.
            banker (Banker): For handling banking and shelving of points

        Raises:
            Quit: A custom exception just for navigating to a certain level.
        """
        print(f'*** {self.dice_str.strip()} ***')
        self._check_zilch(roller,banker)
        print('Enter dice to keep, or (q)uit:')
        prompt = input("> ").lower()
        if prompt == 'q' or prompt == 'quit':
            print(
            f"Thanks for playing. You earned {banker.balance} points")
            raise Quit
        else:
            shelf = [int(n) for n in prompt if n.isdigit()]
            current_dice = Counter(self.dice)

            if not GameLogic.validate_keepers(current_dice, shelf):
                print("Cheater!!! Or possibly made a typo...")
                self._handle_cheating(roller, banker)
            banker.shelf(GameLogic.calculate_score(shelf))
            
            print(f"You have {banker.shelved} unbanked points and {len(self.dice) - len(shelf)} dice remaining")
            print("(r)oll again, (b)ank your points or (q)uit:")
            prompt = input("> ")

            if prompt == "b":
                self.rolls = len(self.dice) - len(shelf)
                print(f"You banked {banker.shelved} points in round {self.round}")
                banker.bank()
                print(f"Total score is {banker.balance} points")
                self.round += 1
                self.rolls = 6
                self._outer_round(roller, banker)
            elif prompt == 'r':
                if GameLogic.calculate_score(shelf) == 1500:
                    self.rolls = 6
                    self._inner_round(roller, banker)
                self.rolls = len(self.dice) - len(shelf)
                self._inner_round(roller, banker)
            elif prompt == 'q' or prompt == 'quit':
                print(f"Thanks for playing. You earned {banker.balance} points")
                raise Quit

    def _check_zilch(self,roller,banker):
        """
        For handling a zilch case

        Args:
            roller (function): The function that takes a number and returns a tuple of random dices.
            banker (Banker): For handling banking and shelving of points
        """
        if not GameLogic.calculate_score(self.dice):
            print("****************************************\n**        Zilch!!! Round over         **\n****************************************")
            print(f"You banked {0} points in round {self.round}")
            print(f"Total score is {banker.balance} points")
            self.round +=1
            self.rolls = 6
            self._outer_round(roller,banker)

    def play(self, roller = GameLogic.roll_dice):
        """
        The main function for starting the game

        Args:
            roller (function, optional): The function that takes a number and returns a tuple of random dices. Defaults to GameLogic.roll_dice.
        """
        print("Welcome to Game of Greed")
        print("(y)es to play or (n)o to decline")
        start = input('> ').lower()
        if start == 'n' or start == 'no':
            print('OK. Maybe another time')
            return
        banker = Banker()
        try:
            self._outer_round(roller, banker)
        except Quit:
            return

if __name__ == "__main__":
    g = Game()
    g.play()