import argparse
import pandas as pd
import json

def get_standings_table_as_dataframe(league: int, stats: bool, file_location_players: str = 'fantasy/players.csv', folder_location_schedule: str = 'fantasy') -> pd.DataFrame:
    players = pd.read_csv(file_location_players)

    league_schedule = pd.read_csv(f'{folder_location_schedule}/schedule_league_{league}.csv')

    league_standings = players[players['League'] == league]
    league_standings = league_standings.drop(columns=['League', 'AVG', 'Sex'])
    league_standings['W'] = 0
    league_standings['L'] = 0
    league_standings['Legs Won'] = 0
    league_standings['Legs Lost'] = 0
    league_standings['Season Average'] = league_standings['Name'].apply(lambda x: player_season_average(x, file_location_players=file_location_players, folder_location_schedule=folder_location_schedule))
    league_standings['Season Average'] = league_standings['Season Average'].round(1)
    if stats:
        league_standings['First 9 / 12 / 15 Average'] = league_standings['Name'].apply(lambda x: f'{round(player_first_x_average(x, 9),1)} / {round(player_first_x_average(x, 12),1)} / {round(player_first_x_average(x,15),1)}')
        league_standings['100+ Visits'] = league_standings['Name'].apply(lambda x: player_above_x_visits(x, 100))
        league_standings['120+ Visits'] = league_standings['Name'].apply(lambda x: player_above_x_visits(x, 120))
        league_standings['140+ Visits'] = league_standings['Name'].apply(lambda x: player_above_x_visits(x, 140))
        league_standings['Highest Visit'] = league_standings['Name'].apply(player_highest_visit)
        league_standings['Highest Finish'] = league_standings['Name'].apply(player_highest_finish)
        league_standings['Best Leg'] = league_standings['Name'].apply(player_best_leg)

    played_games = league_schedule[league_schedule['Result'].notnull()]

    for game in played_games.iterrows():
        result = game[1]['Result']
        legs_won_home_player = int(result.split('-')[0])
        legs_won_away_player = int(result.split('-')[1])

        # update W, L, Legs Won, Legs Lost
        league_standings.loc[league_standings['Name'] == game[1]['Home Player'], 'W'] += 1 if legs_won_home_player > legs_won_away_player else 0
        league_standings.loc[league_standings['Name'] == game[1]['Home Player'], 'L'] += 1 if legs_won_home_player < legs_won_away_player else 0
        league_standings.loc[league_standings['Name'] == game[1]['Home Player'], 'Legs Won'] += legs_won_home_player
        league_standings.loc[league_standings['Name'] == game[1]['Home Player'], 'Legs Lost'] += legs_won_away_player
        league_standings.loc[league_standings['Name'] == game[1]['Away Player'], 'W'] += 1 if legs_won_away_player > legs_won_home_player else 0
        league_standings.loc[league_standings['Name'] == game[1]['Away Player'], 'L'] += 1 if legs_won_away_player < legs_won_home_player else 0
        league_standings.loc[league_standings['Name'] == game[1]['Away Player'], 'Legs Won'] += legs_won_away_player
        league_standings.loc[league_standings['Name'] == game[1]['Away Player'], 'Legs Lost'] += legs_won_home_player
    
    # sort by W, then by Legs Won, then by Legs Lost ascending
    league_standings = league_standings.sort_values(by=['W', 'Legs Won', 'Legs Lost', 'Season Average'], ascending=[False, False, True, False])

    league_standings['#'] = range(1, len(league_standings)+1)
    league_standings = league_standings[['#'] + league_standings.columns[:-1].tolist()]

    return league_standings


def print_league_standings(league: int, stats: bool) -> None:

    league_standings = get_standings_table_as_dataframe(league=league, stats=stats)

    print(f'League {league} Standings:')
    table = league_standings.to_string(index=False)

    # color first 2 rows
    table = table.split('\n')
    table[0] = '\033[1m' + table[0] + '\033[0m'
    if league > 1:
        table[1] = '\033[32m' + table[1] + '\033[0m'
        table[2] = '\033[32m' + table[2] + '\033[0m'
    else:
        table[1] = '\033[34m' + table[1] + '\033[0m'

    # if league < 4:
    table[-1] = '\033[33m' + table[-1] + '\033[0m'
    table[-2] = '\033[33m' + table[-2] + '\033[0m'

    # color PLAYER
    for i, row in enumerate(table):
        table[i] = row.replace('PLAYER', '\033[1mPLAYER\033[22m')

    print('\n'.join(table), end='\n\n')

def get_player_game_logs(player_name: str, file_location_players: str = 'fantasy/players.csv', folder_location_schedule: str = 'fantasy') -> pd.DataFrame:
    # Check if player is in players.csv
    player_df = pd.read_csv(file_location_players)
    player = player_df[player_df['Name'] == player_name]
    if player.empty:
        raise ValueError('Player not found in players.csv')

    # Get all game ids player has played
    league = int(player['League'].values[0])
    schedule = pd.read_csv(f'{folder_location_schedule}/schedule_league_{league}.csv')
    player_games = schedule[(schedule['Home Player'] == player_name) | (schedule['Away Player'] == player_name)]
    return player_games['Game Log'].dropna().values

def player_season_average(player_name: str, file_location_players: str = 'fantasy/players.csv', folder_location_schedule: str = 'fantasy') -> float:
    game_logs = get_player_game_logs(player_name=player_name, file_location_players=file_location_players, folder_location_schedule=folder_location_schedule)
    darts_thrown = 0
    points_scored = 0
    for game in game_logs:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            leg_log = game_obj['log']
            for leg in leg_log:
                for throw in leg:
                    if throw['player'] == player_name:
                        darts_thrown += throw['darts_thrown']
                        points_scored += throw['points_scored']

    return points_scored / darts_thrown * 3 if darts_thrown > 0 else 0

def player_first_x_average(player_name: str, x: int) -> float:
    game_logs = get_player_game_logs(player_name=player_name)
    darts_thrown = 0
    points_scored = 0
    for game in game_logs:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            leg_log = game_obj['log']
            for leg in leg_log:
                leg_darts = 0
                for throw in leg:
                    if throw['player'] == player_name and leg_darts < x:
                        darts_thrown += throw['darts_thrown']
                        points_scored += throw['points_scored']
                        leg_darts += throw['darts_thrown']
    return points_scored / darts_thrown * 3 if darts_thrown > 0 else 0

def player_highest_visit(player_name: str) -> int:
    game_logs = get_player_game_logs(player_name=player_name)
    highest_visit = 0
    for game in game_logs:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            leg_log = game_obj['log']
            for leg in leg_log:
                for throw in leg:
                    if throw['player'] == player_name and throw['points_scored'] > highest_visit:
                        highest_visit = throw['points_scored']
    return highest_visit

def player_above_x_visits(player_name: str, above_x: int) -> int:
    game_logs = get_player_game_logs(player_name=player_name)
    visits_above_x = 0
    for game in game_logs:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            leg_log = game_obj['log']
            for leg in leg_log:
                for throw in leg:
                    if throw['player'] == player_name and throw['points_scored'] >= above_x:
                        visits_above_x += 1
    return visits_above_x

def player_highest_finish(player_name: str) -> int:
    game_logs = get_player_game_logs(player_name=player_name)
    highest_finish = 0
    for game in game_logs:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            leg_log = game_obj['log']
            for leg in leg_log:
                for throw in leg:
                    if throw['player'] == player_name and throw['points_scored'] > highest_finish and throw['remaining_points'] == 0:
                        highest_finish = throw['points_scored']
    return highest_finish

def player_best_leg(player_name: str) -> str:
    game_logs = get_player_game_logs(player_name=player_name)
    best_leg = 0
    for game in game_logs:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            leg_log = game_obj['log']
            for leg in leg_log:
                leg_darts = 0
                for throw in leg:
                    if throw['player'] == player_name:
                        leg_darts += throw['darts_thrown']
                if best_leg == 0 or leg_darts < best_leg:
                    best_leg = leg_darts
    return f'{best_leg} D'

def print_upcoming_games(league: int) -> None:
    league_schedule = pd.read_csv(f'fantasy/schedule_league_{league}.csv')

    upcoming_games = league_schedule[league_schedule['Result'].isna()]
    if upcoming_games.empty:
        print(f'No upcoming games for League {league}')
        return
    next_day = upcoming_games['Day'].min()
    next_day_games = upcoming_games[upcoming_games['Day'] == next_day]

    print(f'Upcoming Games for League {league} (Day {next_day}):')
    for _, game in next_day_games.iterrows():
        home_player = game['Home Player']
        away_player = game['Away Player']
        print(f'-> {home_player} vs {away_player}')

def get_league_of_player() -> int:
    players = pd.read_csv('fantasy/players.csv')
    return int(players[players['Name'] == 'PLAYER']['League'].values[0])

# example: in /dart - python fantasy/standings_table.py -l 4
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-l', '--league', type=int, default=get_league_of_player())
    parser.add_argument('-s', '--stats', action='store_true')
    inputs = parser.parse_args()
    if inputs.league < 1 or inputs.league > 4:
        raise ValueError('Invalid league number')
    print_league_standings(inputs.league, inputs.stats)
    print_upcoming_games(inputs.league)