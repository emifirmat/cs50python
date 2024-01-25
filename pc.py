import random


def main(): 
    ...

def pc_choose_card(row_phase, play_first, phase_winner, hand, table_value):
    """ first phase """
    if row_phase == 1:
        if play_first:
            # Check for a card between 2 and 7 coin
            card_values = hand_values(hand)
            cards_to_play = list(filter(lambda card: 8 < card < 12, card_values))

            if len(cards_to_play) >= 1:
                card_value = random.choice(cards_to_play)
                for card in hand:
                    if card_value == int(card['truco']):
                        return card
            else:
                card = pick_random_card(hand) 
        # Plays second
        else:
            card = compare_cards(hand, table_value)
        return card
    # Second or third phase
    elif row_phase == 2:
        # Pc won phase 1 (1st to play) --> play any card 
        if play_first and phase_winner[0] == "PC":
            card = pick_random_card(hand)
        else:
        # Pc lost or tied phase 1 (2nd to play)-- > 100 % try to win
            card = compare_cards(hand, table_value)
        return card
    else:
        return hand[0]

def hand_values(hand):
    hand_values = [int(card['truco']) for card in hand]
    return hand_values

def compare_cards(hand, table_value):
    # First, try to play higher card 
    if cards_to_play := list(filter(lambda card: int(card['truco']) > table_value, hand)):
        return pick_lowest_card(cards_to_play)
    # Second, try to play same card
    elif cards_to_play := list(filter(lambda card: int(card['truco']) == table_value, hand)):
        return pick_random_card(cards_to_play)
    # Can't win, play lowest card
    else: 
        return pick_lowest_card(hand)


def sort_hand(hand, order=None):
    if order == "reverse":
        hand = list(sorted(hand, key=lambda x: int(x['truco']), reverse=True))
        return hand
    else:
        return list(sorted(hand, key=lambda x: int(x['truco'])))


def pick_highest_card(hand):
    if len(hand) > 1:
        hand = sort_hand(hand, "reverse")
    return hand[0]


def pick_lowest_card(hand):
    if len(hand) > 1:
        hand = sort_hand(hand)
    return hand[0]


def pick_random_card(hand):
    return random.choice(hand)


if __name__ == "__main__":
    main()