import argparse
import empirical_std
import os
import sys
import time
from bullsai import dart

######## SIMPLE TERMINAL FRONTEND

BLUE = '\033[95m'
OKBLUE = '\033[94m'
GREEN = '\033[32m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def parse_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-l', '--legs_to_win', type=int, default=3)
    parser.add_argument('-s', '--sets_to_win', type=int, default=1)
    parser.add_argument('--starting_points', type=int, default=501)
    parser.add_argument('--first_to_throw', type=str, default='player')
    parser.add_argument('-a', '--ai_average', type=float, default=45.0)
    parser.add_argument('-t', '--ai_time', type=float, default=2.4)

    args=parser.parse_args()
    return args

class Game:

    player_set_wins = 0
    player_leg_wins = 0
    ai_set_wins = 0
    ai_leg_wins = 0

    sets_to_win = 0
    legs_to_win = 0

    player_total_darts_thrown = 0
    player_total_points_scored = 0
    ai_total_darts_thrown = 0
    ai_total_points_scored = 0

    def __init__(self, sets_to_win, legs_to_win) -> None:
        self.sets_to_win = sets_to_win
        self.legs_to_win = legs_to_win

    def leg_end(self, winner) -> None:
        if winner == 'player':
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

    def is_game_over(self) -> bool:
        return self.player_set_wins >= self.sets_to_win or self.ai_set_wins >= self.sets_to_win

    def add_leg_stats(self, player_darts_thrown: int, players_points_scored: int, ai_darts_thrown: int, ai_points_scored: int) -> None:
        self.player_total_darts_thrown += player_darts_thrown
        self.player_total_points_scored += players_points_scored
        self.ai_total_darts_thrown += ai_darts_thrown
        self.ai_total_points_scored += ai_points_scored

    def print_winner(self) -> None:
        if self.player_set_wins >= self.sets_to_win:
            print(GREEN + BOLD + 'Player WINS!' + ENDC)
        elif self.ai_set_wins >= self.sets_to_win:
            print(GREEN + BOLD + 'AI WINS!' + ENDC)
        else:
            print('Game not over!' + ENDC)

    def print_stats(self) -> None:
        player_avg = round(self.player_total_points_scored / self.player_total_darts_thrown * 3,2)
        ai_avg = round(self.ai_total_points_scored / self.ai_total_darts_thrown * 3,2)

        col_width = 15
        top_border = "+" + "-" * (col_width + 2) + "+" + "-" * (col_width + 2) + "+"
        header = "| {:^{}} | {:^{}} |".format("Player", col_width, "Average", col_width)
        divider = "+" + "-" * (col_width + 2) + "+" + "-" * (col_width + 2) + "+"
        human_row = "| {:<{}} | {:^{}} |".format("Human Player", col_width, player_avg, col_width)
        ai_row = "| {:<{}} | {:^{}} |".format("AI Opponent", col_width, ai_avg, col_width)

        for row in [top_border, header, divider, human_row, divider, ai_row, divider]:
            print(row)



class Leg:

    player_points_total = 0
    ai_points_total = 0
    ai_std = 0
    turn = ''
    first_to_throw = ''
    last_ai_darts = ''
    last_player_darts = ''

    players_darts_thrown = 0
    ai_darts_thrown = 0

    def __init__(self, starting_points, first_to_throw, std) -> None:
        self.player_points_total = starting_points
        self.ai_points_total = starting_points
        self.first_to_throw = first_to_throw
        self.turn = first_to_throw
        self.ai_std = std

    def is_player_input_valid(self, input: str) -> bool:
        return input.isdigit() and int(input) <= 180 # TODO: Give Feedback if wrong

    def at_oche(self, time_for_ai: float) -> None:
        self.last_player_darts = ''
        self.last_ai_darts = ''
        if self.turn == 'player':
            player_score = ''
            while not self.is_player_input_valid(player_score):
                player_score = input('Player turn: ')
            player_score = int(player_score)
            self.last_player_darts = player_score
            self.players_darts_thrown += 3
            if self.player_points_total - player_score > 1:
                self.player_points_total -= player_score
            elif self.player_points_total - player_score == 0 and player_score <= 170 and player_score not in [169, 168, 166, 165, 163, 162, 159]: # bogey numbers
                finished = input("Did you finish with a double? [Y/N]")
                if finished in ['', 'yes', 'Yes', 'YES', 'y', 'Y']:
                    self.player_points_total -= player_score
                    if player_score <= 110 and player_score not in [109, 108, 106, 105, 103, 102, 99]:
                        self.players_darts_thrown += int(input("How many darts did you need?")) - 3
                    return
            self.turn = 'ai'
        elif self.turn == 'ai':
            print('AI Turn: ', end='')
            points_at_beginning = self.ai_points_total
            for d in range(3):
                coordinates = dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(self.ai_points_total, 3-d)), self.ai_std)
                self.ai_points_total -= dart.get_points_of_coordinates(coordinates)
                self.ai_darts_thrown += 1
                print(dart.get_field_of_coordinates(coordinates), end=' ')
                self.last_ai_darts += f'{dart.get_field_of_coordinates(coordinates)} '
                sys.stdout.flush()
                time.sleep(time_for_ai / 3)
                if self.ai_points_total <= 1:
                    if self.ai_points_total == 0 and dart.was_double_hit(coordinates):
                        return
                    else:
                        self.ai_points_total = points_at_beginning
                    break
            self.turn = 'player'

    def is_leg_over(self) -> bool:
        return self.player_points_total == 0 or self.ai_points_total == 0
    
    def get_winner(self) -> str:
        if self.player_points_total == 0:
            return 'player'
        elif self.ai_points_total == 0:
            return 'ai'
        else:
            return None

    def print_state(self, game: Game) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        if game.sets_to_win == 1:
            header = f'GAME: First to {game.legs_to_win} legs'
        else:
            header = f'GAME: First to {game.sets_to_win} sets'
        print(BOLD + header + ENDC)
        
        player_last_darts = f'({self.last_player_darts})' if self.turn != 'player' else ''
        ai_last_darts = f'({self.last_ai_darts[:-1]})' if self.turn == 'player' else ''

        player_info = [f'{game.player_set_wins} sets', f'{game.player_leg_wins} legs', 'PLAYER', self.player_points_total, player_last_darts]
        ai_info = [f'{game.ai_set_wins} sets', f'{game.ai_leg_wins} legs', 'AI', self.ai_points_total, ai_last_darts]
        
        if game.sets_to_win == 1:
            player_info.pop(0)
            ai_info.pop(0)

        for i, (u, a) in enumerate(zip(player_info, ai_info)):
            player_turn_color = BLUE if self.turn == 'player' and i >= 2 else OKBLUE
            ai_turn_color = BLUE if self.turn != 'player' and i >= 2 else OKBLUE
            if self.first_to_throw == 'player':
                print(f'{player_turn_color}{u:<20}{ai_turn_color}{a:>20}' + ENDC)
            else:
                print(f'{ai_turn_color}{a:<20}{player_turn_color}{u:>20}' + ENDC)

def main():
    inputs=parse_args()
    std = empirical_std.emperical_std(inputs.ai_average)

    game = Game(inputs.sets_to_win, inputs.legs_to_win)

    first_to_throw = inputs.first_to_throw
    current_leg = Leg(inputs.starting_points, first_to_throw, std)

    while not game.is_game_over():
        # play leg
        current_leg.print_state(game)
        current_leg.at_oche(inputs.ai_time)
        if current_leg.is_leg_over():
            winner = current_leg.get_winner()
            game.leg_end(winner)
            game.add_leg_stats(current_leg.players_darts_thrown, 501-current_leg.player_points_total, current_leg.ai_darts_thrown, 501 - current_leg.ai_points_total)
            first_to_throw = 'player' if first_to_throw == 'ai' else 'ai'
            current_leg = Leg(inputs.starting_points, first_to_throw, std)

    current_leg.print_state(game)
    game.print_winner()
    game.print_stats()


if __name__ == "__main__":
    main()

# TODOS
# - Player can also give his fields instead of a score
# - Show what fields players has to throw, if he can finish