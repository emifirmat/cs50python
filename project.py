from sys import exit
from tabulate import tabulate
from time import sleep
from pyfiglet import Figlet
from classes import Menu, Deck, Player, Card, Settings
import random, csv

# Constant variables
TOTAL_PHASES = TOTAL_CARDS = 3

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
     
    # Set deck
    try:
        with open("cards_values.csv") as file: 
            csv_file = csv.DictReader(file)       
            cards_list = [row for row in csv_file]
    
    except FileNotFoundError:
        exit("Can't open cards values file")

    """ Start Row """
    while True:
        settings.phase = 0
        settings.row += 1
        print("Starting row...\n")
        deck = Deck(cards_list)

        # Shuffling
        deck.shuffle()
        deck.cut()
        
        # Dealing 
        for _ in range(TOTAL_CARDS): 
            p1.hand.append(deck.deal()) 
            p2.hand.append(deck.deal()) 

        # Choose dealer in first row
        if settings.row == 1: 
            dealer = random.choice([p1, p2])
            dealer.is_dealer()

        """Start phase"""
        for _ in range(TOTAL_PHASES):                
            settings.phase += 1
            print(f"Starting phase {settings}...\n")

            if settings.phase == 1:
                # Set first to play = p1
                if p1.dealer == True:
                    p1, p2 = p2, p1
                p1.plays_first()
            else:
                # Set first to play in phase 2 - 3
                if p2.first == True:
                    p2, p1 = p1, p2

            print(f"First to play is {p1} and second to play is {p2}\n")
            
            print(f"{p1} = {p1:hand}, {p2} = {p2:hand}\n") 

            # Playing turns - First variable in turn() is current player's turn
            p1card = turn(p1, p2, settings)   
            # Rejected truco
            if p1card == False:
                break
            p2card = turn(p2, p1, settings)
            # Rejected truco
            if p2card == False:
                break

            """ End phase """
            # Compare cards
            msg = f"The winner of phase {settings} is"
            
            # P1 wins
            if p1card > p2card:
                p1.add_phase_point()
                settings.phase_winner.append(p1.name)

            # P2 wins
            elif p1card < p2card:
                p2.add_phase_point()
                settings.phase_winner.append(p2.name)
                # Winner is first to play in next phase
                p2.plays_first()
                p1.plays_last()
            # Tie
            else:
                settings.phase_winner.append("tie")
                msg = f"There is a"
            print(f"{msg} {settings:phasew}\n")
            print(f"Current phase points: {p1} {p1.phase_point} {p2} {p2.phase_point}")
            print(f"Current truco points: {settings.truco_points}")
        
            """ End row """
            if settings.phase > 1:
                if end_row(p1, p2, settings):
                    break

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


def exit_game(msg=None):
    if msg == None:
        print()
        print("Exit game? (Yes/No)")
        menu = Menu([
            ["yes"],
            ["no"],
        ])
        answer = menu.get_answer()

    if msg == "winner" or answer == "yes":
        exit("--Thank you for playing truco, see you!")
    return


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
            choise = Menu(["envido", "real envido", "falta envido"])
            print(f"{choise:horizontal}")
            choise = choise.get_answer()
            envido(px, py, settings, choise)
        case "truco":
            if truco(px, py, settings):
                # Play card after truco
                return play_card(px)
            else:
                return False # End row
        case "play":
            return play_card(px)


def envido(px, py, settings, call):
    phase = settings.envido_phase 
    chain = settings.envido_chain

    print(F"{px} says -{call.upper()}!-\n")

    opt_list = [
        ["accept"],
        ["reject"],
        ["reply"],
    ]

    # Eliminate reply option when "falta envido is called"
    if phase > 1:
        opt_list.pop()    

    # Prompt envido options
    print(f"{py} answers:")  
    options = Menu(opt_list)
    print(f"{options}")
    answer = options.get_answer()

    match answer:
        case "accept":
            for value in chain[phase].values():
                settings.envido_points =+ value
            play_envido()
        case "reject":
            settings.envido_points += 1
            score(px, settings, "envido")

        case "reply":
            replies = [value for value in chain[phase:]]
            reply = Menu(replies)
            phase += 1
            envido(py, px, settings, reply)

def play_envido():
    exit("-----------------TO DO--------------------")
    

def truco(px, py, settings):
    n = settings.truco_phase 
    chain = settings.truco_chain
    
    for key in chain[n]:
        print(f"{px} says -{key.upper()}!-\n") 

    opt_list = [
        ["accept"],
        ["reject"],
        ["reply"],
    ]

    # Eliminate reply option when "vale 4 is called"
    if n > 1:
        opt_list.pop()    
    
    # Prompt truco options
    print(f"{py} answers:")  
    options = Menu(opt_list)
    print(f"{options}")
    answer = options.get_answer()

    match answer:
        case "accept":
            for value in chain[n].values():
                settings.truco_points = value
            settings.truco_phase += 1
            return True
        case "reject":
            return False
        case "reply":
            settings.truco_phase += 1
            truco(py, px, settings)


def end_row(p1, p2, settings):
    # No ties in game
    if tie := "tie" not in settings.phase_winner:
        if p1.phase_point == 2:
            score(p1, settings, "end")
            print(f"{p1} wins, points: {p1.game_score}")
        elif p2.phase_point == 2:
            score(p2, settings, "end")
            print(f"{p2} wins, points: {p2.game_score}")
        # px won phase 1 and py won fase 2, move to phase 3
        else:
            return False
    # Ties in game
    else:
        # Ties in row and p1 wins another phase
        if match := p1.name in settings.phase_winner: 
            score(p1, settings)
            print(f"{p1} wins, points: {p1.game_score}")
        # Ties in row and p2 wins another phase
        elif match := p2.name in settings.phase_winner: 
            score(p2, settings)
            print(f"{p2} wins, points: {p2.game_score}")
        else:
            # 2 Ties in phase 2, move to phase 3
            if settings.phase == 2: 
                return False
            else:
                # Triple tie, p1 wins
                score(p1, settings) 
                print(f"{p1} wins, points: {p1.game_score}")   
    # Clean hands
    p1.clean_hand()
    p2.clean_hand()
    return True


def play_card(px):
    card = Card(px.pick_card(f"{px:hand}"))
    print(f"{px:hand} left\n")
    return card.truco_val


def score(px, settings, phase=None):
    # Sum envido points to personal score
    if phase == "envido":
        px.update_game_score(settings.envido_points)
    # Sum truco points to personal score
    else:
        px.update_game_score(settings.truco_points)  
    
    # Print score points
    print(f"GAME SCORE POINTS --> {px.game_score}")

    # Compare with total score
    if px.game_score >= goal_scre:
        if px.name == "PC":
            print(f"😭😭 I'm sorry, you lost against {px.name} 😭😭")
        else:
            print(f"😁😁 Congratulations {px.name}!! You won the game 😁😁!!")
        exit_game("winner")
    else:    
        return



if __name__ == "__main__":
    main()    