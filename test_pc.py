from pc import *
from unittest.mock import patch
import pytest


# 4 club, 4 sword, 5 sword
@pytest.fixture
def low():
    hand = [
        {"number": "4", "type":"club", "truco": "1", "envido": "4"},
        {"number": "4", "type":"sword", "truco": "1", "envido": "4"},
        {"number": "5", "type":"sword", "truco": "2", "envido": "5"},
    ]
    return hand

# 7 club, 2 cup, 12 sword
@pytest.fixture
def medium():
    hand = [
        {"number": "7", "type":"club", "truco": "4", "envido": "7"},
        {"number": "2", "type":"cup", "truco": "9", "envido": "2"},
        {"number": "12", "type":"sword", "truco": "7", "envido": "0"},   
    ]
    return hand

# 7 coin, 2 coin, 1 club
@pytest.fixture
def high():
    hand = [
        {"number": "7", "type":"coin", "truco": "11", "envido": "7"},
        {"number": "2", "type":"coin", "truco": "9", "envido": "2"},
        {"number": "1", "type":"club", "truco": "13", "envido": "1"},   
    ]
    return hand

@pytest.fixture
def list():
    return ["accept", "reject", "reply"]



def test_sort_hand(high):
    assert sort_hand(high, "reverse") == [
        {"number": "1", "type":"club", "truco": "13", "envido": "1"},
        {"number": "7", "type":"coin", "truco": "11", "envido": "7"},
        {"number": "2", "type":"coin", "truco": "9", "envido": "2"},    
    ]
    assert sort_hand(high) == [
        {"number": "2", "type":"coin", "truco": "9", "envido": "2"}, 
        {"number": "7", "type":"coin", "truco": "11", "envido": "7"},
        {"number": "1", "type":"club", "truco": "13", "envido": "1"},   
    ]


def test_pick_cards(low, medium, high):
    hand = low[:]
    assert pick_highest_card(hand) == low[2]
    assert pick_lowest_card(hand) == low[0]
    hand = medium[:]
    assert pick_highest_card(hand) == medium[1]
    assert pick_lowest_card(hand) == medium[0]
    hand = high[:]
    assert pick_highest_card(hand) == high[2]
    assert pick_lowest_card(hand) == high[1]


def test_compare_cards_higher(medium):
    hand = medium[:]
    # 1 card higher / 2 cards higher
    assert compare_cards(hand, 8) == medium[1]
    assert compare_cards(hand, 5) == medium[2]

def test_compare_cards_equal(low):
    hand1 = low[:]
    hand2 = [
        {"number": "5", "type":"coin", "truco": "2", "envido": "5"},
        {"number": "5", "type":"sword", "truco": "2", "envido": "5"},
        {"number": "4", "type":"sword", "truco": "1", "envido": "5"},
    ]
    # 1 card equal and 2 lower / # 2 cards equal and one lower
    assert compare_cards(hand1, 2) == low[2]
    assert compare_cards(hand2, 2) == {"number": "5", "type":"coin", "truco": "2", "envido": "5"} or {"number": "5", "type":"sword", "truco": "2", "envido": "5"}

def test_compare_cards_lower(medium, high):
    # 3 cards lower
    hand1, hand2 = medium[:], high[:]
    assert compare_cards(hand1, 14) == medium[0]
    assert compare_cards(hand2, 14) == high[1]


def test_hand_values(medium):
    assert hand_values(medium) == [4, 9, 7]


def test_choose_card_firstPhase(medium, high):
    # First to play: choose a card between 2 and 7 coin 
    hand1, hand2 = medium[:], high[:]
    # Hand1 = [4, 9, 7] / Hand2= [11, 9, 13]
    assert choose_card(1, True, None, hand1, None) == medium[1]
    assert choose_card(1, True, None, hand2, None) == high[0] or high[1]
    # Plays second
    assert choose_card(1, False, None, hand1, 6) == medium[2]
    assert choose_card(1, False, None, hand1, 10) == medium[0]
    assert choose_card(1, False, None, hand1, 9) == medium[1]
    assert choose_card(1, False, None, hand2, 6) == high[1]
    assert choose_card(1, False, None, hand2, 10) == high[0]
    assert choose_card(1, False, None, hand2, 9) == high[0]


def test_choose_card_secondPhase(low, medium, high):
    # hand1 = [4, 9, 7] / hand2= [11, 9, 13] / hand3 = [1, 1, 2]
    hand1, hand2, hand3 = medium[:], high[:], low[:]
    for hand in [hand1, hand2, hand3]:
        hand.pop()
    # First to play
    assert choose_card(2, True, ["tie"], hand1, None) == medium[1]
    assert choose_card(2, True, ["tie"], hand2, None) == high[0]
    assert choose_card(2, True, ["tie"], hand3, None) == low[0]
    # Second to play
    assert choose_card(2, False, ["tie"], hand1, 9) == medium[1]
    assert choose_card(2, False, ["emi"], hand2, 10) == high[0]
    assert choose_card(2, False, ["tie"], hand3, 2) == low[0]

def test_add_weight(list):
    with pytest.raises(ValueError, match="Weight sum is not 1"):
        add_weight({}, list, 0.35, 0.30, 0.25)
    with pytest.raises(ValueError, match="Weight sum is not 1"):
        add_weight({}, list, 0.45, 0.30, 0.26)
    assert add_weight({}, list, 0.35, 0.40, 0.25) == {"accept": 0.35, "reject": 0.40, "reply": 0.25}
    assert add_weight({}, list, 0.35, 0.40, 0.25, "yes") == {"accept": 0.35, "reject": 0.40, "reply": 0.25}
    list = ["accept", "reject"]
    assert add_weight({}, list, 0.35, 0.40, 0.25) == {"accept": 0.60, "reject": 0.40}
    assert add_weight({}, list, 0.35, 0.40, 0.25, "yes") == {"accept": 0.35, "reject": 0.65}

def test_assign_weight_firstRow(list): 
    assert assign_weight({}, 1, ["PC"], list, ["t1", "t1", "t1"]) == {"accept": 0.03, "reject": 0.96, "reply": 0.01}
    assert assign_weight({}, 1, ["PC"], list, ["t1", "t1", "t2"]) == {"accept": 0.07, "reject": 0.90, "reply": 0.03}
    assert assign_weight({}, 1, ["PC"], list, ["t2", "t2", "t2"]) == {"accept": 0.30, "reject": 0.60, "reply": 0.10}
    assert assign_weight({}, 1, ["PC"], list, ["t1", "t1", "t3"]) == {"accept": 0.15, "reject": 0.75, "reply": 0.10}
    assert assign_weight({}, 1, ["PC"], list, ["t2", "t2", "t3"]) == {"accept": 0.60, "reject": 0.20, "reply": 0.20}
    assert assign_weight({}, 1, ["PC"], list, ["t3", "t3", "t3"]) == {"accept": 0.40, "reject": 0.00, "reply": 0.60}
    
    # Test calls
    list = ["True", "False"]
    assert assign_weight({}, 1, [""], list, ["t1", "t2", "t3"]) == {"True": 0.55, "False": 0.45}
    assert assign_weight({}, 1, [""], list, ["t3", "t3", "t3"]) == {"True": 1.00, "False": 0.00}


def test_assign_weight_secondRow(list):
    assert assign_weight({}, 2, ["PC"], list, ["t1", "t1"]) == {"accept": 0.30, "reject": 0.60, "reply": 0.10}
    assert assign_weight({}, 2, ["PC"], list, ["t2", "t2"]) == {"accept": 0.50, "reject": 0.35, "reply": 0.15}
    assert assign_weight({}, 2, ["PC"], list, ["t1", "t3"]) == {"accept": 0.70, "reject": 0.15, "reply": 0.15}
    assert assign_weight({}, 2, ["tie"], list, ["t1", "t1"]) == {"accept": 0.10, "reject": 0.70, "reply": 0.20}
    assert assign_weight({}, 2, ["tie"], list, ["t2", "t2"]) == {"accept": 0.25, "reject": 0.50, "reply": 0.25}
    assert assign_weight({}, 2, ["tie"], list, ["t1", "t3"]) == {"accept": 0.40, "reject": 0.30, "reply": 0.30} 
    assert assign_weight({}, 2, ["emi"], list, ["t1", "t1"]) == {"accept": 0.05, "reject": 0.90, "reply": 0.05}
    assert assign_weight({}, 2, ["emi"], list, ["t1", "t2"]) == {"accept": 0.10, "reject": 0.83, "reply": 0.07}
    assert assign_weight({}, 2, ["emi"], list, ["t2", "t3"]) == {"accept": 0.45, "reject": 0.20, "reply": 0.35} 

    # Test calls
    list = ["True", "False"]
    assert assign_weight({}, 2, ["PC"], list, ["t1", "t1"]) == {"True": 0.40, "False": 0.60}
    assert assign_weight({}, 2, ["tie"], list, ["t1", "t2"]) == {"True": 0.15, "False": 0.85}
    assert assign_weight({}, 2, ["emi"], list, ["t3", "t3"]) == {"True": 0.95, "False": 0.05}


def test_assign_weight_thirdRow(list):
    assert assign_weight({}, 3, ["PC"], list, ["t1"]) == {"accept": 0.05, "reject": 0.40, "reply": 0.55}
    assert assign_weight({}, 3, ["PC"], list, ["t2"]) == {"accept": 0.20, "reject": 0.20, "reply": 0.60}
    assert assign_weight({}, 3, ["PC"], list, ["t3"]) == {"accept": 0.09, "reject": 0.01, "reply": 0.90}
    assert assign_weight({}, 3, ["tie"], list, ["t1"]) == {"accept": 0.05, "reject": 0.50, "reply": 0.45}
    assert assign_weight({}, 3, ["tie"], list, ["t2"]) == {"accept": 0.20, "reject": 0.20, "reply": 0.60}
    assert assign_weight({}, 3, ["tie"], list, ["t3"]) == {"accept": 0.10, "reject": 0.05, "reply": 0.85} 
    assert assign_weight({}, 3, ["emi"], list, ["t1"]) == {"accept": 0.05, "reject": 0.90, "reply": 0.05}
    assert assign_weight({}, 3, ["emi"], list, ["t2"]) == {"accept": 0.20, "reject": 0.50, "reply": 0.30}
    assert assign_weight({}, 3, ["emi"], list, ["t3"]) == {"accept": 0.45, "reject": 0.10, "reply": 0.45} 

    # Test calls
    list = ["True", "False"]
    assert assign_weight({}, 3, ["PC"], list, ["t2"]) == {"True": 0.80, "False": 0.20}
    assert assign_weight({}, 3, ["tie"], list, ["t3"]) == {"True": 0.95, "False": 0.05}
    assert assign_weight({}, 3, ["emi"], list, ["t1"]) == {"True": 0.05, "False": 0.95}  

def test_answer_truco_IndexError(low):
    low.pop()
    assert len(low) == 2
    with pytest.raises(IndexError, match="Wrong number of cars in hand"):
        answer_truco(1, "PC", [["accept"], ["reject"], ["reply"]], low)   
    low.pop()  
    assert len(low) == 1     
    with pytest.raises(IndexError, match="Wrong number of cars in hand"):
        answer_truco(2, "PC", [["accept"], ["reject"], ["reply"]], low)     
    low.pop()
    assert len(low) == 0
    with pytest.raises(IndexError, match="Wrong number of cars in hand"):
        answer_truco(3, "PC", [["accept"], ["reject"], ["reply"]], low)

def test_add_envido_weight():
    with pytest.raises(ValueError, match="Weight sum is not 1"):
        add_envido_weight(["accept", "reject", "reply"], 0.30, 0.69)
    with pytest.raises(ValueError, match="Weight sum is not 1"):
        add_envido_weight(["real envido", "falta envido"], 0.70, 0.40)
    assert add_envido_weight(["accept", "reject", "reply"], 0.10, 0.85, 0.05) == {"accept": 0.10, "reject": 0.85, "reply": 0.05}
    assert add_envido_weight(["accept", "reject"], 0.30, 0.70) == {"accept": 0.30, "reject": 0.70}
    
    list = ["envido", "real envido", "falta envido"]
    assert add_envido_weight(list, 0.15, 0.25, 0.60) == {"envido": 0.15, "real envido": 0.25, "falta envido": 0.60}
    list.pop(0)
    assert add_envido_weight(list, 0.70, 0.30) == {"real envido": 0.70, "falta envido": 0.30}

def test_assign_envido_weight(list):
    assert assign_envido_weight(list, "q1", 0, 0) == {"accept": 0.10, "reject": 0.85, "reply":0.05}
    assert assign_envido_weight(list, "q3", 0, 1) == {"accept": 0.50, "reject": 0.25, "reply":0.25}
    assert assign_envido_weight(list, "q1", 2, 0) == {"accept": 0.05, "reject": 0.85, "reply":0.10}
    assert assign_envido_weight(list, "q2", 2, 0) == {"accept": 0.20, "reject": 0.60, "reply":0.20}
    assert assign_envido_weight(list, "q3", 4, 0) == {"accept": 0.55, "reject": 0.10, "reply":0.35}
    assert assign_envido_weight(list, "q4", 4, 0) == {"accept": 0.45, "reject": 0.01, "reply":0.54}
    list = ["accept", "reject"]
    assert assign_envido_weight(list, "q2", 2, 2) == {"accept": 0.40, "reject": 0.60} 
    assert assign_envido_weight(list, "q4", 2, 2) == {"accept": 0.99, "reject": 0.01}
    list =[True, False]
    assert assign_envido_weight(list, "q1", 0, 0) == {True: 0.15, False: 0.85} 
    assert assign_envido_weight(list, "q2", 0, 0) == {True: 0.35, False: 0.65}


def test_assign_envido_reply_weight():
    list = ["envido", "real envido", "falta envido"]
    assert assign_envido_reply_weight(list, "q1", 0) == {"envido": 0.60, "real envido": 0.30, "falta envido": 0.10}
    assert assign_envido_reply_weight(list, "q4", 0) == {"envido": 0.15, "real envido": 0.25, "falta envido": 0.60}
    list = ["real envido", "falta envido"]
    assert assign_envido_reply_weight(list, "q2", 1) == {"real envido": 0.60, "falta envido": 0.40}
    assert assign_envido_reply_weight(list, "q3", 1) == {"real envido": 0.50, "falta envido": 0.50}

def test_reply_envido_faltaEnvido():
    assert reply_envido(["falta envido"], 25, 2) == "falta envido"


