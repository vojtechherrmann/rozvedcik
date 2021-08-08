from typing import List, Dict, Any
from pandas import DataFrame as PDF, Series as PDS


def create_link(row: Dict[str, Any]) -> str:
    raise NotImplementedError


def add_medal_type(medals: List[str], medal_type: str, medal_appearance: str, medal_count: int) -> None:
    medals.extend([f"<span {medal_appearance}>{medal_type}</span>" for _ in range(medal_count)])


_gold_medal = "🥇"
_silver_medal = "🥈"
_bronze_medal = "🥉"
_no_medal = "-"
_invisible_color_code = "ffffff00"


def medals_as_emojis(row: Dict[str, Any]) -> str:

    teams = "style='font-size:28px; background-color: #d1ada8; border-radius: 2px;'"
    pairs = "style='font-size:28px; background-color: #8DACA6; border-radius: 2px;'"
    medals = []

    add_medal_type(medals, _gold_medal, teams, row['result_gold_2'])
    add_medal_type(medals, _gold_medal, pairs, row['result_gold_6'])

    add_medal_type(medals, _silver_medal, teams, row['result_silver_2'])
    add_medal_type(medals, _silver_medal, pairs, row['result_silver_6'])

    add_medal_type(medals, _bronze_medal, teams, row['result_bronze_2'])
    add_medal_type(medals, _bronze_medal, pairs, row['result_bronze_6'])

    if len(medals) == 0:
        medal_cell = f"<span style = 'color: #{_invisible_color_code}'>{_no_medal}</span>"
    else:
        medal_cell = " ".join(medals)

    return medal_cell


def modify_rank(rank: PDS):
    for r_bef, r, idx in zip(rank[:-1], rank[1:], [1 + _ for _ in range(len(rank) - 1)]):
        if r_bef == r:
            rank.iloc[idx] = f"<span style = 'color: #{_invisible_color_code}'>{r}</span>"
    return rank


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

    mt_sorted = (
        master_table
            [[
                "#",
                "player_nickname",
                "tournaments",
                "matches",
                "sets",
                "score",
                "points_ratio_rounded",
                "medals_emoji",
            ]]
            .sort_values(
                ["#", "points_ratio_rounded", "tournaments", "matches", "sets", "player_nickname"],
                ascending=True
            )
            .reset_index(drop=True)
    )

    mt_sorted["#"] = modify_rank(mt_sorted["#"])

    return mt_sorted
