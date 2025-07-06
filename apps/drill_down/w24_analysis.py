import pandas as pd

# Load data
teams_df = pd.read_csv('data/Teams.csv')
game_df = pd.read_csv('data/GameStats.csv')

print("=== W24 SEASON ANALYSIS ===")

# Find W24 teams
w24_teams = []
for _, team in teams_df.iterrows():
    name = team['LongTeamName']
    if name.endswith('W24'):
        w24_teams.append((team['TeamNumber'], name))

print(f"W24 teams found: {len(w24_teams)}")
for team_num, name in w24_teams:
    print(f"  Team {team_num}: {name}")

# Get game data for W24 teams
w24_team_numbers = [team_num for team_num, _ in w24_teams]
w24_games = game_df[game_df['TeamNumber'].isin(w24_team_numbers)]

print(f"\nW24 games found: {len(w24_games)}")

# Calculate standings
standings = {}
for team_num, team_name in w24_teams:
    team_games = w24_games[w24_games['TeamNumber'] == team_num]
    
    wins = 0
    losses = 0
    runs_for = 0
    runs_against = 0
    
    for _, game in team_games.iterrows():
        runs = game['Runs']
        opp_runs = game['OppRuns']
        
        runs_for += runs
        runs_against += opp_runs
        
        if runs > opp_runs:
            wins += 1
        else:
            losses += 1
    
    standings[team_num] = {
        'team_name': team_name,
        'wins': wins,
        'losses': losses,
        'runs_for': runs_for,
        'runs_against': runs_against,
        'games_played': wins + losses
    }

# Sort by wins (descending)
sorted_standings = sorted(standings.items(), key=lambda x: x[1]['wins'], reverse=True)

print("\n=== W24 STANDINGS ===")
print("Rank | Team | W | L | Runs For | Runs Against | Games")
print("-" * 60)
for rank, (team_num, stats) in enumerate(sorted_standings, 1):
    print(f"{rank:4d} | {stats['team_name']:20s} | {stats['wins']:1d} | {stats['losses']:1d} | {stats['runs_for']:8d} | {stats['runs_against']:12d} | {stats['games_played']:5d}")

# Check if we have batting stats for W24 teams
batting_df = pd.read_csv('data/BattingStats.csv')
w24_batting = batting_df[batting_df['TeamNumber'].isin(w24_team_numbers)]

print(f"\nW24 batting records: {len(w24_batting)}")
print(f"W24 players with batting stats: {len(w24_batting['PlayerNumber'].unique())}")

# Sample player stats for W24
if len(w24_batting) > 0:
    print("\nSample W24 player stats:")
    sample_player = w24_batting.iloc[0]
    print(f"  Team {sample_player['TeamNumber']}, Player {sample_player['PlayerNumber']}")
    print(f"  PA: {sample_player['PA']}, R: {sample_player['R']}, H: {sample_player['H']}, HR: {sample_player['HR']}, RBI: {sample_player['RBI']}") 