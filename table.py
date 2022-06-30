"""Table module"""
from tabulate import tabulate

class Tableprint:
    """Class for printing ta"""
    def __init__(self):

        self.table = []


    def print_score_board(self, players):
        """Printing the scoreboard"""

        head = [["Yatzy", "Välj"],
        ["Ettor", 1],
        ["Tvåor", 2],
        ["Treor", 3],
        ["Fyror", 4],
        ["Femmor", 5],
        ["Sexor", 6],
        ["Summa",  ],
        ["Bonus", ],
        ["Par", 7],
        ["Två par", 8],
        ["Triss", 9],
        ["Fyrtal", 10],
        ["Kåk", 11],
        ["Liten", 12],
        ["Stor", 13],
        ["Chans", 14],
        ["Yatzy", 15],
        ["Total", ]]

        for i, player in enumerate(players):
            head[0].insert(i+1, player.board["name"])
            head[1].insert(i+1, player.board["1"])
            head[2].insert(i+1, player.board["2"])
            head[3].insert(i+1, player.board["3"])
            head[4].insert(i+1, player.board["4"])
            head[5].insert(i+1, player.board["5"])
            head[6].insert(i+1, player.board["6"])
            head[7].insert(i+1, player.board["sum"])
            head[8].insert(i+1, player.board["bonus"])
            head[9].insert(i+1, player.board["pair"])
            head[10].insert(i+1, player.board["twoPair"])
            head[11].insert(i+1, player.board["three"])
            head[12].insert(i+1, player.board["four"])
            head[13].insert(i+1, player.board["fullHouse"])
            head[14].insert(i+1, player.board["small"])
            head[15].insert(i+1, player.board["large"])
            head[16].insert(i+1, player.board["chanse"])
            head[17].insert(i+1, player.board["yatzy"])
            head[18].insert(i+1, player.board["total"])
   
        self.table = [head[0], head[1], head[2], head[3], head[4], head[5],
        head[6], head[7], head[8], head[9], head[10], head[11],
        head[12], head[13], head[14], head[15], head[16],
        head[17], head[18]]

        print(tabulate(self.table, headers="firstrow",missingval="", tablefmt="fancy_grid"))
