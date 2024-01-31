import pandas as pd
import argparse
import uuid
from bullsai.game_sim import handle_game

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', '--day', type=int, default=0)

    args=parser.parse_args()
    return args

def get_league_of_player() -> int:
    players = pd.read_csv('fantasy/players.csv')
    return int(players[players['Name'] == 'PLAYER']['League'].values[0])

def get_player_average(name: str) -> float:
    players = pd.read_csv('fantasy/players.csv')
    return float(players[players['Name'] == name]['AVG'].values[0])

def play(day: int):
    league_schedule = pd.read_csv(f'fantasy/schedule_league_{get_league_of_player()}.csv')

    game_to_play = league_schedule[league_schedule['Day'] == day]
    game_to_play = game_to_play[(game_to_play['Home Player'] == "PLAYER") | (game_to_play['Away Player'] == "PLAYER")]

    opponent = game_to_play['Home Player'].values[0] if game_to_play['Away Player'].values[0] == 'PLAYER' else game_to_play['Away Player'].values[0]

    first_to_throw = 'player' if game_to_play['Home Player'].values[0] == 'PLAYER' else 'bot'

    game_id = str(uuid.uuid4())
    handle_game(game_id=game_id, bot_average=get_player_average(opponent), sets_to_win=1, legs_to_win=5, first_to_throw=first_to_throw, starting_points=501, bot_name=opponent, save_log_location='fantasy/game_logs/')
    print(f'Game ID: {game_id}')

if __name__ == '__main__':
    inputs=parse_args()
    if inputs.day == 0:
        raise ValueError('Please specify a day')
    else:
        play(inputs.day)
