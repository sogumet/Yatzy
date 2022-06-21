import random

class Dice():
    """Dice"""

    def __init__(self):
        """Init"""
        self.value = random.randint(1,6)

    def roll(self):
        """Return value"""
        self.value = random.randint(1,6)

class Hand():
    """Hand"""
    
    def __init__(self):
        """init"""
        self.hand = []
        for x in range(5):
            self.hand.append(Dice())