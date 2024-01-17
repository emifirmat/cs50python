from sys import exit
from tabulate import tabulate
from time import sleep
from pyfiglet import Figlet
from classes import Menu, Deck, Player, Settings
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
        print(f"{menu}\n")
        
        # User answer
        choise = menu.get_answer()

        # Move to options
        match choise:
            case "rules":
                rules()
            case "quit":
                exit_game()
            case "start":
                play()
    
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
        # Clean hands and values from previous rows
        p1.restart_values()
        p2.restart_values()
        settings.restart_values()
        
        # Start row
        settings.row += 1
        print("Starting row...\n")
        deck = Deck(cards_list)

        # Shuffling
        deck.shuffle()
        deck.cut()
        
        # Dealing 
        for _ in range(TOTAL_CARDS): 
            p1.add_card(deck.deal()) 
            p2.add_card(deck.deal()) 
        
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

                # Unlock truco
                p1.truco_call = True
                p2.truco_call = True
            else:
                # Set first to play in phase 2 - 3
                if p2.first == True:
                    p2, p1 = p1, p2
                # Lock envido
                settings.envido = False
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
                end_row(p2, p1, settings)
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
            print(f"Current truco points: {settings.truco_score}")
        
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
    while True:
        # Set menu
        trucostr = None
        try:
            for string in settings.truco_chain[settings.truco_phase].keys():
                trucostr = string
        except IndexError:
            trucostr = "vale cuatro"
        menu = [
            ["envido", "Call envido"],           
            ["truco", "Call " + trucostr],     
            ["play", "Play a card"],
        ]
        # Contemplate ingame cases
        if px.truco_call == False:
            menu = menu[2:] 
        elif settings.envido == False:
            menu = menu[1:]
        else:
            pass
        
        # Open menu
        options = Menu(menu)
        print(f"{options}\n")
        option = options.get_answer()

        # Execute option
        match option:
            case "envido":
                settings.envido = False
                choise = Menu(["envido", "real envido", "falta envido"])
                print(f"{choise:horizontal}")
                choise = choise.get_answer()
                envido(px, py, settings, choise)
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

    # Py answers
    match answer:
        case "accept":        
            # Play envido
            winner, loser = play_envido(px, py)
            
            # Update score
            # case: falta envido
            if phase == 2:
                settings.envido_chain[2]['falta envido'] = goal_scre - loser.game_score 
                if settings.envido_chain[2]['falta envido'] > settings.envido_score:
                    settings.envido_score = settings.envido_chain[2]['falta envido'] 
            else:
                for value in chain[phase].values():
                    settings.envido_score += value
            score(winner, loser, settings, "envido")
        case "reject":
            if settings.envido_score == 0:
                settings.envido_score = 1
            score(px, py, settings, "envido")
        case "reply":
            # Update points
            for value in chain[phase].values():
                settings.envido_score += value
            print(f"envido score = {settings.envido_score}")
            
            # Set possible options to answer
            if settings.envido_score == 2:
                phase = 0
            else:
                phase += 1
            
            # Order new menu and get answer
            replies = []
            for row in chain[phase:]:
                for key in row.keys():
                    replies.append(key)    
            reply = Menu(replies)
            print(f"{reply:horizontal}")
            reply = reply.get_answer()
            envido(py, px, settings, reply)


def play_envido(px, py):   
    """ Get envido points from each player """
    py.update_env_points(get_envido_points(py))
    px.update_env_points(get_envido_points(px))

    """ py(replier) is first to play """ 
    # See hand
    print(f"{py:hand}")

    # py says its cards       
    print(f"{py.name}: I have {py.envido_points} points!")

    """ px answers """
    # See hand
    print(f"{px:hand}")
    
    if px.envido_points < py.envido_points:
        print(f"{px.name}: Son buenas!")
        return py, px
    else:
        print(f"{px.name}: And I have {px.envido_points} points. I win!")    
        return px, py


def get_envido_points(p):
    type_filter = None
    env_cards = [] 
    points = 0

    # Set filter if there are 2 cards of the same type
    for n in range(TOTAL_CARDS):
        for j in range(n + 1, TOTAL_CARDS):
            if p.fullhand[n]['type'] == p.fullhand[j]['type']:
                type_filter = p.fullhand[n]['type']
                break
        if type != None:
            break
    # Take cards of the filter type
    if type_filter is not None:
        # Get and sort cards 
        env_cards = list(filter(lambda card: card['type'] == type_filter, p.fullhand))
        env_cards = sorted(env_cards, key=lambda x: x['envido'], reverse=True) 
        
        # If there are 3 cards of the same type, remove the one with less value
        if len(env_cards) == 3:
            env_cards.pop()
        
        # Add points for having 2 of the same type cards
        points = 20
    else: 
        env_cards = sorted(p.hand, key=lambda x: x['envido'], reverse=True)
        
        # Leave only the card with the highest points
        while len(env_cards) != 1:
            env_cards.pop()
    # Add points 
    for card in env_cards:
        points += int(card['envido'])
    return points


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
    options = Menu(opt_list)
    print(f"{options}")
    answer = options.get_answer()

    # py answers
    match answer:
        case "accept":
            # Set truco and envido calls allowance
            if phase == 2:
                py.truco_call = False
            else:
                py.truco_call = True
                settings.truco_phase += 1
            px.truco_call = False
            settings.envido = False
            for value in chain[phase].values():
                settings.truco_score = value
            return True
        case "reject":
            for value in chain[phase].values():
                settings.truco_score = value - 1
            return False
        case "reply":
            settings.truco_phase += 1
            truco(py, px, settings)
            return True


def end_row(p1, p2, settings):
    # Truco was not called in whole row
    if settings.truco_score == 0:
        settings.truco_score = 1
    
    # No ties in game
    if tie := "tie" not in settings.phase_winner:
        if p1.phase_point == 2:
            score(p1, p2, settings, "end")
            print(f"{p1}", end="")
        elif p2.phase_point == 2:
            score(p2, p1, settings, "end")
            print(f"{p2}", end="")
        # px won phase 1 and py won fase 2, move to phase 3
        else:
            return False
    # Ties in game
    else:
        # Ties in row and p1 wins another phase
        if match := p1.name in settings.phase_winner: 
            score(p1, p2, settings)
            print(f"{p1}", end="")
        # Ties in row and p2 wins another phase
        elif match := p2.name in settings.phase_winner: 
            score(p2, p1, settings)
            print(f"{p2}", end="")
        else:
            # 2 Ties in phase 2, move to phase 3
            if settings.phase == 2: 
                return False
            else:
                # Triple tie, p1 wins
                score(p1, p2, settings) 
                print(f"--{p1}", end=" ")   
    print(f"wins this row--")
    return True


def play_card(px):
    print(f"{px.name} picks a card: ")
    card = px.pick_card(f"{px:hand}")
    print(f"{px.name} plays {card['number']} {card['type']}\n\n{px:hand} left\n")
    return int(card['truco'])


def score(px, py, settings, phase=None):
    # Sum envido points to personal score
    if phase == "envido":
        px.update_game_score(settings.envido_score)
    # Sum truco points to personal score
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


if __name__ == "__main__":
    main()    