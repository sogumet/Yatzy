from tabulate import tabulate
from score import Score


class Tableprint:
        

        

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
                self.twoPair = ["Två par", 8]
                self.threeOf = ["Triss", 9]
                self.fourOf = ["Fyrtal", 10]
                self.fullHouse = ["Kåk", 11]
                self.small = ["Liten", 12]
                self.big = ["Stor", 13]
                self.chanse = ["Chans", 14]
                self.yatzy = ["Yatzy", 15]
                self.total = ["Total", ]

                self.Table = [self.head, self.one, self.two, self.three, self.four, self.five, 
                self.six, self.sum, self.bonus, self.pair, self.twoPair, self.threeOf,
                self.fourOf, self.fullHouse, self.small, self.big, self.chanse,
                self.yatzy, self.total]

        def print(self, player):
                for i in range(len(player)):
                        self.head.insert(i+1, player[i].board["name"]) 
                        self.one.insert(i+1, player[i].board["1"]) 
                        self.two.insert(i+1, player[i].board["2"]) 
                        self.three.insert(i+1, player[i].board["3"])
                        self.four.insert(i+1, player[i].board["4"]) 
                        self.five.insert(i+1, player[i].board["5"]) 
                        self.six.insert(i+1, player[i].board["6"]) 
                        self.sum.insert(i+1, player[i].board["sum"]) 
                        self.bonus.insert(i+1, player[i].board["bonus"]) 
                        self.pair.insert(i+1, player[i].board["pair"]) 
                        self.twoPair.insert(i+1, player[i].board["twoPair"]) 
                        self.threeOf.insert(i+1, player[i].board["threeOf"]) 
                        self.fourOf.insert(i+1, player[i].board["fourOf"]) 
                        self.fullHouse.insert(i+1, player[i].board["fullHouse"]) 
                        self.small.insert(i+1, player[i].board["small"]) 
                        self.big.insert(i+1, player[i].board["big"]) 
                        self.chanse.insert(i+1, player[i].board["chanse"]) 
                        self.yatzy.insert(i+1, player[i].board["yatzy"]) 
                        self.total.insert(i+1, player[i].board["total"]) 
        
                
                print(tabulate(self.Table, headers="firstrow",missingval="", tablefmt="fancy_grid"))


















        

