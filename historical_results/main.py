
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
from src.historical_records import save_to_csv, print_historical_records
from src.player_detail import player_detail

mt = master_table(
    player_team_tournament=player_team_tournament,
    match_tournament=match_tournament,
    player_team_extra_match_tournament=player_team_extra_match_tournament,
    set_tournament=set_tournament,
    player_tournament=player_tournament,
    player=player,
    tournament=tournament,
    team_tournament=team_tournament
)

ht = historical_table(mt)

# print_historical_records(
#     master_table=mt,
#     tournament=tournament,
#     match_tournament=match_tournament,
#     set_tournament=set_tournament,
# )
#
# for player_nickname in mt.player_nickname.to_list():
#     player_detail(mt, player_nickname=player_nickname)

save_to_csv(ht, 'players.csv')
