
import json
import argparse

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-l', '--file-location', type=str, default='')
    return parser.parse_args()

def extract_stats(game_obj: dict) -> dict:

    # IDEAS:
    # Stats for each leg / set with darts thrown & average
    # Checkout percentage

    player_home = game_obj['player_home']
    player_away = game_obj['player_away']

    leg_log = game_obj['log']

    player_home_points_scored = 0
    player_home_darts_thrown = 0
    player_away_points_scored = 0
    player_away_darts_thrown = 0

    for leg in leg_log:
        for throw in leg:
            if throw['player'] == player_home:
                player_home_points_scored += throw['points_scored']
                player_home_darts_thrown += throw['darts_thrown']
            elif throw['player'] == player_away:
                player_away_points_scored += throw['points_scored']
                player_away_darts_thrown += throw['darts_thrown']
            else:
                raise Exception('Player not found in game object')

    player_home_average = player_home_points_scored / player_home_darts_thrown * 3
    player_away_average = player_away_points_scored / player_away_darts_thrown * 3

    return {
        'average': {
            player_home: player_home_average,
            player_away: player_away_average
        },
    }


if __name__ == '__main__':
    inputs = parse_args()
    if inputs.file_location == '':
        raise Exception('No file location provided')
    with open(inputs.file_location, 'r') as f:
        game_obj = json.load(f)
    print(extract_stats(game_obj))