import os
from pathlib import Path
from datetime import datetime

import pandas as pd
from pandas import DataFrame as PDF

from src.utils import convert_series_to_int, convert_pdf_to_int


def _load_file_to_pdf(path: Path) -> PDF:
    custom_date_parser = \
        lambda dates: [datetime.strptime(_date, '%d.%m.%Y') if not pd.isnull(_date) else None for _date in dates]
    df = pd.read_csv(path, parse_dates=False)
    for c in df.columns:
        try:
            parsed_dates = custom_date_parser(df[c])
            df[c] = parsed_dates
        except (TypeError, ValueError) as e:
            pass
    return df


_path = Path("data")
category = _load_file_to_pdf(_path / "category.csv")
player = _load_file_to_pdf(_path / "player.csv")
tournament = _load_file_to_pdf(_path / "tournament.csv")

category_tournament: PDF = None  # type: ignore
match_tournament: PDF = None  # type: ignore
player_tournament: PDF = None  # type: ignore
player_team_tournament: PDF = None  # type: ignore
player_team_extra_match_tournament: PDF = None  # type: ignore
set_tournament: PDF = None  # type: ignore
team_tournament: PDF = None  # type: ignore

for tournament_code in [_ for _ in os.listdir(_path) if os.path.isdir(_path / _)]:
    _path_tournament = _path / tournament_code

    _category_tournament_new = _load_file_to_pdf(_path_tournament / "category.csv")
    _category_tournament_new["tournament_code"] = tournament_code
    category_tournament = (
        _category_tournament_new if category_tournament is None
        else category_tournament.append(_category_tournament_new, ignore_index=True)
    )

    _match_tournament_new = _load_file_to_pdf(_path_tournament / "match.csv")
    _match_tournament_new["tournament_code"] = tournament_code
    match_tournament = (
        _match_tournament_new if match_tournament is None
        else match_tournament.append(_match_tournament_new, ignore_index=True)
    )

    _player_tournament_new = _load_file_to_pdf(_path_tournament / "player.csv")
    _player_tournament_new["tournament_code"] = tournament_code
    player_tournament = (
        _player_tournament_new if player_tournament is None
        else player_tournament.append(_player_tournament_new, ignore_index=True)
    )

    _player_team_tournament_new = _load_file_to_pdf(_path_tournament / "player_team.csv")
    player_team_tournament = (
        _player_team_tournament_new if player_team_tournament is None
        else player_team_tournament.append(_player_team_tournament_new, ignore_index=True)
    )

    _player_team_extra_match_tournament_new = _load_file_to_pdf(_path_tournament / "player_team_extra_match.csv")
    player_team_extra_match_tournament = (
        _player_team_extra_match_tournament_new if player_team_extra_match_tournament is None
        else player_team_extra_match_tournament.append(_player_team_extra_match_tournament_new, ignore_index=True)
    )

    _set_tournament_new = _load_file_to_pdf(_path_tournament / "set.csv")
    set_tournament = (
        _set_tournament_new if set_tournament is None
        else set_tournament.append(_set_tournament_new, ignore_index=True)
    )

    _team_tournament_new = _load_file_to_pdf(_path_tournament / "team.csv")
    _team_tournament_new["tournament_code"] = tournament_code
    team_tournament = (
        _team_tournament_new if team_tournament is None
        else team_tournament.append(_team_tournament_new, ignore_index=True)
    )

set_tournament = convert_pdf_to_int(pdf=set_tournament, cols_rgx=["score_start_(.*)", "score_end_(.*)"])

team_tournament["team_result"] = convert_series_to_int(team_tournament["team_result"])

player_tournament["player_result"] = convert_series_to_int(player_tournament["player_result"])
