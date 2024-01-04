from sys import exit
from tabulate import tabulate
from time import sleep
from pyfiglet import Figlet
from classes import Menu

def main():
    # Welcome
    introduction()
    
    # Menu options: Start game, Rules, exit
    menu = Menu()
    print(menu, end="\n\n")
    
    # User answer
    choise = get_answer()

    # Move to options
    match choise:
        case "start":
            play()
        case "rules":
            rules()
        case "quit":
            exit("Thank you for playing truco, see you!")
    
# Rules
def rules():   
    ...
    # Deck
    # Envido
    # Truco
    # Scores

def play():
    ...
    # Jugability
        # Dealer
        # First row
        # Second row
        # Third row

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

    # Ask name
    name = input("What's your name?\n\n").strip()
    name = name[0:21]
    print()
    sleep(1)

    # Say hello
    print(f"Welcome {name}! Read the menu in order to start your game:", end="\n\n")    
    sleep(2)    


def get_answer():
    """
    Let de user choise
    """  
    while choise := input("Command:").strip().lower() not in ["start", "rules", "quit"]:
        continue
    return choise


if __name__ == "__main__":
    main()    