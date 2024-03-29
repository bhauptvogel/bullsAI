import pandas as pd
import uuid
import random
from bullsai.game_sim import handle_game
from bullsai import dart
from bullsai import empirical_std

def get_player_average(name: str) -> float:
    players = pd.read_csv(f'fantasy/cup/cup_players.csv')
    return float(players[players['Name'] == name]['AVG'].values[0])

def sim_leg(player_home_avg: str, player_away_avg: str, player_beginning: str, total_points: int):
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
            turn = 1

    return 1 if player_1_points == 0 else 2

import argparse

def show():
    players = pd.read_csv(f'fantasy/cup/cup_players.csv')
    left = len(players)

    for i in range(int(left/2)):
        player1 = players.iloc[i]['Name']
        player2 = players.iloc[left-1 - i]['Name']

        print(f'Match {i+1}: {player1} vs {player2}')

def simulate(round: int):
    # TODO: Only take players that have not lost yet (from results.csv)
    print("Simulating...")
    players = pd.read_csv(f'fantasy/cup/cup_players.csv')
    left = len(players)
    results = pd.read_csv(f'fantasy/cup/results.csv')
    for i in range(int(left/2)):
        player1 = players.iloc[i]['Name']
        player2 = players.iloc[left-1 - i]['Name']

        if player1 != 'PLAYER' and player2 != 'PLAYER':
            print(f"Simulating Match {i+1}: {player1} vs {player2}")
            

            player1_avg = get_player_average(player1)
            player2_avg = get_player_average(player2)

            player1_leg_wins = 0
            player2_leg_wins = 0

            LEGS_TO_WIN = 3 + round
            player_beginning = random.randint(1, 2)

            while player1_leg_wins < LEGS_TO_WIN and player2_leg_wins < LEGS_TO_WIN:
                leg_winner = sim_leg(player1_avg, player2_avg, player_beginning, 501)
                if leg_winner == 1:
                    player1_leg_wins += 1
                elif leg_winner == 2:
                    player2_leg_wins += 1
                player_beginning = 1 if player_beginning == 2 else 2

            print(f"Match Result: {player1_leg_wins} - {player2_leg_wins}")
                
            winner = player1 if player1_leg_wins > player2_leg_wins else player2
            loser = player1 if player1_leg_wins < player2_leg_wins else player2

            results = pd.concat([results, pd.DataFrame([[player1, player2, f'{player1_leg_wins} - {player2_leg_wins}']], columns=['Player 1', 'Player 2', 'Result'])])

            print(f"Adding {winner} to the next round.")
            print(f"Removing {loser} from the next round.")
            print()


    # write results
    results.to_csv(f'fantasy/cup/results.csv', index=False)


def play(round: int):
    print("Playing...")

    players = pd.read_csv(f'fantasy/cup/cup_players.csv')
    left = len(players)
    results = pd.read_csv(f'fantasy/cup/results.csv')
    for i in range(int(left/2)):
        player1 = players.iloc[i]['Name']
        player2 = players.iloc[left-1 - i]['Name']


        if player1 == 'PLAYER' or player2 == 'PLAYER':
            game_id = str(uuid.uuid4())
            opponent_average = get_player_average(player1) if player2 == 'PLAYER' else get_player_average(player2)
            opponent_name = player1 if player2 == 'PLAYER' else player2
            first_to_throw = random.randint(1, 2)
            legs_to_win = 3 + round
            result = handle_game(game_id=game_id, bot_average=opponent_average, sets_to_win=1, legs_to_win=legs_to_win, first_to_throw=first_to_throw, starting_points=501, bot_name=opponent_name, save_log_location='fantasy/cup/game_logs/')

def main():
    parser = argparse.ArgumentParser(description="Process some commands.")
    parser.add_argument("--show", action="store_true", help="Execute the show command")
    parser.add_argument("--simulate", action="store_true", help="Execute the simulate command")
    parser.add_argument("--play", action="store_true", help="Execute the play command")
    parser.add_argument("--round", default=1, type=int, help="Specify the round number")

    args = parser.parse_args()

    # If no arguments are provided, default to show
    if not any(vars(args).values()):
        show()
    else:
        if args.show:
            show()
        if args.simulate:
            simulate(args.round)
        if args.play:
            play(args.round)

if __name__ == "__main__":
    main()