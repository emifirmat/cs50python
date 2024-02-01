import random, csv, re, pc, time
from sys import exit
from tabulate import tabulate
from pyfiglet import Figlet
from classes import *
from tabulate import tabulate
from termcolor import colored, cprint


# Constant variables
TOTAL_PHASES = TOTAL_CARDS = 3

# Default game settings
goal_scre = 30
f = Figlet(font="slant")


def main():
    # Welcome
    game = "Truco card game"
    name = introduction(game)

    # Menu options: Start game, rules, settings, exit.
    while True:
        choise = set_menu(
            [
                ["start", "Start game"],
                ["rules", "Learn how to play"],
                ["settings", "Change settings"],
                ["quit", "Exit game"],
            ]
        )
        match choise:
            case "rules":
                rules()
            case "settings":
                global goal_scre
                goal_scre = set_gscore()
                time.sleep(1)
            case "quit":
                exit_game()
            case "start":
                # Create settings, players and deck
                settings = Settings()
                p1, p2 = Player(name), Player("PC")
                full_deck = set_deck("cards_values.csv")

                cprint(f"Starting game...\n", "white", attrs=["bold"])

                f_text = colored(
                    str(goal_scre) + " POINTS", "light_green", attrs=["bold"]
                )
                print(f"<<< The first who reaches {f_text} wins >>>\n")
                time.sleep(2)

                """ Start Row """
                while True:
                    # Clean hands and values from previous rows
                    if settings.row > 0:
                        for cls in [p1, p2, settings]:
                            cls.restart_values()
                    # Start row
                    settings.new_row()
                    cprint(
                        f"-----Starting row {settings.row}-----\n",
                        "blue",
                        attrs=["bold"],
                    )
                    time.sleep(1)

                    # Shuffling
                    deck = Deck(full_deck)
                    deck.shuffle()
                    deck.cut()

                    # Dealing - nested loop
                    p1, p2 = choose_dealer(p1, p2, settings)
                    [
                        p.add_card(deck.deal())
                        for _ in range(TOTAL_CARDS)
                        for p in [p1, p2]
                    ]
                    for p in [p1, p2]:
                        p.update_env_points(get_envido_points(p))

                    """Start phase"""
                    for _ in range(TOTAL_PHASES):
                        settings.new_phase()
                        f_text = colored("phase " + str(settings.phase), attrs=["bold"])
                        print(f".....Starting {f_text}.....\n")

                        # Copy temp hand for envido and truco situations
                        for p in [p1, p2]:
                            p.temp_hand = p.hand[:]
                        # Set phase 2 - 3
                        if settings.phase > 1:
                            # If neither truco or envido were called in ph1
                            settings.lock_envido()
                            # If p2 won, is first to play
                            if p2.first == True:
                                p2, p1 = p1, p2
                        f_text = [colored("First", "blue"), colored("second", "blue")]
                        print(
                            f"{f_text[0]} to play is {p1} and {f_text[1]} to play is {p2}.\n"
                        )
                        time.sleep(2)
                        if p1.name == "PC":
                            print(f"{p2:s_hand}")
                        else:
                            print(f"{p1:s_hand}")
                        time.sleep(2)

                        # Playing turns - First variable in turn() is current player's turn
                        p1card = turn(p1, p2, settings)
                        # Rejected truco
                        if p1card == False:
                            break
                        time.sleep(1)
                        p2card = turn(p2, p1, settings, p1card)
                        if p2card == False:
                            break
                        time.sleep(1)

                        """ End phase """
                        end_phase(p1card, p2card, p1, p2, settings)

                        """ End row """
                        if settings.phase > 1:
                            winner = end_row(p1, p2, settings)
                            if winner:
                                print(f"<< {winner[0]} wins this row >>\n")
                                break


""" Primary functions"""


def introduction(game):
    # Welcome msg
    cprint(f.renderText(game), "light_blue")
    time.sleep(1)

    # Ask name and limit length up to 20 chars
    while True:
        name = input("-- What's your name?\n>> ").strip()
        if len(name) > 0:
            name = name[0:21]
            break
    time.sleep(1)

    # Say hello
    print(
        f"\n-- Welcome {name}! Read the menu in order to start your game:", end="\n\n"
    )
    time.sleep(2)
    return name


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


def rules():
    while True:
        print("--To learn how to play, choose a command from the menu\n")

        # Rules menu
        choise = set_menu(
            [
                ["intro"],
                ["cards"],
                ["main"],
                ["envido"],
                ["truco"],
                ["scores"],
                ["back"],
            ]
        )
        if choise in ["quit", "back"]:
            break
        # Show text from file
        try:
            with open(f"rules/{choise}.txt") as file:
                print(f"{file.read()}\n")
        except FileNotFoundError:
            print("Sorry, missing information, try another option")
        time.sleep(1)

        # Ask to continue or leave rules
        nchoise = input(
            "Enter <any letter> to continue navigating or <quit> to go back to main menu.\n>> "
        )
        if nchoise == "quit":
            break
        print()
    return


def set_gscore():
    while True:
        # Prompt 15 or 30
        score = input("Set goal score to <15> or <30>:\n>> ").strip()
        if score == "15" or score == "30":
            # Print confirmation msg
            f_text = colored(score, "light_green", attrs=["bold"])
            print(f"Game now is up to {f_text} points.\n")
            return int(score)


def exit_game(msg=None):
    if msg == None:
        # Ask confirmation to quit
        print("\nExit game? (Yes/No)")
        while True:
            answer = input(">> ").lower().strip()
            if match := re.search(r"(^y(es)?$)|(^no?$)", answer):
                break
    # End game
    if msg == "winner" or (match := re.search(r"(^y(es)?$)", answer)):
        exit("----Thank you for playing truco, see you!----")
    # Go back to menu
    return


def set_deck(filerute):
    try:
        with open(filerute) as file:
            csv_file = csv.DictReader(file)
            cards_list = [row for row in csv_file]
    except FileNotFoundError:
        exit("Can't open cards values file")
    if len(cards_list) != 40:
        raise ValueError("This file doesn't have 40 cards")
    return cards_list


def choose_dealer(p1, p2, settings):
    # Row 1, pick random dealer
    if settings.row == 1:
        dealer = random.choice([p1, p2])
        dealer.change_dealer()
    # Dealer changes every row
    else:
        [p.change_dealer() for p in [p1, p2]]
    # As p1 and p2 change during phases, I have to check every row
    if p1.dealer == True:
        p1, p2 = p2, p1
    p1.plays_first()
    return p1, p2


def get_envido_points(p):
    points = 0
    # Sort cards from higher to lower value
    env_cards = sorted(p.temp_hand, key=lambda x: x["envido"], reverse=True)
    # Set filter if there are 2 cards of the same type
    type_filter = search_type(p)
    if type_filter is not None:
        # Get cards of the filter type
        env_cards = list(filter(lambda card: card["type"] == type_filter, env_cards))
        # If there are 3 cards of the same type, remove the one with less value
        if len(env_cards) == 3:
            env_cards.pop()
        # Add points for having 2 of the same type cards
        points = 20
    else:
        # Leave only the card with the highest points
        while len(env_cards) != 1:
            env_cards.pop()
    # Add points
    for card in env_cards:
        points += int(card["envido"])
    return points


def turn(px, py, settings, p1card=None):
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
        # PC or player calls
        if px.name == "PC":
            option = pc.call(
                len(menu),
                px.envido_points,
                settings.phase,
                settings.phase_winner,
                px.hand,
            )
        else:
            menu.extend(
                [["hand", "Show hand"], ["score", "Show scores"], ["quit", "Quit game"]]
            )
            option = set_menu(menu)
        match option:
            case "envido":
                choice = choose_envido(px, settings)
                winner, loser = envido(px, py, settings, choice)
                score(winner, loser, settings, "envido")
            case "truco":
                if truco(px, py, settings):
                    # Play card after truco
                    return play_card(px, settings, p1card)
                else:
                    # End row
                    return False
            case "play":
                return play_card(px, settings, p1card)
            case "hand":
                print(f"{px:s_hand}")
                time.sleep(2)
            case "score":
                show_score(px, py, settings)
                time.sleep(2)
            case "quit":
                exit_game()


def end_phase(p1card, p2card, p1, p2, settings):
    msg = f"The winner of {colored('phase ' + str(settings), attrs=['bold'])} is"

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
    print(f"{msg} {settings:phasew}")
    print(f"Current phase points: {p1} {p1.phase_point} {p2} {p2.phase_point}\n")
    time.sleep(1)


def end_row(p1, p2, settings):
    # Truco was not called in whole row
    if settings.truco_score == 0:
        settings.truco_score = 1
    # No ties in game
    if settings.phase_winner[0] != "tie":
        if p1.phase_point == 2:
            score(p1, p2, settings)
            return (p1, True)
        elif p2.phase_point == 2:
            score(p2, p1, settings)
            return (p2, True)
        # None won 2 phases
        elif settings.phase == 2 and settings.phase_winner[1] != "tie":
            return False
        # There was a tie in third row, first phase winner wins
        else:
            if p1.name == settings.phase_winner[0]:
                score(p1, p2, settings)
                return (p1, True)
            else:
                score(p2, p1, settings)
                return (p2, True)
    # Tie in first row
    else:
        # p1 wins another phase
        if p1.name in settings.phase_winner:
            score(p1, p2, settings)
            return (p1, True)
        # p2 wins another phase
        elif p2.name in settings.phase_winner:
            score(p2, p1, settings)
            return (p2, True)
        # 2 Ties move to phase 3
        elif settings.phase == 2:
            return False
        else:
            # Triple tie, p1 wins
            score(p1, p2, settings)
            return (p1, True)


""" Secondary functions"""


def search_type(p):
    for n in range(TOTAL_CARDS):
        for j in range(n + 1, TOTAL_CARDS):
            if p.temp_hand[n]["type"] == p.temp_hand[j]["type"]:
                return p.temp_hand[n]["type"]
    return


def set_truco_call(settings):
    try:
        for string in settings.truco_chain[settings.truco_phase].keys():
            trucostr = string
    except IndexError:
        trucostr = "vale cuatro"
    return trucostr


def choose_envido(px, settings):
    """Used only for envido call (not answer)"""
    settings.lock_envido()
    envido_list = ["envido", "real envido", "falta envido"]
    if px.name == "PC":
        return pc.select_envido(envido_list, px.envido_points)
    else:
        return set_menu(envido_list, "envido")


def envido(px, py, settings, call):
    phase = settings.envido_phase
    chain = settings.envido_chain[phase:]

    # Update envido phase
    if call == "real envido":
        phase = 1
    elif call == "falta envido":
        phase = 2
    print(f"{px} says -{colored(call.upper() + '!', 'blue', attrs=['bold'])}-\n")
    time.sleep(1)

    """ Py answers """
    print(f"{py} answers:")
    opt_list = [
        ["accept"],
        ["reject"],
        ["reply"],
    ]
    # Eliminate reply option when "falta envido" is called.
    if phase > 1:
        opt_list.pop()
    # PC or player answers
    if py.name == "PC":
        answer = pc.answer_envido(
            opt_list, py.envido_points, settings.envido_score, phase
        )
        print(f">> {answer.title()}\n")
    else:
        answer = set_menu(opt_list)
    match answer:
        case "accept":
            winner, loser = play_envido(px, py)
            # Update score: falta envido vs others.
            if phase == 2:
                settings.set_falta_envido(goal_scre, loser.game_score)
                # There are NOT accumulative score points.
                settings.envido_score = chain[phase]["falta envido"]
            else:
                # Up to real envido, score is accumulative.
                for value in chain[phase].values():
                    settings.envido_score += value
            time.sleep(3)
            return winner, loser
        case "reject":
            time.sleep(1)
            # First envido rejected
            if settings.envido_score == 0:
                settings.envido_score = 1
            return px, py
        case "reply":
            # Update score
            for value in chain[phase].values():
                settings.envido_score += value
            # Enable another envido if it was called once
            if settings.envido_score == 2:
                phase = 0
            else:
                phase += 1
            # Set new menu and get answer
            replies = [key for row in chain[phase:] for key in row.keys()]
            if py.name == "PC":
                reply = pc.reply_envido(replies, py.envido_points, phase)
            else:
                reply = set_menu(replies, "envido")
            return envido(py, px, settings, reply)


def truco(px, py, settings):
    phase = settings.truco_phase
    chain = settings.truco_chain
    for key in chain[phase]:
        print(f"{px} says -{colored(key.upper() + '!', 'blue', attrs=['bold'])}-\n")
    time.sleep(1)

    opt_list = [
        ["accept"],
        ["reject"],
        ["reply"],
    ]
    # Let py call envido if they haven't played yet.
    if (
        px.first == True
        and settings.phase == 1
        and settings.envido == True
        and phase == 0
    ):
        opt_list.insert(0, ["envido"])
    # Eliminate reply if vale 4 was called
    if phase > 1:
        opt_list.pop()

    """ py answers"""
    print(f"{py} answers:")
    # PC or user answers
    if py.name == "PC":
        answer = pc.answer_truco(
            settings.phase,
            settings.phase_winner,
            opt_list,
            py.temp_hand,
            py.envido_points,
        )
        print(f">> {answer.title()}\n")
    else:
        answer = set_menu(opt_list)
    match answer:
        case "envido":
            # Py called envido
            choice = choose_envido(py, settings)
            winner, loser = envido(py, px, settings, choice)
            score(winner, loser, settings, "envido")
            # Retake truco
            return truco(px, py, settings)
        case "accept":
            # Vale 4 vs other truco calls
            if phase == 2:
                py.lock_truco()
            else:
                # Let replier call next truco phase
                py.unlock_truco()
                settings.new_truco_phase()
            # Caller can't call twice in a row, envido can't be called after truco
            px.lock_truco()
            settings.lock_envido()
            for value in chain[phase].values():
                settings.truco_score = value
            return True
        case "reject":
            time.sleep(1)
            for value in chain[phase].values():
                settings.truco_score = value - 1
            print(f"<< {px} wins this row >>\n")
            # Add score here to contemplate reply chain rejection
            score(px, py, settings)
            return False
        case "reply":
            settings.new_truco_phase()
            return truco(py, px, settings)


def play_card(px, settings, p1card=None):
    print(f"{px} picks a card...")
    time.sleep(1)
    if px.name == "PC":
        card = pc.choose_card(
            settings.phase, px.first, settings.phase_winner, px.hand, p1card
        )
    else:
        while True:
            try:
                number, c_type = input(f"{px:hand}\n>> ").lower().strip().split(" ")
                card = px.pick_card(number, c_type)
                break
            except (ValueError, TypeError):
                continue
    px.hand.remove(card)
    f_text = colored(
        str(card["number"]) + " " + str(card["type"]), "blue", attrs=["bold"]
    )
    print(f"\n** {px} plays {f_text} **\n")
    return int(card["truco"])


def score(px, py, settings, phase=None):
    # Sum row score to player score
    if phase == "envido":
        px.update_game_score(settings.envido_score)
    else:
        px.update_game_score(settings.truco_score)
    # Print score points
    settings.update_row_points(settings.envido_score, settings.truco_score)
    show_score(px, py, settings)

    # Compare with total score
    if px.game_score >= goal_scre:
        if px.name == "PC":
            print(f"\n😭😭 I'm sorry, you lost against {px.name} 😭😭\n\n")
        else:
            f_text = colored(
                f.renderText(f"Congratulations {px.name}!!"),
                "light_green",
            )
            print(f"{f_text}!! You won the game 😁😁!!\n\n")
        exit_game("winner")
    else:
        return


def show_score(px, py, settings):
    for p in [px, py]:
        print(f"{p} TOTAL POINTS --> {p:gscore}")
    print(f"CURRENT ROW SCORE POINTS --> {settings.row_points}")
    print(f"GOAL --> {goal_scre} POINTS\n")


def play_envido(caller, replier):
    """Replier is first to play"""
    # Say points
    f_text = colored(str(replier.envido_points) + " points!", attrs=["bold"])
    print(f"{replier}: I have {f_text}\n")
    time.sleep(2)

    """ Caller answers """
    # Replier wins (tie included)
    if caller.envido_points <= replier.envido_points:
        print(f"{caller}: Son buenas!\n")
        return replier, caller
    # Caller wins
    else:
        f_text = colored(str(caller.envido_points) + " points!", attrs=["bold"])
        print(f"{caller}: And I have {f_text} I win!\n")
        return caller, replier


if __name__ == "__main__":
    main()
