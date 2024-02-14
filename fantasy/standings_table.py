import argparse
import pandas as pd
import json

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-l', '--league', type=int, default=4)
    return parser.parse_args()

# TODO: If league not given -> show league with player
def print_league_standings(league: int = 4) -> None:

    players = pd.read_csv('fantasy/players.csv')
    
    league_schedule = pd.read_csv(f'fantasy/schedule_league_{league}.csv')

    league_standings = players[players['League'] == league]
    league_standings = league_standings.drop(columns=['League', 'AVG', 'Sex'])
    league_standings['W'] = 0
    league_standings['L'] = 0
    league_standings['Legs Won'] = 0
    league_standings['Legs Lost'] = 0
    league_standings['Season Average'] = league_standings['Name'].apply(player_season_average)
    league_standings['Season Average'] = league_standings['Season Average'].round(2)

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
        table[i] = row.replace('PLAYER', '\033[1mPLAYER\033[0m')

    print('\n'.join(table), end='\n\n')

def player_season_average(player_name: str):
    # 1. Check if player is in players.csv
    player_df = pd.read_csv('fantasy/players.csv')
    player = player_df[player_df['Name'] == player_name]
    if player.empty:
        raise ValueError('Player not found in players.csv')

    # 2. Get all game ids player has played
    league = player['League'].values[0]
    schedule = pd.read_csv(f'fantasy/schedule_league_{league}.csv')
    player_games = schedule[(schedule['Home Player'] == player_name) | (schedule['Away Player'] == player_name)]
    game_logs = player_games['Game Log'].dropna().values

    # 3. Iterate through games to get stats
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

    return points_scored / darts_thrown * 3

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

# example: in /dart - python fantasy/standings_table.py -l 4
if __name__ == '__main__':
    inputs=parse_args()
    print_league_standings(inputs.league)
    print_upcoming_games(inputs.league)