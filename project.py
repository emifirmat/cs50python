from sys import exit
from tabulate import tabulate
from time import sleep
from pyfiglet import Figlet
from classes import *
from tabulate import tabulate
import random, csv, re, itertools


# Constant variables
TOTAL_PHASES = TOTAL_CARDS = 3

# Default game settings
goal_scre = 30


def main():
    # Welcome
    ...
    
    # Menu options: Start game, Rules, exit
    while True:
        choise = set_menu([
            ["start", "Start game"],
            ["rules", "Learn how to play"],
            ["quit", "Exit game"],
        ])

        # Move to options
        match choise:
            case "rules":
                rules()
            case "quit":
                exit_game()
            case "start":
                # Create settings, players and deck
                settings = Settings()
                p1, p2 = Player("Emi"), Player("PC")
                full_deck = set_deck("cards_values.csv")
                
                print(f"Starting game...\n\nThe first who reaches {goal_scre} points wins\n")               

                """ Start Row """
                while True:
                    # Clean hands and values from previous rows
                    for cls in [p1, p2, settings]:
                        cls.restart_values()
                    
                    # Start row
                    settings.new_row()
                    print(f"Starting row {settings.row}\n")

                    # Shuffling
                    deck = Deck(full_deck)
                    deck.shuffle()
                    deck.cut()

                    # Dealing - nested loop
                    p1, p2 = choose_dealer(p1, p2, settings)
                    [p.add_card(deck.deal()) for _ in range(TOTAL_CARDS) for p in [p1, p2]] 
                    
                    """Start phase"""
                    for _ in range(TOTAL_PHASES):                
                        settings.new_phase()
                        print(f"Starting phase {settings.phase}...\n")

                        # Set phase 2 - 3 
                        if settings.phase > 1:
                            settings.lock_envido()
                            # If p2 won, is first to play
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
                        if p2card == False:
                            break

                        """ End phase """
                        end_phase(p1card, p2card, p1, p2, settings)
                    
                        """ End row """
                        if settings.phase > 1:
                            winner = end_row(p1, p2, settings)
                            if winner:
                                print(f"{winner} wins this row--")
                                break
    
# Rules
def rules():   
    while True:
        # Intro rules
        print("--To learn how to play, choose a command from the menu\n")
            
        # Rules menu
        choise = set_menu([
            ["intro"],
            ["cards"],
            ["main"],
            ["envido"],
            ["truco"],
            ["scores"],
        ])
        if choise == "quit":
            break
        # Show text from file
        try:
            with open(f"rules/{choise}.txt") as file:
                print(f"{file.read()}\n")
        except FileNotFoundError:
            print("Sorry, missing information, try another option")
        
        # Ask to continue or leave rules
        sleep(1)
        nchoise = input("Enter <any letter> to continue navigating or <quit> to go back to main menu.\n\n>> ")
        if nchoise == "quit":
           break
    # Go back to main menu
    print()
    return 


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
        print("\nExit game? (Yes/No)")
        # Reprompt until receive a proper answer
        while True:
            answer = input(">> ").lower().strip()
            if match := re.search(r"(^y(es)?$)|(^no?$)", answer):
                break
    # End game
    if msg == "winner" or (match := re.search(r"(^y(es)?$)", answer)):
        exit("--Thank you for playing truco, see you!")
    # Go back
    return


def turn(px, py, settings):
    # Print turn
    print(f"It's {px}'s turn...\n")
    while True:
        # Set menu
        trucostr = set_truco_call(settings)
        menu = [
            ["envido", "Call envido"],           
            ["truco", "Call " + trucostr],     
            ["play", "Play a card"],
        ]
        # Contemplate in-game cases
        if px.truco_call == False:
            menu = menu[2:] 
        elif settings.envido == False:
            menu = menu[1:]
        else:
            pass
        option = set_menu(menu)

        # Execute option
        match option:
            case "envido":
                settings.lock_envido()
                choise = set_menu(["envido", "real envido", "falta envido"], "envido")
                winner, loser = envido(px, py, settings, choise)
                score(winner, loser, settings, "envido")
            case "truco":
                if truco(px, py, settings):
                    # Play card after truco
                    return play_card(px)
                else:
                    score(px, py, settings)
                    return False # End row
            case "play":
                return play_card(px)


def envido(px, py, settings, call):  
    phase = settings.envido_phase 
    chain = settings.envido_chain[phase:]

    # Update envido phase
    if call == "real envido":
        phase = 1
    if call == "falta envido":
        phase = 2

    print(f"{px} says -{call.upper()}!-\n")

    # Prompt envido options and eliminate reply option when "falta envido" is called
    opt_list = [["accept"], ["reject"], ["reply"],]
    if phase > 1:
        opt_list.pop()    
    print(f"{py} answers:")  
    answer = set_menu(opt_list)

    # Py answers
    match answer:
        case "accept":        
            winner, loser = play_envido(px, py)
            
            # Update score / falta envido vs others
            if phase == 2:
                settings.set_falta_envido(goal_scre, loser.game_score)
                if chain[phase]['falta envido'] > settings.envido_score:
                    settings.envido_score = chain[phase]['falta envido'] 
            else:
                for value in chain[phase].values():
                    settings.envido_score += value
            print(f"envido score = {settings.envido_score}")
            return winner, loser
        case "reject":
            if settings.envido_score == 0:
                settings.envido_score = 1
            print(f"envido score = {settings.envido_score}")
            return px, py
        case "reply":
            # Update points
            for value in chain[phase].values():
                settings.envido_score += value
            # Enable another envido if it was called once
            if settings.envido_score == 2:
                phase = 0
            else:
                phase += 1
            # Order new menu and get answer
            replies = [key for row in chain[phase:] for key in row.keys()]   
            reply = set_menu(replies, "envido")
            return envido(py, px, settings, reply)


def play_envido(caller, replier):   
    """ Get envido points from each player """
    for p in (replier, caller):
        p.update_env_points(get_envido_points(p))

    """ Replier is first to play """ 
    # See hand and say points
    print(f"{replier:hand}") 
    print(f"{replier.name}: I have {replier.envido_points} points!")

    """ Caller answers """
    # See hand and say points
    print(f"{caller:hand}")

    # Replier wins (tie included)
    if caller.envido_points <= replier.envido_points:
        print(f"{caller.name}: Son buenas!")
        return replier, caller
    # Caller wins
    else:
        print(f"{caller.name}: And I have {caller.envido_points} points. I win!")    
        return caller, replier


def get_envido_points(p):
    points = 0

    # Set filter if there are 2 cards of the same type
    type_filter = search_type(p)
    
    if type_filter is not None:
        # Get and sort cards of the filter type
        env_cards = list(filter(lambda card: card['type'] == type_filter, p.fullhand))
        env_cards = sorted(env_cards, key=lambda x: x['envido'], reverse=True) 
        
        # If there are 3 cards of the same type, remove the one with less value
        if len(env_cards) == 3:
            env_cards.pop()
        # Add points for having 2 of the same type cards
        points = 20
    else: 
        # Leave only the card with the highest points
        env_cards = list(sorted(p.fullhand, key=lambda x: x['envido'], reverse=True))
        while len(env_cards) != 1:
            env_cards.pop()
    # Add points 
    for card in env_cards:
        points += int(card['envido'])
    return points


def search_type(p):
    for n in range(TOTAL_CARDS):
        for j in range(n + 1, TOTAL_CARDS):
            if p.fullhand[n]['type'] == p.fullhand[j]['type']:
                return p.fullhand[n]['type']
    return


def truco(px, py, settings):
    phase = settings.truco_phase 
    chain = settings.truco_chain
    
    for key in chain[phase]:
        print(f"{px} says -{key.upper()}!-\n") 

    opt_list = [
        ["accept"],
        ["reject"],
        ["reply"],
    ]

    # Eliminate reply option when "vale 4 is called"
    if phase > 1:
        opt_list.pop()    
    
    # Prompt truco options
    print(f"{py} answers:")  
    answer = set_menu(opt_list)

    # py answers
    match answer:
        case "accept":
            # Vale 4 vs other truco calls
            if phase == 2:
                py.lock_truco()
            else:
                py.unlock_truco()
                settings.new_truco_phase()
            # Caller can't call twice in a row, envido can't be called after truco
            px.lock_truco()
            settings.lock_envido()
            for value in chain[phase].values():
                settings.truco_score = value
            return True
        case "reject":
            for value in chain[phase].values():
                settings.truco_score = value - 1
            print(f"{px} wins this row--\n")
            return False
        case "reply":
            settings.new_truco_phase()
            return truco(py, px, settings)
            

def play_card(px):
    print(f"{px.name} picks a card: ")
    while True:
        try:
            number, c_type = input(f"{px:hand}\n").lower().strip().split(" ")
            card = px.pick_card(number, c_type)
            print(f"\n{px.name} plays {card['number']} {card['type']}\n\n{px:hand} left\n")
        except (ValueError, TypeError):
            continue
        else:
            return int(card['truco'])


def end_phase(p1card, p2card, p1, p2, settings):
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
    print(f"Current truco points: {settings.truco_score}")


def end_row(p1, p2, settings):
    # Truco was not called in whole row
    if settings.truco_score == 0:
        settings.truco_score = 1
    
    # No ties in game
    if settings.phase_winner[0] != "tie":
        if p1.phase_point == 2:
            score(p1, p2, settings)
            return p1
        elif p2.phase_point == 2:
            score(p2, p1, settings)
            return p2
        # None won 2 phases
        elif settings.phase == 2 and settings.phase_winner[1] != "tie":
            return False
        # There was a tie in third row, first phase winner wins
        else:
            if p1.name == settings.phase_winner[0]:
                return p1
            else:
                return p2
    # Tie in first row
    else:
        # p1 wins another phase
        if p1.name in settings.phase_winner: 
            score(p1, p2, settings)
            return p1
        # p2 wins another phase
        elif p2.name in settings.phase_winner: 
            score(p2, p1, settings)
            return p2
        # 2 Ties move to phase 3
        elif settings.phase == 2: 
            return False
        else:
            # Triple tie, p1 wins
            score(p1, p2, settings) 
            return p1  


def score(px, py, settings, phase=None):
    # Sum row score to player score
    if phase == "envido":
        px.update_game_score(settings.envido_score)
    else:
        px.update_game_score(settings.truco_score) 

    # Print score points
    settings.update_row_points(settings.envido_score, settings.truco_score)
    print(f"{px} POINTS --> {px.game_score}")
    print(f"{py} POINTS --> {py.game_score}")
    print(f"GAME SCORE POINTS --> {settings.row_points}")

    # Compare with total score
    if px.game_score >= goal_scre:
        if px.name == "PC":
            print(f"😭😭 I'm sorry, you lost against {px.name} 😭😭")
        else:
            print(f"😁😁 Congratulations {px.name}!! You won the game 😁😁!!")
        exit_game("winner")
    else:    
        return


def set_menu(list, call=None):
    menu = Menu(list)
    if call == "envido":
        print(f"{' | '.join(list)}\n")
    else: 
        print(f"{tabulate(list, headers=['Command', 'Description'])}\n")
        
    # Check user answer
    while True:
        choise = input("Command: ").strip().lower().replace("exit", "quit")
        if menu.in_menu(choise):
            return choise


def set_deck(filerute):
    try:
        with open(filerute) as file: 
            csv_file = csv.DictReader(file)       
            cards_list = [row for row in csv_file]  
    except FileNotFoundError:
        exit("Can't open cards values file")  
    return cards_list


def choose_dealer(p1, p2, settings):
    if settings.row == 1: 
        dealer = random.choice([p1, p2])
        dealer.change_dealer()
        
        # Set first to play = p1
        if p1.dealer == True:
            p1, p2 = p2, p1
    else:
        p1, p2 = p2, p1
        for p in [p1, p2]:
            p.change_dealer()
    p1.plays_first()
    return p1, p2


def set_truco_call(settings):
    try:
        for string in settings.truco_chain[settings.truco_phase].keys():
            trucostr = string
    except IndexError:
        trucostr = "vale cuatro"
    return trucostr


if __name__ == "__main__":
    main()    