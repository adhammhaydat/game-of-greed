from random import randint

class GameLogic:
    game_rolls={}
    def __init__(self):
        pass
    @staticmethod
    def calculate_score(cls,dice_roll):
        pass
    
    @staticmethod    
    def roll_dice(num_dice):
        return tuple(randint(1,6) for _ in range(0,num_dice))
    

class Banker():
    def __init__(self) :
        pass
    def shelf(self):
        pass
    def banik(self):
        pass
    def clear_shelf(self):
        pass
# print(GameLogic.roll_dice(6))    
# print(GameLogic.roll_dice(6))  