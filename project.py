from sys import exit
from tabulate import tabulate
from time import sleep
from pyfiglet import Figlet
from classes import Menu, Deck

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
    pc_scre = 0
    hm_scre = 0
    
    # Starting message
    print(f"Starting game...\n\nThe first who reaches {goal_scre} points wins", end="\n\n") 
    print("")
        
    # Shuffling
    deck = Deck()
    deck.shuffle()
    deck.cut()
    
    # Dealing
    ...
    print(deck)    
        
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


if __name__ == "__main__":
    main()    