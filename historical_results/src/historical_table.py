from typing import List, Dict, Any
from pandas import DataFrame as PDF, Series as PDS


def create_link(row: Dict[str, Any]) -> str:
    raise NotImplementedError


def add_to_medals(medals: List[str], medal_type: str, medal_appearance: str, medal_count: int) -> None:
    medals.extend([f"<span {medal_appearance}>{medal_type}</span>" for _ in range(medal_count)])


_GOLD_MEDAL = "🥇"
_SILVER_MEDAL = "🥈"
_BRONZE_MEDAL = "🥉"
_INVISIBLE_COLOR_CODE = "ffffff00"


def int_as_str(i: int) -> str:
    if i < 0:
        raise ValueError
    if i < 10:
        return f"00{i}"
    if i < 100:
        return f"0{i}"
    return str(i)


def medals_as_emojis(row: Dict[str, Any]) -> str:

    _NO_MEDAL = "-"

    order_as_str = int_as_str(row["#"])

    teams = "style='font-size:28px; background-color: #d1ada8; border-radius: 2px;'"
    pairs = "style='font-size:28px; background-color: #8DACA6; border-radius: 2px;'"
    medals = []

    add_to_medals(medals, _GOLD_MEDAL, teams, row['result_gold_2'])
    add_to_medals(medals, _GOLD_MEDAL, pairs, row['result_gold_6'])

    add_to_medals(medals, _SILVER_MEDAL, teams, row['result_silver_2'])
    add_to_medals(medals, _SILVER_MEDAL, pairs, row['result_silver_6'])

    add_to_medals(medals, _BRONZE_MEDAL, teams, row['result_bronze_2'])
    add_to_medals(medals, _BRONZE_MEDAL, pairs, row['result_bronze_6'])

    if len(medals) == 0:
        medal_cell = f"<span style = 'color: #{_INVISIBLE_COLOR_CODE}'>{_NO_MEDAL}</span>"
    else:
        medal_cell = " ".join(medals)

    return medal_cell


def modify_rank(rank: PDS):
    for r_bef, r, idx in zip(rank[:-1], rank[1:], [1 + _ for _ in range(len(rank) - 1)]):
        if r_bef == r:
            rank.iloc[idx] = f"<span style = 'color: #{_INVISIBLE_COLOR_CODE}'>{r}</span>"
    return rank


def modify_score_diff(row: Dict[str, Any]) -> str:
    score_diff = row["score_diff"]
    # TODO
    return score_diff


def historical_table(master_table: PDF) -> PDF:

    master_table = master_table.copy()

    # master_table["gold"] = master_table.apply(
    #     lambda x: f"{x['result_gold_6'] + x['result_gold_2']} ({x['result_gold_6']}+{x['result_gold_2']})",
    #     axis=1,
    # )
    # master_table["silver"] = master_table.apply(
    #     lambda x: f"{x['result_silver_6'] + x['result_silver_2']} ({x['result_silver_6']}+{x['result_silver_2']})",
    #     axis=1,
    # )
    # master_table["bronze"] = master_table.apply(
    #     lambda x: f"{x['result_bronze_6'] + x['result_bronze_2']} ({x['result_bronze_6']}+{x['result_bronze_2']})",
    #     axis=1,
    # )
    # master_table["medals"] = master_table.apply(
    #     lambda x:
    #       f"{x['result_gold_6'] + x['result_gold_2'] + x['result_silver_6'] + x['result_silver_2'] + x['result_bronze_6'] + x['result_bronze_2']} "
    #       f"({x['result_gold_6'] + x['result_silver_6'] + x['result_bronze_6']}+{x['result_gold_2'] + x['result_silver_2'] + x['result_bronze_2']})"
    #     ,
    #     axis=1,
    # )

    # master_table["#"] = \
    #    master_table["score"].rank(method="min").astype(int)

    master_table["#"] = (
        master_table
            [["medals_score", "points_ratio"]]
            .apply(tuple, axis=1)
            .rank(method="min", ascending=False)
            .astype(int)
    )

    master_table["medals_emoji"] = master_table.apply(medals_as_emojis, axis=1)
    master_table["points_ratio_rounded"] = master_table["points_ratio"].apply(
        lambda x: "{:.3f}".format(x),
    )
    master_table["score_diff"] = master_table.apply(modify_score_diff, axis=1)

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
                ["#", "tournaments", "matches", "sets", "player_nickname"],
                ascending=True
            )
            .reset_index(drop=True)
    )

    mt_sorted["#"] = modify_rank(mt_sorted["#"])

    return mt_sorted
