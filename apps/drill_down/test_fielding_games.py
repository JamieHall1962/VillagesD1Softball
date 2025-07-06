import pandas as pd
import os

def count_games_from_fielding_stats(player_name="Steve Held"):
    """Count games played for a player using FieldingStats.csv"""
    
    # Load the data
    fielding_file = os.path.join('data', 'FieldingStats.csv')
    people_file = os.path.join('data', 'People.csv')
    
    print(f"Loading data from {fielding_file}...")
    fielding_df = pd.read_csv(fielding_file)
    people_df = pd.read_csv(people_file)
    
    print(f"FieldingStats.csv has {len(fielding_df)} records")
    print(f"People.csv has {len(people_df)} records")
    
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
    
    # Get all player numbers for Steve Held
    held_player_numbers = held_records['PersonNumber'].tolist()
    print(f"\nSteve Held's player numbers: {held_player_numbers}")
    
    # Find fielding records for Steve Held
    held_fielding = fielding_df[fielding_df['PlayerNumber'].isin(held_player_numbers)]
    print(f"\nFound {len(held_fielding)} fielding records for Steve Held")
    
    if len(held_fielding) == 0:
        print("No fielding records found for Steve Held")
        return
    
    # Count unique games (TeamNumber, GameNumber combinations)
    unique_games = held_fielding.groupby(['TeamNumber', 'GameNumber']).size().reset_index(name='appearances')
    total_games = len(unique_games)
    
    print(f"\nSteve Held played in {total_games} unique games according to FieldingStats.csv")
    print(f"Total fielding appearances: {len(held_fielding)}")
    
    # Show breakdown by team
    print("\nBreakdown by team:")
    for team_num in unique_games['TeamNumber'].unique():
        team_games = unique_games[unique_games['TeamNumber'] == team_num]
        print(f"  Team {team_num}: {len(team_games)} games")
    
    # Show first few games
    print(f"\nFirst 10 games:")
    print(unique_games.head(10).to_string())
    
    return total_games

if __name__ == "__main__":
    count_games_from_fielding_stats() 