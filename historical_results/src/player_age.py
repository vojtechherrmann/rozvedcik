from dateutil.relativedelta import relativedelta

import pandas as pd
from pandas import DataFrame as PDF


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
