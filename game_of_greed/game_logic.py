from random import gammavariate, randint
from collections import Counter
#from tests.flo import diff
scors = {
    "three_paris": 1500,
    "stright": 1500,
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
    # game_rolls={}
    def __init__(self):
        pass

    @staticmethod
    def roll_dice(num_dice):
        return tuple(randint(1, 6) for _ in range(0, num_dice))

    @staticmethod
    def calculate_score(dice):
        dice = Counter(dice)
        if len(dice) == 0:
            return 0
        elif len(dice) == 6: 
            return 1500
        elif len(dice) == 3 and len(list(filter(lambda itm: itm[1] == 2, dice.items()))) == 3: 
            return 1500
        else:
            total = 0
            for item, occ in dice.items():
                total += scors[(item, occ)]
            return total


class Banker():
    def __init__(self, balance=0, shelved=0):
        self.balance = balance
        self.shelved = shelved

    def shelf(self, point):
        self.shelved = point

    def bank(self):
        self.balance = self.balance+self.shelved
        self.clear_shelf()
        return self.balance

    def clear_shelf(self):
        self.shelved = 0

class Game():
    
    def play(self, roller = GameLogic.roll_dice):
        print("""Welcome to Game of Greed
(y)es to play or (n)o to decline""")
        start = input('> ').lower()
        round = 1
        if start != 'n' and start != 'no':
            banker = Banker()
            while True:
                
                print(f'Starting round {round}')
                print("Rolling 6 dice...")
                dice = roller(6)
                str_dice = ' '.join(map(str, dice))
                print(f'*** {str_dice.strip()} ***')
                print('Enter dice to keep, or (q)uit:')
                prompt = input("> ").lower()
                if prompt == 'q' or prompt == 'quit':
                    print(f"Thanks for playing. You earned {banker.balance} points")
                    break 
                else:
                    shelve = [int(n) for n in prompt]
                    dice_remaining = len(dice) - len(shelve)
                    sum_shelved = GameLogic.calculate_score(shelve)
                    print(f"You have {sum_shelved} unbanked points and {dice_remaining} dice remaining")
                    print("(r)oll again, (b)ank your points or (q)uit:")
                    prompt = input("> ")
                    if prompt == "b":
                        banker.shelf(sum_shelved)
                        banker.bank()
                        print(f"You banked {sum_shelved} points in round {round}")
                        print(f"Total score is {banker.balance} points")
                        round+=1

        else:
            print('OK. Maybe another time')
        
        



# if __name__ == "__main__":
#     g = Game()
#     g.play()
