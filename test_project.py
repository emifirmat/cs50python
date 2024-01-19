import pytest
from project import set_menu, set_deck
from classes import *
from unittest.mock import Mock, patch
 


@patch("builtins.input", side_effect=[" quit", "exit ", "Intro", " ScoRes "])
def test_set_menu(mock):
    # Create list and borrow Menu class for testing 
    list = [['intro'], ['scores']]
    Menu(list).in_menu(mock)
    
    for result in ["quit", "quit", "intro", "scores"]:
        assert set_menu(list) == result


def test_set_deck():
    # Test wrong name
    with pytest.raises(SystemExit, match= "Can't open cards values file"):
        set_deck("test")

    deck_dict = set_deck("cards_values.csv")
    
    # Test keys exist
    keys = deck_dict[0].keys()
    for key in ['number', 'type', 'truco', 'envido']:
        assert key in keys

    # Test values exist
    values = deck_dict[14].values()
    for value in ["10", "sword", "5", "0"]:
        assert value in values

    # Test length
    assert len(deck_dict) == 40