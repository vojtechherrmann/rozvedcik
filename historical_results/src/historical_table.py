from typing import List, Dict, Any

from pandas import DataFrame as PDF, Series as PDS
import unidecode


def create_link(row: Dict[str, Any]) -> str:
    raise NotImplementedError


def add_to_medals(medals: List[str], medal_type: str, medal_appearance: str, medal_count: int) -> None:
    medals.extend([f"<span {medal_appearance}>{medal_type}</span>" for _ in range(medal_count)])


_GOLD_MEDAL = "🥇"
_SILVER_MEDAL = "🥈"
_BRONZE_MEDAL = "🥉"
_INVISIBLE_COLOR_CODE = "#ffffff00"


def int_as_str(i: int, decimals: int = 3) -> str:
    if i < 0:
        raise ValueError
    m = 1
    while m < decimals:
        if i < 10 ** m:
            zeros = (decimals - m) * "0"
            return f"{zeros}{i}"
        m += 1
    return str(i)


def medals_as_emojis(row: Dict[str, Any]) -> str:
    teams = "style='font-size: 28px; background-color: #d1ada8; border-radius: 2px;'"
    pairs = "style='font-size: 28px; background-color: #8DACA6; border-radius: 2px;'"
    medals = []

    add_to_medals(medals, _GOLD_MEDAL, teams, row['result_gold_2'])
    add_to_medals(medals, _GOLD_MEDAL, pairs, row['result_gold_6'])

    add_to_medals(medals, _SILVER_MEDAL, teams, row['result_silver_2'])
    add_to_medals(medals, _SILVER_MEDAL, pairs, row['result_silver_6'])

    add_to_medals(medals, _BRONZE_MEDAL, teams, row['result_bronze_2'])
    add_to_medals(medals, _BRONZE_MEDAL, pairs, row['result_bronze_6'])

    order_as_str = int_as_str(row["#"])
    medals_order = f"<span style='font-size: 0; color: {_INVISIBLE_COLOR_CODE};'>Pořadí hráče {order_as_str}: </span>"
    medal_cell = f"{medals_order}{' '.join(medals)}"

    return medal_cell


def modify_rank(rank: PDS):
    cnt = 0
    for r_bef, r, idx in zip(rank[:-1], rank[1:], [1 + _ for _ in range(len(rank) - 1)]):
        if r_bef == r:
            cnt += 1
            rank.iloc[idx] = f"<span style='font-size: 0; color: {_INVISIBLE_COLOR_CODE}'>{r}.{cnt}</span>"
        else:
            cnt = 0
    return rank


def score_with_diff(row: Dict[str, Any]) -> str:
    score = row["score"]
    score_diff = row["score_diff"]
    order_as_str = int_as_str(row["score_diff_order"])
    return f"<span style='font-size: 0;" \
           f" color: {_INVISIBLE_COLOR_CODE};'>Pořadí hráče {order_as_str}, rozdíl balónů {score_diff}: </span>{score}"


def modify_nickname(nickname: str) -> str:
    return f"<span style='font-size: 0; color: {_INVISIBLE_COLOR_CODE}'>{unidecode.unidecode(nickname)} | </span>{nickname}"


def historical_table(master_table: PDF) -> PDF:
    hist_table = master_table.copy()

    # hist_table["#"] = \
    #    hist_table["score"].rank(method="min").astype(int)

    hist_table["#"] = (
        hist_table
        [["medals_score", "points_ratio"]]
            .apply(tuple, axis=1)
            .rank(method="min", ascending=False)
            .astype(int)
    )

    hist_table["score_diff_order"] = (
        hist_table
        [["score_diff", "points_scored"]]
            .apply(tuple, axis=1)
            .rank(method="min", ascending=False)
            .astype(int)
    )

    hist_table["medals_emoji"] = hist_table.apply(medals_as_emojis, axis=1)
    hist_table["points_ratio_rounded"] = hist_table["points_ratio"].apply(
        lambda x: "{:.3f}".format(x),
    )
    hist_table["score_with_diff"] = hist_table.apply(score_with_diff, axis=1)

    ht_sorted = (
        hist_table
        [[
            "#",
            "player_nickname",
            "tournaments",
            "matches",
            "sets",
            "score_with_diff",
            "points_ratio_rounded",
            "medals_emoji",
        ]]
            .sort_values(
            ["#", "tournaments", "matches", "sets", "player_nickname"],
            ascending=True,
        )
            .reset_index(drop=True)
    )

    ht_sorted["#"] = modify_rank(ht_sorted["#"])
    ht_sorted["player_nickname"] = ht_sorted["player_nickname"].apply(modify_nickname)

    ht_sorted.columns = ["#", "Hráč", "Turnaje", "Zápasy", "Sety", "Míče", "Poměr míčů", "Medaile"]

    return ht_sorted
