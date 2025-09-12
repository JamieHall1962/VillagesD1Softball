#!/usr/bin/env python3
"""
Complete Softball Stats Sync - All Tables + Sub Logic + Aggregation
"""

import sqlite3
import pandas as pd
from datetime import datetime
import shutil

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

def extract_table(csv_file, table_name):
    """Extract a specific table from the multi-table CSV"""
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    
    # Find table section
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip() == f"Table: {table_name}":
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
                    print(f"  Team {team_num}: Player {old_player} → Subs Player {new_player}")
                    sub_count += 1
    if sub_count > 0:
        print(f"Redirected {sub_count} sub records")
    return df

def sync_batting_stats(conn):
    """Sync batting stats with proper sub aggregation"""
    print("\n--- SYNCING BATTING STATS ---")
    
    temp_file = extract_table("data.csv", "BattingStats")
    if not temp_file:
        return 0, 0, 0
    
    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} batting records")
        
        # Apply sub logic BEFORE aggregation
        df = apply_subs_logic(df)
        
        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber', 'D': '2B', 'T': '3B'})
        df['G'] = 1
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'G']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        print(f"Before aggregation: {len(df_clean)} records")
        
        # CRITICAL: AGGREGATE SUB STATS - Group by key fields and sum numeric stats
        numeric_cols = ['PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'G']
        available_numeric = [col for col in numeric_cols if col in df_clean.columns]
        
        # Group by team, game, player and sum the stats
        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',  # Take first HomeTeam value
            **{col: 'sum' for col in available_numeric}
        }).reset_index()
        
        print(f"After aggregation: {len(df_aggregated)} unique player/game records")
        
        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_batting")
        df_aggregated.to_sql("temp_staging_batting", conn, index=False)
        
        # Count changes
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_batting s
        LEFT JOIN batting_stats b ON s.TeamNumber = b.TeamNumber 
                                 AND s.GameNumber = b.GameNumber 
                                 AND s.PlayerNumber = b.PlayerNumber
        WHERE b.TeamNumber IS NULL
        """)
        new_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_batting s
        JOIN batting_stats b ON s.TeamNumber = b.TeamNumber 
                            AND s.GameNumber = b.GameNumber 
                            AND s.PlayerNumber = b.PlayerNumber
        WHERE s.HomeTeam != b.HomeTeam OR s.PA != b.PA OR s.R != b.R OR s.H != b.H 
           OR s.[2B] != b.[2B] OR s.[3B] != b.[3B] OR s.HR != b.HR OR s.OE != b.OE 
           OR s.BB != b.BB OR s.RBI != b.RBI OR s.SF != b.SF OR s.G != b.G
        """)
        changed_count = cursor.fetchone()[0]
        
        # Execute changes
        if new_count > 0:
            cursor.execute("""
            INSERT INTO batting_stats (TeamNumber, GameNumber, PlayerNumber, HomeTeam, PA, R, H, [2B], [3B], HR, OE, BB, RBI, SF, G)
            SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, PA, R, H, [2B], [3B], HR, OE, BB, RBI, SF, G
            FROM temp_staging_batting s
            WHERE NOT EXISTS (
                SELECT 1 FROM batting_stats b 
                WHERE s.TeamNumber = b.TeamNumber 
                AND s.GameNumber = b.GameNumber 
                AND s.PlayerNumber = b.PlayerNumber
            )
            """)
        
        if changed_count > 0:
            cursor.execute("""
            UPDATE batting_stats 
            SET HomeTeam = s.HomeTeam, PA = s.PA, R = s.R, H = s.H, [2B] = s.[2B], [3B] = s.[3B],
                HR = s.HR, OE = s.OE, BB = s.BB, RBI = s.RBI, SF = s.SF, G = s.G
            FROM temp_staging_batting s
            WHERE batting_stats.TeamNumber = s.TeamNumber 
            AND batting_stats.GameNumber = s.GameNumber 
            AND batting_stats.PlayerNumber = s.PlayerNumber
            """)
        
        cursor.execute("DROP TABLE temp_staging_batting")
        unchanged_count = len(df_aggregated) - new_count - changed_count
        
        print(f"Batting: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count
        
    finally:
        import os
        os.remove(temp_file)

def sync_pitching_stats(conn):
    """Sync pitching stats with sub aggregation"""
    print("\n--- SYNCING PITCHING STATS ---")
    
    temp_file = extract_table("data.csv", "PitchingStats")
    if not temp_file:
        return 0, 0, 0
    
    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} pitching records")
        
        # Apply sub logic
        df = apply_subs_logic(df)
        
        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber'})
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'IP', 'BB', 'W', 'L', 'IBB']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        if df_clean.empty:
            print("No valid pitching data found")
            return 0, 0, 0
        
        # AGGREGATE PITCHING STATS
        numeric_cols = ['IP', 'BB', 'W', 'L', 'IBB']
        available_numeric = [col for col in numeric_cols if col in df_clean.columns]
        
        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric}
        }).reset_index()
        
        print(f"Pitching aggregated from {len(df_clean)} to {len(df_aggregated)} records")
        
        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_pitching")
        df_aggregated.to_sql("temp_staging_pitching", conn, index=False)
        
        # Count changes
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_pitching s
        LEFT JOIN pitching_stats p ON s.TeamNumber = p.TeamNumber 
                                   AND s.GameNumber = p.GameNumber 
                                   AND s.PlayerNumber = p.PlayerNumber
        WHERE p.TeamNumber IS NULL
        """)
        new_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_pitching s
        JOIN pitching_stats p ON s.TeamNumber = p.TeamNumber 
                             AND s.GameNumber = p.GameNumber 
                             AND s.PlayerNumber = p.PlayerNumber
        WHERE s.IP != p.IP OR s.BB != p.BB OR s.W != p.W OR s.L != p.L
        """)
        changed_count = cursor.fetchone()[0]
        
        # Execute changes
        if new_count > 0:
            cursor.execute("""
            INSERT INTO pitching_stats (TeamNumber, GameNumber, PlayerNumber, HomeTeam, IP, BB, W, L, IBB)
            SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, IP, BB, W, L, IBB
            FROM temp_staging_pitching s
            WHERE NOT EXISTS (
                SELECT 1 FROM pitching_stats p 
                WHERE s.TeamNumber = p.TeamNumber 
                AND s.GameNumber = p.GameNumber 
                AND s.PlayerNumber = p.PlayerNumber
            )
            """)
        
        if changed_count > 0:
            cursor.execute("""
            UPDATE pitching_stats 
            SET HomeTeam = s.HomeTeam, IP = s.IP, BB = s.BB, W = s.W, L = s.L, IBB = s.IBB
            FROM temp_staging_pitching s
            WHERE pitching_stats.TeamNumber = s.TeamNumber 
            AND pitching_stats.GameNumber = s.GameNumber 
            AND pitching_stats.PlayerNumber = s.PlayerNumber
            """)
        
        cursor.execute("DROP TABLE temp_staging_pitching")
        unchanged_count = len(df_aggregated) - new_count - changed_count
        
        print(f"Pitching: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count
        
    finally:
        import os
        os.remove(temp_file)

def sync_game_stats(conn):
    """Sync game stats"""
    print("\n--- SYNCING GAME STATS ---")
    
    temp_file = extract_table("data.csv", "GameStats")
    if not temp_file:
        return 0, 0, 0
    
    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} game records")
        
        # Map CSV columns to database columns
        column_mapping = {
            'GameDate': 'Date',
            'INN1': 'RunsInning1', 'INN2': 'RunsInning2', 'INN3': 'RunsInning3',
            'INN4': 'RunsInning4', 'INN5': 'RunsInning5', 'INN6': 'RunsInning6', 
            'INN7': 'RunsInning7', 'INN8': 'RunsInning8', 'INN9': 'RunsInning9'
        }
        df = df.rename(columns=column_mapping)
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'Date', 'Innings', 'HomeTeam', 'Opponent', 'Runs', 'OppRuns',
                'RunsInning1', 'RunsInning2', 'RunsInning3', 'RunsInning4', 'RunsInning5',
                'RunsInning6', 'RunsInning7', 'RunsInning8', 'RunsInning9']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        if df_clean.empty:
            print("No valid game data found")
            return 0, 0, 0
        
        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_game")
        df_clean.to_sql("temp_staging_game", conn, index=False)
        
        # Count changes
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_game s
        LEFT JOIN game_stats g ON s.TeamNumber = g.TeamNumber 
                              AND s.GameNumber = g.GameNumber
        WHERE g.TeamNumber IS NULL
        """)
        new_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_game s
        JOIN game_stats g ON s.TeamNumber = g.TeamNumber 
                         AND s.GameNumber = g.GameNumber
        WHERE s.Runs != g.Runs OR s.OppRuns != g.OppRuns OR s.Innings != g.Innings
        """)
        changed_count = cursor.fetchone()[0]
        
        # Execute changes
        if new_count > 0:
            col_list = ', '.join(available_cols)
            cursor.execute(f"""
            INSERT INTO game_stats ({col_list})
            SELECT {col_list}
            FROM temp_staging_game s
            WHERE NOT EXISTS (
                SELECT 1 FROM game_stats g 
                WHERE s.TeamNumber = g.TeamNumber 
                AND s.GameNumber = g.GameNumber
            )
            """)
        
        if changed_count > 0:
            set_clauses = [f"{col} = s.{col}" for col in available_cols if col not in ['TeamNumber', 'GameNumber']]
            cursor.execute(f"""
            UPDATE game_stats 
            SET {', '.join(set_clauses)}
            FROM temp_staging_game s
            WHERE game_stats.TeamNumber = s.TeamNumber 
            AND game_stats.GameNumber = s.GameNumber
            """)
        
        cursor.execute("DROP TABLE temp_staging_game")
        unchanged_count = len(df_clean) - new_count - changed_count
        
        print(f"Game Stats: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count
        
    finally:
        import os
        os.remove(temp_file)

def main():
    print("COMPLETE SOFTBALL STATS SYNC")
    print("=" * 50)
    
    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"softball_stats.db.backup_{timestamp}"
    shutil.copy2("softball_stats.db", backup_path)
    print(f"Backup created: {backup_path}")
    
    # Connect to database
    conn = sqlite3.connect("softball_stats.db")
    
    try:
        # Sync all tables
        bat_new, bat_changed, bat_unchanged = sync_batting_stats(conn)
        pitch_new, pitch_changed, pitch_unchanged = sync_pitching_stats(conn)
        game_new, game_changed, game_unchanged = sync_game_stats(conn)
        
        conn.commit()
        
        # Final results
        print("\n" + "=" * 50)
        print("COMPLETE SYNC RESULTS")
        print("=" * 50)
        print(f"Total new records: {bat_new + pitch_new + game_new}")
        print(f"Total changed records: {bat_changed + pitch_changed + game_changed}")
        print(f"Total unchanged records: {bat_unchanged + pitch_unchanged + game_unchanged}")
        print("ALL TABLES SYNCED SUCCESSFULLY!")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()