import argparse
import empirical_std
import os
import dart

BLUE = '\033[95m'
OKBLUE = '\033[94m'
GREEN = '\033[32m'
WARNING = '\033[93m'
FAIL = '\033[91m'
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

    def __init__(self, starting_points, first_to_throw, std) -> None:
        self.user_points = starting_points
        self.ai_points = starting_points
        self.first_to_throw = first_to_throw
        self.turn = first_to_throw
        self.ai_std = std

    def at_oche(self):
        if self.turn == 'user':
            points_at_beginning = int(input())
            if points_at_beginning > 180:
                raise Exception('Score not possible (over 180)!')
            self.user_points -= points_at_beginning
            if self.user_points == 0:
                finished = input("Did you finish with a double? [Y/N]")
                if finished == 'yes' or finished == 'y' or finished == 'Y' or finished =='Yes':
                    return True
                else:
                    self.user_points += points_at_beginning
            elif self.user_points < 0:
                self.user_points += points_at_beginning
            self.turn = 'ai'
        elif self.turn == 'ai':
            points_at_beginning = self.ai_points
            for d in range(3):
                coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(self.ai_points, 3-d)), self.ai_std)
                self.ai_points -= dart.get_points_of_coordinates(coordinates)
                if self.ai_points <= 1:
                    if self.ai_points == 0 and dart.was_double_hit(coordinates):
                        return True
                    else:
                        self.ai_points = points_at_beginning
                    break
            self.turn = 'user'
        return False
    
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
        print(ENDC + BOLD + header + ENDC)

        if game.sets_to_win > 1:
            print(OKBLUE +f'{game.player_set_wins} sets\t\t\t\t{game.ai_set_wins} sets')
        print(OKBLUE + f'{game.player_leg_wins} legs\t\t\t\t{game.ai_leg_wins} legs')

        user_turn_color = ENDC + BLUE if self.turn == 'user' else ENDC + OKBLUE
        ai_turn_color = ENDC +  BLUE if self.turn != 'user' else ENDC + OKBLUE

        print(user_turn_color + 'USER\t\t\t\t' + ai_turn_color + 'AI')
        print(user_turn_color + f'{self.user_points}\t\t\t\t' + ai_turn_color + f'{self.ai_points}')


def main():
    inputs=parse_args()
    std = empirical_std.emperical_std(inputs.opponent_average)

    game = Game(inputs.sets_to_win, inputs.legs_to_win)

    first_to_throw = inputs.first_to_throw
    current_leg = Leg(inputs.starting_points, first_to_throw, std)

    while not game.is_game_over():
        # play leg
        current_leg.print_state(game)
        if current_leg.at_oche():
            winner = current_leg.get_winner()
            game.leg_end(winner)
            first_to_throw = 'user' if first_to_throw == 'ai' else 'ai'
            current_leg = Leg(inputs.starting_points, first_to_throw, std)
            
    game.print_winner()


if __name__ == "__main__":
    main()

# TODOS
# - Show the player who is throwing first in this leg on the left
# - Show what which fields AI has thrown (with time delay)
# - Player can also give his fields instead of a score
# - Show what fields players has to throw, if he can finish
# - Show stats at the end
    