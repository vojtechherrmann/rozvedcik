from pandas import DataFrame as PDF


def historical_table(master_table: PDF) -> PDF:

    return (
        master_table
            [[
                "rank",
                "player_nickname",
                "tournaments",
                "matches",
                "sets",
                "points_scored",
                "points_received",
                "points_ratio",
            ]]
            .sort_values(
                ["rank", "points_ratio", "points_scored", "tournaments", "matches", "sets", "player_nickname"],
                ascending=True
            )
    )
