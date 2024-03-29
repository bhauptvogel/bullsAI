# import players.csv as pandas dataframe
import pandas as pd

players = pd.read_csv(f'fantasy/players.csv')

in_cup = players[players['League'].isin([1, 2])]

def get_player_average(name: str) -> float:
    return float(players[players['Name'] == name]['AVG'].values[0])

from bullsai import dart
from bullsai import empirical_std
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

################################################################
###################### BATTLE OF LEAGUE 3 ######################
################################################################

players_of_league_4 = players[players['League'] == 4]
players_of_league_3 = players[players['League'] == 3]

# Shuffle the DataFrame
players_of_league_3_shuffled = players_of_league_3.sample(frac=1).reset_index(drop=True)

# Create matchups
matchups = []
for i in range(0, len(players_of_league_3_shuffled) - 1, 2):
    player1 = players_of_league_3_shuffled.iloc[i]['Name']
    player2 = players_of_league_3_shuffled.iloc[i + 1]['Name']
    matchups.append((player1, player2))

# Print matchups
for i, matchup in enumerate(matchups, 1):
    

    player1 = matchup[0]
    player2 = matchup[1]

    player1_avg = get_player_average(player1)
    player2_avg = get_player_average(player2)

    player1_leg_wins = 0
    player2_leg_wins = 0
    LEGS_TO_WIN = 6

    player_beginning = 1

    while player1_leg_wins < LEGS_TO_WIN and player2_leg_wins < LEGS_TO_WIN:
        leg_winner = sim_leg(player1_avg, player2_avg, player_beginning, 501)
        if leg_winner == 1:
            player1_leg_wins += 1
        elif leg_winner == 2:
            player2_leg_wins += 1
        player_beginning = 1 if player_beginning == 2 else 2
    
    winner = player1 if player1_leg_wins > player2_leg_wins else player2
    loser = player1 if player1_leg_wins < player2_leg_wins else player2
    print(f'Match {i}: {player1} vs {player2} -> {player1_leg_wins}-{player2_leg_wins} -> {winner}')

    # add winner to in_cup
    in_cup = pd.concat([in_cup, players[players['Name'] == winner]])

    # add losers to players_of_league_4
    players_of_league_4 = pd.concat([players_of_league_4, players[players['Name'] == loser]])

################################################################
###################### BATTLE OF LEAGUE 4 ######################
################################################################


# Group into 3 random groups of the same amount of players (5)
groups = []
for i in range(3):
    group = players_of_league_4.sample(n=5)
    groups.append(group)
    players_of_league_4 = players_of_league_4.drop(group.index)


for group in groups:

    # add leg_wins to gruup as column
    group['Leg Wins'] = 0

    # get all combination of matchups
    from itertools import combinations
    matchups = list(combinations(group['Name'], 2))
    
    for matchup in matchups:
        player1_avg = get_player_average(matchup[0])
        player2_avg = get_player_average(matchup[1])

        for i in range(4):
            leg_winner = sim_leg(player1_avg, player2_avg, i%2+1, 501)
            if leg_winner == 1:
                group.loc[group['Name'] == matchup[0], 'Leg Wins'] += 1
            elif leg_winner == 2:
                group.loc[group['Name'] == matchup[1], 'Leg Wins'] += 1

    # sort by leg wins
    group = group.sort_values(by='Leg Wins', ascending=False)

    # get the 2 players with the most leg wins
    group_winner = group.iloc[0]['Name']

    # add them to in_cup
    in_cup = pd.concat([in_cup, players[players['Name'] == group_winner]])
    # in_cup = pd.concat([in_cup, players[players['Name'] == player2]])

###########################################################
###################### EVERYONE ELSE ######################
###########################################################


# get all players that are not in_cup
players_not_in_cup = players[~players['Name'].isin(in_cup['Name'])]
players_not_in_cup = players_not_in_cup.sort_values(by='AVG', ascending=False)


for player in players_not_in_cup['Name']:
    percentage_chance = (get_player_average(player) / 3) / 100
    
    import random
    # get true or false according to percentage_chance
    in_cup_bool = random.random() < percentage_chance
    
    if in_cup_bool and (len(in_cup) < 32):
        in_cup = pd.concat([in_cup, players[players['Name'] == player]])



######################################################
###################### FILL OUT ######################
######################################################
        


missing_players = 32 - len(in_cup)

from names import names
from random import choice
import numpy as np

def generate_new_player():

    county_probabilities = {
        'England': 20, 'Wales': 12, 'Scotland': 12, 'Ireland': 8, 'Spain': 2, 'France': 3,
        'Portugal': 2, 'Germany': 5, 'Netherlands': 4, 'Belgium': 1, 'Denmark': 2, 'Norway': 1,
        'Sweden': 1, 'Finland': 1, 'Iceland': 1, 'Italy': 1, 'USA': 3, 'Canada': 3, 'Australia': 4, 'New Zealand': 2,
        'China': 2, 'Japan': 2, 'South Korea': 2, 'Brazil': 2, 'Nigeria': 1, 'Colombia': 2, 'Argentina': 1,
        'Peru': 1, 'Chile': 1, 'Cuba': 1, 'Mexico': 2, 'Serbia': 1, 'Croatia': 1, 'Russia': 2, 'Ukraine': 1,
        'Turkey': 1, 'Israel': 1, 'India': 1, 'Austria': 2, 'Lithuania': 1, 'Greece': 1, 'South Africa': 1
    }

    sex_probabilities = {'Male': 9, 'Female': 1}

    # make choice with probabilities
    def weighted_choice(choices):
        total = sum(w for c, w in choices.items())
        r = np.random.uniform(0, total)
        upto = 0
        for c, w in choices.items():
            if upto + w >= r:
                return c
            upto += w
        assert False, "Shouldn't get here"

    country = weighted_choice(county_probabilities)

    sex = weighted_choice(sex_probabilities)

    first_name = choice(names[country][f'first_names_{sex.lower()}'])
    last_name = choice(names[country][f'last_names'])

    avg = np.random.normal(30, 3.5)
    # if avg < 25 -> new gaussian distribution with mean 26 and std 1
    avg = np.random.normal(27, 1) if avg < 25 else avg
    avg = np.random.normal(35, 1) if avg > 38 else avg

    return {
        'first_name': first_name,
        'last_name': last_name,
        'country': country,
        'sex': sex,
        'avg': avg
    }


for i in range(missing_players):
    new_player = generate_new_player()
    new_player = pd.DataFrame({'Name': [f'{new_player['first_name']} {new_player['last_name']}'], 'Country': [new_player['country']], 'Sex': [new_player['sex']], 'AVG': [round(new_player['avg'], 2)], 'League': [0]})
    in_cup = pd.concat([in_cup, new_player])


in_cup = in_cup.groupby('League').apply(lambda x: x.sample(frac=1, random_state=42)).reset_index(drop=True)
in_cup = in_cup.sort_values(by='League', key=lambda x: x.replace(0, x.max() + 1)).reset_index(drop=True)
print(in_cup[['Name', 'Sex', 'League']])

# write to file
in_cup.to_csv('fantasy/cup/cup_players.csv', index=False)