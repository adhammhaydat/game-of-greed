from math import gamma
import sys
#from game_logic import  Banker, scores
from game_of_greed.game_logic import  Banker, scores
from collections import Counter
from random import gammavariate, randint

class GameLogic:
    @staticmethod
    def get_scorers(test_input):
        scorers = []
        dice = Counter(test_input)
        for item, occ in dice.items():
            if scores[(item,occ)]:
                for i in range(occ):
                    scorers.append(item)
        return tuple(scorers)
        #return (filter(lambda x : x == 1 or x == 5,test_input))
    @staticmethod
    def roll_dice(num_dice):
        return tuple(randint(1, 6) for _ in range(0, num_dice))
    @staticmethod
    def calculate_score(dice):
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
        temp = dict(Counter(roll))
        for itm in keepers:
            if itm not in temp.keys():
                return False
            temp[itm]-=1
            if temp[itm] < 0:
                return False
        return True

class Quit(Exception):
    pass

class Game():

    def __init__(self):
        self.round = 1
        self.rolls = 6
        self.dice = ()
        self.dice_str = ''
        self.banked = False
        self.quit = False

    def outer_round(self, roller, banker):
        print(f"Starting round {self.round}")
        self.inner_round(roller, banker)
            

    def inner_round(self, roller, banker):
        self.dice = roller(self.rolls)
        self.dice_str = ' '.join(map(str, self.dice))
        print(f"Rolling {self.rolls} dice...")
        self.handle_cheating(roller, banker)


                
    def handle_cheating(self, roller, banker):
        print(f'*** {self.dice_str.strip()} ***')
        self.check_zilch(roller,banker)
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
                self.handle_cheating(roller, banker)
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
                #self.banked = True  
                self.outer_round(roller, banker)
                #return
            elif prompt == 'r':
                self.rolls = len(self.dice) - len(shelf)
                self.inner_round(roller, banker)
            elif prompt == 'q' or prompt == 'quit':
                print(f"Thanks for playing. You earned {banker.balance} points")
                raise Quit

    def check_zilch(self,roller,banker):
        if not GameLogic.calculate_score(self.dice):
            print("****************************************\n**        Zilch!!! Round over         **\n****************************************")
            print(f"You banked {0} points in round {self.round}")
            print(f"Total score is {banker.balance} points")
            self.round +=1
            self.rolls = 6
            self.outer_round(roller,banker)

    def play(self, roller = GameLogic.roll_dice):
        print("Welcome to Game of Greed")
        print("(y)es to play or (n)o to decline")
        start = input('> ').lower()
        if start == 'n' or start == 'no':
            print('OK. Maybe another time')
            return
        banker = Banker()
        try:
            self.outer_round(roller, banker)
        except Quit:
            return

if __name__ == "__main__":
    g = Game()
    g.play()