"""Module play with class Play"""
from dice import Hand
from score import Score
from table import Tableprint
from save_score import SaveScore

class Play:
    """Class play with methods to manage the roll, and turn of players"""
    game_counter = 0
    counter = 0
    save = SaveScore
    scoreList = []              #list with scoreobject

    def play(self, players):
        """
        Calling roll method for each player
        """
        while self.game_counter < 15:
            self.game_counter += 1
            for player in players:
                self.roll(player)
        self.finish()

    def roll(self, player):
        "Rolling dices"
        action = input(f'{player.board["name"]} press enter to roll:\n')
        if action is not None:
            hand = Hand()
            self.counter = 0
            for val in hand.hand:
                print(val.value, end=" ")
            print()
            while self.counter < 2:
                all_dice = [0, 1, 2, 3, 4]
                try:
                    choise = input("Enter to roll or choose \
dices to hold or s for save:\n ")
                    if choise == 's':
                        self.save_rools(player, hand, 2)
                        return
                    for _ in choise:
                        all_dice.remove(int(_)-1)
                    for val in all_dice:
                        hand.hand[val].roll()
                    for val in hand.hand:
                        print(val.value, end=" ")
                    print()
                    self.counter += 1
                except ValueError:
                    print("Only numbers 1 to 5 or letter s is valid\n")
                if self.counter == 2:
                    self.save_rools(player, hand, 0)
                    return

    def save_rools(self, player, hand, counts):
        """Save method"""
        while True:
            try:
                choise = input("Save as?\n ")
                self.save(player, hand, choise) # init savescore
                table = Tableprint()
                table.print(self.scoreList)
                self.counter = counts
                break
            except (ValueError, KeyError):
                print("Must be a number between 1 and 15")

    def players(self, players):
        "Adding player to scoorboard"
        for i in players:               # i = name of each player
            player = Score(i)           # each player is a dictonary/scoreObject
            self.scoreList.append(player)
        table = Tableprint()
        table.print(self.scoreList)
        self.play(self.scoreList)

    def finish(self):
        "Calculating sum when game is finished"
        for player in self.scoreList:
            player.board["total"] = player.board["hidden"]
            if player.board["bonus"] != "":
                player.board["total"] += 50
        table = Tableprint()
        table.print(self.scoreList)
