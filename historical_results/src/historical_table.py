from typing import List, Dict, Any
from pandas import DataFrame as PDF


def create_link(row: Dict[str, Any]) -> str:
    raise NotImplementedError


def add_medal_type(medals: List[str], medal_type: str, medal_appearance: str, medal_count: int) -> None:
    medals.extend([f"<span {medal_appearance}>{medal_type}</span>" for _ in range(medal_count)])


def medals_as_emojis(row: Dict[str, Any]) -> str:
    gold_medal = "🥇"
    silver_medal = "🥈"
    bronze_medal = "🥉"
    teams = "style='font-size:28px; background-color: #d1ada8; border-radius: 2px;'"
    pairs = "style='font-size:28px; background-color: #8DACA6; border-radius: 2px;'"
    medals = []

    add_medal_type(medals, gold_medal, teams, row['result_gold_2'])
    add_medal_type(medals, gold_medal, pairs, row['result_gold_6'])

    add_medal_type(medals, silver_medal, teams, row['result_silver_2'])
    add_medal_type(medals, silver_medal, pairs, row['result_silver_6'])

    add_medal_type(medals, bronze_medal, teams, row['result_bronze_2'])
    add_medal_type(medals, bronze_medal, pairs, row['result_bronze_6'])

    if len(medals) == 0:
        medal_cell = "<span style = 'color: #ffffff00'>Meow</span>"
    else:
        medal_cell = " ".join(medals)

    return medal_cell


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
        lambda x:
            f"{x['result_gold_6'] + x['result_gold_2'] + x['result_silver_6'] + x['result_silver_2'] + x['result_bronze_6'] + x['result_bronze_2']} "
            f"({x['result_gold_6'] + x['result_silver_6'] + x['result_bronze_6']}+{x['result_gold_2'] + x['result_silver_2'] + x['result_bronze_2']})"
        ,
        axis=1,
    )
    master_table["medals_emoji"] = master_table.apply(medals_as_emojis, axis=1,)
    master_table["points_ratio_rounded"] = master_table.apply(
        lambda x: "{:.3f}".format(x["points_ratio"]), axis=1,
    )
    master_table["score"] = master_table.apply(
        lambda x: f"{x['points_scored']}:{x['points_received']}", axis=1,
    )

    return (
        master_table
            [[
                "rank",
                "player_nickname",
                "tournaments",
                "matches",
                "sets",
                "score",
                "points_ratio_rounded",
                "medals_emoji",
            ]]
            .sort_values(
                ["rank", "points_ratio_rounded", "tournaments", "matches", "sets", "player_nickname"],
                ascending=True
            )
            .reset_index(drop=True)
    )
