#!/usr/bin/env python3
"""
CSV Preview Script - Check the format before processing
"""

import csv
from collections import defaultdict

def preview_csv(csv_path):
    """Preview the CSV data and show structure"""
    
    print(f"Reading CSV file: {csv_path}")
    print("=" * 50)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Show the headers
            print(f"Headers found: {reader.fieldnames}")
            print()
            
            # Read all data
            data = list(reader)
            print(f"Total rows: {len(data)}")
            print()
            
            # Group by team to show structure
            teams = defaultdict(list)
            managers_found = []
            
            # Handle different possible column names and BOM
            team_col = None
            player_col = None
            manager_col = None
            
            # Find the right column names (handle BOM and case variations)
            for col in reader.fieldnames:
                col_clean = col.replace('\ufeff', '').upper().strip()
                if col_clean == 'TEAM':
                    team_col = col
                elif col_clean in ['PLAYER', 'PLAYER_NAME']:
                    player_col = col
                elif col_clean in ['IS_MANAGER', 'MANAGER']:
                    manager_col = col
            
            print(f"Using columns: Team='{team_col}', Player='{player_col}', Manager='{manager_col}'")
            print()
            
            # Only process if we found the essential columns
            if team_col and player_col and manager_col:
                for row in data:
                    team = row.get(team_col, '').strip()
                    player = row.get(player_col, '').strip()
                    is_manager = row.get(manager_col, '').strip().lower()
                    
                    teams[team].append({
                        'player': player,
                        'is_manager': is_manager in ['yes', 'y', 'true', '1']
                    })
                    
                    if is_manager in ['yes', 'y', 'true', '1']:
                        managers_found.append(f"{team}: {player}")
            else:
                print("❌ Could not find required columns - skipping data processing")
            
            # Show team breakdown
            print("TEAMS AND PLAYERS:")
            print("-" * 30)
            for team, players in teams.items():
                print(f"\n{team} ({len(players)} players):")
                for i, player_info in enumerate(players, 1):
                    manager_flag = " (MANAGER)" if player_info['is_manager'] else ""
                    print(f"  {i:2d}. {player_info['player']}{manager_flag}")
            
            # Show managers summary
            print(f"\nMANAGERS FOUND ({len(managers_found)}):")
            print("-" * 30)
            if managers_found:
                for manager in managers_found:
                    print(f"  {manager}")
            else:
                print("  No managers found")
            
            # Show first few raw rows for verification
            print(f"\nFIRST 5 RAW ROWS:")
            print("-" * 30)
            for i, row in enumerate(data[:5]):
                print(f"  Row {i+1}: {dict(row)}")
            
            # Validation checks
            print(f"\nVALIDATION:")
            print("-" * 30)
            issues = []
            
            # Check if we found the required columns
            if not team_col:
                issues.append("Could not find TEAM column")
            if not player_col:
                issues.append("Could not find PLAYER column")
            if not manager_col:
                issues.append("Could not find IS_MANAGER column")
            
            # Check for empty teams (only if we found the team column)
            if team_col:
                empty_teams = [team for team in teams.keys() if not team]
                if empty_teams:
                    issues.append("Found rows with empty team names")
            
            # Check for empty player names (only if we found the player column)
            if player_col:
                empty_players = [row for row in data if not row.get(player_col, '').strip()]
                if empty_players:
                    issues.append(f"Found {len(empty_players)} rows with empty player names")
            
            # Check for duplicate players within teams
            for team, players in teams.items():
                player_names = [p['player'] for p in players]
                if len(player_names) != len(set(player_names)):
                    issues.append(f"Team '{team}' has duplicate player names")
            
            if issues:
                print("  ISSUES FOUND:")
                for issue in issues:
                    print(f"    ❌ {issue}")
            else:
                print("  ✅ CSV format looks good!")
                print(f"  ✅ Found {len(teams)} teams")
                print(f"  ✅ Found {len(data)} total players")
                print(f"  ✅ Found {len(managers_found)} managers")
                print(f"  ✅ Column mapping: Team='{team_col}', Player='{player_col}', Manager='{manager_col}'")
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find file '{csv_path}'")
        print("Make sure the file is in the same folder as this script.")
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        import traceback
        traceback.print_exc()

def main():
    csv_path = "draft_f25.csv"  # Change this if your file has a different name
    preview_csv(csv_path)

if __name__ == "__main__":
    main()