import pandas as pd

# Load data
batting_df = pd.read_csv('data/BattingStats.csv')
people_df = pd.read_csv('data/People.csv')

print("=== PLAYER DEBUG INFO ===")
print(f"Total players in People.csv: {len(people_df)}")
print(f"Unique players in BattingStats.csv: {len(batting_df['PlayerNumber'].unique())}")

# Check for substitute players
subs_players = []
for player_num in batting_df['PlayerNumber'].unique():
    player_info = people_df[people_df['PersonNumber'] == player_num]
    if len(player_info) > 0:
        name = f"{player_info.iloc[0]['FirstName']} {player_info.iloc[0]['LastName']}"
        if name.endswith('Subs'):
            subs_players.append(name)

print(f"Players with names ending in 'Subs': {len(subs_players)}")
if subs_players:
    print("Sample substitute players:")
    for name in subs_players[:5]:
        print(f"  - {name}")

# Check multiple teams
teams_to_check = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50]
print(f"\n=== TEAM DEBUG ===")
for team_num in teams_to_check:
    team_batting = batting_df[batting_df['TeamNumber'] == team_num]
    if len(team_batting) > 0:
        print(f"Team {team_num}: {len(team_batting)} records, {len(team_batting['PlayerNumber'].unique())} unique players")
        
        # Count non-subs players
        non_subs_count = 0
        non_subs_names = []
        for player_num in team_batting['PlayerNumber'].unique():
            player_info = people_df[people_df['PersonNumber'] == player_num]
            if len(player_info) > 0:
                name = f"{player_info.iloc[0]['FirstName']} {player_info.iloc[0]['LastName']}"
                if not name.endswith('Subs'):
                    non_subs_count += 1
                    non_subs_names.append(name)
        
        print(f"  Non-subs players: {non_subs_count}")
        if non_subs_names:
            print(f"  Sample players: {', '.join(non_subs_names[:3])}")
    else:
        print(f"Team {team_num}: No data") 