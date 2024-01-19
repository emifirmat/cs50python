from tabulate import tabulate
from random import shuffle, randint


class Menu:
    def __init__(self, list):
        self._menu = list
           
    @property
    def menu(self):
        return self._menu
    
    def __str__(self):
       return tabulate(self.menu, headers=["Command", "Description"])
        
    def __format__(self, fmt_spec):
        if fmt_spec == "horizontal":
            return " | ".join(self.menu)
        else:
            return self.__str__()
    
    def in_menu(self, choise):
        if choise == "quit":
            return True
        for line in self.menu:
            if choise in line: 
                print()
                return True 
        return False
            

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
        # Random cut around the middle of the deck
        size = randint(10, 30)
        self._deck = self.deck[size:] + self.deck[:size]

    def len(self):
        return len(self.deck)
    
    def deal(self):
        for card in self.deck:
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
        self._game_score = 0
        self._envido_points = 0

    @property
    def phase_point(self):
        return self._phase_point
    
    @property
    def game_score(self):
        return self._game_score
    
    @property
    def envido_points(self):
        return self._envido_points
    
    def add_phase_point(self):
        self._phase_point += 1
    
    def restart_phase_point(self):
        self._phase_point = 0

    def update_game_score(self, points):
        # Points = envido or truco points
        self._game_score += points 

    def update_env_points(self, points):
        self._envido_points += points

    def restart_env_points(self):  
        self._envido_points = 0   

    def __str__(self):
        return f"{self.phase_point}"


class Hand:
    def __init__(self):
        self.hand = []
        self.fullhand = []

    def pick_card(self, hand):
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

    def add_card(self, card):
        if len(self.hand) > 3 or len(self.fullhand) > 3:
            raise ValueError("Too many cards in hand!")
        self.fullhand.append(card)
        self.hand.append(card)
        
    def clean_hand(self):
        self.hand = []
        self.fullhand = []
 

class Player(Points, Hand):
    def __init__(self, name):
        self.name = name
        self.dealer = False
        self.first = False
        self.truco_call = True
        Hand.__init__(self)
        Points.__init__(self)
        
    def is_dealer(self):
        self.dealer = True        

    def plays_first(self):
        self.first = True
    
    def plays_last(self):
        self.last = False

    def restart_values(self):
        self.clean_hand()
        self.restart_env_points()
        self.restart_phase_point()

    def __str__(self):
        return f"{self.name}"   

    def __format__(self, format_spec):
        if format_spec == "hand":
            values = [f"{card['number']} {card['type']}" for card in self.hand]
            return f"[{'] ['.join(values)}]"
        else:
            return self.__str__()
  

class Settings:
    def __init__(self):
        self.row = 0
        self.row_points = 0
        self.phase = 0
        self.phase_winner = []
        self.truco_score = 0
        self.truco_chain = [
            {"truco": 2},
            {"retruco": 3},
            {"vale cuatro": 4},
        ]
        self.truco_phase = 0
        self.envido = True
        self.envido_score = 0
        self.envido_chain = [
            {"envido": 2},
            {"real envido": 3},
            {"falta envido": 0},
        ]
        self.envido_phase = 0

    def set_falta_envido(self, game_score, points):
        self.envido_chain["falta envido"] = game_score - points

    def update_row_points(self, envido, truco):
        self.row_points = envido + truco

    def restart_values(self):
        self.row_points = 0
        self.phase = 0
        self.phase_winner = []
        self.truco_phase = 0
        self.truco_score = 0
        self.envido = True
        self.envido_score = 0
        self.envido_phase = 0

    def __str__(self):
        return f"{self.phase}"
    
    def __format__(self, fmt_spec):
        if fmt_spec == "phasew":
            # Fin winner of last phase
            last_win = None
            for winner in self.phase_winner:
                last_win = winner    
            return f"{last_win}"     
        elif fmt_spec == "trucos":
            return f"{self.truco_score}"
        elif fmt_spec == "trucoc":
            return f"{self.truco_chain}"
        elif fmt_spec == "envidos":
            return f"{self.envido_score}"
        else:
            return self.__str__()
        