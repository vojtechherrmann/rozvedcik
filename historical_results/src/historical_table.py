from pandas import DataFrame as PDF


def historical_table(master_table: PDF) -> PDF:

    master_table = master_table.copy()
    master_table["gold"] = master_table.apply(
        lambda x: f"{x['result_gold_6'] + x['result_gold_2']} ({x['result_gold_6']}+{x['result_gold_2']})",
        axis=1,
    )
    master_table["silver"] = master_table.apply(
        lambda x: f"{x['result_silver_6'] + x['result_silver_2']} ({x['result_silver_6']}+{x['result_silver_2']})",
        axis=1,
    )
    master_table["bronze"] = master_table.apply(
        lambda x: f"{x['result_bronze_6'] + x['result_bronze_2']} ({x['result_bronze_6']}+{x['result_bronze_2']})",
        axis=1,
    )
    master_table["medals"] = master_table.apply(
        lambda x: \
            f"{x['result_gold_6'] + x['result_gold_2'] + x['result_silver_6'] + x['result_silver_2'] + x['result_bronze_6'] + x['result_bronze_2']} "
            f"({x['result_gold_6'] + x['result_silver_6'] + x['result_bronze_6']}+{x['result_gold_2'] + x['result_silver_2'] + x['result_bronze_2']})"
        ,
        axis=1,
    )

    return (
        master_table
            [[
                "rank",
                "player_nickname",
                "tournaments",
                "matches",
                "sets",
                "rallies",
                "points_scored",
                "points_received",
                "points_ratio",
                "medals",
                "gold",
                "silver",
                "bronze",
            ]]
            .sort_values(
                ["rank", "points_ratio", "points_scored", "tournaments", "matches", "sets", "player_nickname"],
                ascending=True
            )
            .reset_index(drop=True)
    )
