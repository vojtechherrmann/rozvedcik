import os
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, Tuple

from dateutil.relativedelta import relativedelta


import pandas as pd
from pandas import DataFrame as PDF


custom_date_parser = lambda dates: [datetime.strptime(_date, '%d.%m.%Y') if not pd.isnull(_date) else None for _date in dates]


def load_file_to_pdf(path: Path) -> PDF:
    df = pd.read_csv(path, parse_dates=False)
    for c in df.columns:
        try:
            parsed_dates = custom_date_parser(df[c])
            df[c] = parsed_dates
        except (TypeError, ValueError) as e:
            pass
    return df


path = Path("data")
category = load_file_to_pdf(path / "category.csv")
player = load_file_to_pdf(path / "player.csv")
tournament = load_file_to_pdf(path / "tournament.csv")

category_tournament: PDF = None  # type: ignore
match_tournament: PDF = None  # type: ignore
player_tournament: PDF = None  # type: ignore
player_team_tournament: PDF = None  # type: ignore
player_team_extra_match_tournament: PDF = None  # type: ignore
set_tournament: PDF = None  # type: ignore
team_tournament: PDF = None  # type: ignore

for tournament_code in [_ for _ in os.listdir(path) if os.path.isdir(path / _)]:
    path_tournament = path / tournament_code

    category_tournament_new = load_file_to_pdf(path_tournament / "category.csv")
    category_tournament_new["tournament_code"] = tournament_code
    category_tournament = (
        category_tournament_new if category_tournament is None
        else category_tournament.append(category_tournament_new, ignore_index=True)
    )

    match_tournament_new = load_file_to_pdf(path_tournament / "match.csv")
    match_tournament_new["tournament_code"] = tournament_code
    match_tournament = (
        match_tournament_new if match_tournament is None
        else match_tournament.append(match_tournament_new, ignore_index=True)
    )

    player_tournament_new = load_file_to_pdf(path_tournament / "player.csv")
    player_tournament_new["tournament_code"] = tournament_code
    player_tournament = (
        player_tournament_new if player_tournament is None
        else player_tournament.append(player_tournament_new, ignore_index=True)
    )

    player_team_tournament_new = load_file_to_pdf(path_tournament / "player_team.csv")
    player_team_tournament = (
        player_team_tournament_new if player_team_tournament is None
        else player_team_tournament.append(player_team_tournament_new, ignore_index=True)
    )

    player_team_extra_match_tournament_new = load_file_to_pdf(path_tournament / "player_team_extra_match.csv")
    player_team_extra_match_tournament = (
        player_team_extra_match_tournament_new if player_team_extra_match_tournament is None
        else player_team_extra_match_tournament.append(player_team_extra_match_tournament_new, ignore_index=True)
    )

    set_tournament_new = load_file_to_pdf(path_tournament / "set.csv")
    set_tournament = (
        set_tournament_new if set_tournament is None
        else set_tournament.append(set_tournament_new, ignore_index=True)
    )

    team_tournament_new = load_file_to_pdf(path_tournament / "team.csv")
    team_tournament_new["tournament_code"] = tournament_code
    team_tournament = (
        team_tournament_new if team_tournament is None
        else team_tournament.append(team_tournament_new, ignore_index=True)
    )


def player_age(player_tournament: PDF, player: PDF, tournament: PDF) -> str:

    player_tournament = (
        player_tournament
            .merge(player, how="left", on="player_code")
            .merge(tournament, how="left", on="tournament_code")
    )

    player_tournament["age_years"] = (
        player_tournament[["date", "date_of_birth"]]
            .apply(
                lambda x:
                    None if pd.isnull(x).any()
                    else relativedelta(
                            x[0] if not pd.isnull(x[0]) else None,
                            x[1] if not pd.isnull(x[1]) else None,
                    ).years,
                axis=1,
            )
    )

    player_tournament["age_days"] = (
        player_tournament[["date", "date_of_birth", "age_years"]]
            .apply(
                lambda x:
                    None if pd.isnull(x).any()
                    else (x[0] - x[1].replace(year=x[0].year - (1 if (x[0] - x[1].replace(year=x[0].year)).days < 0 else 0))).days,
                axis=1,
            )
    )

    oldest = player_tournament.sort_values(by=["age_years", "age_days"], na_position="last", inplace=False, ascending=False).iloc[0]
    youngest = player_tournament.sort_values(by=["age_years", "age_days"], na_position="last", inplace=False).iloc[0]

    return f"Oldest: {oldest['player_code']}, age {int(oldest['age_years'])} years, {int(oldest['age_days'])} days at {oldest['tournament_code']}\n" \
           f"Youngest: {youngest['player_code']}, age {int(youngest['age_years'])} years, {int(youngest['age_days'])} days at {youngest['tournament_code']}"


print(player_age(player_tournament, player, tournament))
