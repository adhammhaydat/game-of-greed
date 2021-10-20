from collections import Counter
from random import randint
# pytest and bot
from game_of_greed.scores import scores
# run
#from scores import scores

class GameLogic:
    """
    A class holding methods for handling game logic like calculations and handling dice rolls
    """
    @staticmethod
    def get_scorers(test_input):
        """
        Checks for the dice that evaluates to something

        Args:
            test_input (tuple): The dice to check

        Returns:
            tuple : The dice that actually evaluates to something
        """
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
        """
        Generate a dice roll given a number of rolls

        Args:
            num_dice (int): The number of dice to roll

        Returns:
            tuple : a set of dice
        """
        return tuple(randint(1, 6) for _ in range(0, num_dice))
    @staticmethod
    def calculate_score(dice):
        """
        To calculate the value of a dice

        Args:
            dice (tuple): a tuple of dice

        Returns:
            int : the value of the dice
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
        Similar to get scorers, but also used to check if player is cheating

        Args:
            roll (tuple): The actual dice
            keepers (tuple): The dice kept or shelved

        Returns:
            boolean : True if the kept dice is valid False otherwise
        """
        temp = dict(Counter(roll))
        for itm in keepers:
            if itm not in temp.keys():
                return False
            temp[itm]-=1
            if temp[itm] < 0:
                return False
        return True

        


# class Game():
#     def __init__(self):
#         self.round = 1
#         self.rolls = 6
#         self.cheated = False
#         self.str_dice = ''
#         self.on = False
#     # def handle_start(self):
#     #     print("Welcome to Game of Greed")
#     #     print("(y)es to play or (n)o to decline")
#     #     start = input('> ').lower()
#     #     if start != 'n' and start != 'no':
#     #         self.on = True
#     #         return Banker()
#     #     return
#     def play(self, roller = GameLogic.roll_dice):
#         print("Welcome to Game of Greed")
#         print("(y)es to play or (n)o to decline")
#         start = input('> ').lower()
#         if start != 'n' and start != 'no':
#             self.on = True
#             banker = Banker()


#         while self.on:
#             print(f'Starting round {self.round}')
#             while True:
#                 if not self.cheated:
#                     print(f"Rolling {self.rolls} dice...")
#                 dice = roller(self.rolls)
#                 self.str_dice = ' '.join(map(str, dice)) if not self.cheated else self.str_dice
#                 print(f'*** {self.str_dice.strip()} ***')
#                 # need to check if the last roll evaluates to nothing
#                 # ***************************************************
#                 if not GameLogic.calculate_score(dice):
#                     print("****************************************\n**        Zilch!!! Round over         **\n****************************************")
#                     print(f"You banked {0} points in round {self.round}")
#                     print(f"Total score is {banker.balance} points")
#                     self.round += 1
#                     self.rolls = 6
#                     break
#                 print('Enter dice to keep, or (q)uit:')
#                 prompt = input("> ").lower()
#                 if prompt == 'q' or prompt == 'quit':
#                     print(
#                         f"Thanks for playing. You earned {banker.balance} points")
#                     return
#                 else:
#                     shelf = [int(n) for n in prompt if n.isdigit()]
#                     #print(shelf)
#                     # if values shelved violate what is correct continue
#                     current_dice = Counter(dice)
#                     if not GameLogic.validate_keepers(current_dice, shelf):
#                         print("Cheater!!! Or possibly made a typo...")
#                         self.cheated = True
#                         continue
#                     banker.add_to_shelf(GameLogic.calculate_score(shelf))
#                     print(
#                         f"You have {banker.shelved} unbanked points and {len(dice) - len(shelf)} dice remaining")
#                     print("(r)oll again, (b)ank your points or (q)uit:")
#                     prompt = input("> ")
#                     if prompt == "b":
#                         self.rolls = len(dice) - len(shelf)
#                         print(
#                             f"You banked {banker.shelved} points in round {self.round}")
#                         banker.bank()
#                         print(f"Total score is {banker.balance} points")
#                         self.round += 1
#                         self.rolls = 6
#                         break
#                     elif prompt == 'r':
#                         self.rolls = len(dice) - len(shelf)
#                         if not self.rolls:
#                             self.rolls = 6
#                             continue
#                         continue
#                     elif prompt == 'q':
                        
#                         print(f"Thanks for playing. You earned {banker.balance} points")
#                         return
#         print('OK. Maybe another time')

# if __name__ == "__main__":
#     g = Game()
#     g.play()