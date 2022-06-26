"""Module score"""
class Score:
    """Score class for score board"""
    def __init__(self, name):
        """ Initialize class """
        self.board = {"name": name, "1": "", "2": "", "3": "", "4": "",
        "5": "", "6": "", "sum": "", "bonus": "", "pair": "", "twoPair": "",
        "three": "", "four": "", "fullHouse": "", "small": "",
        "large": "", "chanse": "", "yatzy": "", "total": "", "hidden": 0 }
