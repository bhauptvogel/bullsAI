import os
import time
import sys
from dataclasses import dataclass
from bullsai import dart
from bullsai import empirical_std

BLUE = '\033[95m'
OKBLUE = '\033[94m'
GREEN = '\033[32m'
ENDC = '\033[0m'
BOLD = '\033[1m'

@dataclass
class Game:

    # PLAYER 'player'
    # AI Bot 'bot'

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
            if winner == 'PLAYER':
                self.player_sets_won += 1
            elif winner == self.bot_name:
                self.bot_sets_won += 1

            self.player_legs_won = 0
            self.bot_legs_won = 0

        if winner == 'PLAYER':
            self.player_legs_won += 1
            if self.player_legs_won == self.legs_to_win:
                _new_set_won('PLAYER')
        elif winner == self.bot_name:
            self.bot_legs_won += 1
            if self.bot_legs_won == self.legs_to_win:
                _new_set_won(self.bot_name)
        else:
            raise ValueError(f'Invalid winner: {winner}')

    def is_game_over(self) -> bool:
        return self.player_sets_won == self.sets_to_win or self.bot_sets_won == self.sets_to_win
 
    def __repr__(self):
        output = ''

        if self.is_game_over():
            output += f'{BOLD}GAME OVER!{ENDC}\n'
            if self.player_sets_won == self.sets_to_win:
                output += f'{GREEN}PLAYER won!{ENDC}\n'
            elif self.bot_sets_won == self.sets_to_win:
                output += f'{GREEN}{self.bot_name} won!{ENDC}\n'
            else:
                raise ValueError('Game is over but no winner was found')

        return output

class Leg:

    log: list = []

    player_score: int
    bot_score: int

    turn: str # either 'bot' or 'player'
    first_to_throw: str
    game_information: Game

    def __init__(self, first_to_throw: str, game_information: Game) -> None:
        self.player_score = game_information.starting_score
        self.bot_score = game_information.starting_score
        self.first_to_throw = first_to_throw
        self.turn = first_to_throw
        self.game_information = game_information

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
        return score - points == 0 and score <= 170 and score not in [169, 168, 166, 165, 163, 162, 159]

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
            return input("Did you finish with a double? [Y/N]") in ['', 'yes', 'Yes', 'YES', 'y', 'Y']

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
            return dart.dart_throw_sim(dart.get_target_coordinates(dart.get_next_target_field(self.bot_score, remaining_darts)), self.game_information.bot_std)

        for dart_index in range(3):
            bot_coordinates = _sim_bot_throw(3 - dart_index)
            bot_points += dart.get_points_of_coordinates(bot_coordinates)
            fields_thrown.append(dart.get_field_of_coordinates(bot_coordinates))

            print(dart.get_field_of_coordinates(bot_coordinates), end=' ')
            sys.stdout.flush()
            time.sleep(0.8)

            if self.bot_score - bot_points <= 1:
                if self._is_checkout(self.bot_score, bot_points) and dart.was_double_hit(bot_coordinates):
                    darts_thrown = dart_index + 1
                    break
                else:
                    bot_points = 0

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
            return 'PLAYER'
        elif self.bot_score == 0:
            return self.game_information.bot_name
        else:
            raise ValueError('Leg is not over yet')

    def __repr__(self):
        output = ''

        if self.game_information:

            if self.game_information.sets_to_win == 1:
                output += f'{BOLD}GAME: First to {self.game_information.legs_to_win} legs{ENDC}\n'
                player_info = [f'{self.game_information.player_legs_won} legs']
                bot_info = [f'{self.game_information.bot_legs_won} legs']
            else:
                output += f'{BOLD}SET: First to {self.game_information.sets_to_win} sets{ENDC}\n'
                player_info = [f'{self.game_information.player_sets_won} sets', f'{self.game_information.player_legs_won} legs']
                bot_info = [f'{self.game_information.bot_sets_won} sets', f'{self.game_information.bot_legs_won} legs']

        last_darts_of_player = f'({self.log[-1]['points_scored']})' if self.log and self.log[-1]['player'] == 'PLAYER' else ''
        last_darts_of_bot = f'({self.log[-1]['fields']})' if self.log and self.log[-1]['player'] == self.game_information.bot_name else ''

        player_info.extend(['PLAYER', self.player_score, last_darts_of_player])
        bot_info.extend([self.game_information.bot_name, self.bot_score, last_darts_of_bot])

        # TODO: Fix coloring
        for i, (u, a) in enumerate(zip(player_info, bot_info)):
            player_turn_color = BLUE if self.turn == 'player' and i >= 2 else OKBLUE
            ai_turn_color = BLUE if self.turn != 'player' and i >= 2 else OKBLUE
            if self.first_to_throw == 'player':
                output += f'{player_turn_color}{u:<20}{ai_turn_color}{a:>20}{ENDC}\n' 
            else:
                output += f'{ai_turn_color}{a:<20}{player_turn_color}{u:>20}{ENDC}\n'
        return output


def handle_game():
    leg_turn = 'player'
    game = Game(sets_to_win=1, legs_to_win=1, bot_std=1.0, starting_score=501)
    game_log = []

    def _clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    # game loop
    while not game.is_game_over():
        leg = Leg(leg_turn, game)
        
        # leg loop
        while not leg.is_leg_over():
            _clear_console()
            print(leg)
            leg.visit()
        
        game_log.append(leg.log)
        game.new_leg_won(leg.get_winner())
        leg_turn = 'player' if leg_turn == 'bot' else 'bot'

    # TODO: Create game log json
    _clear_console()
    print(leg)
    print(game)


if __name__ == '__main__':
    handle_game()