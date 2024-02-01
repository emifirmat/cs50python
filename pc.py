import random
from itertools import chain


# Main is only used for testing purposes
def main():
    ...


""" Primary functions"""


def call(opt_size, envido_points, game_phase, phase_winner, hand):
    # Make a call according to available options
    if opt_size == 3:
        if call_envido(envido_points):
            return "envido"
        if call_truco(game_phase, phase_winner, hand):
            return "truco"
        return "play"
    elif opt_size == 2:
        if call_truco(game_phase, phase_winner, hand):
            return "truco"
        else:
            return "play"
    else:
        return "play"


def select_envido(opt_list, envido_points):
    quartile = assign_quartile(envido_points)
    weight = assign_envido_reply_weight(opt_list, quartile, 0)
    answer = random.choices(
        opt_list, [weight[opt_list[0]], weight[opt_list[1]], weight[opt_list[2]]]
    )
    return answer[0]


def answer_envido(opt_list, envido_points, envido_score, envido_phase):
    opt_list = list(chain(*opt_list))
    quartile = assign_quartile(envido_points)
    weight = assign_envido_weight(opt_list, quartile, envido_score, envido_phase)

    # Choose according to available options
    if len(opt_list) == 3:
        answer = random.choices(
            opt_list, [weight[opt_list[0]], weight[opt_list[1]], weight[opt_list[2]]]
        )
    else:
        answer = random.choices(opt_list, [weight[opt_list[0]], weight[opt_list[1]]])
    return answer[0]


def reply_envido(opt_list, envido_points, envido_phase):
    if envido_phase == 2:
        return "falta envido"
    # Give reply options according to envido_phase
    quartile = assign_quartile(envido_points)
    weight = assign_envido_reply_weight(opt_list, quartile, envido_phase)
    if envido_phase == 1:
        answer = random.choices(opt_list, [weight[opt_list[0]], weight[opt_list[1]]])
        return answer[0]
    elif envido_phase == 0:
        answer = random.choices(
            opt_list, [weight[opt_list[0]], weight[opt_list[1]], weight[opt_list[2]]]
        )
        return answer[0]


def answer_truco(phase, phase_winner, opt_list, hand, envido_points=0):
    # Check number of cards in hand are correct
    if (4 - phase) != len(hand):
        raise IndexError("Wrong number of cars in hand")
    # Flatten list of lists
    opt_list = list(chain(*opt_list))

    # Case: Option to reply envido:
    if len(opt_list) == 4:
        if call_envido(envido_points):
            return opt_list[0]
        # If not called, eliminate option for weight purposes
        else:
            opt_list.pop(0)
    # Get tertiles ordered from lowest to highest
    hand = sort_hand(hand)
    cards = [card for card in assign_tertile(hand)]

    # Select proper weight according to cards in hand
    weight = assign_weight(phase, phase_winner, opt_list, cards)

    # Give an answer
    try:
        answer = random.choices(
            opt_list, [weight[opt_list[0]], weight[opt_list[1]], weight[opt_list[2]]]
        )
    except IndexError:
        answer = random.choices(opt_list, [weight[opt_list[0]], weight[opt_list[1]]])
    return answer[0]


def choose_card(row_phase, play_first, phase_winner, hand, table_value):
    """first phase"""
    if row_phase == 1:
        if play_first:
            # Check for a card between 2 and 7 coin
            card_values = hand_values(hand)
            cards_to_play = list(filter(lambda card: 8 < card < 12, card_values))
            if len(cards_to_play) >= 1:
                card_value = random.choice(cards_to_play)
                for card in hand:
                    if card_value == int(card["truco"]):
                        return card
            else:
                return pick_random_card(hand)
        # Plays second
        else:
            return compare_cards(hand, table_value)
    # Second
    elif row_phase == 2:
        # Pc won phase 1 (1st to play) --> play any card
        if play_first:
            if phase_winner[0] == "PC":
                return pick_random_card(hand)
            elif phase_winner[0] == "tie":
                return pick_highest_card(hand)
        # Plays second (PC lost or tied)
        else:
            return compare_cards(hand, table_value)
    # third phase
    else:
        return hand[0]


""" Secondary functions"""


def call_truco(game_phase, phase_winner, hand):
    answer = answer_truco(game_phase, phase_winner, [["True"], ["False"]], hand)
    return check_bool(answer)


def call_envido(envido_points):
    quartile = assign_quartile(envido_points)
    opt_list = ["True", "False"]
    # Envido phase and score are always 0
    weight = assign_envido_weight(opt_list, quartile, 0, 0)
    answer = random.choices(opt_list, [weight[opt_list[0]], weight[opt_list[1]]])
    return check_bool(answer[0])


def assign_tertile(hand):
    tertiles = []
    cards_values = hand_values(hand)
    for card in cards_values:
        if card < 5:
            card = "t1"
        elif card < 9:
            card = "t2"
        else:
            card = "t3"
        tertiles.append(card)
    return tertiles


def assign_quartile(envido_points):
    if envido_points < 21:
        return "q1"
    elif envido_points < 27:
        return "q2"
    elif envido_points < 31:
        return "q3"
    else:
        return "q4"


def assign_weight(phase, phase_winner, opt_list, cards):
    if len(phase_winner) > 0:
        phase_winner = phase_winner[0]
    if phase == 1:
        # First highest card
        if cards[-1] == "t1":
            weight = add_weight(opt_list, 0.03, 0.96, 0.01)
        elif cards[-1] == "t2":
            # Second highest card
            if cards[-2] == "t1":
                # Third highest card
                weight = add_weight(opt_list, 0.07, 0.90, 0.03)
            elif cards[-2] == "t2":
                if cards[-3] == "t1":
                    weight = add_weight(opt_list, 0.20, 0.75, 0.05)
                else:
                    weight = add_weight(opt_list, 0.30, 0.60, 0.10)
        elif cards[-1] == "t3":
            if cards[-2] == "t1":
                weight = add_weight(opt_list, 0.15, 0.75, 0.10)
            elif cards[-2] == "t2":
                if cards[-3] == "t1":
                    weight = add_weight(opt_list, 0.40, 0.45, 0.15)
                elif cards[-3] == "t2":
                    weight = add_weight(opt_list, 0.60, 0.20, 0.20)
            else:
                if cards[-3] == "t1":
                    weight = add_weight(opt_list, 0.65, 0.05, 0.30)
                elif cards[-3] == "t2":
                    weight = add_weight(opt_list, 0.54, 0.01, 0.45)
                else:
                    weight = add_weight(opt_list, 0.40, 0.00, 0.60)
    elif phase == 2:
        if phase_winner == "PC":
            if cards[-1] == "t1":
                weight = add_weight(opt_list, 0.30, 0.60, 0.10)
            elif cards[-1] == "t2":
                if cards[-2] == "t1":
                    weight = add_weight(opt_list, 0.40, 0.45, 0.15)
                else:
                    weight = add_weight(opt_list, 0.50, 0.35, 0.15)
            elif cards[-1] == "t3":
                if cards[-2] == "t1":
                    weight = add_weight(opt_list, 0.70, 0.15, 0.15)
                elif cards[-2] == "t2":
                    weight = add_weight(opt_list, 0.70, 0.10, 0.20)
                else:
                    weight = add_weight(opt_list, 0.50, 0.00, 0.50)
        elif phase_winner == "tie":
            if cards[-1] == "t1":
                weight = add_weight(opt_list, 0.10, 0.70, 0.20, "yes")
            elif cards[-1] == "t2":
                if cards[-2] == "t1":
                    weight = add_weight(opt_list, 0.15, 0.60, 0.25, "yes")
                else:
                    weight = add_weight(opt_list, 0.25, 0.50, 0.25)
            elif cards[-1] == "t3":
                if cards[-2] == "t1":
                    weight = add_weight(opt_list, 0.40, 0.30, 0.30)
                elif cards[-2] == "t2":
                    weight = add_weight(opt_list, 0.45, 0.20, 0.35)
                else:
                    weight = add_weight(opt_list, 0.20, 0.00, 0.80)
        # Player won phase 1
        else:
            if cards[-1] == "t1":
                weight = add_weight(opt_list, 0.05, 0.90, 0.05, "yes")
            elif cards[-1] == "t2":
                if cards[-2] == "t1":
                    weight = add_weight(opt_list, 0.10, 0.83, 0.07, "yes")
                else:
                    weight = add_weight(opt_list, 0.15, 0.75, 0.10)
            elif cards[-1] == "t3":
                if cards[-2] == "t1":
                    weight = add_weight(opt_list, 0.40, 0.40, 0.20)
                elif cards[-2] == "t2":
                    weight = add_weight(opt_list, 0.45, 0.20, 0.35)
                else:
                    weight = add_weight(opt_list, 0.60, 0.05, 0.35)
    elif phase == 3:
        if phase_winner == "PC":
            if cards[0] == "t1":
                weight = add_weight(opt_list, 0.05, 0.40, 0.55, "yes")
            elif cards[0] == "t2":
                weight = add_weight(opt_list, 0.20, 0.20, 0.60)
            else:
                weight = add_weight(opt_list, 0.09, 0.01, 0.90)
        elif phase_winner == "tie":
            if cards[0] == "t1":
                weight = add_weight(opt_list, 0.05, 0.50, 0.45, "yes")
            elif cards[0] == "t2":
                weight = add_weight(opt_list, 0.20, 0.20, 0.60)
            else:
                weight = add_weight(opt_list, 0.10, 0.05, 0.85)
        # Player won first row
        else:
            if cards[0] == "t1":
                weight = add_weight(opt_list, 0.05, 0.90, 0.05, "yes")
            elif cards[0] == "t2":
                weight = add_weight(opt_list, 0.20, 0.50, 0.30)
            else:
                weight = add_weight(opt_list, 0.45, 0.10, 0.45)
    return weight


def assign_envido_weight(opt_list, quartile, envido_score, envido_phase):
    "Percentages are determinated according to the points at risk"
    # Answer falta envido
    if envido_phase == 2:
        if quartile == "q1":
            return add_envido_weight(opt_list, 0.30, 0.70)
        elif quartile == "q2":
            return add_envido_weight(opt_list, 0.40, 0.60)
        elif quartile == "q3":
            return add_envido_weight(opt_list, 0.70, 0.30)
        else:
            return add_envido_weight(opt_list, 0.99, 0.01)
    # Answer envido or real envido (up to 3 points at risk)
    elif envido_score == 0:
        if quartile == "q1":
            return add_envido_weight(opt_list, 0.10, 0.85, 0.05)
        elif quartile == "q2":
            return add_envido_weight(opt_list, 0.25, 0.65, 0.10)
        elif quartile == "q3":
            return add_envido_weight(opt_list, 0.50, 0.25, 0.25)
        else:
            return add_envido_weight(opt_list, 0.60, 0.05, 0.35)
    # Answer double envido (4 point)
    elif envido_score == 2 and envido_phase == 0:
        if quartile == "q1":
            return add_envido_weight(opt_list, 0.05, 0.85, 0.10)
        elif quartile == "q2":
            return add_envido_weight(opt_list, 0.20, 0.60, 0.20)
        elif quartile == "q3":
            return add_envido_weight(opt_list, 0.60, 0.15, 0.25)
        else:
            return add_envido_weight(opt_list, 0.55, 0.05, 0.40)
    # Answer above 4 points at risk
    else:
        if quartile == "q1":
            return add_envido_weight(opt_list, 0.03, 0.85, 0.12)
        elif quartile == "q2":
            return add_envido_weight(opt_list, 0.15, 0.65, 0.20)
        elif quartile == "q3":
            return add_envido_weight(opt_list, 0.55, 0.10, 0.35)
        else:
            return add_envido_weight(opt_list, 0.45, 0.01, 0.54)


def assign_envido_reply_weight(opt_list, quartile, envido_phase):
    # Envido was called
    if envido_phase == 0:
        # First envido
        if quartile == "q1":
            return add_envido_weight(opt_list, 0.60, 0.30, 0.10)
        elif quartile == "q2":
            return add_envido_weight(opt_list, 0.45, 0.40, 0.15)
        elif quartile == "q3":
            return add_envido_weight(opt_list, 0.35, 0.35, 0.30)
        else:
            return add_envido_weight(opt_list, 0.15, 0.25, 0.60)
    # Seocond envido called
    elif envido_phase == 1:
        if quartile == "q1":
            return add_envido_weight(opt_list, 0.70, 0.30)
        elif quartile == "q2":
            return add_envido_weight(opt_list, 0.60, 0.40)
        elif quartile == "q3":
            return add_envido_weight(opt_list, 0.50, 0.50)
        else:
            return add_envido_weight(opt_list, 0.40, 0.60)


def add_envido_weight(opt_list, opt_1, opt_2, opt_3=0):
    sum = round(opt_1 + opt_2 + opt_3, 2)
    # Make function versatile for call_envido function
    if len(opt_list) == 2:
        opt_1 += opt_3
    if sum != 1:
        raise ValueError("Weight sum is not 1")
    weight = {}
    weight[opt_list[0]] = round(opt_1, 2)
    weight[opt_list[1]] = opt_2
    if len(opt_list) == 3:
        weight[opt_list[2]] = opt_3
    return weight


def add_weight(opt_list, accept, reject, reply, reverse=None):
    sum = round(accept + reject + reply, 2)
    size = len(opt_list)
    weight = {}
    if sum != 1:
        raise ValueError("Weight sum is not 1")
    if size == 3:
        weight[opt_list[0]] = accept
        weight[opt_list[1]] = reject
        weight[opt_list[2]] = reply
    elif size == 2 and reverse == "yes":
        weight[opt_list[0]] = accept
        weight[opt_list[1]] = round(reject + reply, 2)
    else:
        weight[opt_list[0]] = round(accept + reply, 2)
        weight[opt_list[1]] = reject
    return weight


def hand_values(hand):
    hand_values = [int(card["truco"]) for card in hand]
    return hand_values


def compare_cards(hand, table_value):
    # First, try to play higher card
    if cards_to_play := list(
        filter(lambda card: int(card["truco"]) > table_value, hand)
    ):
        return pick_lowest_card(cards_to_play)
    # Second, try to play same card
    elif cards_to_play := list(
        filter(lambda card: int(card["truco"]) == table_value, hand)
    ):
        return pick_random_card(cards_to_play)
    # Can't win, play lowest card
    else:
        return pick_lowest_card(hand)


def sort_hand(hand, order=None):
    if order == "reverse":
        return list(sorted(hand, key=lambda x: int(x["truco"]), reverse=True))
    else:
        return list(sorted(hand, key=lambda x: int(x["truco"])))


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


def check_bool(str):
    if str not in ["False", "True"]:
        raise ValueError("String should be False or True")
    if str == "False":
        return False
    else:
        return True


if __name__ == "__main__":
    main()
