# Truco Card Game
#### Video Demo: [Watch here](https://youtu.be/aWjiNQVxBqQ)
#### Description:
**The project**
The current project is a card game, very popular in Argentina, that is played with a 40-card Spanish deck. This version of the game only supports 1v1 and does not include "flor" rules. The **objective** of the game is to reach a total score of 15 or 30 points depending on the chosen settings. In order to achieve it, players can earn points from "envido" and "truco" every row. At the beginning of the row, 3 cards are given to each player, and they take turns playing one card each. Once both players end their turns, the phase concludes. There are 3 phases per row, but it can be ended before depending on how the game develops. The project itself contains a "rules" section to learn how to play, with more details and examples.

**Files**
There are 6 Python files.

***project.py***  
It contains the functions of the game that let its execution. Most of the libraries were seen through the course. Additionally, "time" and "termcolor" were incorporated to make the game more user-friendly, including colors and controlling the execution speed of the program. 

*Main function*: Has the main structure of the game. At the very beginning, it calls the introduction<sup>(1)</sup> function, and returns the name of the user, which will serve as the player's name. After that, it displays a menu with the following options: 
    * start: See "primary functions related to start game option in main".
    * rules: It calls rules<sup>(3)</sup> function.
    * settings: It calls set_gscore<sup>(4)</sup> to change the global variable goal_scre.
    * quit: It calls exit_game<sup>(5)</sup> function.

*Primary functions*: They are called by main. 
*Secondary functions*: They are called by a primary function.

*Primary functions*
1) Function introduction: Shows the name of the game in ASCII art and prompts the user to tell their name to welcome them. The name should at least have a printable character, and it will be truncated to 20 characters.
2) Function set_menu: It is called every time there is a menu of options. It needs a list as an argument, and it will display it formatted by the tabulate library. In case of envido, it will display options horizontally. Besides, it uses a Menu class to make sure the user is typing the option correctly.
3) Function rules: It displays a menu with different parts of the game, to let the user choose in detail what they want to know. The chosen option is passed to a CSV reader to open the right file and print the rules of that section. The files were written manually and are located in the "rules" folder. If the file doesn't exist, an error will raise. The user can then continue reading or go back to the main menu.
4) Function set_gscore: It is called by the settings option in the main function, to change the global variable goal_scre, and only the values 15 or 30 are allowed. After picking a number it prints a confirmation message.
5) Function exit_game: It is called when the player wants to quit the game. It prints a confirmation message that supports multiple common answers such as, "y" and "yEs", thanks to the "re" library. In case the player chooses "yes" or someone won the game, it will finish the program with a goodbye message. If players choose "no", it goes back to the previous menu.

*Primary functions related to start game option*
When start game option is chosen, first, the Players and Settings classes are created. After that, a deck is created using the function set_deck<sup>(6)</sup>. Then, some messages are displayed explaining the goal score to win. The row starts, and some class values are restarted if it is not the first one. A message is printed indicating the beginning of a new row, and then the deck is shuffled and cut. It continues choosing a dealer through the function choose_dealer<sup>(7)</sup> to determine who plays first. The first to play will be called "p1". Both p1 and p2 receive their 3 cards in the same order of the real game and update their envido points<sup>(8)</sup> that will be necessary for the PC to make choices. The cards are dictionaries with the keys "number", "type", "truco_value" and "envido_value".
Next, the phase starts, and a message is printed. It can loop 3 times. Temp_hand is copied as sometimes the PC needs to make decisions after playing a card, and it needs to include that played card for it. In phase 2 and 3, envido cannot be called anymore, and p1 must be the player who plays first. The player's hand is showed and then each player plays their turn<sup>(9)</sup>. If truco was called and rejected, the loop breaks and start a new row. If not, it returns the truco value of the played card, that will be compared when the end_phase<sup>(10)</sup> function is called to determine the winner of the phase. Finally, if at least 2 phases were played, <sup>end_row(11)</sup> will be called to determine if someone won the row and print a message.

6) Function set_deck: It takes the location of a file that contains the cards with their truco and envido values. The function only checks if the file exists, although the Deck class will control that the size of the deck is between 36 and 40.

7) Function choose_dealer: If it is the first row, it picks a random player to be the dealer. Otherwise, the dealer is changed from one player to another. As in every phase p1 and p2 can change, the function always designates p1 as the first to play after choosing the dealer.

8) Function get_envido_points: First, it sorts the hand from higher to lower envido points. Then, it calls the function search_type<sup>(a)</sup> to check if the player has at least 2 cards of the same type. If it returns a type, the function filters those type cards. If all cards are of the same type, it pops the one with the lowest value. Finally, it adds 20 envido points. If no type is returned, it only leaves the card of the highest envido points. Lastly, it sums each card envido points.  

9) Function turn: At the beginning, it sets the menu according to the available options. E.g.: Envido cannot be called if truco was accepted, and the same player cannot call truco twice. If it is PC's turn, it will play by itself (see pc.py). If it is the user's turn, the menu will also show hand, score, and quit options, and the player will be prompted to choose along the menu. Full menu options are: 
    * envido: It calls "choose_envido"<sup>(c)</sup> for prompting the user to call envido, real envido or falta envido. Then it calls "envido"<sup>(d)</sup> function to return who wins and loses, and finally calls score<sup>(g)</sup> to update de game score. 
    * truco: It calls "truco"<sup>(e)</sup> function. If it was accepted, then it calls and return "play_card"<sup>(f)</sup> function. If not, it returns False to end the row.
    * play: It returns play_card<sup>(f)</sup> function. 
    * hand: It prints the current player's hand.
    * score: Calls show_score<sup>(f)</sup> function.
    * quit: Calls exit_game function<sup>(5)</sup>.

10) Function end_phase: It compares the values returned by turn<sup>(9)</sup> function. If one of the players won, it adds them to a winners list and gives them a phase point. If p2 won, it will also make it play first in the next phase. Finally, it prints a message saying who won the current phase and how many in total. In case of tie, it will add "tie" to the winners list, and no one will receive a phase point.

11) Function end_row: First, if truco was not called in the whole row, it updates the score points it gives to 1. Then it contemplates all different situations and updates the score of the winner. If there is no winner, it returns False, and the row continues to the next phase. If someone won, it returns a tuple: the winner object and True. Note: True is added because at phase 3 hand list is empty, and the function returns the winner but also False.

*Secondary functions*
a) Function search_type: Using a nested loop, it goes through all the cards of the hand looking for a coincidence in the "type" key. If there is a coincidence, it returns the string representation of the type of the card (club, coin, sword, cup), else None.

b) Function set_truco_call: It looks through the chain of truco and returns "truco", "retruco or "vale cuatro". This will be then shown in the truco description.

c) Function choose_envido: Only when envido is called by PC or the user, it sets the menu to let them choose between "envido", "real envido" and "falta envido". 

d) Function envido: It uses phase and chain variables for readability purposes. First, it updates the envido phase according to what call was made. Both PC and the user can choose between answer, reject or reply. If "falta envido" was called, they cannnot reply anymore. Options:
    * accept: Play_envido<sup>(i)</sup> is called to determine winner and loser. If "falta envido" was called, it updates the envido score according to the left_to_win points of the loser. Else, it sums the envido score of all envido calls and replies made. Lastly, it returns the winner and loser tuple.
    * reject: If the first call was rejected, it updates the envido score to 1. It returns px and py as the last is the one who lost.
    * reply: First it updates the envido score as replying is like accepting and calling again. Envido can be replied with a second envido, so in case the envido score is 2, the phase remains being 0. For any other case, the phase is updated. After this, a new menu is displayed, showing only the available options for the new phase. Lastly, PC or user choose what to call, and envido function is returned recursively. Recursion can continue up to the "falta envido" reply.

e) Function truco: It follows a similar logic to the envido<sup>(d)</sup> function. The options menu can include "envido" if the first who plays in the first phase starts their turn calling "truco". After truco is accepted or replied, envido cannot be called anymore. If "vale 4" is called, players cannot reply anymore. Options:
    * envido: It follows the same logic of envido in turn<sup>(9)</sup> function, but it finishes returning the truco function recursively, as truco call must continue after envido.
    * accept: If replier accepts truco, the caller cannnot call again until the replier decides to reply. However, if someone says "vale 4", truco cannot be called again for the rest of the row. Besides, after truco is accepted, envido cannot be called until the row finishes. Lastly, truco points are updated, and it returs True to let the phase continue.
    * reject: It updates the truco score and calls score<sup>(g)</sup> function. To keep track of who is calling and who is answering, the score function should be here. Finally, it returns False to finish the row. 
    * reply: It updates the truco phase and then returns truco recursively. Recursion ends after "vale 4" was called.

f) Function play_card: Both PC and the user choose a card from their hand. The user will be reprompted if they do not write the right number and type. Then, the card will be removed from hand, and a message will say which card was played. It returns the truco value of the card, with int format to allow comparison.

g) Function score: It passes envido score to player's game score if the "envido" argument is passed. Otherwise, it will pass the truco score at the end of the row or when it is rejected. After this, it will call show_score<sup>(h)</sup> to show new scores. If the player's game score reaches the goal score, a congratulations or sorry message will raise, depending on who won, and it will call exit_game<sup>(5)</sup>. 

h) Function show_score: It prints the total score of each player, the current row score, and the goal score.

i) Function play_envido: It is called by the envido<sup>(d)</sup> function. It prints the points of the replier, as they should play first. Then it compares each player's envido score. If the replier won or tied, it prints "Son buenas" from the caller; else it prints the caller's points. In both cases, it returns a tuple of the winner and loser.

***classes.py***
It uses the libraries random and termcolor. It contains 6 classes, which are separated from project.py for readability purposes.

*Menu class*: It receives a list as an argument and raises a ValueError if it is empty.
    * Method in_menu:  It receives a string value as an argument and returns True if it is in the list or False if it is not.

*Deck class*: It receives a list of dictionaries as an argument. It raise a ValueError if deck size is not between 36 and 40.
    * Method shuffle: It shuffles the deck in-place randomly.
    * Method cut: It cuts the deck in-place by a random size, simulating a real-world cut.
    * Method deal: It returns and pops the first card from the deck. As 3 cards per player are given, the lowest deck size will be 36.
    * Method __str__: Returns the number and type of each card. It is used for testing purposes.
    * Method __len__: It return the number of cards left in the deck.

*Points class*: Parent of the Player class. It contains all the points relevant to a player (game score, phase point, envido points) initialized with a value of 0. Variables can only be changed with methods.
    * Method add_phase_point: Increases phase point by 1.
    * Method restart_phase_point: sets the phase point to 0.
    * Method update_game_score: Increases the game score by the argument passed. The argument can belong to envido score or truco score.
    * Method update_env_points: Sets envido points according to the int argument passed. If the argument is bigger than 33, it raises ValueError.
    * Method restart_env_points: Sets envido points to 0.

*Hand class*: Parent of the Player class. It contains 2 empty lists: hand and temp_hand.
    * Method add_card: Adds cards (dictionary) to both hands. If the player has 3 cards, it will raise ValueError.
    * Method pick_card: Takes and returns a card from hand. If the card does not exist, it will rise a TypeError.
    * Method cards: Creates a string representation of the current hand for printing. It only shows the number and type of each card.
    * Method clean_hand: Empties both hands.
    * Method __len__: It returns the number of cards in the hand.

*Player class*: It has some own attributes and initializes Points and Hand classes.
    * Method change_dealer: Changes self.dealer from True to False and vice versa. When it is True, the player is the dealer.
    * Method plays_first: Sets self.first to True, indicating that the player plays first in the phase.
    * Method plays_last: Sets self.first to False, indicating that the player plays second.
    * Method lock_truco: Sets self.truco_call to False, indicating that the player cannot call truco.
    * Method unlock_truco: Sets self.truco_call to True, indicating that the player can call truco.
    * Method restart_values: Calls unlock_truco, plays_last, clean_hand, restart_env_points, restart_phase_point.
    * Method __str__: It returns the colored name of the player, distinguishing the PC from the user.

*Settings class*: It contains all values related to the game in general, such as row, phase, truco, envido.
    * Method new_row: Increases the row by 1.
    * Method new_phase: Increases the phase by 1.
    * Method new_truco_phase: Increases the truco_phase by 1.
    * Method lock_envido: Sets self.envido to False.
    * Method set_falta_envido: Takes 2 arguments, score_game and player points. It updates envido_chain["falta envido"] value to left-to-win points (score_game - player points).
    * Method update_row_points: Takes truco and envido points to update row pints. If the sum is 0 it raises ValueError.
    * Method restart_values: Resets the following values: row_points, phase, phase winner, truco_phase, truco_score, envido, envido_score, envido_phase.
    * Method __str__: It returns self.phase.
    * Method __format__: Acording to the selected format it can return:
        - phasew: It returns a string representation of the winner of the last phase.
        - trucos: It returns a string representation of truco score.
        - envidos: It returns a string representation of envido score.
        - __str__. See the method __str__.

***pc.py***
It contains functions related to PC decision-making. It only uses random and itertools libraries. Main function is empty as it is only used for complex testing. Sometimes, random or negative choices are given to the PC to make it unpredictable to the user and give it the sense of lying.

*Primary functions*: These are called by project.py. 
*Secondary functions*: These are called by a primary or other secondary function.

*Primary functions*
1) Function call: It is called by the turn function in project.py. It takes the size of the option menu as an argument, which is used to go through each possible decision. For instance, if the size is 3, it will first check if it calls envido<sup>(b)</sup> (it returns "envido"). Secondly it will check if it calls truco (it returns "truco") <sup>(a)</sup> and finally, it will return "play". If the size is 2, it will check truco<sup>(a)</sup> and then return "play", and if the size is 1 it will return "play". Other arguments are taken to determine the odds of making a call.

2) Function select_envido: It is called by choose_envido and envido function in project.py. It takes an options list and envido points as arguments. It calls assign_quartile<sup>(d)</sup> to convert envido points into a quartile and assign_envido_reply_weight<sup>(g)</sup> to give a probability of choosing any of the available options ("envido", "real envido", "falta envido"). The envido phase argument is only taken after the PC returs "reply" in the envido function from project.py. In this case, the option list can vary by popping the first option and changing the weight of each choice. 

3) Function answer_envido: It is called by the envido function in project.py to return an option from the given list ("accept", "reject", "reply"). First, it flattens the list of lists. Secondly, it calls assign_quartile<sup>(d)</sup> and assign_envido_weight<sup>(f)</sup> to give a probability of choosing any of the available options. Apart from the options list and envido points, it takes envido score and envido phase as arguments.

4) Function answer_truco: It is called by the truco function in project.py to return an option from the given list ("accept", "reject", "reply"). If the number of cards in hand is not correct for the current phase, it raises an IndexError. Then it checks if it can call envido<sup>(b)</sup> as an answer. If it does not call it, the option is popped. Next, it sorts the hand<sup>(l)</sup> from the lowest to highest truco value and proceeds to return a list of tertiles, calling assing_tertile<sup>(c)</sup> for each card. After that, it calls assign_weight<sup>(e)</sup> and makes a choice of the available options according to the weight given to each one. The weight of each option will vary according to the size of the options (it can include or not "reply"), the truco phase and the winner of the first phase if it was played.

5) Function choose_card: It is called by the play_card function in project.py. Decisions are made according to the current game phase. In the first phase, if it is the first to play, it will create a list of truco values from the cards in hand, calling the function hand_values<sup>(j)</sup>. With this list, it will pick a card between the truco values 8 and 12. If it does not have a card between those values, it will play a random card. If it plays second, it will call the function compare_cards<sup>(k)</sup>.
In the second phase, if PC won the first phase, it will play a random card<sup>(o)</sup>. If it tied, it will play the highest card<sup>(m)</sup> and if it lost, it will call the compare_cards<sup>(k)</sup> function. 
In the third phase, it will play the only card that remains in hand.

*Secondary functions*
a) Function call_truco: It calls answer_truco<sup>(4)</sup> to decide whether to return a True or False boolean<sup>(p)</sup>, representing the decision of calling or not calling truco.

b) Function call_envido: It calls assign quartile<sup>(d)</sup>, which will be used to assign weight<sup>(f)</sup> and choose between True or False booleans<sup>(p)</sup>, representing the decision of calling or not calling envido.

c) Function assign_tertile: It assigns each card of the hand to a tertile depending on its truco value. t1<5, t2<9, t3 9+.  

d) Function assign_quartile: It checks the envido points of the player and puts it in a quartile. The limit value for each quartile was designated by experience in the game.

e) Function assign_weight: With the help of the function add_weight<sup>(i)</sup>, it assigns a probability to each option. Values are based on my experience in the game, and they change according to the cards, which now have tertiles as values. The higher the tertile, the higher the odds of accepting or replying "truco". Also, who won the first phase affects these values. To let the function work, phase_winner is only used when it has at least one value.

f) Function assign_envido_weight: With the help of the function add_envido_weight<sup>(h)</sup>, it assigns a probability to each option. Values are based on my experience in the game, and they change according to the score points at risk and the quartile. The higher the quartile, the higher the odds of accepting or replying "envido".

g) Function assign_envido_reply_weight: With the help of the function add_envido_weight<sup>(h)</sup>,  it assigns a probability to each option (envido, real envido, falta envido). The higher the quartile, the higher the chance to reply with a higher value envido. It does not include envido phase 2, as in this case the only available option is falta envido.

h) Function add_envido_weight: It sets each option in a dictionary as a key, and each probability as the value. The function is flexible, as two or three options can be given. In case the values given do not sum to 1, a ValueError will be raised.

i) Function add_weight: Similar spirit to h), it creates a dictionary with the options as keys and probabilities as values. It is flexible for 2 or 3 options. It has an extra argument for doble option situations; when it is "yes", the probability for option 3 will sum to option 2 instead of 1.

j) Function hand_values: It takes the cards of the hand as argument and returns a list of truco values.

k) Function compare_cards: When it is called, it takes the card played by the opponent as a reference and creates a list of all the cards in hand higher than that one. If the list is empty, it then tries to play a card of the same value. If it is also empty, it plays the lowest card in hand. 

l) Function sort_hand: It sorts the hand by truco value. The default is lower to higher, "reverse" is higher to lower.

m) Function pick_highest_card: It sorts the hand by truco value and takes the highest card.

n) Function pick_lowest_card: It sorts the hand by truco value and takes the lowest card.

o) Function pick_random_card: it returns a random card in hand.

p) Functino check_bool: It converts string representations of booleans into actual booleans and returns them. Input is case sensitive.

***TESTERS***
They are implemented using pytest and unittest.mock

***test_project.py***
It utilizes pytest fixtures to prevent repetition while creating the tests. Additionally, the non_sleep fixture has the attribute 'autouse' to disable 'time.sleep' during the test.

Functions tested:
* set_gscore: It employs an input mock and raises a StopIteration when wrong inputs are given. It checks that both 15 and 30 work despite having whitespaces.
* set_menu: It uses an input mock to check the validity of inputs that coincide with the options. The test is case insensitive and ignores whitespaces.
* set_deck: Tests that if the file is not found it raises a SystemExit. It also verifies that the imported dictionary has a size of 40, 4 keys, and uses one card as an example to check that the values exist.
* choose_dealer: Tests the first row (random mock) and the second row separately. It checks the player atributed and ensures that the function returns players in the correct order.  
* play_card: Uses an input mock to test that only cards in hand are accepted as inputs.
* truco: Divided into 5 functions, it mocks PC and user answers. It ensures that each answer (accept, reject, reply, envido) returns the correct boolean and that the players and settings attributes are correctly updated.
* search_type: Tests that a card type is found when two cards have the same type, and no type is found otherwise.
* get_envido_points: Tests that the function returns the envido points correctly, Whether or not the first card is played.
* play_envido: Ensures that the function returns the tuple correctly when the caller wins, loses or ties.
* envido: Tests each answer situation in 3 different functions. It mocks PC and user answers, and envido winner when accepted. It checks that returned tuples and settings attributes are correct.
* end_phase: Ensures that players and settings are correct in each phase situation.
* end_row: Divided into 2 functions, it checks that the function returns the right tuple and updates players and settings correctly. While not covering all cases, it addresses most important scenarios.
* score: Divided into 2 functions, the first test checks that the function calls SystemExit when there is a winner. The second test verifies that the player's score is updated correctly after winning envido or truco
* exit_game: Divided into 2 functions, the first one uses an input mock to test that different "yes" or "no" inputs work properly. The second test examines the functionality of the "winner" argument.

***test_classes.py***
It utilizes python fixtures to initialize classes that will be tested more than once. Cards and fullhand functions are created to facilitate testing of hands.

Classes tested:
* Menu: Divided into 2 functions. Firstly, it tests that intializing empty lists or appending a value raise an error. Secondly, it ensures that the in_menu method returns True when the input matches the options list and False when it does not. 
* Deck: Divided into 2 functions. Firstly, it tests that the class raises a ValueError when it has fewer than 36 or more than 40 card, but not if it is within those values. Secondly, it tests that the deal method returns the correct card and removes it from deck.
* Hand: Divided into 2 functions. Firstly, it tests that the add_card method appends a card to both hand and temp_hand lists until reaching a size of 3. Then, it raises a ValueError. Secondly, it tests that the pick_card method raises a TypeError if the card does not exit and returns the correct card if exists.
* Player: Divided into 2 functions. Firstly, it tests that modifying attributes directly raises an AttributeError, and it does not raise an error when they are changed by a method. Secondly, it tests that the format method returns strings as expected.
* Points: It tests that update_env_points raises a ValueError if the argument is over 33, but does not if it is 33.
* Settings: Divided into 3 functions. Firstly, it tests that attributes raises an AttributeError if they are not modified by methods. Secondly, it tests that set_falta_envido method updates the envido_chain["falta envido"] value correctly. Lastly, it tests that update_row_points method works properly, but raises ValueError if it does not receive a point when called.  

***test_pc.py***
In pytest.fixture there are a few hands and options lists used to simplify testing. The functions tested are:
* sort_hands: It tests that cards in hand get sorted by truco value. 
* pick_cards: It tests that pick_lowest_card returns the lowest card in hand, and pick_highest_card returns the highest card in hand.
* compare cards: It is divided into 3 functions. Firstly, it tests that the function returns a higher card, and if there are 2 higher cards, it returns the lowest of those 2. Secondly, it tests that the function returns a card of the same value. Lastly, it tests that it returns the lowest card in hand.
* hand_values: It tests that it returns a list with only the truco values of the cards. 
* choose_card: Divided into 2 functions. Firstly, it is related to phase 1 and tests that if it is the first to play and has a card between a 2 or 7 gold, it will return a card between those values.  If it is second to play, it tests that the card played follows the "compare_cards" function rules. Secondly, it tests the phase 2 scenario. If there was a tie and it is the first to play, it tests that the highest card is played. If it is second to play, that it will try to win or tie the opponent's card. 
* add_weight: It tests that if the values do not sum to 1, it raises a ValueError. Then, it checks that keys and values are passed correctly when there are both 3 options or 2 options.
* assign_weight: It is divide into 3 functions, representing each phase. It tests that some groups of tertiles return a dictionary with the right values in both reply and call situations. 
* answer_truco: It tests that the function raises an IndexError when the player does not have the right amount of cards in every phase.
* add_envido_weight: It tests that if the values do not sum to 1, it raises a ValueError. Then, it checks that keys and values are passed correctly when there are both 3 or 2 options.
* assign_envido_weight: It tests that some quartiles return a dictionary with the right values in both reply and call situations.
* assign_envido_reply_weight: It tests that some quartiles return a dictionary with the right values when there are 3 or 2 options available.
* select_envido: It tests that the function returns "falta envido".

**Final comments**
This is my first significant project, and I learned a lot through it, such as the use of mocks for testing and gaining a better comprehension of the use of classes and properties. I discovered many bugs through this way, but I could find and fix them without any complications. I am sure that the design of code can be improved, but I set a deadline of one month for the project, and I think I should finish it now. Thank you very much for reading the document.  