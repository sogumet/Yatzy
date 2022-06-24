"""save_score module"""
import itertools

class SaveScore:
    """Class SaveScore with methodes to
    manage the differnt save options"""

    _OPTIONS = {
        "1": "save_numbers",
        "2": "save_numbers",
        "3": "save_numbers",
        "4": "save_numbers",
        "5": "save_numbers",
        "6": "save_numbers",
        "7": "save_pair",
        "8": "save_two_pair",
        "9": "save_three_of_a_kind",
        "10": "save_four_of_a_kind",
        "11": "save_full_house",
        "12": "save_small_straight",
        "13": "save_big_straight",
        "14": "save_chanse",
        "15": "save_yatzy",
    }

    def __init__(self, player, hand, choice):
        """ Initialize class """
        self.hand = hand
        self.player = player
        self.choice = choice
        if int(choice) < 7:
            self.save_numbers(choice)
        else:
            self._get_method(choice)()

    def re_select(self):
        """ If selection is already taken"""

        while True:
            choice = input("Spara som:\n-> ")
            try:
                if int(choice) < 7:
                    self.save_numbers(choice)
                    break
                test = self._get_method(choice)()
                test()
                break
            except KeyError:
                print("Invalid choice!")

    def _get_method(self, method_name):
        """
        Uses function getattr() to dynamically get value of an attribute.
        """
        return getattr(self, self._OPTIONS[method_name])

    def save_numbers(self, choice):
        """Saving 1 to 6 """
        val = 0
        if self.player.board[choice] != '':
            print( f'{choice} is already taken choose another number\n')
            self.re_select()
        else:
            for i in self.hand.hand:
                if i.value == int(choice):
                    val += i.value
            if val == 0:
                self.player.board[choice] = '-'
                print(f'Stryker {choice}')
            else:
                self.player.board[choice] = val
                self.player.board["hidden"] += val
                if self.player.board['sum'] == '':
                    self.player.board['sum'] = 0
                self.player.board['sum'] += val
                print(f'Sparar som {choice}')
            if self.player.board['sum'] != '' and self.player.board['sum'] > 62:
                self.player.board['bonus'] = 50

    def save_pair(self):
        """Saving pair"""
        val = 0
        if self.player.board["pair"] != '':
            print("Pair is already taken")
            self.re_select()
        out = itertools.combinations(self.hand.hand, 2)
        for _ in out:
            if _[0].value == _[1].value and _[0].value + _[1].value > val:
                val =_[0].value + _[1].value
        if val == 0:
            print("Stryker par")
            self.player.board["pair"] = "-"
        else:
            self.player.board["pair"] = val
            self.player.board["hidden"] += val

    def save_two_pair(self):
        """Saving two pair"""
        val = 0
        pair = set()
        if self.player.board["twoPair"] != '':
            print("Two pair is already taken")
            self.re_select()
        out = itertools.combinations(self.hand.hand, 2)
        for _ in out:
            if _[0].value == _[1].value:
                val = _[0].value + _[1].value
                pair.add(val)
        if len(pair) == 2:
            val = sum(pair)
            self.player.board["twoPair"] = val
            self.player.board["hidden"] += val
        else:
            print("Stryker tvåpar")
            self.player.board["twoPair"] = "-"

    def save_three_of_a_kind(self):
        """Saving three of a kind"""
        val = 0
        values = []
        if self.player.board["threeOf"] != '':
            print("Three of a kind is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            y = values.count(i)
            if y > 2:
                val = 3 * i
                self.player.board["threeOf"] = val
                self.player.board["hidden"] += val
                break
        else:
            print("Stryker triss")
            self.player.board["threeOf"] = "-"

    def save_four_of_a_kind(self):
        """Saving four of a kind"""
        val = 0
        values = []
        if self.player.board["fourOf"] != '':
            print("Four of a kind is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            occ = values.count(i)
            if occ > 3:
                val = 4 * i
                self.player.board["fourOf"] = val
                self.player.board["hidden"] += val
                break
        else:
            print("Stryker fyrtal")
            self.player.board["fourOf"] = "-"

    def save_full_house(self):
        """Saving full house"""
        val = 0
        values = []
        if self.player.board["fullHouse"] != '':
            print("Fullhouse is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            if values.count(i) == 3:
                val = 3 * i
                three = i
                for i in range(1, 4):
                    values.remove(three)
            continue
        if values[0] == values[1]:
            val += values[0] * 2
            self.player.board["fullHouse"] = val
            self.player.board["hidden"] += val
        else:
            print("Stryker kåk")
            self.player.board["fullHouse"] = '-'

    def save_small_straight(self):
        """Saving small straight"""
        values = []
        setval = set()
        if self.player.board["small"] != '':
            print("Small straight is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(i.value)
            setval.add(i.value)
        if len(setval) != 5:
            print("Stryker liten stege")
            self.player.board["small"] = '-'
            return
        for i in range(2,6):
            occ = values.count(i)
            if occ == 0:
                print("Stryker liten stege")
                self.player.board["small"] = '-'
                return
        if values.count(1):
            self.player.board["small"] = 15
            self.player.board["hidden"] += 15

    def save_big_straight(self):
        """Saving big straight"""
        values = []
        setval = set()
        if self.player.board["big"] != '':
            print("Big straight is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(i.value)
            setval.add(i.value)
        if len(setval) != 5:
            print("Stryker stor stege")
            self.player.board["big"] = '-'
            return
        for i in range(2,6):
            occ = values.count(i)
            if occ == 0:
                print("Stryker stor stege")
                self.player.board["big"] = '-'
                return
        if values.count(6):
            self.player.board["big"] = 20
            self.player.board["hidden"] += 20

    def save_chanse(self):
        """Saving chanse"""
        values = []
        if self.player.board["chanse"] != '':
            print("Chanse is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(int(i.value))
        self.player.board["chanse"] = sum(values)
        self.player.board["hidden"] += sum(values)

    def save_yatzy(self):
        """Saving yatzy"""
        values = []
        if self.player.board["yatzy"] != '':
            print("Yatzy is already taken")
            self.re_select()
        for i in self.hand.hand:
            values.append(int(i.value))
        if len(set(values)) == 1:
            self.player.board["yatzy"] = 50
            self.player.board["hidden"] += 50
        else:
            print("Stryker yatzy")
            self.player.board["yatzy"] = '-'
