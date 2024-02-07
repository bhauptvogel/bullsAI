import pandas as pd
import argparse
import uuid
import json
from bullsai import dart
from bullsai import empirical_std

def get_player_average(name: str) -> float:
    players = pd.read_csv('fantasy/players.csv')
    return float(players[players['Name'] == name]['AVG'].values[0])

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-d', '--day', type=int, default=0)
    parser.add_argument('-n', '--next', action='store_true')
    args=parser.parse_args()
    return args

LEGS_TO_WIN = 5
def sim(day: int) -> None:

    for league in range(4):
        print('\nSimulating gameday of league ', league+1, '...')
        games = pd.read_csv(f'fantasy/schedule_league_{league+1}.csv')

        games_on_day = games[games['Day'] == day]
        games_to_simulate = games_on_day[(games_on_day['Home Player'] != "PLAYER") & (games_on_day['Away Player'] != "PLAYER")]


        # loop through games to simulate
        for index, game in games_to_simulate.iterrows():
            player_home = game['Home Player']
            player_away = game['Away Player']

            print(player_home, ' vs ', player_away + ':', end=' ')

            player_home_average = get_player_average(player_home)
            player_away_average = get_player_average(player_away)

            player_home_leg_wins = 0
            player_away_leg_wins = 0
            player_beginning = 1

            game_log = {
                'id': str(uuid.uuid4()),
                'player_home': player_home,
                'player_away': player_away,
                'starting_points': 501,
                'sets_to_win': 1,
                'legs_to_win': LEGS_TO_WIN,
                'winner': '',
                'log': []
            }

            while player_home_leg_wins < LEGS_TO_WIN and player_away_leg_wins < LEGS_TO_WIN:
                sim_leg_obj = sim_leg(player_home, player_away, player_home_average, player_away_average, player_beginning, 501)
                if sim_leg_obj['winner'] == 1:
                    player_home_leg_wins += 1
                else:
                    player_away_leg_wins += 1
                game_log['log'].append(sim_leg_obj['log']['at_oches'])
                player_beginning = 1 if player_beginning == 2 else 2

            result = f'{player_home_leg_wins}-{player_away_leg_wins}'
            print(result)

            game_log['winner'] = player_home if player_home_leg_wins > player_away_leg_wins else player_away            

            # save game_log to json file 
            with open(f'fantasy/game_logs/{game_log["id"]}.json', 'wt') as file:
                file.write(json.dumps(game_log))

            games.loc[index, 'Result'] = result
            games.loc[index, 'Game Log'] = game_log['id']

        games.to_csv(f'fantasy/schedule_league_{league+1}.csv', index=False)


def sim_leg(player_home_name: str, player_away_name: str, player_home_avg: str, player_away_avg: str, player_beginning: str, total_points: int):
    leg_log = {
        'at_oches': []
    }
    player_1_points = total_points
    player_2_points = total_points
    player_1_std = empirical_std.emperical_std(player_home_avg)
    player_2_std = empirical_std.emperical_std(player_away_avg)
    turn = player_beginning

    while player_1_points > 0 and player_2_points > 0:
        if turn == 1:
            points_at_oche = player_1_points
            player_1_darts_thrown = 3
            fields = []
            for d in range(3):
                coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(player_1_points, 3-d)), player_1_std)
                player_1_points -= dart.get_points_of_coordinates(coordinates)
                fields.append(dart.get_field_of_coordinates(coordinates))
                if player_1_points <= 1:
                    if player_1_points == 0 and dart.was_double_hit(coordinates):
                        player_1_darts_thrown -= 2-d
                    else:
                        player_1_points = points_at_oche
                    break
            leg_log['at_oches'].append({
                'player': player_home_name,
                'points_scored': points_at_oche - player_1_points,
                'remaining_points': player_1_points,
                'darts_thrown': player_1_darts_thrown,
                'fields': ','.join(fields),
            })
            turn = 2
        elif turn == 2:
            points_at_oche = player_2_points
            player_2_darts_thrown = 3
            fields = []
            for d in range(3):
                coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(player_2_points, 3-d)), player_2_std)
                player_2_points -= dart.get_points_of_coordinates(coordinates)
                fields.append(dart.get_field_of_coordinates(coordinates))
                if player_2_points <= 1:
                    if player_2_points == 0 and dart.was_double_hit(coordinates):
                        player_2_darts_thrown -= 2-d
                    else:
                        player_2_points = points_at_oche
                    break
            leg_log['at_oches'].append({
                'player': player_away_name,
                'points_scored': points_at_oche - player_2_points,
                'remaining_points': player_2_points,
                'darts_thrown': player_2_darts_thrown,
                'fields': ','.join(fields),
            })
            turn = 1

    return {"winner": 1 if player_1_points == 0 else 2, "log": leg_log}

def is_day_already_played(day: int) -> bool:
    for league in range(4):
        games = pd.read_csv(f'fantasy/schedule_league_{league+1}.csv')
        day_games = games[games['Day'] == day]
        exclude_player = day_games[(day_games['Home Player'] != "PLAYER") & (day_games['Away Player'] != "PLAYER")]
        not_played = exclude_player[exclude_player['Result'].isna()]
        if not_played.empty:
            return True
    return False

def get_next_game_day() -> int:
    day = 0
    for league in range(4):
        games = pd.read_csv(f'fantasy/schedule_league_{league+1}.csv')
        exclude_player = games[(games['Home Player'] != "PLAYER") & (games['Away Player'] != "PLAYER")]
        played_games = exclude_player[exclude_player['Result'].notnull()]
        max_day = played_games['Day'].max()
        if max_day > day:
            day = max_day
    return day + 1

# example: in /dart - python fantasy/simulate_day.py -d 1  
if __name__ == '__main__':
    inputs=parse_args()

    if inputs.next == True and inputs.day == 0:
        day = get_next_game_day()
    else:
        day = inputs.day

    # Input 'Do you want to simulate day {day}'
    user_input = input(f'Do you want to simulate day {day}? (y/n) ')
    if user_input.lower() in ['y', 'yes']:
        if day == 0:
            raise ValueError('Please specify a day')
        elif is_day_already_played(day):
            print(f'Cannot simulate day {day}, since it is already played!')
        else:
            sim(day)
    else:
        print(f'Day {day} not simulated')
