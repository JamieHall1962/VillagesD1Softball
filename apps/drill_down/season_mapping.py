import pandas as pd

# Load both datasets
filters_df = pd.read_csv('data/Filters.csv')
teams_df = pd.read_csv('data/Teams.csv')

print("=== SEASON MAPPING ANALYSIS ===")

# Create mapping from season codes to FilterNumbers
season_to_filter = {}
for _, row in filters_df.iterrows():
    filter_num = row['FilterNumber']
    season_name = row['FilterName']
    
    # Convert "Winter 2011" to "W11"
    parts = season_name.split()
    if len(parts) >= 2:
        season_type = parts[0]  # Winter, Summer, Fall
        year = parts[1]  # 2011, 2012, etc.
        
        # Convert to short codes
        type_code = {'Winter': 'W', 'Summer': 'S', 'Fall': 'F'}.get(season_type, '')
        year_code = year[-2:]  # Last 2 digits of year
        
        if type_code and year_code:
            season_code = f"{type_code}{year_code}"
            season_to_filter[season_code] = filter_num
            print(f"  {season_code} -> Filter {filter_num} ({season_name})")

print(f"\nTotal season mappings: {len(season_to_filter)}")

# Test the mapping with some team names
print("\n=== TESTING TEAM MAPPING ===")
test_teams = [
    "Mighty Ducks W11",  # Should map to Filter 1 (Winter 2011)
    "Avalanche S11",     # Should map to Filter 2 (Summer 2011)
    "Canucks F11",       # Should map to Filter 3 (Fall 2011)
    "Flames W25",        # Should map to Filter 57 (Winter 2025)
]

for team_name in test_teams:
    if ' ' in team_name:
        season_code = team_name.split()[-1]
        filter_num = season_to_filter.get(season_code, 'NOT FOUND')
        print(f"  {team_name} -> Season {season_code} -> Filter {filter_num}")

# Count teams per season
print("\n=== TEAMS PER SEASON ===")
season_counts = {}
for _, team in teams_df.iterrows():
    name = team['LongTeamName']
    if ' ' in name:
        season_code = name.split()[-1]
        if season_code in season_to_filter:
            season_counts[season_code] = season_counts.get(season_code, 0) + 1

sorted_seasons = sorted(season_counts.items(), key=lambda x: x[1], reverse=True)
for season_code, count in sorted_seasons[:10]:
    filter_num = season_to_filter.get(season_code, 'Unknown')
    print(f"  {season_code} (Filter {filter_num}): {count} teams") 