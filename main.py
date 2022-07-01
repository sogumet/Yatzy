"""Module with  main class Menu"""
import sys
import inspect
import art

from play import Play
from database import Database

class Menu:
    """Class Menu with methods to init the game"""
    _OPTIONS = {
        "1": "start_game",
        "2": "show_scores",
        "q": "quit"
    }

    def __init__(self):
        """ Initialize class """
        self.play = Play()
        self.start()

    def start(self):
        """ Start method """
        while True:
            print(art.YATZY_ART)
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
            choice=key
            explanation=docstring
            menu += f"{choice}: {explanation}\n"

        print("")
        print(menu)

    def start_game(self):
        """Start game"""
        while True:
            player_list = []         # strings with name of players
            number_of_player = input("Enter number of players: 1 to 4:\n-> ")
            try:
                if int(number_of_player) > 4:
                    print("Max 4 players")
                else:
                    for val in range(int(number_of_player)):
                        val += 1
                        player = input(f'Enter name of player {val}\n')
                        player_list.append(player)
                    self.play.players(player_list)
                break
            except (ValueError, TypeError):
                print("Must be an integer from 1 to 4!")
                
    @staticmethod
    def show_scores():
        """Show scores"""
        data = Database()
        data.get_all_scores()

    @staticmethod
    def quit():
        """ Quit the program """
        sys.exit()

if __name__ == "__main__":
    Menu()
