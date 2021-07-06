
from src.initial_loading import (
    category,
    player,
    tournament,
    category_tournament,
    match_tournament,
    player_tournament,
    player_team_tournament,
    player_team_extra_match_tournament,
    set_tournament,
    team_tournament,
)
from src.master_table import master_table
from src.historical_table import historical_table
from src.historical_records import historical_records

mt = master_table(
    player_team_tournament=player_team_tournament,
    match_tournament=match_tournament,
    player_team_extra_match_tournament=player_team_extra_match_tournament,
    set_tournament=set_tournament,
    player_tournament=player_tournament,
    player=player,
    tournament=tournament,
)

ht = historical_table(mt)

hr = historical_records(mt)

a = 1
