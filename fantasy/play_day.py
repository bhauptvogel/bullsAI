import pandas as pd
import argparse
import uuid
from bullsai.game_sim import handle_game, Game

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', '--day', type=int, default=0)

    args=parser.parse_args()
    return args

def get_league_of_player() -> int:
    players = pd.read_csv('fantasy/players.csv')
    return int(players[players['Name'] == 'PLAYER']['League'].values[0])

def get_opponent_average(name: str) -> float:
    players = pd.read_csv('fantasy/players.csv')
    return float(players[players['Name'] == name]['AVG'].values[0])

def put_result_in_csv(player_legs_won: int, opponent_legs_won: int, game_id: str, home_player: str, opponent_name: str):
    league_schedule_csv = f'fantasy/schedule_league_{get_league_of_player()}.csv'
    league_schedule_df = pd.read_csv(league_schedule_csv)

    if home_player == 'player':
        result = f'{player_legs_won}-{opponent_legs_won}'
        league_schedule_df.loc[(league_schedule_df['Home Player'] == 'PLAYER') & (league_schedule_df['Away Player'] == opponent_name), 'Result'] = result
        league_schedule_df.loc[(league_schedule_df['Home Player'] == 'PLAYER') & (league_schedule_df['Away Player'] == opponent_name), 'Game Log'] = game_id
    else:
        result = f'{opponent_legs_won}-{player_legs_won}'
        league_schedule_df.loc[(league_schedule_df['Away Player'] == 'PLAYER') & (league_schedule_df['Home Player'] == opponent_name), 'Result'] = result
        league_schedule_df.loc[(league_schedule_df['Away Player'] == 'PLAYER') & (league_schedule_df['Home Player'] == opponent_name), 'Game Log'] = game_id
    
    league_schedule_df.to_csv(league_schedule_csv, index=False)

def play(day: int):
    league_schedule = pd.read_csv(f'fantasy/schedule_league_{get_league_of_player()}.csv')

    game_to_play = league_schedule[league_schedule['Day'] == day]
    game_to_play = game_to_play[(game_to_play['Home Player'] == "PLAYER") | (game_to_play['Away Player'] == "PLAYER")]

    opponent = game_to_play['Home Player'].values[0] if game_to_play['Away Player'].values[0] == 'PLAYER' else game_to_play['Away Player'].values[0]

    first_to_throw = 'player' if game_to_play['Home Player'].values[0] == 'PLAYER' else 'bot'

    game_id = str(uuid.uuid4())
    result = handle_game(game_id=game_id, bot_average=get_opponent_average(opponent), sets_to_win=1, legs_to_win=5, first_to_throw=first_to_throw, starting_points=501, bot_name=opponent, save_log_location='fantasy/game_logs/')
    put_result_in_csv(result.player_legs_won, result.bot_legs_won, game_id, first_to_throw, opponent)

def has_player_already_played(day: int) -> bool:
    league_schedule = pd.read_csv(f'fantasy/schedule_league_{get_league_of_player()}.csv')
    game_to_play = league_schedule[(league_schedule['Day'] == day) & ((league_schedule['Home Player'] == "PLAYER") | (league_schedule['Away Player'] == "PLAYER"))]
    return not game_to_play['Result'].isnull().values[0]

if __name__ == '__main__':
    inputs=parse_args()
    if inputs.day == 0:
        raise ValueError('Please specify a day')
    elif has_player_already_played(inputs.day):
        print('Player has already played on this day')
    else:
        play(inputs.day)