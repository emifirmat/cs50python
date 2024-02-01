import pytest
from classes import Menu, Deck, Hand, Player, Settings, Points
from project import set_deck


@pytest.fixture
def menu():
    return Menu([["a"], ["quit"]])


@pytest.fixture
def deck():
    return Deck(set_deck("cards_values.csv"))


@pytest.fixture
def hand():
    return Hand()


@pytest.fixture
def cards():
    cards = [
        {"number": "4", "type": "club", "truco": "1", "envido": "4"},
        {"number": "4", "type": "sword", "truco": "1", "envido": "4"},
        {"number": "5", "type": "sword", "truco": "2", "envido": "5"},
        {"number": "10", "type": "coin", "truco": "7", "envido": "0"},
        {"number": "7", "type": "club", "truco": "4", "envido": "7"},
        {"number": "6", "type": "cup", "truco": "3", "envido": "6"},
    ]
    return cards


@pytest.fixture
def fullhand(hand, cards):
    for card in cards[0:3]:
        hand.add_card(card)
    return hand


@pytest.fixture
def p1():
    return Player("Emi")


@pytest.fixture
def set():
    return Settings()


def test_Menu_errors(menu):
    with pytest.raises(ValueError, match="Menu arg is not a list!"):
        Menu([])
    with pytest.raises(AttributeError):
        menu.append("2")


def test_Menu_in_menu(menu):
    for input in ["a", "quit"]:
        assert menu.in_menu(input) == True
    assert menu.in_menu("b") == False


def test_Deck_len(deck):
    with pytest.raises(ValueError, match="Deck has lost too many cards"):
        Deck(set_deck("test_files/test_cards_less.csv"))
    with pytest.raises(ValueError, match="Too many cards in deck!"):
        Deck(set_deck("test_files/test_cards_more.csv"))
    assert len(Deck(set_deck("test_files/test_cards_limit.csv"))) == 34
    assert len(deck) == 40


def test_Deck_deal(deck):
    # Test 1st card
    card = deck.deal()
    assert card == {"number": "4", "type": "sword", "truco": "1", "envido": "4"}
    assert len(deck) == 39
    # Test 2nd card
    card = deck.deal()
    assert card == {"number": "4", "type": "club", "truco": "1", "envido": "4"}
    assert len(deck) == 38


def test_Hand_add_cards(hand, cards):
    # Add a card
    hand.add_card(cards[0])
    assert hand.hand == [{"number": "4", "type": "club", "truco": "1", "envido": "4"}]
    assert hand.temp_hand == [cards[0]]
    # Add 2 more cards
    hand.add_card(cards[1])
    hand.add_card(cards[2])
    assert hand.hand == cards[:3]
    assert hand.temp_hand == [
        {"number": "4", "type": "club", "truco": "1", "envido": "4"},
        {"number": "4", "type": "sword", "truco": "1", "envido": "4"},
        {"number": "5", "type": "sword", "truco": "2", "envido": "5"},
    ]
    # Raise Error with one last card
    with pytest.raises(ValueError, match="Too many cards in hand!"):
        hand.add_card(cards[3])


def test_Hand_pick_card(fullhand):
    with pytest.raises(TypeError):
        fullhand.pick_card("4", "swor")
    picked = fullhand.pick_card("4", "sword")
    assert picked == {"number": "4", "type": "sword", "truco": "1", "envido": "4"}
    picked = fullhand.pick_card("5", "sword")
    assert picked == {"number": "5", "type": "sword", "truco": "2", "envido": "5"}


def test_Player_attributes(p1):
    # Test direct modifications
    with pytest.raises(AttributeError):
        p1.name = "Pablo"
    with pytest.raises(AttributeError):
        p1.dealer = True
    with pytest.raises(AttributeError):
        p1.first = True
    with pytest.raises(AttributeError):
        p1.truco_call = False
    # Test method modification
    p1.change_dealer()
    assert p1.dealer == True


def test_Player_format(p1, cards):
    # 0 cards
    assert f"{p1:hand}" == "None cards"
    # 3 cards
    for card in cards[:3]:
        p1.add_card(card)
    assert f"{p1:hand}" == "[4 club] [4 sword] [5 sword]"


def test_Points_envido_points():
    points = Points()
    with pytest.raises(ValueError, match="Envido points exceed limit"):
        points.update_env_points(34)
    points.update_env_points(33)
    assert points.envido_points == 33


def test_Settings_attributes(set):
    # Test direct changes
    with pytest.raises(AttributeError):
        set.row = 1
    with pytest.raises(AttributeError):
        set.phase = 1
    with pytest.raises(AttributeError):
        set.truco_phase = 1
    with pytest.raises(AttributeError):
        set.envido = False
    with pytest.raises(AttributeError):
        set.envido_phase = 2
    # test changes by method
    set.new_phase()
    set.new_row()
    set.lock_envido()
    for object in [set.phase, set.row]:
        assert object == 1
    assert set.envido == False


def test_Settings_set_falta_envido(set):
    set.set_falta_envido(30, 3)
    assert set.envido_chain[2]["falta envido"] == 27
    set.set_falta_envido(30, 30)
    assert set.envido_chain[2]["falta envido"] == 0
    set.set_falta_envido(30, 0) == 30


def test_Settings_update_row_points(set):
    with pytest.raises(ValueError, match="There should be at least 1 point"):
        set.update_row_points(0, 0)
    set.update_row_points(4, 2)
    assert set.row_points == 6
    set.update_row_points(7, 1)
    assert set.row_points == 8
