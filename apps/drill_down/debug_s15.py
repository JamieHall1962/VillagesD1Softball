import pandas as pd

# Load data
batting_df = pd.read_csv('data/BattingStats.csv')
teams_df = pd.read_csv('data/Teams.csv')
game_df = pd.read_csv('data/GameStats.csv')
filters_df = pd.read_csv('data/Filters.csv')

print("=== S15 DEBUG ===")

# Find S15 season
season_info = filters_df[filters_df['FilterNumber'] == 24]
print(f"Season info: {season_info.iloc[0]['FilterName']}")

# Find S15 teams
s15_teams = teams_df[teams_df['LongTeamName'].str.contains('S15', na=False)]
print(f"S15 teams found: {len(s15_teams)}")

teams_data = []
target_season_code = 'S15'

for _, team in s15_teams.iterrows():
    team_num = team['TeamNumber']
    team_name = team['LongTeamName']
    
    # Get team batting data
    team_batting = batting_df[batting_df['TeamNumber'] == team_num]
    
    # Get team game data for standings
    team_games = game_df[game_df['TeamNumber'] == team_num]
    
    # Calculate standings
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
    
    if len(team_batting) > 0:
        games_played = wins + losses
        win_pct = wins / games_played if games_played > 0 else 0
        
        teams_data.append({
            'team_number': int(team_num),
            'team_name': team_name,
            'wins': wins,
            'losses': losses,
            'games_played': games_played,
            'win_pct': win_pct,
            'runs_for': runs_for,
            'runs_against': runs_against
        })
        
        print(f"Team {team_num}: {team_name}")
        print(f"  Batting records: {len(team_batting)}")
        print(f"  Games: {len(team_games)}")
        print(f"  Record: {wins}-{losses}")
        print(f"  Runs: {runs_for} for, {runs_against} against")
        print()

print(f"Total teams with data: {len(teams_data)}")

# Check if this season has divisions
divisions = {}
for team in teams_data:
    team_name = team['team_name']
    # Look for division in parentheses: "Team Name (Division) Season"
    if '(' in team_name and ')' in team_name:
        # Extract division name from parentheses
        start = team_name.find('(')
        end = team_name.find(')')
        if start < end:
            division = team_name[start+1:end]
            # Skip D1/2 notation - this is not a division, just player composition info
            if division != 'D1/2':
                if division not in divisions:
                    divisions[division] = []
                divisions[division].append(team)

print(f"Divisions found: {list(divisions.keys()) if divisions else 'None'}")
print(f"Teams without divisions: {len([t for t in teams_data if t['team_name'] not in [team for div in divisions.values() for team in div]])}") 