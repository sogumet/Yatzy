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
        "9": "save_three_or_four",
        "10": "save_three_or_four",
        "11": "save_full_house",
        "12": "save_straight",
        "13": "save_straight",
        "14": "save_chanse",
        "15": "save_yatzy",
        "16": "three",
        "17": "four"
    }

    def __init__(self, player, hand, choice):
        """ Initialize class """
        self.hand = hand
        self.player = player
        self.choice = choice
        if int(choice) < 7:
            self.save_numbers(choice)
        else:
            self._get_method(choice)(choice)

    def re_select(self):
        """ If selection is already taken"""

        while True:
            choice = input("Save as:\n ")
            try:
                if int(choice) < 7:
                    self.save_numbers(choice)
                    break
                self._get_method(choice)(choice)
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
            self.taken(choice)
        else:
            for i in self.hand.hand:
                if i.value == int(choice):
                    val += i.value
            if val == 0:
                self.stroke(choice, choice)
            else:
                self.save(choice, val)
                if self.player.board['sum'] == '':
                    self.player.board['sum'] = 0
                self.player.board['sum'] += val
            if self.player.board['sum'] != '' and self.player.board['sum'] > 62:
                self.player.board['bonus'] = 50

    def save_pair(self, _unused=False):
        """Saving pair"""
        val = 0
        if self.player.board["pair"] != '':
            self.taken("pair")
        out = itertools.combinations(self.hand.hand, 2)
        for _ in out:
            if _[0].value == _[1].value and _[0].value + _[1].value > val:
                val =_[0].value + _[1].value
        if val == 0:
            self.stroke("pair", "par")
        else:
            self.save("pair", val)

    def save_two_pair(self, _unused=False):
        """Saving two pair"""
        val = 0
        pair = set()
        if self.player.board["twoPair"] != '':
            self.taken("two pair")
        out = itertools.combinations(self.hand.hand, 2)
        for _ in out:
            if _[0].value == _[1].value:
                val = _[0].value + _[1].value
                pair.add(val)
        if len(pair) == 2:
            val = sum(pair)
            self.save("twoPair", val)
        else:
            self.stroke("twoPair", "two pair")

    def save_three_or_four(self, choice):
        """Saving three or four of a kind"""
        if choice == "9":
            save = "three"
            met = getattr(self, self._OPTIONS["16"])
        else:
            save = "four"
            met = getattr(self, self._OPTIONS["17"])
        values = []
        val = 0
        numb = 0
        if self.player.board[save] != '':
            self.taken(save + " of a kind")
            return
        for i in self.hand.hand:
            values.append(i.value)
        for i in range(1, 7):
            occ = values.count(i)
            if occ > val:
                val = occ
                numb = i
        met(numb, val)

    def three(self, i, occ):
        """Saving three of a kind"""
        if occ > 2:
            val = 3 * i
            self.save("three", val)
        else:
            self.stroke("three", "three of")

    def four(self, i, occ):
        """Saving four of a kind"""
        if occ > 3:
            val = 4 * i
            self.save("four", val)
        else:
            self.stroke("four", "four of")

    def save_full_house(self, _unused=False):
        """Saving full house"""
        val = 0
        values = []
        if self.player.board["fullHouse"] != '':
            self.taken("full house")
        for i in self.hand.hand:
            values.append(i.value)
        out = itertools.combinations(values, 3)
        for dots in out:
            if dots.count(dots[0]) == len(dots):
                three = dots[0]
                for i in range(1, 4):
                    values.remove(three)
                    val = 3 * three
        if values[0] == values[1] and len(values) == 2:
            val += values[0] * 2
            self.save("fullHouse", val)
        else:
            self.stroke("fullHouse", "full house")

    def save_straight(self, choice):
        """Saving straight"""
        if choice == "12":
            val = "small"
            size = 1
        else:
            val = "large"
            size = 6
        values = []
        setval = set()
        if self.player.board[val] != '':
            self.taken(val + " straight ")
        for i in self.hand.hand:
            values.append(i.value)
            setval.add(i.value)
        if len(setval) != 5:
            self.stroke(val, val)
            return
        for i in range(2,6):
            occ = values.count(i)
            if occ == 0:
                self.stroke(val, val)
                return
        if values.count(size):
            print(f"Saving as {val} straight")
            self.player.board[val] = 14 + size
            self.player.board["hidden"] += 14 + size

    def save_chanse(self, _unused=False):
        """Saving chanse"""
        values = []
        if self.player.board["chanse"] != '':
            self.taken("chanse")
        for i in self.hand.hand:
            values.append(int(i.value))
        self.save("chanse", sum(values))

    def save_yatzy(self, _unused=False):
        """Saving yatzy"""
        values = []
        if self.player.board["yatzy"] != '':
            self.taken("yatzy")
        for i in self.hand.hand:
            values.append(int(i.value))
        if len(set(values)) == 1:
            self.save("yatzy", 50)
        else:
            self.stroke("yatzy", "yatzy")

    def save(self, choice, val):
        """General save"""
        print(f"Saving as {choice}")
        self.player.board[choice] = val
        self.player.board["hidden"] += val

    def stroke(self, choice, val):
        """General stroke"""
        print(f"Deleting {val}")
        self.player.board[choice] = "-"

    def taken(self, choice):
        """General stroke"""
        print(f"{choice.capitalize()} is allready taken")
        self.re_select()
