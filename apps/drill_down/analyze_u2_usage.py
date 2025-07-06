import pandas as pd
import os

def analyze_u2_usage():
    """Analyze U2 column usage across all players"""
    
    # Load the data
    batting_file = os.path.join('data', 'BattingStats.csv')
    people_file = os.path.join('data', 'People.csv')
    
    print(f"Loading data from {batting_file}...")
    batting_df = pd.read_csv(batting_file)
    people_df = pd.read_csv(people_file)
    
    print(f"BattingStats.csv has {len(batting_df)} records")
    print(f"People.csv has {len(people_df)} records")
    
    # Find all records with non-zero U2
    non_zero_u2 = batting_df[batting_df['U2'] > 0]
    print(f"\nTotal records with non-zero U2: {len(non_zero_u2)}")
    print(f"Total U2 value across all records: {non_zero_u2['U2'].sum()}")
    
    # Get unique players affected
    affected_players = non_zero_u2['PlayerNumber'].unique()
    print(f"\nUnique players affected by U2: {len(affected_players)}")
    
    # Analyze each affected player
    print(f"\nDetailed analysis of affected players:")
    print("=" * 80)
    
    for player_num in affected_players:
        player_records = people_df[people_df['PersonNumber'] == player_num]
        if len(player_records) > 0:
            player_name = f"{player_records.iloc[0]['FirstName']} {player_records.iloc[0]['LastName']}"
        else:
            player_name = f"Unknown Player {player_num}"
        
        player_batting = batting_df[batting_df['PlayerNumber'] == player_num]
        player_u2_records = non_zero_u2[non_zero_u2['PlayerNumber'] == player_num]
        
        # Calculate games played both ways
        unique_games = len(player_batting.groupby(['TeamNumber', 'GameNumber']))
        total_u2 = player_batting['U2'].sum()
        games_with_u2 = unique_games + total_u2
        
        print(f"\n{player_name} (Player #{player_num}):")
        print(f"  Unique games: {unique_games}")
        print(f"  U2 sum: {total_u2}")
        print(f"  Total games (with U2): {games_with_u2}")
        print(f"  Records with U2: {len(player_u2_records)}")
        
        # Show the U2 records
        for _, record in player_u2_records.iterrows():
            print(f"    Team {record['TeamNumber']}, Game {record['GameNumber']}: U2={record['U2']}, PA={record['PA']}")
    
    # Analyze by team to see if certain teams/seasons are affected
    print(f"\n" + "=" * 80)
    print(f"Analysis by team:")
    
    team_u2_analysis = non_zero_u2.groupby('TeamNumber').agg({
        'U2': ['sum', 'count'],
        'PlayerNumber': 'nunique'
    }).round(0)
    team_u2_analysis.columns = ['Total_U2', 'Records_Count', 'Players_Count']
    team_u2_analysis = team_u2_analysis.sort_values('Total_U2', ascending=False)
    
    print(team_u2_analysis.head(20).to_string())
    
    # Check if there's a pattern with team numbers (older vs newer)
    print(f"\n" + "=" * 80)
    print(f"Team number analysis (potential age indicator):")
    
    team_numbers = sorted(non_zero_u2['TeamNumber'].unique())
    print(f"Teams with U2 usage: {team_numbers}")
    print(f"Lowest team number: {min(team_numbers)}")
    print(f"Highest team number: {max(team_numbers)}")
    
    # Check if U2 usage is concentrated in lower team numbers (older teams)
    low_teams = [t for t in team_numbers if t < 100]
    high_teams = [t for t in team_numbers if t >= 100]
    
    print(f"Teams < 100: {len(low_teams)} teams")
    print(f"Teams >= 100: {len(high_teams)} teams")
    
    # Show distribution
    print(f"\nU2 usage by team number ranges:")
    ranges = [(0, 50), (51, 100), (101, 150), (151, 200), (201, 250)]
    for start, end in ranges:
        teams_in_range = [t for t in team_numbers if start <= t <= end]
        if teams_in_range:
            total_u2_in_range = non_zero_u2[non_zero_u2['TeamNumber'].between(start, end)]['U2'].sum()
            print(f"  Teams {start}-{end}: {len(teams_in_range)} teams, {total_u2_in_range} total U2")
    
    return affected_players

if __name__ == "__main__":
    analyze_u2_usage() 