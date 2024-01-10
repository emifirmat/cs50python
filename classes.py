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
        values = [f"{card['number']} {card['type']}" for card in self.deck]
        return f"{values}"


class Points:
    def __init__(self):
        self._phase_point = 0

    @property
    def phase_point(self):
        return self._phase_point
    
    def add_phase_point(self):
        self._phase_point += 1

    def __str__(self):
        return f"{self.phase_point}"


class Player(Points):
    def __init__(self, name):
        self.player = name
        self.dealer = False
        self.hand = []
        super().__init__()
        
    def is_dealer(self):
        self.dealer = True        

    def pick_card(self, hand):
        print(f"{self.player} picks a card: ")
        while True:
            # Show cards
            try:
                number, type = input(f"{hand}\n").lower().strip().split(" ")
            except ValueError:
                continue
            # Find card in hand
            else:
                for row in self.hand:
                    if row["number"] == number and row["type"] == type:
                        card = row
                        # Remove card from hand
                        self.hand = list(filter(lambda x: x != card, self.hand))    
                        # Return picked card
                        return card
    
    def show_card(self, card):
        return f"{self.player} plays {card}\n"
 
    
    def __str__(self):
        return f"{self.player}"   

    def __format__(self, format_spec):
        if format_spec == "hand":
            values = [f"{card['number']} {card['type']}" for card in self.hand]
            return f"[{'] ['.join(values)}]"
        else:
            return self.__str__()


class Card:
    def __init__(self, card):
        self._number = card["number"]
        self._type = card["type"]
        self._truco_val = card["truco"]
        self._envido_val = card["envido"]

    def __str__(self):
        return f"{self.number} {self.type}"

    @property
    def number(self):
        return self._number

    @property
    def type(self):
        return self._type

    @property
    def truco_val(self):
        return int(self._truco_val)            

    @property
    def envido_val(self):
        return int(self._envido_val)

class Settings:
    def __init__(self):
        self.pc_scre = 0
        self.hm_scre = 0
        self.phase = 0
        self.phase_winner = []
        self.truco_points = 1
        self.truco_chain = [
            {"truco": 2},
            {"retruco": 3},
            {"vale cuatro": 4},
        ]
        self.truco_phase = 0

    
    
    def __str__(self):
        return f"{self.phase}"
    
    def __format__(self, fmt_spec):
        if fmt_spec == "phasew":
            # Fin winner of last phase
            last_win = None
            for winner in self.phase_winner:
                last_win = winner    
            return f"{last_win}"     
        elif fmt_spec == "trucop":
            return f"{self.truco_points}"
        elif fmt_spec == "trucoc":
            return f"{self.truco_chain}"
        else:
            return self.__str__()
        
"""


-- Hand
        - value
        - envido value
"""