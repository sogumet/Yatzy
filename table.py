"""Table module"""
from tabulate import tabulate

class Tableprint:
    """Class for printing ta"""
    def __init__(self):
        self.head = ["Yatzy", "Välj"]
        self.one = ["Ettor", 1]
        self.two = ["Tvåor", 2]
        self.three = ["Treor", 3]
        self.four = ["Fyror", 4]
        self.five = ["Femmor", 5]
        self.six = ["Sexor", 6]
        self.sum = ["Summa",  ]
        self.bonus = ["Bonus", ]
        self.pair = ["Par", 7]
        self.two_pair = ["Två par", 8]
        self.three_of = ["Triss", 9]
        self.four_of = ["Fyrtal", 10]
        self.full_house = ["Kåk", 11]
        self.small = ["Liten", 12]
        self.big = ["Stor", 13]
        self.chanse = ["Chans", 14]
        self.yatzy = ["Yatzy", 15]
        self.total = ["Total", ]

        self.table = [self.head, self.one, self.two, self.three, self.four, self.five,
        self.six, self.sum, self.bonus, self.pair, self.two_pair, self.three_of,
        self.four_of, self.full_house, self.small, self.big, self.chanse,
        self.yatzy, self.total]

    def print(self, players):
        """Printing the scoreboard"""
        for i, player in enumerate(players):
            self.head.insert(i+1, player.board["name"])
            self.one.insert(i+1, player.board["1"])
            self.two.insert(i+1, player.board["2"])
            self.three.insert(i+1, player.board["3"])
            self.four.insert(i+1, player.board["4"])
            self.five.insert(i+1, player.board["5"])
            self.six.insert(i+1, player.board["6"])
            self.sum.insert(i+1, player.board["sum"])
            self.bonus.insert(i+1, player.board["bonus"])
            self.pair.insert(i+1, player.board["pair"])
            self.two_pair.insert(i+1, player.board["twoPair"])
            self.three_of.insert(i+1, player.board["threeOf"])
            self.four_of.insert(i+1, player.board["fourOf"])
            self.full_house.insert(i+1, player.board["fullHouse"])
            self.small.insert(i+1, player.board["small"])
            self.big.insert(i+1, player.board["big"])
            self.chanse.insert(i+1, player.board["chanse"])
            self.yatzy.insert(i+1, player.board["yatzy"])
            self.total.insert(i+1, player.board["total"])

        print(tabulate(self.table, headers="firstrow",missingval="", tablefmt="fancy_grid"))
