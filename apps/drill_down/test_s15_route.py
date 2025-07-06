import pandas as pd
from simple_csv_app import season_detail

# Test the S15 season (Filter 24)
print("=== TESTING S15 SEASON ROUTE ===")

# Simulate the route logic
batting_df = pd.read_csv('data/BattingStats.csv')
people_df = pd.read_csv('data/People.csv')
teams_df = pd.read_csv('data/Teams.csv')
game_df = pd.read_csv('data/GameStats.csv')
filters_df = pd.read_csv('data/Filters.csv')

filter_number = 24
season_info = filters_df[filters_df['FilterNumber'] == filter_number]
print(f"Season: {season_info.iloc[0]['FilterName']}")

# Create mapping from season codes to FilterNumbers
season_to_filter = {}
for _, row in filters_df.iterrows():
    filter_num = row['FilterNumber']
    season_name_full = row['FilterName']
    
    # Convert "Winter 2011" to "W11"
    parts = season_name_full.split()
    if len(parts) >= 2:
        season_type = parts[0]  # Winter, Summer, Fall
        year = parts[1]  # 2011, 2012, etc.
        
        # Convert to short codes
        type_code = {'Winter': 'W', 'Summer': 'S', 'Fall': 'F'}.get(season_type, '')
        year_code = year[-2:]  # Last 2 digits of year
        
        if type_code and year_code:
            season_code = f"{type_code}{year_code}"
            season_to_filter[season_code] = filter_num

# Find the season code for this filter number
target_season_code = None
for season_code, filter_num in season_to_filter.items():
    if filter_num == filter_number:
        target_season_code = season_code
        break

print(f"Target season code: {target_season_code}")

# Filter teams by season
teams_data = []

for _, team in teams_df.iterrows():
    team_num = team['TeamNumber']
    team_name = team['LongTeamName']
    
    # Check if this team belongs to the selected season
    if ' ' in team_name:
        team_season_code = team_name.split()[-1]
        if team_season_code != target_season_code:
            continue  # Skip teams from other seasons
    
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
        run_diff = runs_for - runs_against
        rpg = runs_for / games_played if games_played > 0 else 0
        rpg_allowed = runs_against / games_played if games_played > 0 else 0
        
        # Calculate team batting stats
        team_pa = team_batting['PA'].sum()
        team_hits = team_batting['H'].sum()
        team_hr = team_batting['HR'].sum()
        team_bb = team_batting['BB'].sum()
        team_sf = team_batting['SF'].sum() if 'SF' in team_batting.columns else 0
        team_sh = team_batting['SH'].sum() if 'SH' in team_batting.columns else 0
        
        # Calculate doubles and triples
        team_doubles = team_batting['D'].sum() if 'D' in team_batting.columns else 0
        team_triples = team_batting['T'].sum() if 'T' in team_batting.columns else 0
        
        # Calculate at-bats and total bases
        team_ab = team_pa - team_bb - team_sh - team_sf
        team_singles = team_hits - team_doubles - team_triples - team_hr
        team_tb = team_singles + 2*team_doubles + 3*team_triples + 4*team_hr
        
        # Calculate averages
        team_ba = team_hits / team_ab if team_ab > 0 else 0
        team_obp = (team_hits + team_bb) / team_pa if team_pa > 0 else 0
        team_slg = team_tb / team_ab if team_ab > 0 else 0
        
        teams_data.append({
            'team_number': int(team_num),
            'team_name': team_name,
            'wins': wins,
            'losses': losses,
            'games_played': games_played,
            'win_pct': win_pct,
            'runs_for': runs_for,
            'runs_against': runs_against,
            'run_diff': run_diff,
            'rpg': rpg,
            'rpg_allowed': rpg_allowed,
            'ba': team_ba,
            'obp': team_obp,
            'slg': team_slg,
            'hr': team_hr
        })

print(f"Teams found: {len(teams_data)}")

# Sort by winning percentage (descending), then by run differential as tiebreaker
teams_data.sort(key=lambda x: (x['win_pct'], x['run_diff']), reverse=True)

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

if divisions:
    print("Division teams:")
    for div_name, div_teams in divisions.items():
        print(f"  {div_name}: {len(div_teams)} teams")
        for team in div_teams[:3]:  # Show first 3 teams
            print(f"    - {team['team_name']}: {team['wins']}-{team['losses']}")
else:
    print("Single division - all teams:")
    for team in teams_data[:5]:  # Show first 5 teams
        print(f"  - {team['team_name']}: {team['wins']}-{team['losses']} (W%: {team['win_pct']:.3f})") 