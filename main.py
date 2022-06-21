import sys
import inspect

from play import Play



class Menu:

    _OPTIONS = {
        "1": "start_game",
        "q": "quit"
        
    }

    

    def __init__(self):
        """ Initialize class """
        self.play = Play()
        self.start()
        
    def start(self):
        """ Start method """
        while True:
            self._print_menu()
            choice = input("Enter menu selection:\n-> ")

            try:
                self._get_method(choice.lower())()
            except KeyError:
                print("Invalid choice!")
    
    def _get_method(self, method_name):
        """
        Uses function getattr() to dynamically get value of an attribute.
        """
        return getattr(self, self._OPTIONS[method_name])

    def _print_menu(self):
        """
        Use docstring from methods to print options for the program.
        """
        menu = ""

        for key in sorted(self._OPTIONS):
            method = self._get_method(key)
            docstring = inspect.getdoc(method)

            menu += "{choice}: {explanation}\n".format(
                choice=key,
                explanation=docstring
            )
        print("")
        print(menu)

    def start_game(self):
        """start_game"""
        while True:
            playerList = []         # strings with name of players
            numberOfPlayer = input("Enter number of players: 1 to 4:\n-> ")
            try:
                if int(numberOfPlayer) > 4:
                    print("Max 4 players")
                else:
                    for x in range(int(numberOfPlayer)):
                        x += 1
                        player = input('Enter name of player %d \n' %x)
                        playerList.append(player)
                    self.play.players(playerList)
                break
            except (ValueError, TypeError):
                    print("Must be an integer from 1 to 4!")
            


    @staticmethod
    def quit():
        """ Quit the program """
        sys.exit()

if __name__ == "__main__":
    Menu()