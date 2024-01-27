from random import shuffle, randint
from termcolor import colored

class Menu:
    def __init__(self, list):
        self.menu = list
           
    @property
    def menu(self):
        return self._menu
    
    @menu.setter
    def menu(self, list):
        if len(list) < 1:
            raise ValueError("Menu arg is not a list!")
        self._menu = list
    
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
        elif len(deck) < 34:
            raise ValueError("Deck has lost too many cards")
        else:
            self._deck = deck
    
    def shuffle(self):
        shuffle(self.deck)

    def cut(self):
        # Random cut around the middle of the deck
        size = randint(10, 30)
        self.deck = self.deck[size:] + self.deck[:size]
    
    def deal(self):
        # deal and remove card from deck
        card = self.deck.pop(0)
        return card
    
    def __str__(self):
        values = [f"{card['number']} {card['type']}" for card in self.deck]
        return f"{values}"

    def __len__(self):
        return len(self.deck)

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
        if points > 33:
            raise ValueError("Envido points exceed limit")    
        self._envido_points = points

    def restart_env_points(self):  
        self._envido_points = 0   

    def __str__(self):
        return f"{self.phase_point}"

class Hand:
    def __init__(self):
        self.hand = []
        self.temp_hand = []

    @property
    def hand(self):
        return self._hand
    
    @hand.setter
    def hand(self, list):
        self._hand = list

    @property
    def temp_hand(self):
        return self._temp_hand
    
    @temp_hand.setter
    def temp_hand(self, list):
        self._temp_hand = list

    def add_card(self, card):    
        # Note: 
        if len(self.hand) > 2:
            raise ValueError("Too many cards in hand!")
        self.hand.append(card)
        self.temp_hand.append(card)
    
    def pick_card(self, number, c_type):     
        for card in self.hand:
            if card["number"] == number and card["type"] == c_type:    
                # Return picked card
                return card
        raise TypeError

    def clean_hand(self):
        self.hand = []
        self.temp_hand = []

    def __len__(self):
        return len(self.hand)
 
class Player(Points, Hand):
    def __init__(self, name):
        self._name = name
        self._dealer = False
        self._first = False
        self._truco_call = True
        Hand.__init__(self)
        Points.__init__(self)

    @property
    def name(self):
        return self._name      

    @property
    def dealer(self):
        return self._dealer
    
    @property
    def first(self):
        return self._first
    
    @property
    def truco_call(self):
        return self._truco_call
    
    def change_dealer(self):
        if self.dealer == False:
            self._dealer = True
        else:
            self._dealer = False        

    def plays_first(self):
        self._first = True
    
    def plays_last(self):
        self._first = False

    def lock_truco(self):
        self._truco_call = False

    def unlock_truco(self):
        self._truco_call = True

    def restart_values(self):
        self.unlock_truco()
        self.plays_last()
        self.clean_hand()
        self.restart_env_points()
        self.restart_phase_point()

    def __str__(self):
        if self.name == "PC":
            return f"{colored(self.name, 'red', attrs=['bold'])}"
        else:
            return f"{colored(self.name, 'green', attrs=['bold'])}"   

    def __format__(self, format_spec):
        if format_spec == "hand":
            values = [f"{card['number']} {card['type']}" for card in self.hand]
            if len(values) > 0:
                return f"[{'] ['.join(values)}]"
            else:
                return f"None cards"
        else:
            return self.__str__()
  
class Settings:
    def __init__(self):
        self._row = 0
        self.row_points = 0
        self._phase = 0
        self.phase_winner = []
        self.truco_score = 0
        self._truco_chain = [{"truco": 2}, {"retruco": 3}, {"vale cuatro": 4}]
        self._truco_phase = 0
        self._envido = True
        self.envido_score = 0
        self._envido_chain = [{"envido": 2}, {"real envido": 3}, {"falta envido": 0}]
        self._envido_phase = 0

    @property
    def row(self):
        return self._row
    
    @property
    def phase(self):
        return self._phase
    
    @property
    def truco_chain(self):
        return self._truco_chain
    
    @property
    def truco_phase(self):
        return self._truco_phase   
    
    @property
    def envido(self):
        return self._envido    

    @property
    def envido_chain(self): 
        return self._envido_chain
    
    @property
    def envido_phase(self):
        return self._envido_phase

    def new_row(self):
        self._row += 1
    
    def new_phase(self):
        self._phase += 1

    def new_truco_phase(self):
        self._truco_phase += 1
    
    def lock_envido(self):
        self._envido = False

    def set_falta_envido(self, game_score, points):
        self.envido_chain[2]["falta envido"] = game_score - points

    def update_row_points(self, envido, truco):
        if truco + envido == 0:
            raise ValueError("There should be at least 1 point")
        self.row_points = envido + truco

    def restart_values(self):
        self.row_points = 0
        self._phase = 0
        self.phase_winner = []
        self._truco_phase = 0
        self.truco_score = 0
        self._envido = True
        self.envido_score = 0
        self._envido_phase = 0

    def __str__(self):
        return f"{self.phase}"
    
    def __format__(self, fmt_spec):
        if fmt_spec == "phasew":
            # Find winner of last phase
            last_win = None
            for winner in self.phase_winner:
                last_win = winner    
            return f"{last_win}"     
        elif fmt_spec == "trucos":
            return f"{self.truco_score}"
        elif fmt_spec == "envidos":
            return f"{self.envido_score}"
        else:
            return self.__str__()
        