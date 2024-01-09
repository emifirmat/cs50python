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
    def __init__(self, deck):
        self.deck = deck
    
    @property
    def deck(self):
        return self._deck
    
    @deck.setter
    def deck(self, deck):     
        if len(deck) > 40:
            raise ValueError("Too many cards in deck!")
        self._deck = deck
    
    def shuffle(self):
        shuffle(self.deck)

    def cut(self):
        size = int(len(self.deck) / 2)
        self._deck = self.deck[size:] + self.deck[:size]

    def len(self):
        return len(self.deck)
    
    def deal(self):
        for card in itertools.cycle(self.deck):
            # Move card to deal to the end and pop it
            self.deck = self.deck[1:] + self.deck[:1] 
            self.deck.pop()
            # Return card
            return card
    
    def __str__(self):
        return f"{self.deck}"   


class Player:
    def __init__(self, name):
        self.player = name
        self.dealer = False
        self.hand = []
        
    def is_dealer(self):
        self.dealer = True
    
    def hand(self):
        if len(self.hand) > 3:
            raise ValueError("Too many cards in hand")
        return f"{self.hand}"

    def pick_card(self):
        print("Pick a card: ")
        while True:
            card = input(f"{self.hand}\n")
            if card in self.hand:
                return card
    
    def show_card(self, card):
        return f"{self.player} plays {card}\n"

    def remove_card(self, card):
        self.hand = list(filter(lambda x: x != card, self.hand))
        return f"{self.hand}"

    def __str__(self):
        return f"{self.player}"   


"""


-- Hand
        - value
        - envido value
"""