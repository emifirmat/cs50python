from tabulate import tabulate
from random import shuffle
import itertools

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
        self._deck = []
        index = -1

        for type in ["sword", "coin", "cup", "club"]:
            for number in range(12):
                if 7 < number + 1 < 10:
                    continue
                else: 
                    index += 1 
                    self._deck.append({"number": number + 1, "type": type})
    
    @property
    def deck(self):
        return self._deck
    
    def shuffle(self):
        shuffle(self._deck)

    def cut(self):
        size = int(len(self._deck) / 2)
        self._deck = self._deck[size:] + self._deck[:size]

    def deal(self):
        for card in itertools.cycle(self._deck):
            # Move card to deal to the end and pop it
            self._deck = self._deck[1:] + self._deck[:1] 
            self.deck.pop()
            # Return card
            return card
    
    def __str__(self):
        values = []
        for row in self._deck:
            values.append(f"{row['number']} {row['type']}")
        return f"{values}"   


class Player:
    def __init__(self, name):
        self.player = name
        self.is_dealer = False
        self.hand = []
        
    def is_dealer(self):
        return self.is_dealer
    
    def hand(self, *cards):
        if len(cards) > 3:
            raise ValueError("Too many cards in hand")

    def __str__(self):
        return f"{self.player}"

"""


-- Hand
        - number
        - type
        - value
        - envido value
    

"""