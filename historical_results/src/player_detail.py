from typing import Tuple, Any

from pandas import DataFrame as PDF

from src.utils import convert_pdf_to_int


def _extract_criterium(master_table: PDF, player_nickname: str, criterium: str, *rank_args, **rank_kwargs) -> Tuple[Any, str]:
    master_table = master_table.copy()
    master_table["min_"] = master_table[criterium].rank(method="min", *rank_args, **rank_kwargs)
    master_table["max_"] = master_table[criterium].rank(method="max", *rank_args, **rank_kwargs)
    master_table = convert_pdf_to_int(pdf=master_table, cols_rgx=["min_", "max_"])

    one_row_master_table = master_table[master_table['player_nickname'] == player_nickname]
    value = one_row_master_table[criterium].iloc[0]
    min_ = one_row_master_table["min_"].iloc[0]
    max_ = one_row_master_table["max_"].iloc[0]
    order = f"{min_}. - {max_}."
    if min_ == max_:
        order = f"{min_}."
    return value, order


def player_detail(master_table: PDF, player_nickname: str) -> None:
    print(f"\nPLAYER DETAIL: {player_nickname}")

    one_master_table = master_table[master_table['player_nickname'] == player_nickname]

    value, order = _extract_criterium(
        master_table=master_table,
        player_nickname=player_nickname,
        criterium="tournaments",
        ascending=False,
    )

    print(f"Tournaments: {value} ({order})")

    value, order = _extract_criterium(
        master_table=master_table,
        player_nickname=player_nickname,
        criterium="matches",
        ascending=False,
    )

    print(f"Matches: {value} ({order})")

    value, order = _extract_criterium(
        master_table=master_table,
        player_nickname=player_nickname,
        criterium="sets",
        ascending=False,
    )

    print(f"Sets {value}: ({order})")

    value, order = _extract_criterium(
        master_table=master_table,
        player_nickname=player_nickname,
        criterium="rallies",
        ascending=False,
    )

    print(f"Rallies {value}: ({order})")

    value, order = _extract_criterium(
        master_table=master_table,
        player_nickname=player_nickname,
        criterium="points_ratio",
        ascending=False,
    )

    print(f"Points ratio: {value} ({order})")
