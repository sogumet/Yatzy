
from dice import Hand
from score import Score
from table import Tableprint
from save_score import SaveScore

class Play:

    gameCounter = 0
    counter = 0
    save = SaveScore
    scoreList = []              #list with scoreobject

    def roll(self, players):
        """
        Rolling dice
        """
        while self.gameCounter < 15:
            self.gameCounter += 1
            for player in players:
                action = input('%s press enter to roll:\n' %player.board["name"])
                if action is not None:
                    hand = Hand()
                    self.counter = 0
                    for x in hand.hand:
                        print(x.value, end=" ")
                    print()
                    while self.counter < 2:
                        allDice = [0, 1, 2, 3, 4]
                        try:
                            choise = input("Enter to roll or choose dices to hold or s for save:\n ")
                            if choise == 's':
                                try:
                                    choise = input("Save as?\n ")
                                    self.save(player, hand, choise)
                                    table = Tableprint()
                                    table.print(self.scoreList)
                                    self.counter = 2
                                    break
                                except ValueError:
                                    print("Must be a number between 1 and 15") 
                            else:
                                for _ in choise:
                                    allDice.remove(int(_)-1)
                                for x in allDice:
                                    hand.hand[x].roll()
                                for x in hand.hand:
                                    print(x.value, end=" ")
                                print()
                                self.counter += 1
                        except ValueError:
                            print("Only numbers 1 to 5 or letter s is valid\n")
                        if self.counter == 2:
                            self.saveAfterTreeRoll(player, hand)
                            break
        self.finish()
         
    def saveAfterTreeRoll(self, player, hand):
        """After three rolls"""
        while True:
            try: 
                choise = input("Save as?\n ")
                self.save(player, hand, choise) # init savescore
                table = Tableprint()
                table.print(self.scoreList)
                self.counter = 0
                break       
            except (ValueError, KeyError):
                print("Must be a number between 1 and 15")

    def players(self, players):
        for i in players:               # i = name of each player
            player = Score(i)           # each plyer is a dictonary/scoreObject
            self.scoreList.append(player)
        table = Tableprint()
        table.print(self.scoreList)
        self.roll(self.scoreList)

    def finish(self):
        for player in self.scoreList:
            player.board["total"] = player.board["hidden"]
            if player.board["bonus"] != "":
                player.board["total"] += 50
        table = Tableprint()
        table.print(self.scoreList)



    
    


    
        

    
        
