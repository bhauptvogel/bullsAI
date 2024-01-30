import pandas as pd

def create_schedules() -> None:
    players = pd.read_csv('fantasy/players.csv')

    for league in range(4):
        players_in_league = players[players['League'] == league+1]

        games = pd.DataFrame(columns=['Day', 'Home Player', 'Away Player', 'Result', 'Game Log'])

        num_days = (len(players_in_league) - 1) * 2 
        half_size = len(players_in_league) // 2

        # put names column of players_in_league into list
        players_list = players_in_league['Name'].tolist()

        for day in range(num_days):
            for i in range(half_size):
                if players_list[i] is not None and players_list[-i-1] is not None:
                    if day < len(players_list) - 1:  # First half of the schedule
                        games.loc[len(games)] = [day+1, players_list[i], players_list[-i-1], None, None]
                    else:  # Second half of the schedule
                        games.loc[len(games)] = [day+1, players_list[-i-1], players_list[i], None, None]

            # Rotate the list of players_list except the first one
            players_list = players_list[:1] + players_list[-1:] + players_list[1:-1]

        # save games to csv
        games.to_csv(f'fantasy/schedule_league_{league+1}.csv', index=False)

if __name__ == '__main__':
    create_schedules()