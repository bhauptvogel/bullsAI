import argparse
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
from scipy.interpolate import make_interp_spline

def draw_graph(player_name: str, stat_id: str) -> None:
     # Check if player is in players.csv
    player_df = pd.read_csv('fantasy/players.csv')
    player = player_df[player_df['Name'] == player_name]
    if player.empty:
        raise ValueError('Player not found in players.csv')

    # Get all game ids player has played
    league = int(player['League'].values[0])
    schedule = pd.read_csv(f'fantasy/schedule_league_{league}.csv')
    player_games = schedule[(schedule['Home Player'] == player_name) | (schedule['Away Player'] == player_name)]
    played_games = player_games['Game Log'].dropna().values

    AVAILABLE_STATS = [{
        'id': 'avg',
        'name': 'Average Score',
        'function': get_avg_from_game
    },
    {
        'id': 'highest_visit',
        'name': 'Highest Visit',
        'function': get_highest_visit_from_game
    },
    {
        'id': 'first9',
        'name': 'First 9 Darts Average',
        'function': lambda leg_log: get_first_x_avg_from_game(leg_log, 9)
    },
    {
        'id': 'first12',
        'name': 'First 12 Darts Average',
        'function': lambda leg_log: get_first_x_avg_from_game(leg_log, 12)
    },   
    ]

    if stat_id not in [option['id'] for option in AVAILABLE_STATS]:
        raise ValueError('Invalid stat')

    stats = []
    wins = []

    for game in played_games:
        with open(f'fantasy/game_logs/{game}.json', 'r') as f:
            game_obj = json.load(f)
            wins.append(get_is_game_won(game_obj, player_name))
            leg_log = game_obj['log']

            stats.append(next(option['function'](leg_log) for option in AVAILABLE_STATS if option['id'] == stat_id))
            if stat_id not in [option['id'] for option in AVAILABLE_STATS]:
                raise ValueError('Invalid stat')
            
            
    # Generating the x-axis values (Week numbers)
    weeks = list(range(1, len(stats) + 1))

    MOVING_N = 5 if len(stats) > 12 else 4 if len(stats) > 9 else 3 if len(stats) > 5 else 0
    if MOVING_N > 0:
        moving_avg_stats = moving_average(stats, MOVING_N)
        x_new = np.linspace(min(weeks), max(weeks), 300)  # More points for a smoother line
        spl = make_interp_spline(weeks, moving_avg_stats, k=3)  # Using cubic spline interpolation
        smooth_moving_avg = spl(x_new)

    # Re-creating the plot with the smoothed moving average line
    plt.style.use('default')  # Resetting to default for manual adjustments
    fig, ax = plt.subplots(figsize=(10, 6))

    # Setting dark grey background
    fig.patch.set_facecolor('#2e2e2e')  # Dark grey background
    ax.set_facecolor('#2e2e2e')

    # Bright grey font for ticks, labels, and title
    ax.tick_params(axis='x', colors='#b8b8b8')
    ax.tick_params(axis='y', colors='#b8b8b8')
    ax.xaxis.label.set_color('#b8b8b8')
    ax.yaxis.label.set_color('#b8b8b8')
    ax.title.set_color('#b8b8b8')

    # Plotting original stats with dot markers
    for i, stat in enumerate(stats):
        color = 'green' if wins[i] else 'red'
        plt.scatter(weeks[i], stat, color=color, s=100, marker='o')
        plt.text(weeks[i], stat + 2, f'{stat:.2f}', color='#b8b8b8', ha='center')

    # Adding the smoothed moving average line
    if MOVING_N > 0:
        plt.plot(x_new, smooth_moving_avg, color='#808080', label=f'{MOVING_N}-Game Moving Avg', linewidth=2)

    # Adjusting plot details
    plt.title('Dart League Performance')
    plt.xlabel('Week')
    idx = [option['id'] for option in AVAILABLE_STATS].index(stat_id)
    plt.ylabel(AVAILABLE_STATS[idx]['name'])
    top = max(stats + list(smooth_moving_avg)) + 10 if MOVING_N > 0 else max(stats) + 10
    plt.ylim(bottom=0, top=top)
    plt.xticks(weeks)
    ax.grid(True, which='both', axis='x', color='gray', linestyle='-', linewidth=0.5)
    ax.grid(False, which='both', axis='y')

    # Customizing the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.show()

def moving_average(values, n=5):
    if n == 0: return values
    averages = []
    for i in range(len(values)):
        if i < n:  # If less than n games, calculate average up to that point
            averages.append(sum(values[:i+1]) / (i+1))
        else:  # For game n and beyond, calculate the moving average of the last n games
            averages.append(sum(values[i-n+1:i+1]) / n)
    return averages

def get_avg_from_game(leg_log: object) -> float:
    darts_thrown = 0
    points_scored = 0
    for leg in leg_log:
        for throw in leg:
            if throw['player'] == player_name:
                darts_thrown += throw['darts_thrown']
                points_scored += throw['points_scored']

    return points_scored / darts_thrown * 3

def get_first_x_avg_from_game(leg_log: object, x: int) -> float:
    darts_thrown = 0
    points_scored = 0
    for leg in leg_log:
        leg_darts = 0
        for throw in leg:
            if throw['player'] == player_name and leg_darts < x:
                darts_thrown += throw['darts_thrown']
                points_scored += throw['points_scored']
                leg_darts += throw['darts_thrown']

    return points_scored / darts_thrown * 3

def get_highest_visit_from_game(leg_log: object) -> int:
    highest_visit = 0
    for leg in leg_log:
        for throw in leg:
            if throw['player'] == player_name:
                if throw['points_scored'] > highest_visit:
                    highest_visit = throw['points_scored']
    return highest_visit

def get_is_game_won(game_obj: object, player_name: object) -> bool:
    return game_obj['winner'] == player_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Name of the player')
    parser.add_argument('--stat', type=str, help='Stat to display', default='avg')
    args = parser.parse_args()
    player_name = args.name
    draw_graph(player_name, args.stat)
