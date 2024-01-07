import argparse
import empirical_std
import os
import sys
import time
import dart

######## SIMPLE TERMINAL FRONTEND

BLUE = '\033[95m'
OKBLUE = '\033[94m'
GREEN = '\033[32m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('--legs_to_win', type=int, default=3)
    parser.add_argument('--sets_to_win', type=int, default=1)
    parser.add_argument('--opponent_average', type=float, default=45.0)
    parser.add_argument('--starting_points', type=int, default=501)
    parser.add_argument('--first_to_throw', type=str, default='user')

    args=parser.parse_args()
    return args

class Game:

    player_set_wins = 0
    player_leg_wins = 0
    ai_set_wins = 0
    ai_leg_wins = 0

    sets_to_win = 0
    legs_to_win = 0

    def __init__(self, sets_to_win, legs_to_win) -> None:
        self.sets_to_win = sets_to_win
        self.legs_to_win = legs_to_win

    def leg_end(self, winner):
        if winner == 'user':
            self.player_leg_wins += 1
            if self.player_leg_wins >= self.legs_to_win:
                self.player_set_wins += 1
                self.player_leg_wins = 0
                self.ai_leg_wins = 0
        elif winner == 'ai':
            self.ai_leg_wins += 1
            if self.ai_leg_wins >= self.legs_to_win:
                self.ai_set_wins += 1
                self.player_leg_wins = 0
                self.ai_leg_wins = 0

    def is_game_over(self):
        return self.player_set_wins >= self.sets_to_win or self.ai_set_wins >= self.sets_to_win

    def print_winner(self):
        if self.player_set_wins >= self.sets_to_win:
            print(GREEN + BOLD + 'USER WINS!' + ENDC)
        elif self.ai_set_wins >= self.sets_to_win:
            print(GREEN + BOLD + 'AI WINS!' + ENDC)
        else:
            print('Game not over!' + ENDC)


class Leg:

    user_points = 0
    ai_points = 0
    ai_std = 0
    turn = ''
    first_to_throw = ''
    last_ai_darts = ''
    last_user_darts = ''

    def __init__(self, starting_points, first_to_throw, std) -> None:
        self.user_points = starting_points
        self.ai_points = starting_points
        self.first_to_throw = first_to_throw
        self.turn = first_to_throw
        self.ai_std = std

    def is_user_input_valid(self, input: str) -> bool:
        return input.isdigit() and int(input) <= 180

    def at_oche(self):
        self.last_user_darts = ''
        self.last_ai_darts = ''
        if self.turn == 'user':
            user_score = ''
            while not self.is_user_input_valid(user_score):
                user_score = input('User turn: ')
            user_score = int(user_score)
            self.last_user_darts = user_score
            if self.user_points - user_score > 1:
                self.user_points -= user_score
            elif self.user_points - user_score == 0 and user_score <= 170 and user_score not in [169, 168, 166, 165, 163, 162, 159]: # bogey numbers
                finished = input("Did you finish with a double? [Y/N]")
                if finished in ['', 'yes', 'Yes', 'YES', 'y', 'Y']:
                    self.user_points -= user_score
                    return
            self.turn = 'ai'
        elif self.turn == 'ai':
            print('AI Turn: ', end='')
            points_at_beginning = self.ai_points
            for d in range(3):
                coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(self.ai_points, 3-d)), self.ai_std)
                self.ai_points -= dart.get_points_of_coordinates(coordinates)
                print(dart.get_field_of_coordinates(coordinates), end=' ')
                self.last_ai_darts += f'{dart.get_field_of_coordinates(coordinates)} '
                sys.stdout.flush()
                time.sleep(0.8)
                if self.ai_points <= 1:
                    if self.ai_points == 0 and dart.was_double_hit(coordinates):
                        return
                    else:
                        self.ai_points = points_at_beginning
                    break
            self.turn = 'user'

    def is_leg_over(self):
        return self.user_points == 0 or self.ai_points == 0
    
    def get_winner(self):
        if self.user_points == 0:
            return 'user'
        elif self.ai_points == 0:
            return 'ai'
        else:
            return None

    def print_state(self, game: Game):
        os.system('cls' if os.name == 'nt' else 'clear')
        if game.sets_to_win == 1:
            header = f'GAME: First to {game.legs_to_win} legs'
        else:
            header = f'GAME: First to {game.sets_to_win} sets'
        print(BOLD + header + ENDC)
        
        user_last_darts = f'({self.last_user_darts})' if self.turn != 'user' else ''
        ai_last_darts = f'({self.last_ai_darts[:-1]})' if self.turn == 'user' else ''

        user_info = [f'{game.player_set_wins} sets', f'{game.player_leg_wins} legs', 'USER', self.user_points, user_last_darts]
        ai_info = [f'{game.ai_set_wins} sets', f'{game.ai_leg_wins} legs', 'AI', self.ai_points, ai_last_darts]
        
        for i, (u, a) in enumerate(zip(user_info, ai_info)):
            user_turn_color = BLUE if self.turn == 'user' and i >= 2 else OKBLUE
            ai_turn_color = BLUE if self.turn != 'user' and i >= 2 else OKBLUE
            if self.first_to_throw == 'user':
                print(f'{user_turn_color}{u:<20}{ai_turn_color}{a:>20}' + ENDC)
            else:
                print(f'{ai_turn_color}{a:<20}{user_turn_color}{u:>20}' + ENDC)

def main():
    inputs=parse_args()
    std = empirical_std.emperical_std(inputs.opponent_average)

    game = Game(inputs.sets_to_win, inputs.legs_to_win)

    first_to_throw = inputs.first_to_throw
    current_leg = Leg(inputs.starting_points, first_to_throw, std)

    while not game.is_game_over():
        # play leg
        current_leg.print_state(game)
        current_leg.at_oche()
        if current_leg.is_leg_over():
            winner = current_leg.get_winner()
            game.leg_end(winner)
            first_to_throw = 'user' if first_to_throw == 'ai' else 'ai'
            current_leg = Leg(inputs.starting_points, first_to_throw, std)

    current_leg.print_state(game)
    game.print_winner()


if __name__ == "__main__":
    main()

# TODOS
# - Show stats at the end
# - Player can also give his fields instead of a score
# - Show what fields players has to throw, if he can finish