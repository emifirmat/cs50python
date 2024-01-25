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
    table1, table2 = 8, 5
    hand = medium[:]
    # 1 card higher / 2 cards higher
    assert compare_cards(hand, table1) == medium[1]
    assert compare_cards(hand, table2) == medium[2]

def test_compare_cards_equal(low):
    table = 2
    hand1 = low[:]
    hand2 = [
        {"number": "5", "type":"coin", "truco": "2", "envido": "5"},
        {"number": "5", "type":"sword", "truco": "2", "envido": "5"},
        {"number": "4", "type":"sword", "truco": "1", "envido": "5"},
    ]
    # 1 card equal and 2 lower / # 2 cards equal and one lower
    assert compare_cards(hand1, table) == low[2]
    assert compare_cards(hand2, table) == {"number": "5", "type":"coin", "truco": "2", "envido": "5"} or {"number": "5", "type":"sword", "truco": "2", "envido": "5"}

def test_compare_cards_lower(medium, high):
    # 3 cards lower
    table = 14
    hand1, hand2 = medium[:], high[:]
    assert compare_cards(hand1, table) == medium[0]
    assert compare_cards(hand2, table) == high[1]


def test_hand_values(medium):
    assert hand_values(medium) == [4, 9, 7]


@patch("pc.hand_values")
def test_pc_choose_card_firstPhase(mock, low, medium, high):
    # First to play: choose a card between 2 and 7 coin 
    mock.return_value=[4, 9, 7]
    hand1, hand2 = medium[:], high[:]
    assert pc_choose_card(1, True, None, hand1, 1) == medium[1]
    mock.return_value=[11, 9, 13]
    assert pc_choose_card(1, True, None, hand2, 2) == high[0] or high[1]
    # Other options in first phase where tested in other functions or are random


