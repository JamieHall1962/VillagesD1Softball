#!/usr/bin/env python3
"""
Fall 2025 Stats Audit
Compares data.csv from provider against database to identify discrepancies
"""

import sqlite3
import pandas as pd
from datetime import datetime
import sys

# Import extract_table and apply_subs_logic from data_update.py
def extract_table(csv_file, table_name):
    """Extract a specific table from the multi-table CSV"""
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    
    # Find table section
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"Table: {table_name}"):
            start_idx = i + 1
            break
    
    if start_idx is None:
        print(f"Table {table_name} not found")
        return None
    
    # Find end of section  
    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if lines[i].strip().startswith("Table: "):
            end_idx = i
            break
    
    # Write section to temp file
    temp_file = f"temp_{table_name.lower()}.csv"
    with open(temp_file, 'w') as f:
        f.writelines(lines[start_idx:end_idx])
    
    return temp_file

# HARDCODED SUB MAPPINGS FOR FALL 2025
SUBS_MAPPING = {
    529: 600,   # Bad News Bears Subs
    534: 493,   # Buckeyes Subs  
    527: 480,   # Clippers Subs
    532: 540,   # Lightning Strikes Subs
    537: 584,   # Norsemen Subs
    531: 542,   # Raptors Subs
    533: 302,   # Rebels Subs
    535: 548,   # Shorebirds Subs
    526: 274,   # Stars Subs
    536: 617,   # The Sandlot Subs
    528: 400,   # Warhawks Subs
    530: 554,   # Xtreme Subs
}

def apply_subs_logic(df):
    """Apply sub player redirections"""
    sub_count = 0
    if 'Roster' in df.columns:
        for i in range(len(df)):
            if df.iloc[i]['Roster'] == 'Sub':
                team_num = df.iloc[i]['TeamNumber']
                if team_num in SUBS_MAPPING:
                    old_player = df.iloc[i]['PersonNumber']
                    new_player = SUBS_MAPPING[team_num]
                    df.iloc[i, df.columns.get_loc('PersonNumber')] = new_player
                    sub_count += 1
    return df

def load_csv_batting():
    """Load and process batting stats from CSV"""
    temp_file = extract_table("data.csv", "BattingStats")
    if not temp_file:
        return None
    
    try:
        df = pd.read_csv(temp_file)
        
        # Apply sub logic
        df = apply_subs_logic(df)
        
        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber', 'D': '2B', 'T': '3B'})
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        # AGGREGATE: Group by team, game, player and sum the stats
        numeric_cols_to_sum = ['PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF']
        available_numeric_to_sum = [col for col in numeric_cols_to_sum if col in df_clean.columns]
        
        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric_to_sum}
        }).reset_index()
        
        return df_aggregated
    finally:
        import os
        os.remove(temp_file)

def load_csv_pitching():
    """Load and process pitching stats from CSV"""
    temp_file = extract_table("data.csv", "PitchingStats")
    if not temp_file:
        return None
    
    try:
        df = pd.read_csv(temp_file)
        
        # Apply sub logic
        df = apply_subs_logic(df)
        
        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber'})
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'IP', 'BB', 'W', 'L', 'IBB']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        if df_clean.empty:
            return None
        
        # AGGREGATE
        numeric_cols_to_sum = ['IP', 'BB', 'W', 'L', 'IBB']
        available_numeric_to_sum = [col for col in numeric_cols_to_sum if col in df_clean.columns]
        
        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric_to_sum}
        }).reset_index()
        
        return df_aggregated
    finally:
        import os
        os.remove(temp_file)

def load_csv_games():
    """Load and process game stats from CSV"""
    temp_file = extract_table("data.csv", "GameStats")
    if not temp_file:
        return None
    
    try:
        df = pd.read_csv(temp_file)
        
        # Map CSV columns to database columns
        column_mapping = {
            'GameDate': 'Date',
            'INN1': 'RunsInning1', 'INN2': 'RunsInning2', 'INN3': 'RunsInning3',
            'INN4': 'RunsInning4', 'INN5': 'RunsInning5', 'INN6': 'RunsInning6', 
            'INN7': 'RunsInning7', 'INN8': 'RunsInning8', 'INN9': 'RunsInning9'
        }
        df = df.rename(columns=column_mapping)
        
        # Keep only key columns for comparison
        base_cols = ['TeamNumber', 'GameNumber', 'Date', 'Innings', 'HomeTeam', 'Opponent', 'Runs', 'OppRuns']
        inning_cols = ['RunsInning1', 'RunsInning2', 'RunsInning3', 'RunsInning4', 'RunsInning5',
                      'RunsInning6', 'RunsInning7', 'RunsInning8', 'RunsInning9']
        
        all_possible_cols = base_cols + inning_cols
        available_cols = [col for col in all_possible_cols if col in df.columns]
        df_clean = df[available_cols]
        
        return df_clean
    finally:
        import os
        os.remove(temp_file)

def load_db_batting(conn):
    """Load batting stats from database (G=1 only)"""
    query = """
    SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, 
           PA, R, H, [2B], [3B], HR, OE, BB, RBI, SF, G
    FROM batting_stats
    WHERE G = 1
    """
    df = pd.read_sql_query(query, conn)
    df = df.rename(columns={'2B': '2B', '3B': '3B'})  # Ensure column names match
    return df

def load_db_pitching(conn):
    """Load pitching stats from database"""
    query = """
    SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, 
           IP, BB, W, L, IBB
    FROM pitching_stats
    """
    df = pd.read_sql_query(query, conn)
    return df

def load_db_games(conn):
    """Load game stats from database"""
    query = """
    SELECT TeamNumber, GameNumber, Date, Innings, HomeTeam, Opponent, Runs, OppRuns,
           RunsInning1, RunsInning2, RunsInning3, RunsInning4, RunsInning5,
           RunsInning6, RunsInning7, RunsInning8, RunsInning9
    FROM game_stats
    """
    df = pd.read_sql_query(query, conn)
    return df

def get_player_name(conn, player_number):
    """Get player name from database"""
    cursor = conn.cursor()
    cursor.execute("SELECT FirstName, LastName FROM People WHERE PersonNumber = ?", (player_number,))
    result = cursor.fetchone()
    if result:
        return f"{result[0]} {result[1]}"
    return f"Unknown (#{player_number})"

def compare_batting(csv_df, db_df, conn):
    """Compare batting stats"""
    print("\n" + "="*80)
    print("BATTING STATS AUDIT")
    print("="*80)
    
    # Create comparison keys
    csv_df['_key'] = csv_df['TeamNumber'].astype(str) + '|' + csv_df['GameNumber'].astype(str) + '|' + csv_df['PlayerNumber'].astype(str)
    db_df['_key'] = db_df['TeamNumber'].astype(str) + '|' + db_df['GameNumber'].astype(str) + '|' + db_df['PlayerNumber'].astype(str)
    
    csv_keys = set(csv_df['_key'])
    db_keys = set(db_df['_key'])
    
    # Find differences
    only_in_csv = csv_keys - db_keys
    only_in_db = db_keys - csv_keys
    in_both = csv_keys & db_keys
    
    print(f"\nSummary:")
    print(f"  Records in CSV: {len(csv_df)}")
    print(f"  Records in DB: {len(db_df)}")
    print(f"  Only in CSV (need to ADD to DB): {len(only_in_csv)}")
    print(f"  Only in DB (might need to DELETE): {len(only_in_db)}")
    print(f"  In both (checking for differences): {len(in_both)}")
    
    # Records only in CSV
    if len(only_in_csv) > 0:
        print(f"\n--- RECORDS TO ADD (in CSV but not in DB): {len(only_in_csv)} ---")
        missing_df = csv_df[csv_df['_key'].isin(only_in_csv)].sort_values(['TeamNumber', 'GameNumber', 'PlayerNumber'])
        for idx, row in missing_df.iterrows():
            player_name = get_player_name(conn, row['PlayerNumber'])
            print(f"  Team {row['TeamNumber']}, Game {row['GameNumber']}, Player {row['PlayerNumber']} ({player_name})")
            print(f"    Stats: PA={row.get('PA',0)}, H={row.get('H',0)}, HR={row.get('HR',0)}, RBI={row.get('RBI',0)}")
    
    # Records only in DB
    if len(only_in_db) > 0:
        print(f"\n--- RECORDS TO CONSIDER DELETING (in DB but not in CSV): {len(only_in_db)} ---")
        extra_df = db_df[db_df['_key'].isin(only_in_db)].sort_values(['TeamNumber', 'GameNumber', 'PlayerNumber'])
        for idx, row in extra_df.iterrows():
            player_name = get_player_name(conn, row['PlayerNumber'])
            print(f"  Team {row['TeamNumber']}, Game {row['GameNumber']}, Player {row['PlayerNumber']} ({player_name})")
            print(f"    Stats: PA={row.get('PA',0)}, H={row.get('H',0)}, HR={row.get('HR',0)}, RBI={row.get('RBI',0)}")
    
    # Check records in both for differences
    differences = []
    stat_cols = ['PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'HomeTeam']
    
    for key in in_both:
        csv_row = csv_df[csv_df['_key'] == key].iloc[0]
        db_row = db_df[db_df['_key'] == key].iloc[0]
        
        diffs = {}
        for col in stat_cols:
            if col in csv_row and col in db_row:
                csv_val = csv_row[col]
                db_val = db_row[col]
                # Handle NaN comparisons
                if pd.isna(csv_val) and pd.isna(db_val):
                    continue
                if csv_val != db_val:
                    diffs[col] = {'csv': csv_val, 'db': db_val}
        
        if diffs:
            differences.append({
                'key': key,
                'TeamNumber': csv_row['TeamNumber'],
                'GameNumber': csv_row['GameNumber'],
                'PlayerNumber': csv_row['PlayerNumber'],
                'diffs': diffs
            })
    
    if differences:
        print(f"\n--- RECORDS WITH DIFFERENCES: {len(differences)} ---")
        for diff in differences:
            player_name = get_player_name(conn, diff['PlayerNumber'])
            print(f"\n  Team {diff['TeamNumber']}, Game {diff['GameNumber']}, Player {diff['PlayerNumber']} ({player_name})")
            for col, vals in diff['diffs'].items():
                print(f"    {col}: CSV={vals['csv']} vs DB={vals['db']}")
    else:
        print(f"\n[OK] No differences found in matching records")

def compare_pitching(csv_df, db_df, conn):
    """Compare pitching stats"""
    print("\n" + "="*80)
    print("PITCHING STATS AUDIT")
    print("="*80)
    
    if csv_df is None or len(csv_df) == 0:
        print("\nNo pitching stats in CSV")
        return
    
    # Create comparison keys
    csv_df['_key'] = csv_df['TeamNumber'].astype(str) + '|' + csv_df['GameNumber'].astype(str) + '|' + csv_df['PlayerNumber'].astype(str)
    db_df['_key'] = db_df['TeamNumber'].astype(str) + '|' + db_df['GameNumber'].astype(str) + '|' + db_df['PlayerNumber'].astype(str)
    
    csv_keys = set(csv_df['_key'])
    db_keys = set(db_df['_key'])
    
    # Find differences
    only_in_csv = csv_keys - db_keys
    only_in_db = db_keys - csv_keys
    in_both = csv_keys & db_keys
    
    print(f"\nSummary:")
    print(f"  Records in CSV: {len(csv_df)}")
    print(f"  Records in DB: {len(db_df)}")
    print(f"  Only in CSV (need to ADD to DB): {len(only_in_csv)}")
    print(f"  Only in DB (might need to DELETE): {len(only_in_db)}")
    print(f"  In both (checking for differences): {len(in_both)}")
    
    # Records only in CSV
    if len(only_in_csv) > 0:
        print(f"\n--- RECORDS TO ADD (in CSV but not in DB): {len(only_in_csv)} ---")
        missing_df = csv_df[csv_df['_key'].isin(only_in_csv)].sort_values(['TeamNumber', 'GameNumber', 'PlayerNumber'])
        for idx, row in missing_df.iterrows():
            player_name = get_player_name(conn, row['PlayerNumber'])
            print(f"  Team {row['TeamNumber']}, Game {row['GameNumber']}, Player {row['PlayerNumber']} ({player_name})")
            print(f"    Stats: IP={row.get('IP',0)}, W={row.get('W',0)}, L={row.get('L',0)}, BB={row.get('BB',0)}")
    
    # Records only in DB
    if len(only_in_db) > 0:
        print(f"\n--- RECORDS TO CONSIDER DELETING (in DB but not in CSV): {len(only_in_db)} ---")
        extra_df = db_df[db_df['_key'].isin(only_in_db)].sort_values(['TeamNumber', 'GameNumber', 'PlayerNumber'])
        for idx, row in extra_df.iterrows():
            player_name = get_player_name(conn, row['PlayerNumber'])
            print(f"  Team {row['TeamNumber']}, Game {row['GameNumber']}, Player {row['PlayerNumber']} ({player_name})")
            print(f"    Stats: IP={row.get('IP',0)}, W={row.get('W',0)}, L={row.get('L',0)}, BB={row.get('BB',0)}")
    
    # Check records in both for differences
    differences = []
    stat_cols = ['IP', 'BB', 'W', 'L', 'IBB', 'HomeTeam']
    
    for key in in_both:
        csv_row = csv_df[csv_df['_key'] == key].iloc[0]
        db_row = db_df[db_df['_key'] == key].iloc[0]
        
        diffs = {}
        for col in stat_cols:
            if col in csv_row and col in db_row:
                csv_val = csv_row[col]
                db_val = db_row[col]
                if pd.isna(csv_val) and pd.isna(db_val):
                    continue
                if csv_val != db_val:
                    diffs[col] = {'csv': csv_val, 'db': db_val}
        
        if diffs:
            differences.append({
                'key': key,
                'TeamNumber': csv_row['TeamNumber'],
                'GameNumber': csv_row['GameNumber'],
                'PlayerNumber': csv_row['PlayerNumber'],
                'diffs': diffs
            })
    
    if differences:
        print(f"\n--- RECORDS WITH DIFFERENCES: {len(differences)} ---")
        for diff in differences:
            player_name = get_player_name(conn, diff['PlayerNumber'])
            print(f"\n  Team {diff['TeamNumber']}, Game {diff['GameNumber']}, Player {diff['PlayerNumber']} ({player_name})")
            for col, vals in diff['diffs'].items():
                print(f"    {col}: CSV={vals['csv']} vs DB={vals['db']}")
    else:
        print(f"\n[OK] No differences found in matching records")

def compare_games(csv_df, db_df):
    """Compare game stats"""
    print("\n" + "="*80)
    print("GAME STATS AUDIT")
    print("="*80)
    
    # Create comparison keys - convert to int first to handle float/int mismatch
    csv_df['_key'] = csv_df['TeamNumber'].astype(int).astype(str) + '|' + csv_df['GameNumber'].astype(int).astype(str)
    db_df['_key'] = db_df['TeamNumber'].astype(int).astype(str) + '|' + db_df['GameNumber'].astype(int).astype(str)
    
    csv_keys = set(csv_df['_key'])
    db_keys = set(db_df['_key'])
    
    # Find differences
    only_in_csv = csv_keys - db_keys
    only_in_db = db_keys - csv_keys
    in_both = csv_keys & db_keys
    
    print(f"\nSummary:")
    print(f"  Records in CSV: {len(csv_df)}")
    print(f"  Records in DB: {len(db_df)}")
    print(f"  Only in CSV (need to ADD to DB): {len(only_in_csv)}")
    print(f"  Only in DB (might need to DELETE): {len(only_in_db)}")
    print(f"  In both (checking for differences): {len(in_both)}")
    
    # Records only in CSV
    if len(only_in_csv) > 0:
        print(f"\n--- RECORDS TO ADD (in CSV but not in DB): {len(only_in_csv)} ---")
        missing_df = csv_df[csv_df['_key'].isin(only_in_csv)].sort_values(['TeamNumber', 'GameNumber'])
        for idx, row in missing_df.iterrows():
            print(f"  Team {row['TeamNumber']}, Game {row['GameNumber']}")
            print(f"    Opponent: {row.get('Opponent','?')}, Score: {row.get('Runs','?')}-{row.get('OppRuns','?')}")
    
    # Records only in DB
    if len(only_in_db) > 0:
        print(f"\n--- RECORDS TO CONSIDER DELETING (in DB but not in CSV): {len(only_in_db)} ---")
        extra_df = db_df[db_df['_key'].isin(only_in_db)].sort_values(['TeamNumber', 'GameNumber'])
        for idx, row in extra_df.iterrows():
            print(f"  Team {row['TeamNumber']}, Game {row['GameNumber']}")
            print(f"    Opponent: {row.get('Opponent','?')}, Score: {row.get('Runs','?')}-{row.get('OppRuns','?')}")
    
    # Check records in both for differences
    differences = []
    stat_cols = ['Date', 'Innings', 'HomeTeam', 'Opponent', 'Runs', 'OppRuns',
                 'RunsInning1', 'RunsInning2', 'RunsInning3', 'RunsInning4', 'RunsInning5',
                 'RunsInning6', 'RunsInning7', 'RunsInning8', 'RunsInning9']
    
    for key in in_both:
        csv_row = csv_df[csv_df['_key'] == key].iloc[0]
        db_row = db_df[db_df['_key'] == key].iloc[0]
        
        diffs = {}
        for col in stat_cols:
            if col in csv_row and col in db_row:
                csv_val = csv_row[col]
                db_val = db_row[col]
                if pd.isna(csv_val) and pd.isna(db_val):
                    continue
                # Convert to string for comparison (handles date formats)
                if str(csv_val) != str(db_val):
                    diffs[col] = {'csv': csv_val, 'db': db_val}
        
        if diffs:
            differences.append({
                'key': key,
                'TeamNumber': csv_row['TeamNumber'],
                'GameNumber': csv_row['GameNumber'],
                'diffs': diffs
            })
    
    if differences:
        print(f"\n--- RECORDS WITH DIFFERENCES: {len(differences)} ---")
        for diff in differences:
            print(f"\n  Team {diff['TeamNumber']}, Game {diff['GameNumber']}")
            for col, vals in diff['diffs'].items():
                print(f"    {col}: CSV={vals['csv']} vs DB={vals['db']}")
    else:
        print(f"\n[OK] No differences found in matching records")

def main():
    """Main audit function"""
    print("="*80)
    print("FALL 2025 STATS AUDIT")
    print("Comparing data.csv vs softball_stats.db")
    print("="*80)
    
    # Fall 2025 team numbers (based on SUBS_MAPPING)
    F25_TEAMS = [526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537]
    
    # Connect to database
    conn = sqlite3.connect("softball_stats.db")
    
    try:
        # Load CSV data
        print("\nLoading CSV data...")
        try:
            csv_batting = load_csv_batting()
        except Exception as e:
            print(f"  ERROR loading batting CSV: {e}")
            csv_batting = None
        
        try:
            csv_pitching = load_csv_pitching()
        except Exception as e:
            print(f"  ERROR loading pitching CSV: {e}")
            csv_pitching = None
        
        try:
            csv_games = load_csv_games()
        except Exception as e:
            print(f"  ERROR loading games CSV: {e}")
            csv_games = None
        
        print(f"  CSV Batting: {len(csv_batting) if csv_batting is not None else 0} records")
        print(f"  CSV Pitching: {len(csv_pitching) if csv_pitching is not None else 0} records")
        print(f"  CSV Games: {len(csv_games) if csv_games is not None else 0} records")
        
        # Load DB data
        print("\nLoading database data (G=1 only for batting)...")
        db_batting = load_db_batting(conn)
        db_pitching = load_db_pitching(conn)
        db_games = load_db_games(conn)
        
        # Filter to F25 teams only
        print(f"\nFiltering to Fall 2025 teams only ({F25_TEAMS})...")
        db_batting = db_batting[db_batting['TeamNumber'].isin(F25_TEAMS)]
        db_pitching = db_pitching[db_pitching['TeamNumber'].isin(F25_TEAMS)]
        db_games = db_games[db_games['TeamNumber'].isin(F25_TEAMS)]
        
        print(f"  DB Batting (F25 only): {len(db_batting)} records")
        print(f"  DB Pitching (F25 only): {len(db_pitching)} records")
        print(f"  DB Games (F25 only): {len(db_games)} records")
        
        # Run comparisons
        if csv_batting is not None:
            compare_batting(csv_batting, db_batting, conn)
        
        if csv_pitching is not None:
            compare_pitching(csv_pitching, db_pitching, conn)
        
        if csv_games is not None:
            compare_games(csv_games, db_games)
        
        print("\n" + "="*80)
        print("AUDIT COMPLETE")
        print("="*80)
        print("\nNext Steps:")
        print("1. Review all differences above")
        print("2. Decide which source is correct for each discrepancy")
        print("3. Prepare list of corrections needed")
        print("4. Run correction script (to be created)")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()

