import pandas as pd

# Load teams data
teams_df = pd.read_csv('data/Teams.csv')

print("=== TEAM NAME ANALYSIS ===")
print(f"Total teams: {len(teams_df)}")
print("\nSample team names:")
print(teams_df['LongTeamName'].head(20))

# Check for season codes in team names
season_codes = ['W11', 'S11', 'F11', 'W12', 'S12', 'F12', 'W13', 'S13', 'F13', 
                'W14', 'S14', 'F14', 'W15', 'S15', 'F15', 'W16', 'S16', 'F16',
                'W17', 'S17', 'F17', 'W18', 'S18', 'F18', 'W19', 'S19', 'F19',
                'W20', 'S20', 'F20', 'W21', 'S21', 'F21', 'W22', 'S22', 'F22',
                'W23', 'S23', 'F23', 'W24', 'S24', 'F24', 'W25', 'S25', 'F25']

season_teams = []
for _, team in teams_df.iterrows():
    name = team['LongTeamName']
    if ' ' in name:
        last_part = name.split()[-1]
        if last_part in season_codes:
            season_teams.append((team['TeamNumber'], name, last_part))

print(f"\nTeams with season codes: {len(season_teams)}")
if season_teams:
    print("Sample teams with season codes:")
    for team_num, name, season in season_teams[:10]:
        print(f"  Team {team_num}: {name} (Season: {season})")

# Check what the most common suffixes are
suffixes = {}
for _, team in teams_df.iterrows():
    name = team['LongTeamName']
    if ' ' in name:
        suffix = name.split()[-1]
        suffixes[suffix] = suffixes.get(suffix, 0) + 1

print(f"\nMost common team name suffixes:")
sorted_suffixes = sorted(suffixes.items(), key=lambda x: x[1], reverse=True)
for suffix, count in sorted_suffixes[:15]:
    print(f"  {suffix}: {count} teams") 