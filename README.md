# Truco card game
#### Video Demo: https://youtu.be/aWjiNQVxBqQ
#### Description:
**The project**
The current project is a card game, very popular in Argentina, that is played with a Spanish deck. 
This version of the game only supports 1v1 and does not apply "flor" rules. 
The **objective** of the game is to reach a total score of 15 or 30 depending on the settings. In order to achieve it, players can earn points from "envido" and "truco" every row.
At the beggining of the row, 3 cards are given to each player, and they can play one card per turn. When both players end their turns, the phase is finished. There are 3 phases per row, but it can be ended before depending on how the game develops. 
The project itself contains a "rules" section to learn how to play, with more details and examples.

**Files**
There are 6 python files.

***project.py***  
It cointains the main functions of the game. Most of the libraries were seen through the course. However "time" and "termcolor" were added and used to make the game more user friendly, including colours and slowering the execution of the program. 

*Main function*: Has the main structure of the game. At the very beggining calls the introduction<sup>(1)</sup> function, and returns the name of the user, which will be used then as the player name. 
After that, it displays a menu with the following options: 
    * start: See "primary functions related with start game option in main"
    * rules: It calls rules<sup>(3)</sup> function
    * settings: It calls set_gscore<sup>(4)</sup> to change the global variable goal score.
    * quit: it calls exit_game<sup>(5)</sup> function.

*Primary functions*: They are called by main. 
*Secondary functions*: They are called by a primary function.

*Primary functions*
1) introduction: Shows the name of the game in ASCII art, and prompt the user to tell their name to welcome them. Name should at least have a printable character, and it will be shorten if it has more than 20 characters.
2) set_menu: It is called every time there is a menu of options. It needs a list as an argument and it will display it with the help of tabulate library. In case of envido, it will display options horizontally. Besides, it uses a Menu class to make sure the user is typing the option correctly.
3) rules: It displays a menu with different parts of the game, to let the user choose in detail what they want to know. The chosen option is passed to a csv reader to open the right file and print the rules of that section. The files were written manually and are located in "rules" folder. If the file doesn't exist, an error will raise. User can then continue reading or go back to main menu.
4) set_gscore: It is called by the settings option in main function, to change the global variable goal_score to 15 or 30. No other options is allowed, and after picking a number it prints a confirmation message.
5) exit_game: It is called when player wants to quit game. It prints a confirmation message that supports multiple common answers thanks to "re" library. In case the player choose "yes" or someone won the game, it will finish the program with a goodbye message. If players choose "no" it goes back to previous menu.

*Primary functions related with start game option in main*
When start game is chosen, first the players and settings class are created. After that, a deck is created using the function set_deck<sup>(6)</sup>. Then, some messages are displayed explaining the goal score to win.
Row starts and some class values are restarted if it is not the first one. A message is printed indicating the beginning of a new row and then the deck is shuffled and cut. It continues choosing a dealer through the function choose_dealer<sup>(7)</sup> to determine who plays first. First to play will be called "p1". Both p1 and p2 receive their 3 cards in the same order of the real game, and update their envido points<sup>(8)</sup> that will be necessary for PC to make choises.
Next, the phase start and a message is printed. It can loop 3 times. Temp_hand is copied as sometimes PC needs to make decitions after playing a card, and it needs to include that played card for it. In phase 2 and 3, envido cannot be called anymore, and p1 must be the player who plays first. Player's hand is showed and then each player plays their turn<sup>(9)</sup>. If truco was called and rejected, the loop breaks and start a new row. If not, it returns the truco value of the played card, that will be compared when the end_phase<sup>(10)</sup> functions is called to determine the winner of the phase.  Finally, if at least 2 phases were played, <sup>end_row(11)</sup> will be called to determine if someone won the row and print a message.


6) set_deck: It takes the location of a file which contais the cards with their truco and envido values. The function only checks if the file exists and if there is a list of size 40, which is the size of the deck.

7) choose_dealer: If it is the first row, it picks a random player to be the dealer. Otherwise, the dealer is changed to one player to another. As in every phase p1 and p2 can change, the function always designate the other player as P1 and first to play.

8) get_envido_points: First, it sorts the hand from higher to lower envido points. Then, it  calls the function search_type<sup>(a)</sup> to check if the player has at least 2 cards of the same type. If it returns a type, the function filters those type cards. If all cards are of the same type, it pops the one with lowest value. Finally, it adds 20 envido points. If none type is returned, it only leaves the card of highest envido points. Lastly, it sum each card envido points.  

9) turn: At the beginning, it sets the menu according to the available options. E.G.: Envido cannot be called if truco was accepted and the same player cannot call truco twice. If it is PC turn, it will play by itself (see PC file). If it is player turn, the menu will also show hand, score, and quit options, and the player will be prompted to choose along the menu. Full menu options are: 
    * envido:  It calls "choose_envido"<sup>(c)</sup> for prompt the user to call envido, real envido or falta envido. Then it calls "envido"<sup>(d)</sup> function to return who wins and loses, and finally calls score<sup>(g)</sup> to update de game score. 
    * truco: It calls "truco"<sup>(e)</sup> function. If it was accepted, then it calls and return "play_card"<sup>(f)</sup> function. If not, it returns False to end the row.
    * play: It returns play_card<sup>(f)</sup> function 
    * hand: It prints current player's hand
    * score: Calls show_score<sup>(f)</sup> function.
    * quit: Calls exit_game function <sup>(5)</sup>


10) end_phase: It compares the values returned by turn<sup>(9)</sup> function. If one of the players won, it adds them in a winners list, otherwise it will add "tie". If p2 won, it will also make it play first in next phase. Finally, it prints a message saying who won the current phase and how many in total.

11) end_row: First, if truco was not called in the whole row, it updates the score points it gives to 1. Then it contemplates all different situations, and update the score of the winner. If there is no winner, it returns False, and the row continues to the next phase. If someone won, it returns a tupple: the winner object and True. Note: True is added because at phase 3 hand list is empty and the function returns the winner, but also False.

*Secondary functions*
a) search_type: Using a nested loop, it goes through all the cards of the hand looking for a coincidence in type key. If there is a coincidence, it returns the type (club, coin, sword, cup), else None.

b) set_truco_call: It looks through the chain of truco and returns "truco", "retruco or "vale cuatro". This will be then showed in truco description.

c) choose_envido: Only when envido is called, it sets the menu to let PC or user choose between "envido", "real envido" and "falta envido. 

d) envido: It uses phase and chain variables for readability purposes. First it updates the envido phase according to what call was made. Both PC and user can choose between answer, reject or reply. If "falta envido" was called, they cannnot reply any more. Options:
    * accept: Play_envido<sup>(i)</sup> is called to determine winner and loser. If "falta envido" was called, it updates the envido score according to the left_to_win points of the loser. Else, it sums the envido score of all envido calls and replies made. Lastly, it returns winner and loser.
    * reject: If the first call was rejected, it updates the envido score to 1. It returns px and py as the last is the one who lost.
    * reply: First it updates the envido score as replying is like accepting and calling again. Envido can be replied with a second envido, so in case the envido score is 2, the phase remains being 0. For any other case, the phase is updated. After this, a new menu is displayed, showing only the available options for the new phase. Lastly, PC or user choose what to call, and envido function is returned recursively. Recursion can continue up to "falta envido" reply.

e) truco: It follows a similar logic to the envido<sup>(d)</sup> function. The options menu can include "envido" if the first who plays in the first phase starts their turn calling "truco". After truco is accepted or replied, envido cannot be called anymore. If "vale 4" is called, players cannot reply anymore. Options:
    * envido: It follows the same logic of envido in turn<sup>(9)</sup> function, but it finish returning truco function (recursive), as truco call must continue after envido.
    * accept: If replier accepts truco, caller cannnot call again until replier decides to reply. However, if someone says "vale 4", truco cannot be called again for the rest of the row. Besides, after truco is accepted, envido cannot be called until the row finishes. Lastly, truco points are updated and it returs True to let the phase continue.
    * reject: It updates the truco score and calls score<sup>(g)</sup> function. In order to keep track of who is calling and who is answering, score function should be here. Finally, it returns False to finish the row. 
    * reply: It updates the truco phase and then return truco recursively. Recursion ends after "vale 4" was called.

f) play_card: Both PC and users choose a card from their hand. User will be reprompted if they do not write the right number and type. Then, the card will be removed from hand and a message will say which card was played. It returns de truco value of the card, with int format to allow comparison.

g) score: It pass envido score to player's game score if "envido" argument is passed. Otherwise, it will pass truco score at the end of the row or when it is rejected. After this, it will call show_score<sup>(h)</sup> to show new scores. If player's game score reach the goal score, a congratulations or sorry message will raise, depending on who won and it will call exit_game<sup>(5)</sup>. 

h) show_score: It prints the total score of each player, the current row score, and the goal score.

i) play_envido: It prints the points of the replier, as they should play first. Then it compares each player envido score. If the replier won or tied, it prints "Son buenas" from the caller, else it prints the caller points. In both cases, it returns a tuple of winner, loser.

***classes.py***
It uses the library random and termcolor. It contains 6 classes, that are separated from project.py for readability purposes.

*Menu*: It receives a list as argument and raises ValueError if it is empty. It has in_menu method that returns True if the value is in the list or False if it is not.

*Deck*: It receives a list of dictionaries as argument. It raise ValueError if deck size is not between 36 and 40. Methods:
    * shuffle: Using random library, it shuffles the deck.
    * cut: It uses random library to help simulating that the deck is being cut randomly.
    * deal: It returns and pop the first card of the deck. As 3 cards per player are given, lowest deck size will be 36.
    * __str__: Returns the number and type of each card. It was used for testing purposes.
    *__len__

*Points*: Parent of Player class. It contains all the points relevant to a player (game score, phase point, envido points). Variables can only be changed with methods:
    * add_phase_point: increase phase point by 1
    * restart_phase_point: set phase point to 0
    * update_game_score: increase game score by arg passed, arg can belong to envido score or truco score.
    * update_env_points: set envido points to arg passed. If arg is bigger than 33, it raises ValueError.
    * restart_env_points: set envido points to 0.

*Hand*: Parent of Player class. It contains 2 empty lists, hand and temp_hand. Methods:
    * add_card: It add cards (dictionary) to both hands. If player has 3 cards, it will raise ValueError.
    * pick_card: It takes and retunr a card from hand. If card does not exist, it will rise TypeError.
    * cards: It creates a string version of the current hand. Used for printing.
    * clean_hand: Empties both hands.
    * __len__

*Player*: It has some own attributes and it init Points and Hand classes. Methods:
    * change_dealer: It changes self.dealer from True to False and viceversa. 
    * plays_first: It sets self.first to True.
    * plays_last: It sets self.first to False.
    * lock_truco: It sets self.truco_call to False.
    * unlock_truco: It sets self.truco_call to True.
    * restart_values: It calls unlock_truco, plays_last, clean_hand, restart_env_points, restart_phase_point
    * __str__: It returns the name of the player, red for PC and green for user.

*Settings*: It contains all values related to game in general, such as row, phase, truco, envido. Methods:
    * new_row: Increase row by 1.
    * new_phase: Increase phase by 1.
    * new_truco_phase: Increase truco_phase by 1.
    * lock_envido: set self.envido to False.
    * set_falta_envido: It takes 2 args, score_game and player points. It updates envido_chain["falta envido"] value to left-to-win points.
    * update_row_points: It takes truco and envido points to update row pints. If sum is 0 it raises ValueError.
    * restart_values: It resets the following values: row_points, phase, phase winner, truco_phase, truco_score, envido, envido_score, envido_phase
    * __str__: It returns self.phase
    * __format__: Acording to the selected format it can return:
        - phasew: Winner of the last phase
        - trucos: Truco score
        - envidos: Envido score

***pc.py***
It contains the functions related to PC choise making. It only uses random and itertools libraries. Main function is empty as it is only used for making complex testing. 

*Primary functions*: They are called by project.py. 
*Secondary functions*: They are called by a primary or other secondary function.

*Primary functions*
1) call: It is called by turn function in project.py. It takes as an argument the size of the option menu, which uses to go through each possible decisition. That is to say, if size is 3, it will first check if it calls envido<sup>(b)</sup> (it returns "envido"), secondly it will check if it calls truco(it returns "truco") <sup>(a)</sup> and finally it will return "play". Other arguments are taken to determine odds of making a call.

2) select_envido: It is called by choose_envido function in project.py. It takes an options list and envido points as arguments. It calls assign_quartile<sup>(d)</sup> and assign_envido_reply_weight<sup>(g)</sup> to give a probability of choosing any of the available options ("envido", "real envido", "falta envido").

3) answer_envido: It is called by envido function in project.py. First it flats the list of lists. Secondly, it calls assign_quartile<sup>(d)</sup> and assign_envido_weight<sup>(f)</sup> to give a probability of choosing any of the available options ("accept", "reject", "reply"). Apart from the options list and envido points, it takes envido score and envido phase as arguments.

4) reply_envido: It is called by envido function in project.py after PC return "reply". 


5) answer_truco:
6) choose_card:

*Secondary functions*
a) call_truco:
b) call_envido:
c) assign_tertile:
d) assign_quartile:
e) assign_weight:
f) assign_envido_weight: 
g) assign_envido_reply_weight:
h) add_envido_weight:
i) add_weight:
j) hand_values:
k) compare_cards:
l) sort_hand:
m) pick_highest_card:
n) pick_lowest_card:
o) pick_random_card:
p) check_bool: