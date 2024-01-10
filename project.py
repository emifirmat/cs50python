from sys import exit
from tabulate import tabulate
from time import sleep
from pyfiglet import Figlet
from classes import Menu, Deck, Player, Card, Settings
import random, csv

# Default game settings
goal_scre = 30



def main():
    # Welcome
    ...
    
    # Menu options: Start game, Rules, exit
    while True:
        menu = Menu([
            ["start", "Start game"],
            ["rules", "Learn how to play"],
            ["quit", "Exit game"],
        ])
        print(menu, end="\n\n")
        
        # User answer
        choise = menu.get_answer()

        # Move to options
        match choise:
            case "start":
                play()
            case "rules":
                rules()
            case "quit":
                exit_game()

    
# Rules
def rules():   
    while True:
    
        # Intro rules
        print("--To learn how to play, choose a command from the menu", end="\n\n")
            
        # Rules menu
        menu = Menu([
            ["intro"],
            ["cards"],
            ["main"],
            ["envido"],
            ["truco"],
            ["scores"],
        ])

        # Print menu and choose
        print(menu, end="\n\n")
        rchoise = menu.get_answer()
        sleep(1)
        
        if rchoise == "quit" or rchoise =="exit":
            print()
            sleep(1)
            return 
        
        # Show text from file
        try:
            with open(f"rules/{rchoise}.txt") as file:
                print(file.read(), end="\n\n")
        except FileNotFoundError:
            print("Sorry, command is not working, try another option")
        
        # Ask to continue or leave rules
        sleep(1)
        fchoise = input("Type <any letter> to continue navigating or <quit> to go back.\n\n")
        sleep(1)

        if fchoise == "quit":
            print()
            sleep(1)
            return 


def play():
    # Settings
    settings = Settings()
    
    # Starting message
    print(f"Starting game...\n\nThe first who reaches {goal_scre} points wins\n") 
        
    # Create players
    p1 = Player("Emi") 
    p2 = Player("PC")
     
    """ Start Row """
    print("Starting row...\n")

    # Set deck
    try:
        with open("cards_values.csv") as file: 
            csv_file = csv.DictReader(file)       
            cards_list = [row for row in csv_file]
    
    except FileNotFoundError:
        exit("Can't open cards values file")

    deck = Deck(cards_list)
    
    """Start phase"""
    settings.phase += 1
    print(f"Starting phase {settings}...\n")
    
    # Choose dealer
    dealer = random.choice([p1, p2])
    dealer.is_dealer()

    # Set first to play = p1
    if p1.dealer == True:
        p1, p2 = p2, p1
        
    print(f"First to play is {p1} and second to play is {p2}\n")
    
    # Shuffling
    deck.shuffle()
    deck.cut()
    
    # Dealing 
    for _ in range(3): 
        p1.hand.append(deck.deal()) 
        p2.hand.append(deck.deal()) 

    print(f"{p1} = {p1:hand}, {p2} = {p2:hand}\n") 

    # Playing turns - First variable is current player's turn
    p1card = turn(p1, p2, settings)   
    p2card = turn(p2, p1, settings)

    # Compare cards
    msg = f"The winner of phase {settings} is"
    if p1card > p2card:
        p1.add_phase_point()
        settings.phase_winner.append(p1.player)
    elif p1card < p2card:
        p2.add_phase_point()
        settings.phase_winner.append(p2.player)
    # Tie
    else:
        settings.phase_winner.append("Tie")
        msg = f"There is a"
    print(f"{msg} {settings:phasew}")
    
    
    # Second phase


    # Third phase




def score():
    ...    
    # Score
        # Sum total score
        # Check total score

def introduction():
    # Welcome
    figlet = Figlet()
    print(figlet.renderText("Truco card game"))
    sleep(1)

    # Ask name and limit length up to 20 chars
    name = input("--What's your name?\n\n").strip()
    name = name[0:21]
    print()
    sleep(1)

    # Say hello
    print(f"--Welcome {name}! Read the menu in order to start your game:", end="\n\n")    
    sleep(2)    


def exit_game():
    print()
    print("Exit game? (Yes/No)")
    menu = Menu([
        ["yes"],
        ["no"],
    ])

    answer = menu.get_answer()

    if answer == "yes":
        exit("--Thank you for playing truco, see you!")


def turn(px, py, settings):
    # Print turn
    print(f"It's {px}'s turn...\n")
    
    # Open menu and input an option
    options = Menu([
        ["envido", "Call envido"],
        ["truco", "Call truco"],     
        ["play", "Play a card"],
    ])
    print(f"{options}\n")
    option = options.get_answer()

    # Execute option
    match option:
        case "envido":
            envido()
        case "truco":
            truco(py, settings)
            # Play card after truco
            return play_card(px)
        case "play":
            return play_card(px)


def envido():
    ...


def truco(py, settings):
    n = settings.truco_phase 
    chain = settings.truco_chain
    
    for key in chain[n]:
        print(f"-{key.upper()}!-\n") 

    print(f"{py} answers:")  
    options = Menu([
        ["accept"],
        ["reject"],
        ["reply"],
    ])

    print(f"{options}")

    answer = options.get_answer()

    match answer:
        case "accept":
            for value in chain[n].values():
                settings.truco_points = value
            settings.truco_phase += 1
        case "reject":
            ...
        case "reply":
            ...
        
def play_card(px):
    card = Card(px.pick_card(f"{px:hand}"))
    print(f"{px:hand} left\n")
    return card.truco_val


if __name__ == "__main__":
    main()    