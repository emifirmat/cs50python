import pytest
from project import *
from classes import *
from unittest.mock import patch


# Initialize classes
@pytest.fixture
def cards():
    cards = [
        {"number": "4", "type":"club", "truco": "1", "envido": "4"},
        {"number": "4", "type":"sword", "truco": "1", "envido": "4"},
        {"number": "5", "type":"sword", "truco": "2", "envido": "5"},
        {"number": "10", "type":"coin", "truco": "7", "envido": "0"},
        {"number": "7", "type":"club", "truco": "4", "envido": "7"},
        {"number": "6", "type":"cup", "truco": "3", "envido": "6"},
    ]
    return cards

@pytest.fixture
def p1(cards):
    p1 = Player("Emi")
    # 4 club, 4 sword, 5 sword 
    for card in cards[:3]:
        p1.add_card(card)
    return p1

@pytest.fixture
def p2(cards):
    p2 = Player("PC")
    # 10 coin, 7 club, 6 cup 
    for card in cards[-3:]:
        p2.add_card(card)
    return p2

@pytest.fixture
def set():
    return Settings()

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

@patch("random.choice")
def test_choose_dealer_firstRow(mock, p1, p2, set):
    # Emi is dealer
    mock.return_value = p1
    set.new_row()
    p1, p2 = choose_dealer(p1, p2, set)
    assert p1.name == "PC"
    assert p1.first == True
    assert p1.dealer == False
    assert p2.name == "Emi"
    assert p2.first == False
    assert p2.dealer == True
    assert choose_dealer(p1, p2, set) == (p1, p2)
   
def test_choose_dealer_SecondRow(p1, p2, set):
    # Set test - Emi was dealer in First row
    for _ in range(2):
        set.new_row()
    p1, p2 = p2, p1 
    p2.change_dealer()

    # Test
    p1, p2 = choose_dealer(p1, p2, set)
    assert p1.name == "Emi"
    assert p1.first == True
    assert p1.dealer == False
    assert p2.name == "PC"
    assert p2.first == False
    assert p2.dealer == True
    assert choose_dealer(p1, p2, set) == (p2, p1) 

@patch("builtins.input", side_effect=["4 sw", "4 sword club", "4 sword", "7 club", "5 sword"])
def test_play_card(mock, p1, set):
    # Iterate until getting a valid input 4 sword
    assert play_card(p1, set) == 1
    # 7 club invalid input, 5 sword valid
    assert play_card(p1, set) == 2

@patch("project.set_menu", side_effect=["accept", "reject"])
def test_truco_accept(mock, p1, p2, set):
    assert truco(p1, p2, set) == True
    assert set.envido == False
    assert set.truco_phase == 1
    assert set.truco_score == 2
    assert p1.truco_call == False
    assert p2.truco_call == True

@patch("project.set_menu", return_value="reject")
def test_truco_reject(mock, p1, p2, set):
    assert truco(p1, p2, set) == False
    assert set.truco_phase == 0
    assert set.truco_score == 1

@patch("project.set_menu", side_effect=["reply", "reply", "accept"])
def test_truco_full_replies(mock, p1, p2, set):
    assert truco(p1, p2, set) == True
    assert set.envido == False
    assert set.truco_phase == 2
    assert set.truco_score == 4
    assert p1.truco_call == False
    assert p2.truco_call == False

@patch("project.set_menu", side_effect=["reply", "reject"])
def test_truco_partial_replies(mock, p1, p2, set):
    assert truco(p1, p2, set) == False
    assert set.truco_phase == 1
    assert set.truco_score == 2

def test_seach_type(p1, p2):
    assert search_type(p1) == "sword"
    assert search_type(p2) == None
    # two cards in hand
    p1.pick_card("4", "sword")
    assert search_type(p1) == "sword"

@patch("project.search_type", side_effect=["sword", None, "sword", None])
def test_get_envido_points(mock, p1, p2):
    assert get_envido_points(p1) == 29
    assert get_envido_points(p2) == 7
    # 2 cards
    p1.pick_card("4", "sword")
    p2.pick_card("7", "club")
    assert get_envido_points(p1) == 29
    assert get_envido_points(p2) == 7

@patch("project.get_envido_points", side_effect=[26, 30, 29, 20, 0, 0])
def test_play_envido(mock, p1, p2):
    # Caller wins
    assert play_envido(p1, p2) == (p1, p2)
    
    # Caller loses
    [p.restart_env_points() for p in [p1, p2]]
    assert play_envido(p1, p2) == (p2, p1)
    
    # Tie (caller loses)
    [p.restart_env_points() for p in [p1, p2]]
    assert play_envido(p1, p2) == (p2, p1)

def test_envido_accept(p1, p2, set):
    with (
        patch("project.set_menu", return_value="accept"),
        patch("project.play_envido", side_effect=[(p1, p2), (p2, p1)]),
    ):
        # p1 won envido
        assert envido(p1, p2, set, "envido") == (p1, p2)
        assert set.envido_score == 2
        set.restart_values()
        
        # p2 won falta envido
        assert envido(p1, p2, set, "falta envido") == (p2, p1)
        assert set.envido_score == 30

@patch("project.set_menu", return_value="reject")
def test_envido_reject(mock, p1, p2, set):
    # Reject real envido - p1 called, p2 answered
    assert envido(p1, p2, set, "real envido") == (p1, p2)
    assert set.envido_score == 1
    set.restart_values()
    
    # p2 called falta envido, p1 rejected
    assert envido(p2, p1, set, "falta envido") == (p2, p1)
    assert set.envido_score == 1

def test_envido_call(p1, p2, set):
    with (
        patch("project.set_menu", side_effect=["reply", "envido", "accept"]),
        patch("project.play_envido", return_value=(p2, p1)),
    ):
        # P1 called envido, p2 envido, p1 accepted, p2 won
        assert envido(p1, p2, set, "envido") == (p2, p1)
        assert set.envido_phase == 0
        assert set.envido_score == 4
    set.restart_values()
    with (
        patch("project.set_menu", side_effect=["reply", "envido", "reply", "real envido", "reply", "falta envido", "reject"]),
    ):
        # P2 envido, p1 envido, p2 re, p1 fe, p2 reject. p1 wins 
        assert envido(p2, p1, set, "envido") == (p1, p2)
        assert set.envido_score == 7

def test_end_phase(p1, p2, set):
    # Fase 1: p1 played 12 coin, p2 10 club. P1 won
    p1.plays_first()
    end_phase(7, 5, p1, p2, set)
    assert p1.phase_point == 1
    assert p2.phase_point == 0
    assert set.phase_winner == [p1.name]
    assert p1.first == True
    assert p2.first == False

    # Fase 2: p1 played 4 club, p2 5 sword. P2 won
    end_phase(1, 2, p1, p2, set)
    assert p1.phase_point == 1
    assert p2.phase_point == 1
    assert set.phase_winner == [p1.name, p2.name]
    assert p1.first == False
    assert p2.first == True

    # Fase 3, p2 played 6 cup, p1 played 6 coin. Tie
    end_phase(3, 3, p2, p1, set)
    assert p1.phase_point == 1
    assert p2.phase_point == 1
    assert set.phase_winner == [p1.name, p2.name, "tie"]
    assert p2.first == True # Note, p2 is still PC in test
    assert p1.first == False

def test_end_row_ties(p1, p2, set):
    # p1 won ph1, tie ph2
    for _ in range(2):
        set.new_phase() 
    set.phase_winner.extend([p1.name, "tie"])
    p1.add_phase_point()
    assert end_row(p1, p2, set) == p1
    set.restart_values()

    # p2 won ph1, p1 won ph2, tie ph3
    for _ in range(3):
        set.new_phase()
    set.phase_winner.extend([p2.name, p1.name, "tie"])
    p2.add_phase_point()
    assert end_row(p1, p2, set) == p2
    set.restart_values()
    p1.restart_values()

    # tie ph1, p2 won ph2
    for _ in range(2):
        set.new_phase()
    set.phase_winner.extend(["tie", p2.name])
    assert end_row(p1, p2, set) == p2
    set.restart_values()
    p2.restart_values()

    # tie ph1, tie ph 2, p1 won ph3
    for _ in range(3):
        set.new_phase()
    set.phase_winner.extend(["tie", "tie", p1.name])
    p1.add_phase_point()
    assert end_row(p1, p2, set) == p1
    set.restart_values()
    p1.restart_values()

    # tie ph1, tie ph2, tie ph3
    for _ in range(3):
        set.new_phase()
    set.phase_winner.extend(["tie", "tie", "tie"])
    assert end_row(p1, p2, set) == p1

def test_end_row_noties(p1, p2, set):
    # p1 won ph1 and ph2
    for _ in range(2):
        set.phase_winner.append(p1.name)
        set.new_phase()
        p1.add_phase_point()
    assert end_row(p1, p2, set) == p1
    set.restart_values()
    p1.restart_values()

    # p2 win ph1, p1 win ph2, 
    for _ in range(2):
        set.new_phase()
    set.phase_winner.extend([p2.name, p1.name])
    for p in [p2, p1]:
        p.add_phase_point()
    assert end_row(p1, p2, set) == False

    # p2 win ph3
    set.new_phase()
    set.phase_winner.append(p2.name)
    p2.add_phase_point()
    assert end_row(p1, p2, set) == p2

def test_score_winner(p1, p2, set):
    # P1 won the game
    set.envido_score = 30
    with pytest.raises(SystemExit, match="--Thank you for playing truco, see you!"):
        score(p1, p2, set, "envido")

    # P2 won with truco points
    p2.update_game_score(27)
    set.truco_score = 4
    with pytest.raises(SystemExit, match="--Thank you for playing truco, see you!"):
        score(p2, p1, set)

def test_score_nowinner(p1, p2, set):
    # P2 won envido
    set.envido_score = 2
    assert score(p2, p1, set, "envido") == None
    assert p1.game_score == 0
    assert p2.game_score == 2

    # P1 won truco
    set.truco_score = 3
    assert score(p1, p2, set) == None
    assert p1.game_score == 3
    assert p2.game_score == 2

@patch("builtins.input")
def test_exit_game_quit(mock):
    mock.side_effect=["yEs"," y ","yes", "YES"]
    for _ in mock:
        with pytest.raises(SystemExit, match="--Thank you for playing truco, see you!"):
            exit_game()
    mock.side_effect=["no", " nO", "NO ", "n", "N"]
    for _ in mock:
        assert exit_game() == None
    # Test while loop
    mock.side_effect=["y3s", "yessss", "whatever", " n0 ", "nope"]
    for _ in mock:
        with pytest.raises(StopIteration):
            exit_game()     

def test_exit_game_winner():
    with pytest.raises(SystemExit, match="--Thank you for playing truco, see you!"):
        exit_game("winner")