import os
import argparse
import json
import time
import sys
from datetime import datetime
from dataclasses import dataclass
from bullsai import dart
from bullsai import stats
from bullsai import empirical_std

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
    parser.add_argument('-a', '--bot_average', type=float, default=45.0)
    parser.add_argument('-t', '--bot_time', type=float, default=0.8)
    return parser.parse_args()

@dataclass
class Game:
    # PLAYER 'player', AI Bot 'BOT'

    sets_to_win: int
    legs_to_win: int
    bot_std: float
    starting_score: int = 501

    player_legs_won: int = 0
    player_sets_won: int = 0
    bot_legs_won: int = 0
    bot_sets_won: int = 0

    bot_name: str = 'BOT'

    def new_leg_won(self, winner: str) -> None:

        def _new_set_won(winner):
            if winner == 'player':
                self.player_sets_won += 1
            elif winner == self.bot_name:
                self.bot_sets_won += 1

            if self.sets_to_win > 1:
                self.player_legs_won = 0
                self.bot_legs_won = 0

        if winner == 'player':
            self.player_legs_won += 1
            if self.player_legs_won == self.legs_to_win:
                _new_set_won('player')
        elif winner == self.bot_name:
            self.bot_legs_won += 1
            if self.bot_legs_won == self.legs_to_win:
                _new_set_won(self.bot_name)
        else:
            raise ValueError(f'Invalid winner: {winner}')

    def is_game_over(self) -> bool:
        return self.player_sets_won == self.sets_to_win or self.bot_sets_won == self.sets_to_win
 
    def get_winner(self) -> str:
        if self.player_sets_won == self.sets_to_win:
            return 'PLAYER'
        elif self.bot_sets_won == self.sets_to_win:
            return self.bot_name
        else:
            raise ValueError('Game is not over yet')

    def __repr__(self) -> str:
        output = ''

        if self.is_game_over():
            if self.sets_to_win == 1:
                winner_score = self.player_legs_won if self.player_legs_won > self.bot_legs_won else self.bot_legs_won
                loser_score = self.player_legs_won if self.player_legs_won < self.bot_legs_won else self.bot_legs_won
            else:
                winner_score = self.player_sets_won if self.player_sets_won > self.bot_sets_won else self.bot_sets_won
                loser_score = self.player_sets_won if self.player_sets_won < self.bot_sets_won else self.bot_sets_won

            output += f'{BOLD}GAME OVER!{ENDC}\n'
            output += f'{GREEN}{self.get_winner()} won {winner_score} - {loser_score}!{ENDC}\n'
        else:
            output += f'{BOLD}GAME: First to {self.sets_to_win} sets{ENDC}\n'
            output += f'PLAYER -> {self.player_sets_won} sets - {self.player_legs_won} legs\n'
            output += f'{self.bot_name} -> {self.bot_sets_won} sets - {self.bot_legs_won} legs\n'

        return output

class Leg:

    def __init__(self, first_to_throw: str, game_information: Game, bot_time: float) -> None:
        self.log: list = []

        self.player_score = game_information.starting_score
        self.bot_score = game_information.starting_score

        self.first_to_throw = first_to_throw
        self.turn = first_to_throw
        
        self.game_information = game_information
        self.bot_time = bot_time

    def visit(self) -> None:
        if self.turn == 'player':
            self._player_turn()
            self.turn = 'bot'
        elif self.turn == 'bot':
            self._bot_turn()
            self.turn = 'player'
        else:
            raise ValueError(f'Invalid turn: {self.turn}')

    def _is_checkout(self, score: int, points: int) -> bool:
        return score - points == 0 and score <= 170 and score not in [169, 168, 166, 165, 163, 162, 159] # bogey numbers

    def _player_turn(self) -> None:

        def _get_player_input() -> int:
            score_input = input('Player turn: ')
            return int(score_input) if (score_input.isdigit() and int(score_input) <= 180) else _get_player_input()

        player_points = _get_player_input()
        darts_thrown = 3

        def _validate_amount_of_darts(darts_needed: int, points_scored: int) -> bool:
            return (darts_needed.isdigit() and 
                    ((int(darts_needed) == 1 and points_scored <= 40 and points_scored % 2 == 0) or
                    (int(darts_needed) == 2 and points_scored <= 110 and points_scored not in [109, 108, 106, 105, 103, 102, 99]) or
                    (int(darts_needed) == 3)))

        def _get_player_darts_thrown(points_scored: int) -> int:
            if points_scored > 110 or points_scored in [109, 108, 106, 105, 103, 102, 99]:
                return 3
            darts_needed = input("How many darts did you need? ")
            return int(darts_needed) if _validate_amount_of_darts(darts_needed, points_scored) else _get_player_darts_thrown(points_scored)

        def _finished_with_double() -> bool:
            return input("Did you finish with a double? [Y/N] ") in ['', 'yes', 'Yes', 'YES', 'y', 'Y']

        if self.player_score - player_points <= 1:
            if self._is_checkout(self.player_score, player_points) and _finished_with_double():
                darts_thrown = _get_player_darts_thrown(player_points)
            else:
                player_points = 0
            
        self.player_score -= player_points
        self.log.append({
            'player': 'PLAYER',
            'points_scored': player_points,
            'remaining_points': self.player_score,
            'darts_thrown': darts_thrown,
            'fields': ''
        })
    
    def _bot_turn(self):
        fields_thrown = []
        bot_points = 0
        darts_thrown = 3

        def _sim_bot_throw(remaining_darts: int) -> float:
            return dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(self.bot_score-bot_points, remaining_darts)), self.game_information.bot_std)

        print(f'{self.game_information.bot_name} turn: ', end='')
        for dart_index in range(3):
            bot_coordinates = _sim_bot_throw(3 - dart_index)
            bot_points += dart.get_points_of_coordinates(bot_coordinates)
            fields_thrown.append(dart.get_field_of_coordinates(bot_coordinates))

            print(dart.get_field_of_coordinates(bot_coordinates), end=' ')
            sys.stdout.flush()
            time.sleep(self.bot_time)

            if self.bot_score - bot_points <= 1:
                if self._is_checkout(self.bot_score, bot_points) and dart.was_double_hit(bot_coordinates):
                    darts_thrown = dart_index + 1
                else:
                    bot_points = 0
                break

        self.bot_score -= bot_points
        self.log.append({
            'player': self.game_information.bot_name,
            'points_scored': bot_points,
            'remaining_points': self.bot_score,
            'darts_thrown': darts_thrown,
            'fields': ','.join(fields_thrown)
        })

    def is_leg_over(self) -> bool:
        return self.player_score == 0 or self.bot_score == 0  
    
    def get_winner(self) -> str:
        if self.player_score == 0:
            return 'player'
        elif self.bot_score == 0:
            return self.game_information.bot_name
        else:
            raise ValueError('Leg is not over yet')

    def __repr__(self) -> str:
        output = ''
        
        last_darts_of_player = f'({self.log[-1]["points_scored"]})' if self.log and self.log[-1]['player'] == 'PLAYER' else ''
        last_darts_of_bot = f'({self.log[-1]["fields"]})' if self.log and self.log[-1]['player'] == self.game_information.bot_name else ''

        player_info = [f'{self.game_information.player_legs_won} legs', 'PLAYER', self.player_score, last_darts_of_player]
        bot_info = [f'{self.game_information.bot_legs_won} legs', self.game_information.bot_name, self.bot_score, last_darts_of_bot]

        if self.game_information.sets_to_win == 1:
            output += f'{BOLD}GAME: First to {self.game_information.legs_to_win} legs{ENDC}\n'
            coloring = 1
        else:
            output += f'{BOLD}GAME: First to {self.game_information.sets_to_win} sets{ENDC}\n'
            player_info.insert(0, f'{self.game_information.player_sets_won} sets')
            bot_info.insert(0, f'{self.game_information.bot_sets_won} sets')
            coloring = 2

        for i, (u, a) in enumerate(zip(player_info, bot_info)):
            player_turn_color = BLUE if self.turn == 'player' and i >= coloring else OKBLUE
            ai_turn_color = BLUE if self.turn != 'player' and i >= coloring else OKBLUE
            if self.first_to_throw == 'player':
                output += f'{player_turn_color}{u:<20}{ai_turn_color}{a:>20}{ENDC}\n' 
            else:
                output += f'{ai_turn_color}{a:<20}{player_turn_color}{u:>20}{ENDC}\n'
        return output


def handle_game(game_id: str, bot_average: float, sets_to_win: int = 1, legs_to_win: int = 3, first_to_throw: str = 'player', starting_points: int = 501, bot_time: float = 0.8, bot_name: str = 'BOT', save_log_location: str = 'bullsai/game_logs/'):
    game = Game(sets_to_win=sets_to_win, legs_to_win=legs_to_win, bot_std=empirical_std.emperical_std(bot_average), starting_score=starting_points, bot_name=bot_name)
    leg_turn = first_to_throw
    leg_log = []

    def _save_game_log(game_log: dict) -> None:
        with open(f'{save_log_location}{game_id}.json', 'wt') as f:
            json.dump(game_log, f)

    def _print_averages_table(stats: dict) -> None:
        player_avg = round(stats['average']['PLAYER'], 2)
        bot_avg = round(stats['average'][bot_name],2)

        col_width = 15
        top_border = "+" + "-" * (col_width + 2) + "+" + "-" * (col_width + 2) + "+"
        header = "| {:^{}} | {:^{}} |".format("Player", col_width, "Average", col_width)
        divider = "+" + "-" * (col_width + 2) + "+" + "-" * (col_width + 2) + "+"
        human_row = "| {:<{}} | {:^{}} |".format("PLAYER", col_width, player_avg, col_width)
        ai_row = "| {:<{}} | {:^{}} |".format(f"{bot_name}", col_width, bot_avg, col_width)

        for row in [top_border, header, divider, human_row, divider, ai_row, divider]:
            print(row)

    # game loop
    while not game.is_game_over():
        leg = Leg(leg_turn, game, bot_time)
        
        # leg loop
        while not leg.is_leg_over():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(leg)
            leg.visit()
        
        leg_log.append(leg.log)
        game.new_leg_won(leg.get_winner())
        leg_turn = 'player' if leg_turn == 'bot' else 'bot'

    # game over
    os.system('cls' if os.name == 'nt' else 'clear')
    print(leg)
    print(game)

    game_log = {
            'id': game_id,
            'player_home': 'PLAYER' if first_to_throw == 'player' else bot_name,
            'player_away': bot_name if first_to_throw == 'player' else 'PLAYER',
            'legs_to_win': legs_to_win,
            'sets_to_win': sets_to_win,
            'winner': game.get_winner(),
            'log': leg_log
        }
    _save_game_log(game_log)
    _print_averages_table(stats.extract_stats(game_log))

    return game


if __name__ == '__main__':
    inputs=parse_args()
    handle_game(f'{datetime.now().strftime("%d%m%Y%H%M")}_{inputs.bot_average}', inputs.bot_average, inputs.sets_to_win, inputs.legs_to_win, inputs.first_to_throw, inputs.starting_points, inputs.bot_time)

# OTHER TODOS / IDEAS:
# - Player can also give his fields instead of a score
# - Show what fields players has to throw, if he can finish