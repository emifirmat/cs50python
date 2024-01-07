from tabulate import tabulate
from random import shuffle


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
        self.deck = []
        index = -1

        for type in ["sword", "coin", "cup", "club"]:
            for number in range(12):
                if 7 < number + 1 < 10:
                    continue
                else: 
                    index += 1 
                    self.deck.append({"number": number + 1, "type": type})

    def shuffle(self):
        shuffle(self.deck)

    def cut(self):
        size = int(len(self.deck) / 2)
        self.deck = self.deck[size:] + self.deck[:size]

    def __str__(self):
        values = []
        for row in self.deck:
            for value in row.values():
                values.append(value)
        return f"{values}"   
"""
Deck
    -List of cards
    -shuffle
    -cut
    
    -- card
            - number
            - type
            - value
            - envido value
    

"""