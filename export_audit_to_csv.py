#!/usr/bin/env python3
"""
Export Audit Results to CSV for Excel Review
Creates separate CSV files for batting, pitching, and game discrepancies
"""

import sqlite3
import pandas as pd

# Import functions from audit script
from audit_f25_stats import (
    load_csv_batting, load_csv_pitching, load_csv_games,
    load_db_batting, load_db_pitching, load_db_games
)

def get_player_name(conn, player_num):
    """Get player name from database"""
    cursor = conn.cursor()
    cursor.execute("SELECT FirstName, LastName FROM People WHERE PersonNumber = ?", (player_num,))
    result = cursor.fetchone()
    if result:
        return f"{result[0]} {result[1]}"
    return f"Unknown"

def export_batting_discrepancies(csv_df, db_df, conn):
    """Export batting discrepancies to CSV"""
    print("\nExporting batting discrepancies...")
    
    # Create comparison keys
    csv_df['_key'] = csv_df['TeamNumber'].astype(str) + '|' + csv_df['GameNumber'].astype(str) + '|' + csv_df['PlayerNumber'].astype(str)
    db_df['_key'] = db_df['TeamNumber'].astype(str) + '|' + db_df['GameNumber'].astype(str) + '|' + db_df['PlayerNumber'].astype(str)
    
    csv_keys = set(csv_df['_key'])
    db_keys = set(db_df['_key'])
    
    # Records only in DB (need to delete)
    only_in_db = db_keys - csv_keys
    
    if len(only_in_db) > 0:
        extra_df = db_df[db_df['_key'].isin(only_in_db)].copy()
        extra_df = extra_df.sort_values(['TeamNumber', 'GameNumber', 'PlayerNumber'])
        
        # Add player names
        extra_df['PlayerName'] = extra_df['PlayerNumber'].apply(lambda x: get_player_name(conn, x))
        
        # Select and reorder columns
        output_cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'PlayerName', 
                      'HomeTeam', 'PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'G']
        available_cols = [col for col in output_cols if col in extra_df.columns]
        
        result_df = extra_df[available_cols]
        result_df.to_csv('audit_batting_to_delete.csv', index=False)
        print(f"  Created: audit_batting_to_delete.csv ({len(result_df)} records)")
        return result_df
    else:
        print("  No batting discrepancies found")
        return None

def export_pitching_discrepancies(csv_df, db_df, conn):
    """Export pitching discrepancies to CSV"""
    print("\nExporting pitching discrepancies...")
    
    if csv_df is None or len(csv_df) == 0:
        print("  No CSV pitching data")
        return None
    
    # Create comparison keys
    csv_df['_key'] = csv_df['TeamNumber'].astype(str) + '|' + csv_df['GameNumber'].astype(str) + '|' + csv_df['PlayerNumber'].astype(str)
    db_df['_key'] = db_df['TeamNumber'].astype(str) + '|' + db_df['GameNumber'].astype(str) + '|' + db_df['PlayerNumber'].astype(str)
    
    csv_keys = set(csv_df['_key'])
    db_keys = set(db_df['_key'])
    
    # Records only in DB (need to delete)
    only_in_db = db_keys - csv_keys
    
    if len(only_in_db) > 0:
        extra_df = db_df[db_df['_key'].isin(only_in_db)].copy()
        extra_df = extra_df.sort_values(['TeamNumber', 'GameNumber', 'PlayerNumber'])
        
        # Add player names
        extra_df['PlayerName'] = extra_df['PlayerNumber'].apply(lambda x: get_player_name(conn, x))
        
        # Select and reorder columns
        output_cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'PlayerName', 
                      'HomeTeam', 'IP', 'BB', 'W', 'L', 'IBB']
        available_cols = [col for col in output_cols if col in extra_df.columns]
        
        result_df = extra_df[available_cols]
        result_df.to_csv('audit_pitching_to_delete.csv', index=False)
        print(f"  Created: audit_pitching_to_delete.csv ({len(result_df)} records)")
        return result_df
    else:
        print("  No pitching discrepancies found")
        return None

def export_game_differences(csv_df, db_df):
    """Export game stat differences to CSV"""
    print("\nExporting game differences...")
    
    # Create comparison keys - convert to int first
    csv_df['_key'] = csv_df['TeamNumber'].astype(int).astype(str) + '|' + csv_df['GameNumber'].astype(int).astype(str)
    db_df['_key'] = db_df['TeamNumber'].astype(int).astype(str) + '|' + db_df['GameNumber'].astype(int).astype(str)
    
    csv_keys = set(csv_df['_key'])
    db_keys = set(db_df['_key'])
    in_both = csv_keys & db_keys
    
    # Check records in both for actual data differences (not just type differences)
    differences = []
    
    for key in in_both:
        csv_row = csv_df[csv_df['_key'] == key].iloc[0]
        db_row = db_df[db_df['_key'] == key].iloc[0]
        
        # Only check actual data columns (ignore type differences)
        team = csv_row['TeamNumber']
        game = csv_row['GameNumber']
        
        # Check if scores match (convert to int for comparison)
        csv_runs = int(csv_row['Runs'])
        db_runs = int(db_row['Runs'])
        csv_opp = int(csv_row['OppRuns'])
        db_opp = int(db_row['OppRuns'])
        
        if csv_runs != db_runs or csv_opp != db_opp:
            differences.append({
                'TeamNumber': team,
                'GameNumber': game,
                'Opponent': csv_row.get('Opponent', ''),
                'CSV_Runs': csv_runs,
                'DB_Runs': db_runs,
                'CSV_OppRuns': csv_opp,
                'DB_OppRuns': db_opp,
                'RunsDiff': csv_runs - db_runs,
                'OppRunsDiff': csv_opp - db_opp
            })
    
    if differences:
        result_df = pd.DataFrame(differences)
        result_df = result_df.sort_values(['TeamNumber', 'GameNumber'])
        result_df.to_csv('audit_game_differences.csv', index=False)
        print(f"  Created: audit_game_differences.csv ({len(result_df)} records)")
        return result_df
    else:
        print("  No actual game data differences found (only data type formatting)")
        return None

def main():
    """Main export function"""
    print("="*80)
    print("EXPORTING AUDIT RESULTS TO CSV")
    print("="*80)
    
    # Fall 2025 team numbers
    F25_TEAMS = [526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537]
    
    # Connect to database
    conn = sqlite3.connect("softball_stats.db")
    
    try:
        # Load CSV data
        print("\nLoading CSV data...")
        csv_batting = load_csv_batting()
        csv_pitching = load_csv_pitching()
        csv_games = load_csv_games()
        
        # Load DB data
        print("Loading database data...")
        db_batting = load_db_batting(conn)
        db_pitching = load_db_pitching(conn)
        db_games = load_db_games(conn)
        
        # Filter to F25 teams only
        print("Filtering to Fall 2025 teams...")
        db_batting = db_batting[db_batting['TeamNumber'].isin(F25_TEAMS)]
        db_pitching = db_pitching[db_pitching['TeamNumber'].isin(F25_TEAMS)]
        db_games = db_games[db_games['TeamNumber'].isin(F25_TEAMS)]
        
        # Export discrepancies
        batting_df = export_batting_discrepancies(csv_batting, db_batting, conn)
        pitching_df = export_pitching_discrepancies(csv_pitching, db_pitching, conn)
        game_df = export_game_differences(csv_games, db_games)
        
        print("\n" + "="*80)
        print("EXPORT COMPLETE")
        print("="*80)
        print("\nFiles created:")
        if batting_df is not None:
            print("  - audit_batting_to_delete.csv (records in DB but not in CSV)")
        if pitching_df is not None:
            print("  - audit_pitching_to_delete.csv (records in DB but not in CSV)")
        if game_df is not None:
            print("  - audit_game_differences.csv (score mismatches)")
        
        print("\nOpen these CSV files in Excel to review the discrepancies.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()

