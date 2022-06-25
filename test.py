

class Hej:
    def __init__(self):
        self.OPTIONS = {
        "1": "save",
        "2": "save",
        "3": "save_three"
        }
        self.OPTIONS1 = {
        "1": "save_par",
        "2": "save_two",
        "3": "save_three"
        }


    def re_select(self):
            """ If selection is already taken"""

            while True:
                choice = input("Spara som:\n-> ")
                try:
                    self.get_method(choice)(choice)
                    break
                except KeyError:
                    print("Invalid choice!")

    def get_method(self, method_name):
            """
            Uses function getattr() to dynamically get value of an attribute.
            """
            return getattr(self ,self.OPTIONS[method_name])

    def save(self, option):
        if option == "1":
            self.save_1()
        else:
            self.save_2()


    def save_1(self):
        print("Sparar par")

    def save_2(self):
        print("Sparar tvåpar")

if __name__ == "__main__":
    hej = Hej()
    hej.re_select()