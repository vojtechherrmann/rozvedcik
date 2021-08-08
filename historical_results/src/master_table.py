from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame as PDF
from pandas import Series as PDS
from dateutil.relativedelta import relativedelta

from src.utils import convert_series_to_int, convert_pdf_to_int


def player_age(i: PDF) -> Tuple[PDS, PDS]:

    i2 = i[["date", "date_of_birth"]].copy()

    age_years = (
        i2
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

    i2["age_years"] = age_years

    age_days = (
        i2
            .apply(
                lambda x:
                None if pd.isnull(x).any()
                else (x[0] - x[1].replace(
                    year=x[0].year - (1 if (x[0] - x[1].replace(year=x[0].year)).days < 0 else 0))).days,
                axis=1,
            )
    )

    return convert_series_to_int(age_years), convert_series_to_int(age_days)


def master_table(
        player_team_tournament: PDF,
        match_tournament: PDF,
        player_team_extra_match_tournament: PDF,
        set_tournament: PDF,
        player_tournament: PDF,
        player: PDF,
        tournament: PDF,
        team_tournament: PDF,
) -> PDF:

    player_match = pd.concat(
        [
            match_tournament
                .merge(
                    player_team_tournament,
                    how="left",
                    left_on="team_tournament_code_1",
                    right_on="team_tournament_code"
                )
                [["player_tournament_code", "team_tournament_code", "match_tournament_code"]]
                .assign(home_team=True),
            match_tournament
                .merge(
                    player_team_tournament,
                    how="left",
                    left_on="team_tournament_code_2",
                    right_on="team_tournament_code"
                )
                [["player_tournament_code", "team_tournament_code", "match_tournament_code"]]
                .assign(home_team=False),
            player_team_extra_match_tournament
                .merge(
                    match_tournament[["match_tournament_code", "team_tournament_code_1"]],
                    how="left",
                    on="match_tournament_code",
                )
                .assign(home_team=lambda x: x["team_tournament_code"] == x["team_tournament_code_1"])
                .drop("team_tournament_code_1", axis=1)
        ],
        ignore_index=True
    )

    player_set = (
        player_match
            .merge(set_tournament, how="left", on="match_tournament_code")
    )

    player_set["points_scored"] = np.where(
        player_set.home_team,
        player_set.score_end_1 - player_set.score_start_1,
        player_set.score_end_2 - player_set.score_start_2,
    )

    player_set["points_received"] = np.where(
        player_set.home_team,
        player_set.score_end_2 - player_set.score_start_2,
        player_set.score_end_1 - player_set.score_start_1,
    )

    player_set = (
        player_set
            .merge(player_tournament, how="left", on="player_tournament_code")
            .merge(player, how="left", on="player_code")
            .merge(tournament, how="left", on="tournament_code")
    )
    player_set["age_years"], player_set["age_days"] = player_age(player_set)

    master_table_ = (
        player_set
            .groupby(["player_code", "player_nickname", "nationality"])
            .agg(
                tournaments=("tournament_code", PDS.nunique),
                matches=("match_tournament_code", PDS.nunique),
                sets=("set_tournament_code", PDS.nunique),
                points_scored=("points_scored", PDS.sum),
                points_received=("points_received", PDS.sum),
                min_player_age_years=("age_years", PDS.min),
                min_player_age_days=("age_days", PDS.min),
                max_player_age_years=("age_years", PDS.max),
                max_player_age_days=("age_days", PDS.max),
            )
            .reset_index()
    )

    master_table_ = convert_pdf_to_int(pdf=master_table_, cols_rgx=r"(min|max)_player_age_(.*)")

    master_table_["rallies"] = \
        master_table_["points_scored"] + master_table_["points_received"]

    master_table_["points_ratio"] = \
        master_table_["points_scored"] / master_table_["points_received"]

    master_table_["rank"] = \
        master_table_["points_ratio"].rank(method="min", ascending=False).astype(int)

    player_medals = (
        pd.concat(
            [
                team_tournament
                    .merge(player_team_tournament, how="left", on="team_tournament_code")
                    .merge(player_tournament, how="left", on="player_tournament_code")
                    .groupby("player_code")
                    .agg(
                        result_gold_6=("team_result", lambda x: x[x == 1].shape[0]),
                        result_silver_6=("team_result", lambda x: x[x == 2].shape[0]),
                        result_bronze_6=("team_result", lambda x: x[x == 3].shape[0]),
                    )
                    .reset_index(),
                player_tournament
                    .groupby("player_code")
                    .agg(
                        result_gold_2=("player_result", lambda x: x[x == 1].shape[0]),
                        result_silver_2=("player_result", lambda x: x[x == 2].shape[0]),
                        result_bronze_2=("player_result", lambda x: x[x == 3].shape[0]),
                    )
                    .reset_index(),
            ],
            ignore_index=True
        )
            .groupby("player_code")
            .sum()
            .reset_index()
    )

    player_medals = convert_pdf_to_int(player_medals, cols_rgx=r"result_(.*)")

    master_table_ = master_table_.merge(player_medals, how="left", on="player_code")

    return master_table_.drop("player_code", axis=1, inplace=False)
