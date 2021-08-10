from pandas import DataFrame as PDF


def save_to_csv(table: PDF, path) -> None:
    table.to_csv(path, header=True, index=False, encoding='utf-8', sep=',')


def print_historical_records(
        master_table: PDF,
        tournament: PDF,
        match_tournament: PDF,
        set_tournament: PDF,
) -> None:

    print(f"Nr of years: {tournament['year'].nunique()}")

    print(f"Nr of tournaments: {tournament.shape[0]}")

    print(f"Nr of matches: {match_tournament.shape[0]}")

    print(f"Nr of sets: {set_tournament.shape[0]}")

    print(f"Nr of rallies: {set_tournament['score_end_1'].sum() + set_tournament['score_end_2'].sum() - set_tournament['score_start_1'].sum() - set_tournament['score_start_2'].sum()}")

    master_table = master_table.copy()

    print(f"Nr of players: {master_table.shape[0]}")

    print(f"Nr of nationalities: {master_table['nationality'].nunique()}")

    max_appearances = master_table['tournaments'].max()
    players_appearances = ", ".join(
        master_table[master_table['tournaments'] == max_appearances]['player_nickname'].tolist()
    )
    print(f"Most appearances: {max_appearances} ({players_appearances})")

    master_table["wins"] = master_table['result_gold_6'] + master_table['result_gold_2']
    max_wins = master_table['wins'].max()
    players_wins = ", ".join(
        master_table[master_table['wins'] == max_wins]['player_nickname'].tolist()
    )
    print(f"Most wins: {max_wins} ({players_wins})")

    max_rallies = master_table['rallies'].max()
    players_rallies = ", ".join(
        master_table[master_table['rallies'] == max_rallies]['player_nickname'].tolist()
    )
    print(f"Most rallies: {max_rallies} ({players_rallies})")

    oldest = master_table.sort_values(by=["max_player_age_years", "max_player_age_days"], na_position="last", inplace=False, ascending=False).iloc[0]
    youngest = master_table.sort_values(by=["min_player_age_years", "min_player_age_days"], na_position="last", inplace=False).iloc[0]

    print(f"Oldest player: {oldest['player_nickname']}, age {oldest['max_player_age_years']} years, {oldest['max_player_age_days']} days")
    print(f"Youngest player: {youngest['player_nickname']}, age {youngest['min_player_age_years']} years, {youngest['min_player_age_days']} days")
