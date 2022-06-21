import itertools

class SaveScore:

    _OPTIONS = {
        "1": "saveNumbers",
        "2": "saveNumbers",
        "3": "saveNumbers",
        "4": "saveNumbers",
        "5": "saveNumbers",
        "6": "saveNumbers",     
        "7": "savePair",     
        "8": "saveTwoPair",     
        "9": "saveThreeOfaKind",     
        "10": "saveFourOfaKind",     
        "11": "saveFullHouse",     
        "12": "saveSmallStraight",     
        "13": "saveBigStraight",     
        "14": "saveChanse",     
        "15": "saveYatzy",     
    }

    def __init__(self, player, hand, choice):
        """ Initialize class """
        self.hand = hand
        self.player = player
        self.choice = choice
        if int(choice) < 7:
            self.saveNumbers(choice)
        else:
            self._get_method(choice)()
    
    def reSelect(self):
        """ If selection is already taken"""
        
        while True:
            choice = input("Spara som:\n-> ")
            try:
                if int(choice) < 7:
                    self.saveNumbers(choice)
                    break
                else:
                    self._get_method(choice)()
                    break
            except KeyError:
                print("Invalid choice!")
    
    def _get_method(self, method_name):
        """
        Uses function getattr() to dynamically get value of an attribute.
        """
        return getattr(self, self._OPTIONS[method_name])

    def saveNumbers(self, choice):
        """Saving 1 to 6 """
        x = 0
        if self.player.board[choice] != '':                                            
            print('%s is already taken choose another number\n' %choice)
            self.reSelect()
        else:
            for i in self.hand.hand:
                if i.value == int(choice):   
                    x += i.value
            if x == 0:
                self.player.board[choice] = '-'
                print('Stryker %s' %choice)
            else:
                self.player.board[choice] = x
                self.player.board["hidden"] += x
                if self.player.board['sum'] == '':
                    self.player.board['sum'] = 0
                self.player.board['sum'] += x
                
                # print('Sparar som %s' %choice)
            if self.player.board['sum'] != '' and self.player.board['sum'] > 62:
                self.player.board['bonus'] = 50

    def savePair(self):
        """Saving pair"""
        x = 0
        if self.player.board["pair"] != '':
            print("Pair is already taken")
            self.reSelect()
        out = itertools.combinations(self.hand.hand, 2)
        for _ in out:
            if _[0].value == _[1].value and _[0].value + _[1].value > x:
                x =_[0].value + _[1].value
        if x == 0:
            print("Stryker par")
            self.player.board["pair"] = "-"
        else:
            self.player.board["pair"] = x
            self.player.board["hidden"] += x

    def saveTwoPair(self):
        """Saving two pair"""
        x = 0
        pair = set()
        if self.player.board["twoPair"] != '':
            print("Two pair is already taken")
            self.reSelect()
        out = itertools.combinations(self.hand.hand, 2)
        for _ in out:
            if _[0].value == _[1].value:
                x = _[0].value + _[1].value
                pair.add(x)
        if len(pair) == 2:
            x = sum(pair)
            self.player.board["twoPair"] = x
            self.player.board["hidden"] += x    
        else:
            print("Stryker tvåpar")
            self.player.board["twoPair"] = "-"

    def saveThreeOfaKind(self):
        """Saving three of a kind"""
        x = 0
        values = []
        if self.player.board["threeOf"] != '':
            print("Three of a kind is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            y = values.count(i)
            if y > 2:
                x = 3 * i
                self.player.board["threeOf"] = x
                self.player.board["hidden"] += x
                break
        else:
            print("Stryker triss")
            self.player.board["threeOf"] = "-"

    def saveFourOfaKind(self):
        """Saving four of a kind"""
        x = 0
        values = []
        if self.player.board["fourOf"] != '':
            print("Four of a kind is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            y = values.count(i)
            print(y)
            if y > 3:
                x = 4 * i
                self.player.board["fourOf"] = x
                self.player.board["hidden"] += x
                break
        else:
            print("Stryker fyrtal")
            self.player.board["fourOf"] = "-"
    
    def saveFullHouse(self):
        """Saving full house"""
        x = 0
        values = []
        if self.player.board["fullHouse"] != '':
            print("Fullhouse is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            if values.count(i) == 3:
                x = 3 * i
                y = i
                for i in range(1, 4):
                    values.remove(y)
            continue
        if values[0] == values[1]:
            x += values[0] * 2
            self.player.board["fullHouse"] = x
            self.player.board["hidden"] += x
        else:
            print("Stryker kåk") 
            self.player.board["fullHouse"] = '-'

    def saveSmallStraight(self):
        """Saving small straight"""
        x = 0
        values = []
        setval = set()
        if self.player.board["small"] != '':
            print("Small straight is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(i.value)
            setval.add(i.value)
        if len(setval) != 5:
            print("Stryker liten stege")
            self.player.board["small"] = '-'
            return
        for i in range(2,6):
            y = values.count(i)
            if y == 0:
                print("Stryker liten stege")
                self.player.board["small"] = '-'
                return
        if values.count(1):
            self.player.board["small"] = 15
            self.player.board["hidden"] += 15

    def saveBigStraight(self):
        """Saving big straight"""
        x = 0
        values = []
        setval = set()
        if self.player.board["big"] != '':
            print("Big straight is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(i.value)
            setval.add(i.value)
        if len(setval) != 5:
            print("Stryker stor stege")
            self.player.board["big"] = '-'
            return
        for i in range(2,6):
            y = values.count(i)
            if y == 0:
                print("Stryker stor stege")
                self.player.board["big"] = '-'
                return
        if values.count(6):
            self.player.board["big"] = 20
            self.player.board["hidden"] += 20

    def saveChanse(self):
        """Saving chanse"""
        x = 0
        values = []
        if self.player.board["chanse"] != '':
            print("Chanse is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(int(i.value))
        self.player.board["chanse"] = sum(values)
        self.player.board["hidden"] += sum(values)
    
    def saveYatzy(self):
        """Saving yatzy"""
        x = 0
        values = []
        if self.player.board["yatzy"] != '':
            print("Yatzy is already taken")
            self.reSelect()
        for i in self.hand.hand:
            values.append(int(i.value))
        if len(set(values)) == 1:
            self.player.board["yatzy"] = 50
            self.player.board["hidden"] += 50
        else:
            print("Stryker yatzy")
            self.player.board["yatzy"] = '-'