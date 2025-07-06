import pandas as pd

# Load data
batting = pd.read_csv('data/BattingStats.csv')
games = pd.read_csv('data/GameStats.csv')

# Get Player 16 data
player_16 = batting[batting['PlayerNumber'] == 16]

print("Player 16 Analysis:")
print(f"Total batting records: {len(player_16)}")
print(f"Unique GameNumbers: {len(player_16['GameNumber'].unique())}")
print(f"Unique TeamNumbers: {len(player_16['TeamNumber'].unique())}")
print(f"Unique TeamNumber+GameNumber combinations: {len(player_16[['TeamNumber', 'GameNumber']].drop_duplicates())}")

print("\nSample Player 16 data:")
print(player_16[['TeamNumber', 'GameNumber', 'PA']].head(10))

print("\nAll TeamNumbers for Player 16:")
print(sorted(player_16['TeamNumber'].unique()))

print("\nAll GameNumbers for Player 16:")
print(sorted(player_16['GameNumber'].unique()))

# Check if there are any missing games in GameStats
player_games = player_16.merge(games[['TeamNumber', 'GameNumber', 'GameDate']], 
                              on=['TeamNumber', 'GameNumber'], how='left')

print(f"\nAfter joining with GameStats:")
print(f"Records with matching games: {len(player_games.dropna())}")
print(f"Records with missing games: {len(player_games[player_games['GameDate'].isna()])}")

# Count unique games after join
unique_games_after_join = len(player_games[['TeamNumber', 'GameNumber']].drop_duplicates())
print(f"Unique games after join: {unique_games_after_join}")

# Check what games are missing
missing_games = player_games[player_games['GameDate'].isna()][['TeamNumber', 'GameNumber']].drop_duplicates()
if len(missing_games) > 0:
    print(f"\nMissing games in GameStats ({len(missing_games)} total):")
    print(missing_games.head(10))
    if len(missing_games) > 10:
        print(f"... and {len(missing_games) - 10} more")

# Check if the issue is that some games have multiple records per player
print(f"\nChecking for multiple records per game:")
player_16_grouped = player_16.groupby(['TeamNumber', 'GameNumber']).size()
print(f"Games with multiple records: {len(player_16_grouped[player_16_grouped > 1])}")
print(f"Average records per game: {len(player_16) / len(player_16[['TeamNumber', 'GameNumber']].drop_duplicates()):.2f}")

# Show some examples of games with multiple records
multi_record_games = player_16_grouped[player_16_grouped > 1]
if len(multi_record_games) > 0:
    print(f"\nSample games with multiple records:")
    for (team, game), count in multi_record_games.head(5).items():
        print(f"Team {team}, Game {game}: {count} records")

# Export all unique TeamNumber+GameNumber+PA records for Player 16
player_16[['TeamNumber', 'GameNumber', 'PA']].drop_duplicates().to_csv('player16_batting_games.csv', index=False)
print('\nExported player16_batting_games.csv for manual inspection.') 