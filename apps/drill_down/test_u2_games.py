import pandas as pd
import os

def test_u2_games_theory():
    """Test if U2 column contains the missing games for lumped seasons"""
    
    # Load the data
    batting_file = os.path.join('data', 'BattingStats.csv')
    people_file = os.path.join('data', 'People.csv')
    
    print(f"Loading data from {batting_file}...")
    batting_df = pd.read_csv(batting_file)
    people_df = pd.read_csv(people_file)
    
    print(f"BattingStats.csv has {len(batting_df)} records")
    
    # Find Steve Held's player number
    held_records = people_df[
        (people_df['FirstName'].str.contains('Steve', case=False, na=False)) & 
        (people_df['LastName'].str.contains('Held', case=False, na=False))
    ]
    print(f"\nFound {len(held_records)} records for Steve Held in People.csv:")
    print(held_records[['PersonNumber', 'FirstName', 'LastName']].to_string())
    
    if len(held_records) == 0:
        print("No Steve Held found in People.csv")
        return
    
    held_player_number = held_records.iloc[0]['PersonNumber']
    print(f"\nSteve Held's player number: {held_player_number}")
    
    # Find batting records for Steve Held
    held_batting = batting_df[batting_df['PlayerNumber'] == held_player_number]
    print(f"\nFound {len(held_batting)} batting records for Steve Held")
    
    if len(held_batting) == 0:
        print("No batting records found for Steve Held")
        return
    
    # Check U2 column usage
    print(f"\nU2 column analysis:")
    print(f"Total records with non-zero U2: {len(held_batting[held_batting['U2'] > 0])}")
    print(f"Total U2 value: {held_batting['U2'].sum()}")
    
    # Show records with non-zero U2
    non_zero_u2 = held_batting[held_batting['U2'] > 0]
    if len(non_zero_u2) > 0:
        print(f"\nRecords with non-zero U2:")
        print(non_zero_u2[['TeamNumber', 'GameNumber', 'PA', 'U2']].to_string())
    
    # Calculate games played using different methods
    print(f"\nGames Played Calculations:")
    
    # Method 1: Count unique (TeamNumber, GameNumber) pairs
    unique_games = held_batting.groupby(['TeamNumber', 'GameNumber']).size().reset_index(name='appearances')
    games_from_unique = len(unique_games)
    print(f"Method 1 - Unique (TeamNumber, GameNumber): {games_from_unique}")
    
    # Method 2: Count unique games + sum of U2
    total_u2 = held_batting['U2'].sum()
    games_with_u2 = games_from_unique + total_u2
    print(f"Method 2 - Unique games + U2 sum: {games_from_unique} + {total_u2} = {games_with_u2}")
    
    # Method 3: Show breakdown by team
    print(f"\nBreakdown by team:")
    for team_num in unique_games['TeamNumber'].unique():
        team_games = unique_games[unique_games['TeamNumber'] == team_num]
        team_u2 = held_batting[held_batting['TeamNumber'] == team_num]['U2'].sum()
        print(f"  Team {team_num}: {len(team_games)} unique games + {team_u2} U2 = {len(team_games) + team_u2} total")
    
    # Check if this matches the expected 362 games
    expected_games = 362
    print(f"\nExpected games: {expected_games}")
    print(f"Calculated games (with U2): {games_with_u2}")
    print(f"Difference: {games_with_u2 - expected_games}")
    
    return games_with_u2

if __name__ == "__main__":
    test_u2_games_theory() 