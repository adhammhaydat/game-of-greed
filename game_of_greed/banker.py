
class Banker():
    """
    A class for holding the functionality of updating the shelf and the player's balance
    """
    def __init__(self):
        """
        The constructor method
        """
        self.balance = 0
        self.shelved = 0
    def shelf(self, point):
        """
        Add points to the shelf

        Args:
            point (int): The amount of shelved dice
        """
        self.shelved += point
    def bank(self):
        """
        Add the shelved value to the balance of the player

        Returns:
            int : Player's balance
        """
        self.balance = self.balance+self.shelved
        self.clear_shelf()
        return self.balance
    def clear_shelf(self):
        """
        Set the shelf to zero
        """
        self.shelved = 0