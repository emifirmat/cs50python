from tabulate import tabulate

class Menu:
    def __init__(self, list):
        self._menu = list
           
    @property
    def menu(self):
        return self._menu
    
    def __str__(self):
       return tabulate(self.menu, headers=["Command", "Description"])
        
    def get_answer(self):
        while True:
            choise = input("Command: ").strip().lower() 
            if choise == "quit" or choise == "exit":
                return choise
            else:
                for line in self.menu:
                    if choise in line: 
                        print()
                        return choise 
            

class Deck:
    def __init__(self):
        ...