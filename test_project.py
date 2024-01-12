global:
    goal_scre = 30

settings:
    truco_point -- Value from truco call
    envido_points   -- Value from envido call

player:
    phase_points  -- number of winning phase
    game_score -- main score



  # End row
case : 2 wins 
pc 12 co
emi 11 cl
----------
pc 6 co
emi 5 cl

case: row 1 tie, row 2 win

pc 7 cup
emi 7 cl
--------
pc 1 cup
emi 10 club

case: row 1 win row 2 tie 

emi 1 cl
pc 12 sw

----

emi 10 cl
pc 10 sword

case: double tie

pc 12
emi 12
----
pc 10
emi 10
-----
pc 10
emi 1 coin